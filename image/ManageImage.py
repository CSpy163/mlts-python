import os
import magic
import hashlib
from shutil import copy2
from shutil import move
import re
import time

image_inputs = ["/media/cspy/CSpy的数据盘", "/mnt/pc-e", "/mnt/pc-f", "/mnt/fs"]
image_output = "/home/cspy/Images"

#  判断输出目录
if os.path.exists(image_output):
    print("Err: 输出目录已存在！")
    exit(-1)
else:
    os.mkdir(image_output)

begin_timestamp = time.time()
# 创建临时文件夹
tmp_dir_suffix = str(time.time()).split(".")[1]
image_tmp = os.path.join(os.path.dirname(image_output), tmp_dir_suffix)
while os.path.exists(image_tmp):
    print("Err:  临时文件夹已存在: " + image_tmp)
    image_tmp = os.path.join(os.path.dirname(image_output), tmp_dir_suffix)
os.makedirs(image_tmp)
print("创建临时文件夹: " + image_tmp)

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
                image_count += 1
                # 获取目标路径和文件名
                dest_file = os.path.join(image_output, dir_md5.hexdigest() + "_" + file)
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
# md5字典
# file_md5 -> file_names
md5_dict = {}
# 遍历指定文件夹
with os.scandir(image_output) as it:
    for entry in it:
        if entry.is_file():
            # 获取文件md5，并且存入md5_dict
            fullname = os.path.join(image_output, entry.name)
            file = open(fullname, "rb")
            file_content = file.read()
            md5_str = hashlib.md5(file_content).hexdigest()
            if md5_str in md5_dict.keys():
                md5_dict[md5_str].append(fullname)
            else:
                md5_dict[md5_str] = [fullname]

duplicate_name_dir_count = 0
duplicate_name_file_count = 0
# 移动md5重复的文件
for key in md5_dict.keys():
    if len(md5_dict[key]) > 1:

        dir_name = os.path.join(duplicate_md5_dir, key)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        elif not os.path.isdir(dir_name):
            print(dir_name + "是一个文件！")
            continue
        duplicate_name_dir_count += 1
        for src in md5_dict[key]:
            move(src, dir_name)
            duplicate_name_file_count += 1
print("去重结束\tmd5: {}\tfile: {}".format(duplicate_name_dir_count, duplicate_name_file_count))

print("合并")
# 将md5重复的文件，取名称最短的文件，复制到output
merge_count = 0
for root, dirs, files in os.walk(duplicate_md5_dir):
    if len(files) > 1:
        files.sort()
        # 取名称最短的文件
        copy2(os.path.join(root, files[0]), image_output)
        merge_count += 1
print("合并结束\t移动: {}".format(merge_count))

print("二次去重（文件名）")
image_dist = {}
duplicate_name_count = 0
for root, dirs, files in os.walk(image_output):
    for file in files:
        # 替换文件前缀
        original_file_name = re.sub("^[0-9a-f]{32}_", "", file, 1)
        if original_file_name in image_dist.keys():
            image_dist[original_file_name].append(file)
        else:
            image_dist[original_file_name] = [file]
for key in image_dist.keys():
    if len(image_dist[key]) > 1:
        # 在duplicate_name_dir目录下，创建名称为原始文件名（md5）的目录
        dir_name = os.path.join(duplicate_name_dir, hashlib.md5(key.encode()).hexdigest())
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        elif not os.path.isdir(dir_name):
            print(dir_name + "是一个文件！")
            continue
        # 将文件名重复的文件，移入duplicate_name_dir
        for file in image_dist[key]:
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
        new_file_name = ""
        if len(file_name_array) == 1:
            new_file_name = file_name_array[0] + "_" + random_suffix
        else:
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

end_timestamp = time.time()
print("运行时间: {} 秒".format(end_timestamp - begin_timestamp))