import os
import codecs
import re
from Format.T_Drive import mkdir


'''
按照小时切割文件
'''
root_path = "E:\DataSets\Preprocessed\Days\T-Drive\\"
destination_folder = "E:\DataSets\Preprocessed\Hours\T-Drive\\"

if __name__ == '__main__':
    print(os.path.exists(root_path))
    walk_results = os.walk(root_path)
    # 遍历路径下所有文件夹
    for root, dirs, files in walk_results:
        if len(dirs) > 0:
            for dir in dirs:
                for i in range(0, 24):
                    mkdir(destination_folder + dir + '\\' + str(i))

        if len(files) > 0:
            # 针对每个独立文件
            for file in files:
                hour_list = list(list() for i in range(0, 24))
                # 打开文件
                path = root + '\\' + file
                file_handle = codecs.open(path, 'r', encoding='utf-8')
                lines = file_handle.readlines()
                # 针对每行数据
                for line in lines:
                    # 获取该行数据小时数
                    hour = re.search("([0-9]+)\:", line)[1]
                    I_hour = int(hour)
                    # 根据小时数存入24维数组
                    hour_list[I_hour].append(line.strip('\r\n'))
                # 写入输出文件
                for i in range(0, 24):
                    path = str(root + '\\' + str(i) + '\\')
                    path = path.replace('Days', 'Hours', 1) + file.replace('.txt', '_' + str(i) + '.txt')
                    if len(hour_list[i]) > 0:
                        destination_handle = codecs.open(path, 'w', encoding='utf-8')
                        for item in hour_list[i]:
                            destination_handle.writelines(item + '\n')
                        destination_handle.close()
                del hour_list
            print(root)
