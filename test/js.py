import js2py
from bs4 import BeautifulSoup as bs


if __name__ == "__main__":
  with open('./view_video.php') as fp:
    html = fp.read()
  
  html=bs(html,'html.parser')

  
  jsStr = html.select("#player script")[0].string

  try:
    context = js2py.EvalJs()
    context.execute(jsStr)
  except Exception as e:
      pass
      
  context.eval('quality_1080p || quality_720p || quality_480p || quality_240p')
