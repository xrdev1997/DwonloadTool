import os,sys,re,json
from tqdm import tqdm
import requests,time
import MultiDownloader
from concurrent.futures import ThreadPoolExecutor,wait


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3559.6 Safari/537.36'}

def b_hebin(dir,outDir):
  DirFiles = os.listdir(dir)
  DirFiles.sort(key=lambda x: int(x[:-3]))

  OutFile = open(outDir,'wb')
  for temp in tqdm(DirFiles):
    ts = open(dir+temp,'rb')
    OutFile.write(ts.read())
    ts.close()
  OutFile.close()


def GetContentLen(url):
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3559.6 Safari/537.36'}
  headers['Range'] = "bytes=0-1024"
  length = int(requests.get(url,headers=headers).headers['Content-Range'].split('/')[1])
  print('length: '+str(length))
  return length

def download(url,start,end,outdir):
  print('start: '+str(start))

  headers['Range'] = "bytes="+start+"-"+end
  res = requests.get(url,headers=headers)
  if not os.path.exists("m3u8/"):
    os.mkdir("m3u8")
  if not os.path.exists("m3u8/"+outdir):
    os.mkdir("m3u8/"+outdir)
    
  with open('m3u8/'+outdir+'/'+str(start)+'.ts','wb') as f:
    f.write(res.content)
    print('end: '+str(start))


def Pronhub():
  content = requests.get('https://www.pornhub.com/view_video.php?viewkey=ph5bdaddc8be24c').content.decode("utf8")
  c = re.findall(r'var flashvars_\d+?\s+?=\s+?(\{.+?\});',str(content))[0]
  title = re.findall(r'\<title\>(.+?)\</title\>',str(content))[0].replace('-','_').replace(' ','_')
  print(title)
  c = json.loads(c)
  url = c['mediaDefinitions'][2]['videoUrl']
  print(url)

  
if __name__ == "__main__":
  
  
  Pronhub()
  b_hebin('m3u8/Cumming_in_my_Panties_and_Yoga_Pants_and_Pull_them_up_before_Gym___Pornhub.com/','aaa.mp4')

  # headers['Range'] = "bytes=0-1024000"
  # res = requests.get(url,headers=headers)
  # with open('./a.mp4','wb+') as f:
  #   f.write(res.content)
  # print(res.headers['Content-Range'].split('/')[1])

  # ts_list = []
  # f_list = []
  # p = ThreadPoolExecutor(5)
  # for temp in ts_list:
  #     # future = p.submit(download,temp,outputdir)
  #     # f_list.append(future)

  # wait(f_list,return_when='ALL_COMPLETED')
  # MultiDownloader.download(url,'mp4/'+title+'.mp4')

  
    