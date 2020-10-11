import os
import magic
import hashlib
from shutil import copy2
from shutil import move
from shutil import rmtree
import re
import time

image_inputs = ["/media/cspy/CSpy的数据盘", "/mnt/pc-e", "/mnt/pc-f", "/mnt/fs"]
image_output = "/home/cspy/Images"

"""
mode: simple/tradition
    simple: 简易模式
        介绍：文件变动只发生在最后一步，即将文件从inputs复制到output中，不存在其他文件变更操作。
        优点：节省空间；减少硬盘操作次数；
        缺点：如果读取的是网络存储，则受网络性能，远程硬盘性能影响较大；
    tradition: 传统模式
        介绍：将需要操作的文件，复制到同一目录，方便操作。重复文件保存在各个重复文件夹中，一目了然。
        优点：脚本的各个流程及结果一目了然，方便调试；可以选择保留重复文件，容错率较高；
        缺点：占用空间大，读写频繁；
"""
mode = "simple"

"""
是否保留重复文件夹（仅在mode=tradition模式下生效）
"""
save_duplicate = False

#  判断输出目录
if os.path.exists(image_output):
    print("Err: 输出目录已存在！")
    exit(-1)
else:
    os.mkdir(image_output)


def tradition_mode(save_duplicate):
    """传统模式"""
    # 创建临时文件夹
    tmp_dir_suffix = str(time.time()).split(".")[1]
    image_tmp = os.path.join(os.path.dirname(image_output), tmp_dir_suffix)
    while os.path.exists(image_tmp):
        print("Err:  临时文件夹已存在: {}".format(image_tmp))
        image_tmp = os.path.join(os.path.dirname(image_output), tmp_dir_suffix)
    os.makedirs(image_tmp)
    print("创建临时文件夹: {}".format(image_tmp))

    # 在临时文件夹中，创建两个重复文件夹
    duplicate_md5_dir = os.path.join(image_tmp, "duplicate_md5")
    os.makedirs(duplicate_md5_dir)
    duplicate_name_dir = os.path.join(image_tmp, "duplicate_name")
    os.makedirs(duplicate_name_dir)

    print("抓取图片")

    # 抓取的图片总数
    sum = 0

    # 结果集，各个文件內包含的图片数量
    result_list = []

    # md5字典
    # file_md5 -> file_names
    md5_dict = {}

    for image_input in image_inputs:
        for root, dirs, files in os.walk(image_input):
            # 获取当前路径md5
            dir_md5 = hashlib.md5(root.encode())
            image_count = 0
            for file in files:
                # 获取源文件路径
                src_file = os.path.join(root, file)
                src_file_type = magic.from_file(src_file, mime=True)
                # 判断是图片，则复制
                if src_file_type.startswith("image/"):
                    # 获取目标路径和文件名
                    dest_file = os.path.join(image_output, dir_md5.hexdigest() + "_" + file)
                    # 确定是图片之后，直接计算md5
                    print("读取文件：\t{}".format(src_file))
                    src_file_opener = open(src_file, "rb")
                    src_file_content = src_file_opener.read()
                    file_md5 = hashlib.md5(src_file_content).hexdigest()
                    if file_md5 in md5_dict.keys():
                        md5_dict[file_md5].append(dest_file)
                    else:
                        md5_dict[file_md5] = [dest_file]
                    src_file_opener.close()
                    image_count += 1
                    copy2(src_file, dest_file)
                    print(src_file + " -> " + dest_file)
            result_list.append("root: {}\t\timages: {}".format(root, image_count))
            sum += image_count

    # 打印结果集
    for result in result_list:
        print(result)
    print("抓取图片结束")
    print("共抓取{}张图片".format(sum))

    print("去重（md5）")
    duplicate_name_dir_count = 0
    duplicate_name_file_count = 0
    # 移动md5重复的文件
    for key in md5_dict.keys():
        if len(md5_dict[key]) > 1:
            # 创建 duplicate_md5_dir 中的md5子目录
            dir_name = os.path.join(duplicate_md5_dir, key)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            elif not os.path.isdir(dir_name):
                print(dir_name + "是一个文件！")
                continue
            duplicate_name_dir_count += 1
            # 将md5重复的所有文件，都移入 duplicate_md5_dir/md5(file)/
            for src in md5_dict[key]:
                move(src, dir_name)
                duplicate_name_file_count += 1
    print("去重结束\tmd5: {}\tfile: {}".format(duplicate_name_dir_count, duplicate_name_file_count))

    print("合并")
    # 将md5重复的文件，取名称最短的文件，复制到output
    merge_count = 0
    for root, dirs, files in os.walk(duplicate_md5_dir):
        if len(files) > 1:
            # 字符串数组排序，按照字符串大小排序，尽量使用同一个文件夹中的文件版本
            files.sort()
            copy2(os.path.join(root, files[0]), image_output)
            merge_count += 1
    print("合并结束\t移动: {}".format(merge_count))

    print("二次去重（文件名）")
    name_dict = {}
    duplicate_name_count = 0
    for root, dirs, files in os.walk(image_output):
        for file in files:
            # 获取无前缀的原始文件名，加入字典
            original_file_name = re.sub("^[0-9a-f]{32}_", "", file, 1)
            if original_file_name in name_dict.keys():
                name_dict[original_file_name].append(file)
            else:
                name_dict[original_file_name] = [file]
    # 找出重名文件
    for key in name_dict.keys():
        if len(name_dict[key]) > 1:
            # 在duplicate_name_dir目录下，创建名称为原始文件名（md5）的目录
            dir_name = os.path.join(duplicate_name_dir, hashlib.md5(key.encode()).hexdigest())
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            elif not os.path.isdir(dir_name):
                print(dir_name + "是一个文件！")
                continue
            # 将文件名重复的文件，移入duplicate_name_dir
            for file in name_dict[key]:
                move(os.path.join(image_output, file), dir_name)
                duplicate_name_count += 1
    print("二次去重结束\t共: {}".format(duplicate_name_count))

    print("重名文件重命名")
    rename_count = 0
    for root, dirs, files in os.walk(duplicate_name_dir):
        for file in files:
            # 提取文件的文件名和后缀
            file_name_array = os.path.splitext(file)
            random_suffix = str(time.time()).split(".")[1]
            new_file_name = file_name_array[0] + "_" + random_suffix + file_name_array[1]
            rename_count += 1
            copy2(os.path.join(root, file), os.path.join(image_output, new_file_name))
    print("重名文件重命名结束\t共: {}".format(rename_count))

    print("去除output前缀")
    # 去除前缀
    remove_prefix_count = 0
    for root, dirs, files in os.walk(image_output):
        for file in files:
            remove_prefix_count += 1
            new_file_name = re.sub("^[0-9a-f]{32}_", "", file, 1)
            move(os.path.join(root, file), os.path.join(root, new_file_name))
    print("去除output前缀结束\t共: {}".format(remove_prefix_count))

    if not save_duplicate:
        print("删除临时文件夹\t\t{}".format(image_tmp))
        rmtree(image_tmp)
        print("临时文件夹删除成功")
    else:
        print("保留临时文件夹\t\t{}".format(image_tmp))
    print("Finished.")


