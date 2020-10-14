from file_manager.common.FetchFileWithType import fetch_file

# 视频输入目录
video_inputs = ["/media/cspy/CSpy的数据盘", "/mnt/pc-e", "/mnt/pc-f", "/mnt/fs"]
# 视频输出目录
video_output = "/home/cspy/Video"
# 开始获取图片
fetch_file("simple", video_inputs, video_output, "video/")