from file_manager.common.FetchFileWithType import fetch_file

# 图片输入目录
image_inputs = ["/home/cspy/image_input", "/mnt/pc-e", "/mnt/pc-f"]
# 图片输出目录
image_output = "/home/cspy/Image"
# 开始获取图片
fetch_file("simple", image_inputs, image_output, "image/")