def simple_mode():
    """简单模式"""
    # 抓取的图片总数
    sum = 0

    # 结果集，各个文件內包含的图片数量
    result_list = []

    # md5字典
    # file_md5 -> file_names
    md5_dict = {}

    for image_input in image_inputs:
        for root, dirs, files in os.walk(image_input):
            image_count = 0
            for file in files:
                # 获取源文件路径
                src_file = os.path.join(root, file)
                src_file_type = magic.from_file(src_file, mime=True)
                # 判断是图片，则记录到md5_dict
                if src_file_type.startswith("image/"):
                    # 确定是图片之后，直接计算md5
                    src_file_opener = open(src_file, "rb")
                    src_file_content = src_file_opener.read()
                    file_md5 = hashlib.md5(src_file_content).hexdigest()
                    print("Find image: {}".format(src_file))
                    if file_md5 in md5_dict.keys():
                        md5_dict[file_md5].append(src_file)
                    else:
                        md5_dict[file_md5] = [src_file]
                    src_file_opener.close()
                    image_count += 1
            result_list.append("root: {}\t\timages: {}".format(root, image_count))
            sum += image_count

    # 打印结果集
    for result in result_list:
        print(result)
    print("抓取图片结束")
    print("共抓取{}张图片".format(sum))

    print("去重（md5）")
    # 目前所有的文件信息都保存在md5_dict中
    file_list = []
    for key in md5_dict.keys():
        if len(md5_dict[key]) > 1:
            # 只保留1个
            md5_dict[key].sort()
            md5_dict[key] = [md5_dict[key][0]]
        file_list.append(md5_dict[key][0])
    print("去重结束\t{}".format(len(file_list)))

    print("二次去重（文件名）")
    name_dict = {}
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        if file_name in name_dict.keys():
            name_dict[file_name].append(file_path)
        else:
            name_dict[file_name] = [file_path]
    print("二次去重（文件名）结束")

    print("文件重命名")
    duplicate_name_count = 0
    for key in name_dict.keys():
        if len(name_dict[key]) > 1:
            for file_path in name_dict[key]:
                file_name = os.path.basename(file_path)
                file_name_array = os.path.splitext(file_name)
                random_suffix = str(time.time()).split(".")[1]
                new_file = os.path.join(image_output, file_name_array[0] + "_" + random_suffix + file_name_array[1])
                copy2(file_path, new_file)
                duplicate_name_count += 1
        else:
            copy2(name_dict[key][0], image_output)
            duplicate_name_count += 1
    print("文件重命名结束\t共{}".format(duplicate_name_count))
    print("Finished.")


begin_timestamp = time.time()
if mode == "tradition":
    tradition_mode(save_duplicate)
elif mode == "simple":
    simple_mode()
else:
    print("请设置mode参数")
end_timestamp = time.time()
print("运行时间: {} 秒".format(end_timestamp - begin_timestamp))