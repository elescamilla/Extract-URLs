import os
import re

f = open("files.txt", "w")
dir_path = "/home/mklein/pdf/0704/"
prev_file_base = ""
prev_version = ""
file_list = os.listdir(dir_path)
for file_name in sorted(file_list):
    parsed_file = re.findall(r"(\d{4}.\d*)v(\d*).pdf", file_name)[0]
    file_base = parsed_file[0]
    if prev_file_base != file_base:
        if prev_file_base == "":
            prev_file_base = file_base
        else:
            f.write("Run for " + prev_file_base + "v" + prev_version + ".pdf\n")
            prev_file_base = file_base
    prev_version = parsed_file[1]
f.write("Run for " + prev_file_base + "v" + prev_version + ".pdf\n")