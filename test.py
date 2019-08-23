import sys,time
 
for i in range(30):
  #打印一个#号，这种方法打印不会自动换行
  sys.stdout.write('#\r')
  #实时刷新一下，否则上面这一条语句，会等#号全部写入到缓存中后才一次性打印出来
  sys.stdout.flush()
  #每个#号等待0.1秒的时间打印
  time.sleep(0.1)