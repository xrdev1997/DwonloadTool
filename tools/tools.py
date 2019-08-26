import os
from tqdm import tqdm



def b_hebin(dir, outDir):
    if not os.path.exists("mp4/"):
        os.mkdir("mp4")
    DirFiles = os.listdir(dir)
    DirFiles.sort(key=lambda x: int(x[:-3]))
    OutFile = open(outDir, 'wb')
    for temp in DirFiles:
        ts = open(dir+temp, 'rb')
        OutFile.write(ts.read())
        ts.close()
    OutFile.close()
    print('合并成功')