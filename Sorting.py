# coding: utf-8
import os  # 引入文件操作库
import codecs
from Cut.StayPoint import Point
from Format.T_Drive import mkdir


def Sorter(path):
    """
    Sort spatial data,
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
            new_root = root.replace('Hours', 'S_Hours', 1) + '\\'
            mkdir(new_root)
            new_path = new_root + file
            print(new_path)
            destination_handle = codecs.open(new_path, 'w', encoding='utf-8')
            list_temp = list()
            # 存入数组
            for line in lines:
                temp_p = Point(line)
                list_temp.append(temp_p)
            # 按照时间对数组排序
            list_temp = sorted(list_temp, key=lambda point: point.date_time)
            for p in list_temp:
                latitude = p.latitude
                longitude = p.longitude
                id = p.id
                time = p.date_time
                destination_handle.writelines(
                    id + ',' + str(longitude) + ',' + str(latitude) + ',' + str(time) + '\r\n')
            list_temp.clear()
            destination_handle.close()

    print(path, 'Sort over!')


if __name__ == "__main__":  # 执行本文件则执行下述代码
    path = "E:\DataSets\Preprocessed\\Hours\\"  # 输入路径
    Sorter(path)
