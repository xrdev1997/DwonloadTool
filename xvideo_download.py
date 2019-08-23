# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, wait
import re
import requests
import os
import time
import MultiDownloader
import json
import tkinter as tk
from retrying import retry
from tqdm import tqdm


def getTrueUrl(url):
    res = requests.get(url)
    content = res.content.decode("utf8")
    urls = re.findall(r'html5player.setVideoHLS\(\'(.+?)\'\)', str(content))[0]
    title = re.findall(
        r'class="page-title">(.+?)<span class="duration"', str(content))[0]
    print(urls)
    url_head = urls[0:urls.rfind('/') + 1]
    content = requests.get(urls).content.decode("utf8")

    datas = re.findall(r'"\n(.+?)\n', content, re.S)

    m3u8 = ""
    for temp in datas:
        if "720p" in temp:
            m3u8 = temp
            break
        elif "1080p" in temp:
            m3u8 = temp
            break
        else:
            m3u8 = datas[0]

    # print(url_head+datas[0])
    # print(requests.get(url_head+datas[0]).content.decode("utf8"))
    return str(title).replace(" ", "_"), url_head+datas[0], requests.get(url_head+m3u8).content.decode("utf8")


def b_hebin(dir, outDir):
    if not os.path.exists("mp4/"):
        os.mkdir("mp4")
    DirFiles = os.listdir(dir)
    DirFiles.sort(key=lambda x: int(x[:-3]))

    OutFile = open(outDir, 'wb')
    for temp in tqdm(DirFiles):
        ts = open(dir+temp, 'rb')
        OutFile.write(ts.read())
        ts.close()
    OutFile.close()


def xvideo_ffmpeg(size, outdir, outname):
    # if not os.path.exists("mp4/"):
    #     os.mkdir("mp4")
    # cmd = "ffmpeg  -i \"concat:"    # outdir = outname[0:outname.rfind('/') + 1]
    # for temp in range(0, size):
    #     if temp == size - 1:
    #         cmd += "m3u8/"+outdir + "/" + str(temp) + ".ts\" -c copy mp4/" + outname + ".mp4"
    #     else:
    #         cmd += "m3u8/"+outdir + "/" + str(temp) + ".ts|"
    # print(cmd)
    # return cmd
    if not os.path.exists("mp4/"):
        os.mkdir("mp4")
    # outdir = outname[0:outname.rfind('/') + 1]
    cmd = "cd m3u8/"+outdir+"/ && ffmpeg  -i \"concat:"
    for temp in range(0, size):
        if temp == size - 1:
            cmd += str(temp) + ".ts\" -c copy ../../mp4/" + outname + ".mp4"
        else:
            cmd += str(temp) + ".ts|"
    print(cmd)
    cmd += " && cd ../../"
    return cmd


@retry(stop_max_attempt_number=10)
def download(url, outputdir):
    if not os.path.exists("m3u8/"):
        os.mkdir("m3u8")
    content = requests.get(url, timeout=6.2).content
    tsname = url[url.rfind("/") + 1:]
    # tsname = re.findall(r'p.{6}(\d+?\.ts)\?',tsname)[0]
    if len(re.findall(r'p(-)', tsname)):
        # https://www.xvideos.com/video49666459/25/_
        tsname = re.findall(r'p-.{5}(\d+?\.ts)', tsname)[0]
    else:
        tsname = re.findall(r'p(\d+?\.ts)', tsname)[0]

    print(tsname)
    if not os.path.exists("m3u8/"+outputdir):
        os.mkdir("m3u8/"+outputdir+"/")
    with open("m3u8/"+outputdir+"/" + tsname, "wb") as code:
        code.write(content)
    print(tsname)
    # except:
    #     if not os.path.exists("m3u8/"):
    #         os.mkdir("m3u8")
    #     content = requests.get(url,timeout=6.2).content
    #     tsname = url[url.rfind("/") + 1:]
    #     # tsname = re.findall(r'p.{6}(\d+?\.ts)\?',tsname)[0]
    #     if len(re.findall(r'p(-)',tsname)):
    #         # https://www.xvideos.com/video49666459/25/_
    #         tsname = re.findall(r'p-.{5}(\d+?\.ts)',tsname)[0]
    #     else:
    #         tsname = re.findall(r'p(\d+?\.ts)',tsname)[0]
    #     print(tsname)
    #     if not os.path.exists("m3u8/"+outputdir):
    #         os.mkdir("m3u8/"+outputdir+"/")
    #     with open("m3u8/"+outputdir+"/" + tsname, "wb") as code:
    #         code.write(content)
    #     print(tsname)


