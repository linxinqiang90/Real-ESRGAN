import io
import os
from PIL import Image
import logging
import cv2
import removal

removal.init()

# input = '/home/linxinqiang/Desktop/j3';
# input = '/home/linxinqiang/Desktop/backup';
# input = '/home/linxinqiang/Desktop/test/val';
input = '/home/linxinqiang/Desktop/test/3d_demo_3';

# 获取目录下的文件
files = os.listdir(input)
print(f"文件:{len(files)}")
counter = 1
# 拼接图片路径
for i in files:
    portion = os.path.splitext(i)

    img = cv2.imread(input+"/"+i, cv2.IMREAD_UNCHANGED)
    print(f"write file {input + '_result_yf/' + portion[0] + '.png,['+str(counter)+'/'+str(len(files))+']'}")
    counter+=1
    output = removal.run(img,outscale=2)
    if output is not None:
        if not os.path.exists(input+"_result_yf"):
            os.makedirs(input+"_result_yf")
        cv2.imwrite(input+"_result_yf/"+portion[0]+f".{portion[1]}", output)
        del img
    else:
        print("failed running")

