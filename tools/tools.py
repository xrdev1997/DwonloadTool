import os,requests,re,sys,time
from tqdm import tqdm
from retrying import retry
from concurrent.futures import ThreadPoolExecutor, wait




def Replace(content):
    return content.replace('/', '').replace('-', '_').replace(
            ' ', '_').replace(';', '_').replace(')', '_').replace(':', '_').replace('&', '_').replace('#', '_')

def b_hebin(dir, outDir):
    DirFiles = os.listdir(dir)
    DirFiles.sort(key=lambda x: int(x[:-3]))
    OutFile = open(outDir, 'wb')
    for temp in DirFiles:
        ts = open(dir+temp, 'rb')
        OutFile.write(ts.read())
        ts.close()
    OutFile.close()
    print('合并成功')


def GetContentLen(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3559.6 Safari/537.36'}
    headers['Range'] = "bytes=0-2"
    # length = int(requests.get(url, headers=headers).headers['Content-Range'].split('/')[1])
    head = requests.get(url, headers=headers).headers
    length = str(head)
    a = re.findall(r'\d\/(\d+?)\'', length)
    print('大小:'+str(int(a[0])/1024/1024)+'M ('+a[0]+')')
    if len(a) == 0:
        return -1

    return int(a[0])

@retry(stop_max_attempt_number=10)
def download(url,contentLen, start, end, outdir):
    tsname = 'm3u8/'+outdir+'/'+str(start)+'.ts'
    if os.path.exists(tsname):
        if os.path.getsize(tsname) == 1024000 or os.path.getsize(tsname) == 1024001:
            return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3559.6 Safari/537.36'}
    headers['Range'] = "bytes="+str(start)+"-"+str(end)
    res = requests.get(url, headers=headers)

    if not os.path.exists("m3u8/"+outdir):
        os.mkdir("m3u8/"+outdir)

    with open(tsname, 'wb') as f:
        f.write(res.content)
        if end == '':
            print('进度: 100%\n')
            # sys.stdout.write('\r\n')
            return
        num = int(end) / int(contentLen)
        jindu = '{:.1%}'.format(num)
        sys.stdout.flush()
        print(jindu,end='\r')
        # sys.stdout.write(jindu+'\r')


def DefaultDownload(url,title):
    contentLen = GetContentLen(url)
    if contentLen == -1:
        return
    target = [0, 1023999]
    f_list = []
    p = ThreadPoolExecutor(30)
    start_time = time.time()
    haveMore = False
    while True:
        future = p.submit(
            download, url, contentLen,target[0], target[1], title)
        f_list.append(future)
        if (target[1] + 1024000) >= contentLen:
            haveMore = True
            print('最后一部分: '+str(target))
            break
        target[0] = int(target[1]) + 1
        target[1] = target[1] + 1024000

    wait(f_list, return_when='ALL_COMPLETED')
    if haveMore:
        download(url,contentLen,target[1]+1, '', title)
    end_time = time.time()
    print("耗时: "+str(int(end_time)-int(start_time))+'s')
    b_hebin('m3u8/'+title+'/', 'mp4/'+title+'.mp4')   
        
