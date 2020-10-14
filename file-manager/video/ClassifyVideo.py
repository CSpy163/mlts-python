from common.ClassifyFileByName import classify_file
# 视频输入目录
video_src = "/home/cspy/test_video_1810"
# 视频输出目录
video_dest = "/home/cspy/video_test_1819"
# 正则表达式数组
regex_array = [
    {
        "name": "抖音视频",
        "regex": "^"
    }, {
        "name": "录屏",
        "regex": "^VID_[[:digit:]]{8}_[[:digit:]]{6}"
    }
]
# 开始分类
classify_file(video_src, video_dest, regex_array, "video/")
