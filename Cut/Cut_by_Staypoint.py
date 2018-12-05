import re
import codecs
import os
import datetime
from Format.T_Drive import mkdir
from Cut.StayPoint import Point

'''
根据驻留点切割文件
'''
root_path = "E:\DataSets\Preprocessed\Days\Feb\\"
walk_results = os.walk(root_path)
# 对于每一个day 都要创建对应的文件（即使不切割也要排序）
for root, dirs, files in walk_results:
    # 当遍历到叶节点层时，返回所有文件
    for file in files:
        # 如果是文件,读入该文件
        doc_handle = codecs.open(root + '\\' + file, 'r', encoding='utf-8')  # 打开文件
        lines = doc_handle.readlines()
        doc_handle.close()
        # 生成对应的
        new_root = root.replace('Days', 'Path_Days', 1) + '\\'
        mkdir(new_root)
        list_temp = list()
        # 存入数组
        for line in lines:
            temp_p = Point(line)
            list_temp.append(temp_p)
        # 按照时间对数组排序
        list_temp = sorted(list_temp, key=lambda point: point.date_time)
        # 判断是否需要通过staypoint切割；
        stay_point_root = root.replace('Days', 'StayPoint', 1) + '\\'
        stay_point_path = stay_point_root + file
        if os.path.exists(stay_point_path):
            stay_point_handle = codecs.open(stay_point_path, 'r', encoding='utf-8')
            sp_lines = stay_point_handle.readlines()
            sp_index = 0
            for sp_line in sp_lines:
                match_objects = re.split(',', sp_line.strip('\r\n'))
                start_time = datetime.datetime.strptime(match_objects[2], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.datetime.strptime(match_objects[3], "%Y-%m-%d %H:%M:%S")
                sp_index += 1
                sp_path = new_root + file.strip('.txt') + '_' + str(sp_index) + '.txt'
                destination_handle = codecs.open(sp_path, 'w', encoding='utf-8')
                list_index = 0
                while list_index < len(list_temp):
                    p = list_temp[list_index]
                    latitude = p.latitude
                    longitude = p.longitude
                    id = p.id
                    time = p.date_time
                    if time <= start_time:
                        destination_handle.writelines(
                            id + ',' + str(latitude) + ',' + str(longitude) + ',' + str(time) + '\r\n')
                        list_temp.__delitem__(list_index)
                    elif time <= end_time:
                        list_temp.__delitem__(list_index)
                    else:
                        break
                destination_handle.close()

            sp_index += 1
            sp_path = new_root + file.strip('.txt') + '_' + str(sp_index) + '.txt'
            destination_handle = codecs.open(sp_path, 'w', encoding='utf-8')
            # 输出list_temp最后一部分
            for p in list_temp:
                latitude = p.latitude
                longitude = p.longitude
                id = p.id
                time = p.date_time
                destination_handle.writelines(
                    id + ',' + str(latitude) + ',' + str(longitude) + ',' + str(time) + '\r\n')
            list_temp.clear()
            destination_handle.close()

        else:
            # 不切割的情况下，最终写入文件
            new_path = new_root + file
            print(new_path)
            destination_handle = codecs.open(new_path, 'w', encoding='utf-8')
            for p in list_temp:
                latitude = p.latitude
                longitude = p.longitude
                id = p.id
                time = p.date_time
                destination_handle.writelines(
                    id + ',' + str(latitude) + ',' + str(longitude) + ',' + str(time) + '\r\n')
            list_temp.clear()
            destination_handle.close()
        # 切割写入
        list_temp.clear()
        destination_handle.close()
