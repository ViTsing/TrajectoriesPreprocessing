# coding: utf-8
import os  # 引入文件操作库
import codecs
from Format.T_Drive import mkdir
import re
import datetime


class w_Point:
    '''
    To store the wrong point Cab T-drive
    '''

    def __init__(self, line_p):
        self.line = line_p.strip('\r\n')
        match_objects = re.split(',', self.line)
        self.id = match_objects[0]
        # 纬度
        self.latitude = float(match_objects[1])
        # 经度
        self.longitude = float(match_objects[2])
        # 时间日期
        self.date_time = datetime.datetime.strptime(match_objects[3], "%Y-%m-%d %H:%M:%S")

class w_StayPoint:
    def __init__(self, line_p):
        self.line = line_p.strip('\r\n')
        match_objects = re.split(',', self.line)
        self.lat = match_objects[0]
        self.long = match_objects[1]
        self.arv = match_objects[2]
        self.lev = match_objects[3]


def Exchange(path):
    """
    交换指定文件中lat 和long, 清理空文件夹和空文件
    :param path: 文件路径，检查此文件路径下的子文件
    :return: None
    """
    walk_results = os.walk(path)
    # 遍历路径下所有文件夹
    for root, dirs, files in walk_results:
        for file in files:
            print(file)
            # 如果是文件
            doc_handle = codecs.open(root + '\\' + file, 'r', encoding='utf-8')  # 打开文件
            lines = doc_handle.readlines()
            doc_handle.close()
            new_root = root.replace('StayPoint', 'E_StayPoint', 1) + '\\'
            mkdir(new_root)
            new_path = new_root + file
            print(new_path)
            destination_handle = codecs.open(new_path, 'w', encoding='utf-8')
            list_temp = list()
            # 存入数组
            for line in lines:
                temp_p = w_StayPoint(line)
                list_temp.append(temp_p)
            # 按照时间对数组排序
            # list_temp = sorted(list_temp, key=lambda point: point.date_time)
            for p in list_temp:
                latitude = p.lat
                longtitude = p.long
                arv = p.arv
                lev = p.lev
                destination_handle.writelines(
                    longtitude + ',' + latitude + ',' + arv + ',' + lev + '\r\n')
            list_temp.clear()
            destination_handle.close()

    print(path, 'Exchange over!')


if __name__ == "__main__":  # 执行本文件则执行下述代码
    path = "E:\DataSets\Preprocessed\StayPoint\Feb\\"  # 输入路径
    Exchange(path)
