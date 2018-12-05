# coding: utf-8
import os  # 引入文件操作库


'''
清理指定路径下的空文件
'''
def CEF(path):
    """
    CLean empty files, 清理空文件夹和空文件
    :param path: 文件路径，检查此文件路径下的子文件
    :return: None
    """
    walk_results = os.walk(path)
    # 遍历路径下所有文件夹
    for root, dirs, files in walk_results:
        for file in files:
            print(file)
            # 如果是文件
            if os.path.getsize(root+'\\'+file) == 0:  # 文件大小为0
                os.remove(root+'\\'+file)  # 删除这个文件
    print(path, 'Dispose over!')


if __name__ == "__main__":  # 执行本文件则执行下述代码
    path = "E:\DataSets\Preprocessed\Path_Days\T-Drive\\"  # 输入路径
    CEF(path)
