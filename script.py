from requests_html import HTMLSession
import csv
import requests, time, os
from multiprocessing import Pool



def crawl(link):

    session = HTMLSession()
    session.browser
    r=session.get(link)
    r.html.render()

    rate = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[1]/h1')[0].text.split('\n')[0]
    filename = r.html.xpath('//*[@id="file-summary"]/tbody/tr[2]/td')[0].text.split('\n')[0]
    filesize = r.html.xpath('//*[@id="file-summary"]/tbody/tr[3]/td')[0].text.split('\n')[0]
    result = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[2]/h1/div')[0].text.split('\n')[1]
    return(rate,filename,filesize,result)
    #return(rate,result)

if __name__ == '__main__':

    file=open(os.path.join(os.getcwd(),'logvr (copy).csv'), "r")
    reader = csv.reader(file)
    data = list(reader)
    sha = data[1]
    urls = []
    for i in sha:
        url = 'https://www.virustotal.com/#/file/'+i+'/detection'
        urls.append(url)
    print("start.....")
    thread_pool = Pool(5)
    start = time.time()

    print(thread_pool.map(crawl, urls))

    print(str(time.time()-start)+'seconds')
