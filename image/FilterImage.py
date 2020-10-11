import os
import magic
import regex
from shutil import move

# 作用于经过ManageImage.py脚本处理过的图片文件夹
image_src = "/home/cspy/Images"
image_dest = "/home/cspy/PyImageBack"

#  判断输出目录
if os.path.exists(image_dest):
    print("Err: 输出目录已存在！")
    exit(-1)
else:
    os.mkdir(image_dest)

image_list = []
# 循环读取图片列表
with os.scandir(image_src) as it:
    for entry in it:
        if entry.is_file():
            full_name = os.path.join(image_src, entry.name)
            file_type = magic.from_file(full_name, mime=True)
            if file_type.startswith("image/"):
                image_list.append(entry.name)
print(image_list)

regex_array = [
    {
        "name": "微信聊天图片",
        "regex": "^mmexport[[:digit:]]{13}"
    }, {
        "name": "qq_tim截图",
        "regex": "^(microMsg\\.|qq_pic_merged_|TIM截图)"
    }, {
        "name": "截图",
        "regex": "^Screenshot_"
    }, {
        "name": "小米相册",
        "regex": "^IMG_[[:digit:]]{8}_[[:digit:]]{6}"
    }, {
        "name": "旧相册",
        "regex": "^IMG[[:digit:]]{14}$"
    }, {
        "name": "微博",
        "regex": "^img-[[:alnum:]]{32}"
    }, {
        "name": "微信头像",
        "regex": "^hdImg_"
    }, {
        "name": "淘宝",
        "regex": "^\\-?[[:digit:]]{9,10}$"
    }, {
        "name": "京东",
        "regex": "^JDIM_[[:digit:]]{13}"
    }, {
        "name": "咸鱼",
        "regex": "^idlefish-msg-"
    }, {
        "name": "微信视频缩略图",
        "regex": "^wx_camera_"
    }, {
        "name": "抖音缩略图",
        "regex": "^[[:alnum:]]{32}(tmp)?$"
    }, {
        "name": "抖音分享码",
        "regex": "^share_card_[[:digit:]]{19}$"
    }, {
        "name": "录屏缩略图",
        "regex": "^Screenrecorder\\-[[:digit:]]{4}\\-[[:digit:]]{2}\\-[[:digit:]]{2}"
    }, {
        "name": "知乎",
        "regex": "^v2\\-[[:alnum:]]{32}(_r|_hd)?$"
    }, {
        "name": "VID缩略图",
        "regex": "^VID_[[:digit:]]{8}_[[:digit:]]{6}"
    }, {
        "name": "simple",
        "regex": "^[[:alnum:]]{1,4}$"
    }
]

# 创建分类目录
for item in regex_array:
    os.makedirs(os.path.join(image_dest, item["name"]))

# 移动匹配到的文件
for file in image_list:
    file_name_array = os.path.splitext(file)
    file_name = file_name_array[0]
    for item in regex_array:
        if regex.match(item["regex"], file_name) is not None:
            print("{} -> {}".format(os.path.join(image_src, file), os.path.join(image_dest, item["name"])))
            move(os.path.join(image_src, file), os.path.join(image_dest, item["name"]))
            print("match: {} {} {}".format(file_name, item["regex"], item["name"]))
            break
