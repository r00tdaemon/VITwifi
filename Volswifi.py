from flask import Flask,render_template,request
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


app = Flask(__name__)
d={'Jan':'1','Feb':'2','Mar':'3','Apr': '4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sept':'9','Oct':'10','Nov':'11','Dec':'12'}

@app.route('/',methods=['GET','POST'])

def index():
    global d
    if request.method=='POST':
        uname=request.form['uname']
        upass=request.form['upass']
        day=request.form['day']
        m=request.form['month']
        month=d[m]
        day=str(int(day)-1)
        year=request.form['year']
        if (int(month) not in [x for x in range(1,13)] or int(day)>31 or int(day)<1 or len(str(year))>4 or uname=='' or upass==''):
            return render_template("error.html")
        url='http://115.248.50.60/registration/Main.jsp?wispId=1&nasId=28:92:4a:3a:cc:1c'
        headers={'Host':'115.248.50.60','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate','Connection':'keep-alive','Cache-Control':'max-age=0'}

        re=urllib.request.Request(url,headers=headers)
        response=urllib.request.urlopen(re)
        cookie = response.headers.get('Set-Cookie')


        url='http://115.248.50.60/registration/chooseAuth.do'
        values1={'loginUserId':uname,'authType':'Pronto','loginPassword':upass,'submit':'Login'}
        data1=urllib.parse.urlencode(values1)
        data1=data1.encode('utf-8')
        headers={'Cookie':cookie,'Host':'115.248.50.60','User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        req1=urllib.request.Request(url,data1,headers)
        resp1=urllib.request.urlopen(req1)
        #respData1=resp1.read()
        #soup1=BeautifulSoup(respData1,"html.parser")

        month=str(int(month)-1)
        global start_date
        start_date=[]
        start_date.append(day)
        start_date.append(str(int(month)-1))
        if (int(start_date[1])<0):
            start_date[1]=str(int(start_date[1])+12)
        start_date.append(year)
        if (month=='0'):
            start_date[2]=str(int(start_date[2])-1)
        if (int(day)==31 and int(month) in [0,2,4,6,7,9,11]):
            start_date[0]=str(int(start_date[0])-1)
        url="http://115.248.50.60/registration/customerSessionHistory.do"
        values={"location":"allLocations",'parameter':'custom','customStartMonth':start_date[1],'customStartDay':start_date[0],'customStartYear':start_date[2],'customEndMonth':month,'customEndDay':day,'customEndYear':year,'button':'View'}
        headers={'Cookie':cookie}
        data=urllib.parse.urlencode(values)
        data=data.encode('utf-8')
        req=urllib.request.Request(url,data,headers)
        resp=urllib.request.urlopen(req)
        respData=resp.read()


        soup=BeautifulSoup(respData,"html.parser")

        error_date=soup.find('font',{'color':'red'})
        if (error_date!=None):
            error_date=str(error_date).lstrip('</font color="red" face="arialverdana" size="2">')
            error_date=error_date.rstrip('</font>')
            return(error_date)


        output=(soup.find_all('b')[-1])
        output=str(output).strip('</b>')
        return("You've currently used: "+output)
    return render_template('index.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.html'), 500
if __name__ == '__main__':
   app.run()
