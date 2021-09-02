f = open("/home/linxinqiang/Documents/log.txt","r",encoding="gbk",errors="ignore")             # 返回一个文件对象
lines = f.readlines()

f2 = open("/home/linxinqiang/Documents/log2.txt","w")
for line in lines:
    print(line)
    f2.write(line+"\n")
f.close()
f2.close();