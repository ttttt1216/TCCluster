# 2022-09-29

from pyproj import CRS
from pyproj import Transformer


# TODO: EPSG:4326 -> 3857
# 如何打印crs的信息？解决：print(crs_4326.to_wkt(pretty=True))
# wgs84地理坐标系的轴向信息是（纬度，经度）
# 输出结果是伪墨卡托是先x坐标(east)，后y坐标(north)
def wgs_2_mercator(lati: float,
                   longi: float):
    crs_4326 = CRS.from_epsg(4326)
    # print(help(crs_4326))
    print(crs_4326.to_wkt(pretty=True))
    crs_3857 = CRS.from_epsg(3857)
    print(crs_3857.to_wkt(pretty=True))
    transformer = Transformer.from_crs(crs_4326, crs_3857)
    # print(transformer.transform(24.4424, 118.0869))
    return transformer.transform(lati, longi)


# TODO: EPSG:3857 -> 4326
# 输入数据是伪墨卡托是先x坐标(east)，后y坐标(north)
# 输出结果: 纬度，经度
def mercator_2_wgs(lati: float,
                   longi: float):
    crs_4326 = CRS.from_epsg(4326)
    crs_3857 = CRS.from_epsg(3857)
    transformer = Transformer.from_crs(crs_3857, crs_4326)
    # print(transformer.transform(13142531, 2802317))
    return transformer.transform(lati, longi)


if __name__ == "__main__":
    x, y = wgs_2_mercator(24, 118)
    print(x, y)