def get_ts(url, ts_str):
    url = url[0:url.rfind("/") + 1]
    print(url)
    ts = re.findall(r',\n(.+?)\n#', ts_str, re.S)
    ts_list = []
    for temp in ts:
        if not url[0:4] in temp:
            ts_list.append(url + temp)
        else:
            ts_list.append(temp)
    return ts_list


@retry(stop_max_attempt_number=10)
def PHdownload(url, start, end, outdir):
    print('start: '+str(start))

    tsname = 'm3u8/'+outdir+'/'+str(start)+'.ts'

    if os.path.exists(tsname):
        if os.path.getsize(tsname)==1024000 or os.path.getsize(tsname)==1024001 :
            return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3559.6 Safari/537.36'}
    headers['Range'] = "bytes="+start+"-"+end
    res = requests.get(url, headers=headers)
    if not os.path.exists("m3u8/"):
        os.mkdir("m3u8")
    if not os.path.exists("m3u8/"+outdir):
        os.mkdir("m3u8/"+outdir)

    with open(tsname, 'wb') as f:
        f.write(res.content)
        print('end: '+str(start))


def GetContentLen(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3559.6 Safari/537.36'}
    headers['Range'] = "bytes=0-1024"
    length = int(requests.get(
        url, headers=headers).headers['Content-Range'].split('/')[1])
    print('length: '+str(length))
    return length


def pronhubdownload(url):
    content = requests.get(url).content.decode("utf8")
    c = re.findall(r'var flashvars_\d+?\s+?=\s+?(\{.+?\});', str(content))[0]
    title = re.findall(r'\<title\>(.+?)\</title\>',
                       str(content))[0].replace('/', '').replace('-','_').replace(' ','_').replace(';','_').replace(')','_').replace(':','_').replace('&','_').replace('#','_')
    print(title)
    c = json.loads(c)
    # print(c)
    i = 0
    url = c['mediaDefinitions'][i]['videoUrl']
    while url == '':
        i = i+1
        url = c['mediaDefinitions'][i]['videoUrl']
    print(url)

    contentLen = GetContentLen(url)
    target = [0, 1024000]
    f_list = []
    p = ThreadPoolExecutor(20)
    start_time = time.time()
    while target[1] < contentLen:
        future = p.submit(PHdownload, url, str(target[0]), str(target[1]),title)
        f_list.append(future)
        target[0] = int(target[1]) + 1
        target[1] = target[1] + 1024000

    if target[1] > contentLen:
        lastLen = contentLen % 1024000
        # target[0] = target[1] + 1
        target[1] = target[0] + lastLen
        future = p.submit(PHdownload, url, str(target[0]), str(target[1]),title)
        f_list.append(future)

    wait(f_list, return_when='ALL_COMPLETED')
    end_time = time.time()
    print("耗时: "+str(int(end_time)-int(start_time))+'s')
    b_hebin('m3u8/'+title+'/', 'mp4/'+title+'.mp4')


def main():

    while True:
        url = input("请输入页面URL:")
        # url = "https://www.xvideos.com/video24816621/stunning_lesbians_in_the_shower"
        if not url.startswith('http'):
            print('链接错误')
            continue

        if url.startswith('https://www.pornhub'):
            pronhubdownload(url)
            continue

        title, url, content = getTrueUrl(url)
        ts_list = get_ts(url, content)
        print(ts_list)
        outputdir = str(int(time.time()))
        print(outputdir)
        title = title.replace('&', '').replace(';', '').replace(',', '').replace('-','_').replace(' ','_')
        f_list = []
        p = ThreadPoolExecutor(5)
        for temp in ts_list:
            future = p.submit(download, temp, outputdir)
            f_list.append(future)

        wait(f_list, return_when='ALL_COMPLETED')
        # os.popen(b_hebin('m3u8/'+outputdir+'/',title+outputdir))
        b_hebin('m3u8/'+outputdir+'/', 'mp4/'+title+'.mp4')
        # time.sleep(4)


def YesClick():
    url = inpUrl.get()


def TWindow():
    # 创建一个主窗口，用于容纳整个GUI程序
    root = tk.Tk()
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
