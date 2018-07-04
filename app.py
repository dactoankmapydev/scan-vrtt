from flask import Flask, render_template, request, url_for, redirect
from requests_html import HTMLSession
import io, csv, json

app = Flask(__name__)

session = HTMLSession()
session.browser

def crawl(links):
    for link in links:
        r=session.get(link)
        r.html.render(sleep=0.9)
        rate = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[1]/h1')[0].text.split('\n')[0]
        filename = r.html.xpath('//*[@id="file-summary"]/tbody/tr[2]/td')[0].text.split('\n')[0]
        filesize = r.html.xpath('//*[@id="file-summary"]/tbody/tr[3]/td')[0].text.split('\n')[0]
        result = r.html.xpath('//*[@id="pages"]/vt-result-file/div/vt-result-header/section/header/div[2]/h1/div')[0].text.split('\n')[1]   
        

@app.route('/upload', methods=['GET','POST'])
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
        links = []
        for i in sha:
            url = 'https://www.virustotal.com/#/file/'+i+'/detection'
            links.append(url)
        crawl(links)
        return 'ok'

@app.route('/')
def home():
    return render_template("choosefile.html")

if __name__ == '__main__':
    app.run(debug = True)
