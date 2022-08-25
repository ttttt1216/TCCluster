# processData.py: processing of CMA database
# https://tcdata.typhoon.org.cn/zjljsjj_zlhq.html
# 2022-08-18
# Tian Zhenshiyi


import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List
from typing import Union
from typing import Tuple
from base import get_variables


def reader_notime(typhoon_txt: os.PathLike, code: Union[str, int]) -> Tuple[List[str], pd.DataFrame]:
    typhoon_txt = Path(typhoon_txt)
    if isinstance(code, int):
        code = "{:04}".format(code)
    # Python引入了with语句来自动帮我们调用close()方法
    with open(typhoon_txt, "r") as txt_handle:
        while True:
            header = txt_handle.readline().split()
            if not header:
                raise ValueError(f"没有在文件里找到编号为{code}的台风")
            if header[4].strip() == code:
                break
        # [txt_handle.readline() for _ in range(int(header[2]))]
        '''
        the file is like
        ['2006080500 1 100 1485 1000      15\n', '2006080506 1 112 1474 1000      15\n']
        '''
        data_path = pd.read_table(txt_handle, sep=r"\s+", header=None,
                                  names=["TIME", "I", "LAT", "LONG", "PRES", "WND", "OWD"],
                                  nrows=int(header[2]),
                                  index_col="TIME",
                                  dtype={"I": int,
                                         "LAT": np.float32,
                                         "LONG": np.float32,
                                         "PRES": np.float32,
                                         "WND": np.float32,
                                         "OWD": np.float32, },
                                  parse_dates=True,
                                  date_parser=lambda x: pd.to_datetime(x, format=f"%Y%m%d%H"))
        data_path["LAT"] = data_path["LAT"] / 10
        data_path["LONG"] = data_path["LONG"] / 10
    return header, data_path


def reader(typhoon_txt: os.PathLike, code: Union[str, int]) -> Tuple[List[str], pd.DataFrame]:
    typhoon_txt = Path(typhoon_txt)
    if isinstance(code, int):
        code = "{:04}".format(code)
    with open(typhoon_txt, "r") as txt_handle:
        while True:
            header = txt_handle.readline().split()
            if not header:
                header = 'end'
                data_path = 'end'
                print(f"没有在文件里找到编号为{code}的台风")
                return header, data_path
            if header[4].strip() == code and header[0] == '66666' and header[7] != '(nameless)':
                # 对于10年，容易出现和气压相似的code
                break
            if header[4].strip() == code and header[0] == '66666' and header[7] == '(nameless)':
                # 对于10年，容易出现和气压相似的code
                header = 'nameless'
                return header, 0
        # [txt_handle.readline() for _ in range(int(header[2]))]
        '''
        the file is like
        ['2006080500 1 100 1485 1000      15\n', '2006080506 1 112 1474 1000      15\n']
        '''
        data_path = pd.read_table(txt_handle, sep=r"\s+", header=None,
                                  names=["TIME", "I", "LAT", "LONG", "PRES", "WND", "OWD"],
                                  nrows=int(header[2]),
                                  index_col="TIME",
                                  dtype={"I": int,
                                         "LAT": np.float32,
                                         "LONG": np.float32,
                                         "PRES": np.float32,
                                         "WND": np.float32,
                                         "OWD": np.float32, },
                                  parse_dates=True,
                                  date_parser=lambda x: pd.to_datetime(x, format=f"%Y%m%d%H"))
        data_path["TIME"] = data_path.index
        data_path["LAT"] = data_path["LAT"] / 10
        data_path["LONG"] = data_path["LONG"] / 10
    return header, data_path


def get_tc_name(type: str = 'data',
                country: str = 'china',
                tc_list: list = None):
    mod = get_variables(type, country)
    if tc_list is None:
        tc_list = mod.TC_LIST
    return tc_list


def get_year_list(type: str = 'data',
                  country: str = 'china',
                  year_list: list = None):
    mod = get_variables(type, country)
    if year_list is None:
        year_list = mod.YEAR_LIST
    return year_list


"""
    1. 将台风路径存储为单个的文件，删除nameless的台风
    2. 生成对应台风轨迹的_index.py文件
    3. 生成cluster所需的[x,y,x,y...]形式的。txt文件
"""
if __name__ == '__main__':
    year_list = get_year_list()
    # 记录每年有效编号的台风个数
    total_year = {}
    # 记录所有台风信息，方便下次处理
    tc_index = []
    # 记录每一条台风的坐标情况
    ts_dict = {}
    ts_list = []
    for key1 in year_list:
        track = r"../CMABSTdata/CH" + str(key1) + "BST.txt"
        for key2 in range(1, 41, 1):
            number = str(key1)[-2:] + '{:0>2d}'.format(key2)
            head, data = reader(track, number)
            if head == 'end':
                total_year[key1] = int(number[-2:]) - 1
                break
            elif head == 'nameless':
                continue
            else:
                name = r'../output2/' + str(head[4] + head[7]) + '.txt'
                tc_index.append(str(head[4] + head[7]) + '\n')
                data.to_csv(name, index=False, sep=' ')
                ts = []
                ts_list.append(head[4])
                for key in data.index:
                    ts.append(data.LONG[key])
                    ts.append(data.LAT[key])
                ts_dict[head[4]] = ts

    with open(r'../output2/_coordination.txt', "w") as f:
        for key in ts_dict:
            f.write(str(ts_dict[key]) + '\n')

    with open(r'../output2/_index.txt', "w") as f:
        for key in tc_index:
            f.write(key)
