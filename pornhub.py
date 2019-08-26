import os
import re
import requests
import json
import sys
import time
from tools.tools import b_hebin
from tools import tools
from retrying import retry
from concurrent.futures import ThreadPoolExecutor, wait


class PornHub:

    def __init__(self, url, PoolNum=20):
        self.url = url
        self.PoolNum = PoolNum

    @retry(stop_max_attempt_number=10)
    def PHdownload(self, start, end, outdir):
        tsname = 'm3u8/'+outdir+'/'+str(start)+'.ts'
        if os.path.exists(tsname):
            if os.path.getsize(tsname) == 1024000 or os.path.getsize(tsname) == 1024001:
                return
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3559.6 Safari/537.36'}
        headers['Range'] = "bytes="+str(start)+"-"+str(end)
        res = requests.get(self.url, headers=headers)

        if not os.path.exists("m3u8/"+outdir):
            os.mkdir("m3u8/"+outdir)

        with open(tsname, 'wb') as f:
            f.write(res.content)
            if end == '':
                print('进度: 100%\n')
                # sys.stdout.write('\r\n')
                return
            num = int(end) / int(self.contentLen)
            jindu = '{:.1%}'.format(num)
            sys.stdout.flush()
            print(jindu,end='\r')

    def GetContentLen(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3559.6 Safari/537.36'}
        headers['Range'] = "bytes=0-2"
        # length = int(requests.get(url, headers=headers).headers['Content-Range'].split('/')[1])
        head = requests.get(self.url, headers=headers).headers
        length = str(head)
        a = re.findall(r'\d\/(\d+?)\'', length)
        print('大小:'+str(int(a[0])/1024/1024)+'M ('+a[0]+')')
        if len(a) == 0:
            return -1

        return int(a[0])

    def run(self):
        content = requests.get(self.url).content.decode("utf8")
        c = re.findall(
            r'var flashvars_\d+?\s+?=\s+?(\{.+?\});', str(content))[0]
        self.title = tools.Replace(re.findall(r'\<title\>(.+?)\</title\>', str(content))[0])
        print(self.title)
        c = json.loads(c)

        i = 0
        url = c['mediaDefinitions'][i]['videoUrl']
        while url == '':
            i = i+1
            url = c['mediaDefinitions'][i]['videoUrl']
        print('实际地址：'+url)
        self.url = url

        self.contentLen = self.GetContentLen()
        if self.contentLen == -1:
            return

        target = [0, 1023999]
        f_list = []
        p = ThreadPoolExecutor(self.PoolNum)
        start_time = time.time()
        haveMore = False
        while True:
            future = p.submit(
                self.PHdownload, target[0], target[1], self.title)
            f_list.append(future)
            if (target[1] + 1024000) >= self.contentLen:
                haveMore = True
                print('最后一部分: '+str(target))
                break
            target[0] = int(target[1]) + 1
            target[1] = target[1] + 1024000

        wait(f_list, return_when='ALL_COMPLETED')
        if haveMore:
            self.PHdownload(target[1]+1, '', self.title)
        end_time = time.time()
        print("耗时: "+str(int(end_time)-int(start_time))+'s')
        b_hebin('m3u8/'+self.title+'/', 'mp4/'+self.title+'.mp4')
