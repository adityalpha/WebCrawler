
from flask import Flask, redirect, url_for, request , render_template
from bs4 import BeautifulSoup
import csv 
import requests 

app = Flask(__name__) 

@app.route('/') 
def main(): 
    return render_template("main.html")
  
@app.route('/results',methods = ['POST', 'GET']) 
def results(): 
    if request.method == 'POST': 
        query = request.form['query'] 
        #return redirect(url_for('success',query = query)) 
    else: 
        #user = request.args.get('nm') 
        #return redirect(url_for('success',name = user))
        return render_template("access.html")

    query='+'.join(query.split())
    URL1 ="http://www.youtube.com/results?search_query=" + query
    URL2 ="https://en.wikipedia.org/w/index.php?search=%7E"+query+"&title=Special%3ASearch&go=Go&ns0=1"
    r1 = requests.get(URL1)
    r2 = requests.get(URL2)
    soup1 = BeautifulSoup(r1.content, 'html.parser')
    soup2 = BeautifulSoup(r2.content, 'html.parser')

    data = {'YouTube':
            {'title':[],'desc':[],'thumb':[]},
           'Wikipedia':
            {'title':[],'desc':[]},
          }

    n=0
    for content in soup1.find_all('div', class_= "yt-lockup"):
        n+=1
        if n==6:
	        break
        try:
            title = content.find('div', class_="yt-lockup-content").h3.a.text
            data['YouTube']['title'].append(title)

            desc = content.find('div', class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2").text
            data['YouTube']['desc'].append(desc)

            thumb = content.find('span', class_="yt-thumb-simple").img['src']
            data['YouTube']['thumb'].append(thumb)

        except Exception as e:
            description = None
    n=0
    
    for content in soup2.find_all('li', class_= "mw-search-result"):
        n+=1
        if n==6:
	        break    
        try:
            title = content.find('div', class_="mw-search-result-heading").a['title']
            data['Wikipedia']['title'].append(title)
            #''.join(map(str, div.contents))
            description = content.find('div', class_="searchresult").contents
            desc=""
            for i in map(str,description):
                if len(i)>4 and i[:5:]=="<span":
                    desc+=i[i.find('>')+1:i[1::].find('<'):]
                else:
                    desc+=i
            data['Wikipedia']['desc'].append(desc)
        except Exception as e:
            description = None


    return render_template("results.html",data=data)
       
        
  
if __name__ == '__main__': 
   app.run(debug = True) 
