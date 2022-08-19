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
        data_path["TIME"] = data_path.index
        data_path["LAT"] = data_path["LAT"] / 10
        data_path["LONG"] = data_path["LONG"] / 10
    return header, data_path
