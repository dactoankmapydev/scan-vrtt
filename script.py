from requests_html import HTMLSession
import csv
import multiprocessing.dummy
import requests, time



def crawl(link):

    #r=session.get(link)
    #r.html.render()
    #rate = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[1]/h1')[0].text.split('\n')[0]
    #filename = r.html.xpath('//*[@id="file-summary"]/tbody/tr[2]/td')[0].text.split('\n')[0]
    #filesize = r.html.xpath('//*[@id="file-summary"]/tbody/tr[3]/td')[0].text.split('\n')[0]
    #result = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[2]/h1/div')[0].text.split('\n')[1]
    #return(filename+' '+filesize+' '+rate+' '+result)
    #return(rate)
    session.get(link).html.render(sleep=0.9)
    return(session.get(link).html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[1]/h1'))


if __name__ == '__main__':

    file=open('/home/dactoankma/scanvr/scan-vrtt/logvr (copy).csv', "r")
    reader = csv.reader(file)
    data = list(reader)
    sha = data[1]
    urls = []
    for i in sha:
        url = 'https://www.virustotal.com/#/file/'+i+'/detection'
        urls.append(url)
    #print(urls)
    print("start.....")
    thread_pool = multiprocessing.dummy.Pool(4)
    start = time.time()
    session = HTMLSession()
    session.browser

    print(thread_pool.map(crawl, urls))
    print(str(time.time()-start)+'seconds')
