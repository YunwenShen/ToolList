# -*- coding: utf-8 -*-

import requests


def transfer(system, lat, lng):
    """
    利用接口转换坐标系
    :param system: 坐标系
    :param lat: 维度
    :param lng: 经度
    :return: 转换后的经纬度
    """
    url = "https://tool.lu/coordinate/ajax.html"
    data = {
        "src_type": system,
        "src_coordinate": str(lat) + "," + str(lng)
    }
    response = requests.post(url, data).json()
    _lat = response["result"]["wgs84"]["lat"],
    _lng = response["result"]["wgs84"]["lng"]
    return _lat, _lng


if __name__ == '__main__':
    pass
