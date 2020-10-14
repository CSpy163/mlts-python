from file.ClassifyFileByName import classify_file
# 图片输入目录
image_src = "/home/cspy/test_image_1810"
# 图片输出目录
image_dest = "/home/cspy/image_test_1819"
# 正则表达式数组
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
    }
]
# 开始分类
classify_file(image_src, image_dest, regex_array, "image/")
