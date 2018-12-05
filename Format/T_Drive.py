import codecs
import os
import re

source_file_folder = "E:\DataSets\Trajectory Data\T-drive Taxi Trajectories\\taxi_log_2008_by_id\\"
destination_folder = "E:\DataSets\\result\\"


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        # print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


if __name__ == '__main__':
    print(os.path.exists(source_file_folder))
    walk_results = os.walk(source_file_folder)
    for root, dirs, files in walk_results:
        index = 1
        # 每个id对应一个文件
        for file in files:
            file_handle = codecs.open(root + file, "r", encoding='utf-8')
            line_objects = file_handle.readlines()
            # 每个时间对应一行
            for line in line_objects:
                # 获取当前行包含的信息
                match_objects = re.split(",", line)
                T_id = match_objects[0]
                T_date_time = match_objects[1]
                T_longitude = match_objects[2]
                T_latitude = match_objects[3].strip("\r\n")
                T_date = re.split(" ", T_date_time)[0]
                # 根据id和date写入
                # 构建路径
                _destination_folder = destination_folder + T_date
                # store_path = mkdir(_destination_folder)
                destination_file_address = _destination_folder + '\\' + T_id + '_' + T_date + '.txt'
                destination_file_handle = codecs.open(destination_file_address, 'a+', encoding='utf-8')
                destination_file_handle.writelines(
                    T_id + ',' + T_longitude + ',' + T_latitude + ',' + T_date_time + '\r\n')
                destination_file_handle.close()
            file_handle.close()
            print(index)
            index += 1
