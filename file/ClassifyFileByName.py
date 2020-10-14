import os
import regex
from shutil import move
import magic

def classify_file(file_src, file_dest, regex_array, mine_type_prefix):
    """
    分类文件脚本
    :param file_src: 待分类的文件目录
    :param file_dest: 分类完成保存的目录
    :param regex_array: 正则表达式数组
    :param mine_type_prefix: mime类型前缀
    :return: None

    sample:
        regex_array = [{"name": "screenshot", "regex": "^Screenshot_"}]
    """
    # 文件名列表
    file_list = []
    # 循环读取图片列表
    with os.scandir(file_src) as it:
        for entry in it:
            if entry.is_file():
                full_name = os.path.join(file_src, entry.name)
                file_type = magic.from_file(full_name, mime=True)
                if file_type.startswith(mine_type_prefix):
                    file_list.append(entry.name)
    print(file_list)

    #  判断输出目录
    if os.path.exists(file_dest):
        print("Err: 输出目录已存在！")
        exit(-1)
    else:
        os.mkdir(file_dest)

    # 创建分类目录
    for item in regex_array:
        os.makedirs(os.path.join(file_dest, item["name"]))

    # 移动匹配到的文件
    for file in file_list:
        file_name_array = os.path.splitext(file)
        file_name = file_name_array[0]
        for item in regex_array:
            if regex.match(item["regex"], file_name) is not None:
                print("{} -> {}".format(os.path.join(file_src, file), os.path.join(file_dest, item["name"])))
                move(os.path.join(file_src, file), os.path.join(file_dest, item["name"]))
                print("match: {} {} {}".format(file_name, item["regex"], item["name"]))
                break
