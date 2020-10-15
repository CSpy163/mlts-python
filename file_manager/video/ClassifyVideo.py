from file_manager.common.ClassifyFileByName import classify_file
# 视频输入目录
video_src = "/media/cspy/CSpy的数据盘/Video"
# 视频输出目录
video_dest = "/home/cspy/PyBackupVideo"
# 正则表达式数组
regex_array = [
    {
        "name": "抖音视频",
        "regex": "^([[:alnum:]]{32}|(wm_)?[[:digit:]]{19}|[[:digit:]]{14}_[[:digit:]]{6}(_wm)?)"
    }, {
        "name": "抖音拍摄",
        "regex": "^[[:digit:]]{4}(-|_)[[:digit:]]{2}(-|_)[[:digit:]]{2}(-|_)"
    }, {
        "name": "拍摄视频",
        "regex": "^(VID_|VIDEO)[[:digit:]]{8}_[[:digit:]]{6}"
    }, {
        "name": "录屏",
        "regex": "^SVID_[[:digit:]]{8}_[[:digit:]]{6}"
    }, {
        "name": "未知录音",
        "regex": "^mc_audio"
    }, {
        "name": "微信录屏",
        "regex": "^(_merge_video_|wx_camera_[[:digit:]]{13}|tp_merge_[[:digit:]]{13}|mmexport[[:digit:]]{13})"
    }, {
        "name": "微信保存视频",
        "regex": "^[[:digit:]]{13}(_[[:digit:]]{5,6})?$"
    }, {
        "name": "相机短视频",
        "regex": "^[a-zA-Z0-9]{22,26}(_hd)?(_[[:digit:]]{5,6})?$"
    }
]
# 开始分类
classify_file(video_src, video_dest, regex_array, "video/")
