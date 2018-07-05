from flask import Flask, render_template, request, url_for, redirect
from requests_html import HTMLSession
from flask_table import Table, Col
import io, csv, json, time

app = Flask(__name__)

session = HTMLSession()
session.browser


class ItemTable(Table):
    file_name = Col('File Name')
    file_size = Col('File Size')
    file_rate = Col('Rate')
    file_result = Col('Result')


def crawl(links,path):
    list_res = []
    for link in links:
        
        r=session.get(link)
        r.html.render(sleep=0.9)
        rate = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[1]/h1')[0].text.split('\n')[0]
        filetype = r.html.xpath('//*[@id="content"]/vt-file-details-basic/vt-keyval-table/div/div/div[5]/div[2]')[0].text.split('\n')[0]
        filename = r.html.xpath('//*[@id="file-summary"]/tbody/tr[2]/td')[0].text.split('\n')[0]
        filesize = r.html.xpath('//*[@id="file-summary"]/tbody/tr[3]/td')[0].text.split('\n')[0]
        result = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[2]/h1/div')[0].text.split('\n')[1]  
        res = result,rate,filesize,filetype,filename
        list_res.append(res)

    results = (list(zip(list_res,path)))
    list_results = []
    for result in results:
        list_result = list(result[0])
        list_result.append(result[1])
        tuple_result = tuple(list_result)
        list_results.append(tuple_result[::-1])
    print(list_results)


@app.route('/scan', methods=['GET','POST'])
def upload():
    if 'file' not in request.files: 
        return json.dumps({
            'status': '400',
            'message': 'No file found'
        }), 400
    file = request.files['file']

    if file :
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        csv_data = list(csv_input)
        sha = csv_data[1]
        path = csv_data[0]
        links = []
        for i in sha:
            url = 'https://www.virustotal.com/#/file/'+i+'/detection'
            links.append(url)
        start = time.time()
        crawl(links,path)
        print(str(time.time()-start)+'seconds')  
        return 'ok'


@app.route('/')
def home():
    return render_template("choosefile.html")


if __name__ == '__main__':
    app.run(debug = True)
