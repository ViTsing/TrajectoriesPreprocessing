import codecs
import os
import re
from Format.T_Drive import mkdir
import time

source_file_folder = "E:\DataSets\Trajectory Data\cabspottingdata\cabs\\"
dict_cab = "E:\DataSets\Preprocessed\Cab\id_name.txt"
destination_folder = "E:\DataSets\Preprocessed\Cab\\"


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    # 经过localtime转换后变成
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


if __name__ == '__main__':
    print(os.path.exists(source_file_folder))
    walk_results = os.walk(source_file_folder)
    id_name_handle = codecs.open(dict_cab, 'w', encoding='utf-8')
    for root, dirs, files in walk_results:
        index = 0
        # 每个id对应一个文件
        for file in files:
            index += 1
            id_name_handle.writelines(str(index) + '\t' + file + '\r\n')
            file_handle = codecs.open(root + file, "r", encoding='utf-8')
            line_objects = file_handle.readlines()
            # 每个时间对应一行
            for line in line_objects:
                # 解析每一行
                match_objects = re.split(' ', line.strip('\r\n'))
                latitude = match_objects[0]
                longitude = match_objects[1]
                datetime = timestamp_datetime(int(match_objects[3]))
                date = re.split(' ', datetime)[0]
                # 生成目标文件夹
                _destination_folder = destination_folder + date
                mkdir(_destination_folder)
                destination_file_address = _destination_folder + '\\' + str(index) + '_' + date + '.txt'
                destination_file_handle = codecs.open(destination_file_address, 'a+', encoding='utf-8')
                destination_file_handle.writelines(
                    str(index) + ',' + longitude + ',' + latitude + ',' + datetime + '\r\n')
                destination_file_handle.close()
            print(file)
