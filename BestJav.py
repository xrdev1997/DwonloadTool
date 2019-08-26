import sys,time,requests,re
from tools import tools
from retrying import retry
 


class BestJav:
  def __init__(self,url):
    self.url = url

  @retry(stop_max_attempt_number=100)
  def SelectUrl(self):
    while True:
      print(self.title)
      print('============请选择下载============')
      for i,temp in enumerate(self.Types):
        print(str(i)+'.清晰度: '+temp['label'])
      num = input('请输入你要下载的选择(输入q退出):')
      if num == 'q':
        break
      num = int(num)

      print('真实下载地址: '+self.Types[num]['url'])
      tools.DefaultDownload(self.Types[num]['url'],self.title)
      break


  def GetType(self,content):
    self.Types = []
    urls = re.findall(r'file:\s{0,}\"(.+?)\"',content,re.S)
    labels = re.findall(r'label:\s{0,}\"(.+?)\"',content,re.S)
    for i,label in enumerate(labels):
      self.Types.append({'label':label,'url':urls[i]})

  def ResolveIframe(self,iframe_url):
    content = requests.get(iframe_url).content.decode('utf8')
    # with open('out.html','w+',encoding='utf8') as f:
    content = re.findall(r'sources\:\s+?\[\s+?(\{.+?),\]',content,re.S)[0]
    self.GetType(content)
    self.SelectUrl()


  def Resolve(self):
    content = requests.get(self.url).content.decode('utf8')
    self.title = tools.Replace(re.findall(r'<title>(.+?)<',content,re.S)[0])
    content = re.findall(r'append\(\'\<iframe src=\"//(.+?)\"',content)[0]
    
    self.ResolveIframe('https://'+content)

  def download(self):
    self.Resolve()



url = 'https://bestjavporn.com/video/avop-155-english-sub-blind-love-i-d-be-so-lonely-without-my-dad-ayane-suzukawa/'




if __name__ == "__main__":
    best = BestJav(url)
    best.download()