# coding=UTF-8
import sys
import subprocess
from os import path
from glob import glob

reload(sys)
sys.setdefaultencoding("UTF-8")

def closeapp(str):
	raw_input((str+"\n<<< 按Enter離開 >>>").encode("cp950"))
	sys.exit()


# 基本路徑
base_path = getattr(sys, '_MEIPASS', '.')+'/'


# 輸出路徑
file_path = sys.argv[1]
if path.isfile(file_path):
	file_path = file_path.replace(path.basename(file_path), "")


# 圖檔類型
img_ext = ""
for img in ["exr", "png", "jpg", "jpeg", "tga"]:
	images = glob(file_path+"/*.{0}".format(img))
	if len(images) != 0:
		img_ext = img
		break

if img_ext == "":
	closeapp("!!!找不到序列圖檔!!!")


# 圖檔名稱
img_name = path.splitext(path.basename(images[0]))[0]


# 指令判別
if len(sys.argv) == 2:
	getf = (path.splitext(path.basename(sys.argv[0]))[0]).split("_")
	if getf[-1].isdigit() and len(getf) > 1:
		framerate = getf[-1]
	else:
		framerate = raw_input("輸入每秒格數：".encode("cp950"))
	if framerate.isdigit() is not True:
		closeapp("!!!輸入無效!!!")
	output_path = file_path
elif len(sys.argv) == 4:
	framerate = sys.argv[2]
	output_path = sys.argv[3]
else:
	closeapp("接收資訊有誤")

output_path = output_path.rstrip("\\")


# 圖檔編號判別
digit = 0
for i in range(-1, -len(img_name), -1):
	if img_name[i].isdigit():
		digit -= 1
	else:
		break

num = img_name[digit:]
padz = len(num)
prefix = img_name[:digit]
if prefix[-1] == "_" or prefix[-1] == "." or prefix[-1] == "-" or prefix[-1] == " " or prefix[-1] == "~":
	output_name = prefix[:-1]
else:
	output_name = prefix

# 執行轉檔
cmd = '{7}ffmpeg {6}-framerate {0} -start_number {9} -i "{1}\{2}%0{3}d.{4}" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p -crf 18 -y "{8}\{5}.mp4"'.format(framerate, file_path, prefix, padz, img_ext, output_name, "-gamma 2.2 " if img_ext == "exr" else "", base_path, output_path, int(num))
subprocess.call(cmd, shell=True)
subprocess.call( 'explorer /select,"{0}\{1}.mp4"'.format(output_path, output_name) )