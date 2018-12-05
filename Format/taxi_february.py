import codecs
import re
from Format.T_Drive import mkdir

source_file_folder = "E:\DataSets\Trajectory Data\\taxi_february\\taxi_february.txt"
destination_folder = "E:\DataSets\Preprocessed\Feb\\"

source_file_handle = codecs.open(source_file_folder, 'r', encoding='utf-8')

line_object = source_file_handle.readline().strip("/r/n")

last_date = "2014-02-01"
list_temp = []
list_date = []
all_index = 1
while line_object:
    match_objects = re.split(';', line_object)
    Feb_id = match_objects[0]
    Feb_date_time = re.split(' ', match_objects[1])
    Feb_date = Feb_date_time[0]
    Feb_time = Feb_date_time[1]
    points = re.split(' ', re.search("\((.+?)\)", match_objects[2])[1])
    Feb_longitude = points[0]
    Feb_latitude = points[1]
    # print(Feb_id, Feb_longitude, Feb_latitude, match_objects[1])

    if last_date == Feb_date:
        list_temp.append([Feb_id, Feb_longitude, Feb_latitude, match_objects[1]])
    else:
        # 输出上一个
        # 生成date文件夹
        _destination_folder = mkdir(destination_folder + last_date)
        # id标识
        last_id = 'start'
        # 用于存放相同id条目的数组
        list_sameid_temp = []
        # 数组排序
        list_temp.sort()
        # 遍历同date的数组
        for item in list_temp:
            if item[0] == last_id:
                list_sameid_temp.append(item)
            else:
                if last_id != 'start':
                    print(item[0], len(list_sameid_temp))
                    # 生成同id，date文件
                    destination_address = destination_folder + last_date + '\\' + last_id + '_' + last_date + '.txt'
                    destination_handle = codecs.open(destination_address, 'w', encoding='utf-8')
                    # 遍历同id数组
                    for _item in list_sameid_temp:
                        destination_handle.writelines(
                            _item[0] + ',' + _item[1] + ',' + _item[2] + ',' + _item[3] + '\n')
                    destination_handle.close()
                # 获取新标识id
                last_id = item[0]
                list_sameid_temp = []
                list_sameid_temp.append(item)

        list_temp = []
        last_date = Feb_date
        print(last_date, all_index)

    line_object = source_file_handle.readline().strip("/r/n")
    all_index += 1
