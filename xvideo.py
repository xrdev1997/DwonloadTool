from concurrent.futures import ThreadPoolExecutor, wait
import re
import requests
import os
import time
from tools.tools import b_hebin

from retrying import retry

def xvideo_ffmpeg(size, outdir, outname):
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

class Xvideo:
  def __init__(self, url,PoolNum=5):
    self.url = url
    self.PoolNum = PoolNum


  def getTrueUrl(self):
    res = requests.get(self.url)
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
    # print(requests.get(url_head+datas[0]).content.decode("utf8"))
    return str(title), url_head+datas[0], requests.get(url_head+m3u8).content.decode("utf8")

  def get_ts(self, url, ts_str):
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
  def download(self, tsurl, outputdir):
    if not os.path.exists("m3u8/"):
        os.mkdir("m3u8")
    content = requests.get(tsurl, timeout=6.2).content
    tsname = tsurl[tsurl.rfind("/") + 1:]
    # tsname = re.findall(r'p.{6}(\d+?\.ts)\?',tsname)[0]
    if len(re.findall(r'p(-)', tsname)):
        # https://www.xvideos.com/video49666459/25/_
        tsname = re.findall(r'p-.{5}(\d+?\.ts)', tsname)[0]
    else:
        tsname = re.findall(r'p(\d+?\.ts)', tsname)[0]

    if not os.path.exists("m3u8/"+outputdir):
        os.mkdir("m3u8/"+outputdir+"/")
    with open("m3u8/"+outputdir+"/" + tsname, "wb") as code:
        code.write(content)
    print(tsname)


  def run(self):
    self.title, self.url, self.content = self.getTrueUrl()
    self.ts_list = self.get_ts(self.url, self.content)
    print(self.ts_list)
    self.title = re.sub(re.compile(r"(&)|(;)|(/)|(\\)|(\s)|(,)", re.S), "",self.title)
    # title = title.replace('&', '').replace(';', '').replace(',', '').replace('-','_').replace(' ','_')
    f_list = []
    p = ThreadPoolExecutor(self.PoolNum)
    for temp in self.ts_list:
        future = p.submit(self.download, temp, self.title)
        f_list.append(future)

    wait(f_list, return_when='ALL_COMPLETED')

    b_hebin('m3u8/'+self.title+'/', 'mp4/'+self.title+'.mp4')




