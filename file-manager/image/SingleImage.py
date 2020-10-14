# 生成html，方便图片对比
import os

duplicate_dirs = "/home/cspy/ImageDuplicate"
target_html_dir = "/home/cspy/ImageDuplicate/"

count = 0
dir_dict = {}

with os.scandir(duplicate_dirs) as it:
    for entry in it:
        if entry.is_dir():
            dir_dict[entry.name] = []
            with os.scandir(os.path.join(duplicate_dirs, entry.name)) as dir_it:
                for file in dir_it:
                    if file.is_file():
                        dir_dict[entry.name].append(file.name)

template_html = open("index.html", "r").read()
content = ""
count = 0
index_count = 1
for key in dir_dict.keys():
    c = "<div style=\"height: 160px;margin-top: 20px;\"><span>" + key + "</span>"
    for file in dir_dict[key]:
        c += "<img style=\"height:100%;\" src=\"http://localhost/" + key + "/" + file + "\" />"
    c += "</div>"
    content += c
    count += 1

    if count > 400:
        index_html = open(os.path.join(target_html_dir, "index_" + str(index_count) + ".html"), "w")
        index_count += 1
        content += "<a style=\"font-size: 80px;\" href=\"http://localhost/index_" + str(index_count) + ".html\">下一页</a>"
        index_html.write(template_html.replace("{{imageDiv}}", content))
        content = ""
        count = 0
