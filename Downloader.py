# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, wait
import webbrowser
import re
import requests
import os,sys
import time
import MultiDownloader
import json
from xvideo import Xvideo
from pornhub import PornHub
from tools.tools import b_hebin
import tkinter as tk
import tkinter.messagebox
from retrying import retry
from tqdm import tqdm

root = tk.Tk()
root.withdraw()
verion = 1.2


def main():

    # Data = requests.get('https://xrdev.design/file/update/update.txt').json()
    # if float(Data['download_verison']) > verion:
    #     root.withdraw()
    #     Update = tk.messagebox.askquestion('下载器 更新','检测到新版本 是否更新!!!')
    #     if Update=='yes':
    #         webbrowser.open(Data['download_url'])

    while True:
        url = input("请输入页面URL:")
        # url = "https://www.xvideos.com/video24816621/stunning_lesbians_in_the_shower"
        if not url.startswith('http'):
            print('链接错误')
            continue

        if url.find('pornhub') != -1:
            p = PornHub(url, 20)
            p.run()
            del p
            continue

        if url.find('xvideos') != -1:
            t = Xvideo(url, 10)
            t.run()
            del t
            continue
        porn = PornHub(url, 30)
        contentLen = porn.GetContentLen()
        if contentLen == -1:
            return
        
        title = 'BestPornHub1'
        target = [0, 1023999]
        f_list = []
        p = ThreadPoolExecutor(30)
        start_time = time.time()
        haveMore = False
        while True:
            future = p.submit(
                porn.PHdownload, target[0], target[1], title)
            f_list.append(future)
            if (target[1] + 1024000) >= contentLen:
                haveMore = True
                print('最后一部分: '+str(target))
                break
            target[0] = int(target[1]) + 1
            target[1] = target[1] + 1024000

        wait(f_list, return_when='ALL_COMPLETED')
        if haveMore:
            porn.PHdownload(target[1]+1, '', title)
        end_time = time.time()
        print("耗时: "+str(int(end_time)-int(start_time))+'s')
        b_hebin('m3u8/'+title+'/', 'mp4/'+title+'.mp4')


def YesClick():
    url = inpUrl.get()


def TWindow():
    # 创建一个主窗口，用于容纳整个GUI程序

    # 设置主窗口对象的标题栏
    root.title("X-Video下载器")
    root.geometry("400x400+200+50")
    # 添加一个Label组件，Label组件是GUI程序中最常用的组件之一
    # Label组件可以显示文本、图标或者图片
    # 在这里我们让他们显示指定文本
    theLabel = tk.Label(root, text="请输入视频页地址")
    global inpUrl
    inpUrl = tk.Entry(root)
    yesbtn = tk.Button(root, text='确认', command=YesClick)
    # 然后调用Label组建的pack()方法，用于自动调节组件自身的尺寸
    theLabel.pack()
    inpUrl.pack()
    yesbtn.pack()
    # 注意，这时候窗口还是不会显示的...
    # 除非执行下面的这条代码！！！！！
    root.mainloop()


if __name__ == '__main__':
    if not os.path.exists("mp4/"):
        os.mkdir("mp4")
    main()
    if not os.path.exists("m3u8/"):
        os.mkdir("mp4")
    main()

    # p = ThreadPoolExecutor(15)
    # for i in range(0,37):
    #     p.submit(down,i)

    # os.popen(xvideo_ffmpeg(37, "xixi", "HD7"))
