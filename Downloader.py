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
from BestJav import BestJav
from tools import tools
import tkinter as tk
import tkinter.messagebox
from retrying import retry
from tqdm import tqdm

root = tk.Tk()
root.withdraw()
verion = 1.1


def main():

    Data = requests.get('https://xrdev.design/file/update/updata.txt').json()
    if float(Data['download_verison']) > verion:
        root.withdraw()
        Update = tk.messagebox.askquestion('下载器 更新','检测到新版本 是否更新!!!')
        if Update=='yes':
            webbrowser.open(Data['download_url'])

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
        if url.find('bestjavporn') != -1:
            b = BestJav(url)
            b.download()
            del b
            continue

        filename = url.split('/')[-1].split('?')[0]
        tools.DefaultDownload(url,filename,suffix=['file',''])


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
    if not os.path.exists("file/"):
        os.mkdir("file")
    if not os.path.exists("m3u8/"):
        os.mkdir("m3u8")
    main()

    # p = ThreadPoolExecutor(15)
    # for i in range(0,37):
    #     p.submit(down,i)

    # os.popen(xvideo_ffmpeg(37, "xixi", "HD7"))
