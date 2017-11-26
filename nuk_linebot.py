import requests
import re
import random
import configparser
import urllib.request, json 
from snownlp import SnowNLP
import json 
from urllib.request import urlopen
import jieba
import csv
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from bs4 import BeautifulSoup as bs
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")
global g_data
g_data =[]

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'
@handler.add(MessageEvent, message=StickerMessage)
def handle_message_img(event):
    sticker_message = StickerSendMessage(
    package_id='1',
    sticker_id=str(random.randint(100,139))
    )
    line_bot_api.reply_message(event.reply_token,sticker_message)

@handler.add(MessageEvent, message=ImageMessage)
def handle__img(event):

    sticker_message = StickerSendMessage(
    package_id='1',
    sticker_id=str(random.randint(100,139))
    )
    line_bot_api.reply_message(event.reply_token,sticker_message)
      
@handler.add(MessageEvent, message=LocationMessage)
def handle_message_loc(event):
    #print(event.message.address)
    #line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您的位置: "+event.message.address+"\nlatitude:"+str(event.message.latitude)+"\nlongitude:"+str(event.message.longitude)))
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/1/10/TRA_Hsinchu_Station.jpg',
                title='左-功能選單',
                text='請點選以下功能',
                actions=[
                    MessageTemplateAction(
                        label='天氣',
                        text= "天氣 "+event.message.address
                    ),
                    URITemplateAction(
                        label='餐廳',
                        uri='http://140.127.220.234/hsinchuLINE/map.php?func=restaurant&lat='+str(event.message.latitude)+'&lng='+str(event.message.longitude)
                    ),
                    URITemplateAction(
                        label='景點',
                        uri='http://140.127.220.234/hsinchuLINE/map.php?func=sightseeing&lat='+str(event.message.latitude)+'&lng='+str(event.message.longitude)
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cyberisland.teldap.tw/fck_upload/Image/nEO_IMG_%E6%96%B0%E7%AB%B9%E5%B8%82%E6%9D%B1%E5%8D%80.jpg',
                title='右-功能選單',
                text='請點選以下功能',
                actions=[
                    URITemplateAction(
                        label='找廁所',
                        uri='https://www.google.com/maps/d/viewer?ll=24.790136874762855%2C120.92070964865115&hl=zh-TW&z=13&mid=1nQcNHRYIUl8gCvLAKafCQTp6dDoDSgrs'
                    ),
                    MessageTemplateAction(
                        label='公車資訊',
                        text='公車資訊'
                    ),
                    URITemplateAction(
                        label='旅館',
                        uri='http://140.127.220.234/hsinchuLINE/map.php?func=hotel&lat='+str(event.message.latitude)+'&lng='+str(event.message.longitude)
                    )
                ]
            )
        ]
       )
    )
        #event.message.longitude
        #str(event.message.latitude)
    asr=[]  
    profile = line_bot_api.get_profile(event.source.user_id)       
    asr.append(TextSendMessage(text ="您好"+profile.display_name+"，以下是我可以為您即時導覽的功能"))
    asr.append(carousel_template_message)
                 
    line_bot_api.reply_message(event.reply_token,asr)
        
   
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    
   
    if ''.join(event.message.text).find("天氣資訊") != -1:       
        content='請輸入地區查詢 \r\n例如：天氣 新竹'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    
    if ''.join(event.message.text).find("鄰近") != -1 or (''.join(event.message.text).find("觀光") != -1)or (''.join(event.message.text).find("導覽") != -1):       
        content='請分享你的位置\r\n 我們將會為您馬上進行分析'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if ''.join(event.message.text).find("使用") != -1or ''.join(event.message.text).find("開始") != -1:
        buttons_template = TemplateSendMessage(
            alt_text='開始使用 template',
            template=ButtonsTemplate(
                title='你好，您想要什麼服務資訊?',
                text='請選擇',
                thumbnail_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-1/p200x200/21270803_516219278712362_1328105763917699479_n.png?oh=2522fe8916bfde345808b605404c2964&oe=5A4E7B0E',
                actions=[
                    MessageTemplateAction(
                        label='公車資訊',
                        text='公車資訊'
                    ),
                    MessageTemplateAction(
                        label='天氣資訊',
                        text='天氣資訊'
                    ),
                    MessageTemplateAction(
                        label='鄰近地點觀光資訊',
                        text='鄰近地點觀光資訊'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

   

     

    
    if ''.join(event.message.text).find("公車資訊") != -1:  
        asr =[]    
        profile = line_bot_api.get_profile(event.source.user_id)
        asr.append(TextSendMessage(text ="您好"+profile.display_name+"\r\n請您輸入地點或是輸入「公車 查詢站點」 謝謝"))
        line_bot_api.reply_message(event.reply_token, asr)
        return 0  
        
  
         
    if str(event.message.text).find("天氣") != -1 and len(str(event.message.text).split(' '))>1 :
        strw = weather(str(event.message.text).split(' ')[1])
        content="目前 "+str(event.message.text).split(' ')[1] +"\r\n氣溫："+str(strw[1])+"\r\n天氣狀況："+str(strw[0])+"\r\n測量時間："+str(strw[2])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if str(event.message.text).find("公車") != -1 and len(str(event.message.text).split(' '))>1 :
        
        content="請點選網址: \r\n"+"http://140.127.220.234/hsinchuLINE/bus.php?stop="+(event.message.text).split(' ')[1]

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0    
    if str(event.message.text).find("天氣") != -1:
        asr=[]
        profile = line_bot_api.get_profile(event.source.user_id)
        asr.append(TextSendMessage(text ="您好"+profile.display_name+"\\r\n請您輸入地點或是輸入「天氣 查詢地區」 謝謝"))
        line_bot_api.reply_message(event.reply_token, asr)
        return 0    
    asr =[]
    asr.append(TextSendMessage(text = str('不好意思 \r\n本系統目前沒有辦法針對您的問題做解答，以下是我在網路上找到的「'+ event.message.text +'」相關資料如下：')))
    strt = news(event.message.text)
    asr.append(TextSendMessage(text = str(strt)))
        
    line_bot_api.reply_message(event.reply_token, asr) 
def news(strs):
   res = requests.get('https://tw.answers.search.yahoo.com/search?fr=uh3_answers_vert_gs&type=2button&p='+ strs)
   soup = bs(res.text, 'html.parser')
   mydivs = soup.findAll("div", { "class" : "AnswrTWHKv2" })
   s=0
   c=0
   content=''
   for p in mydivs:
     if c <5:
       s=0
       for a in p.find_all('a', href=True):
         if s==0:
           content += a.text+'\r\n'        
           content += str(a['href']).split('&sa')[0]+'\r\n\r\n'
           c = c+1
           s=1
 
   return content
    
def img_get(strs):
   res = requests.get('https://tw.answers.search.yahoo.com/search?fr=uh3_answers_vert_gs&type=2button&p='+ strs)
   soup = bs(res.text, 'html.parser')
   mydivs = soup.findAll("div", { "class" : "AnswrTWHKv2" })
   s=0
   c=0
   content=''
   for p in mydivs:
     if c <5:
       s=0
       for a in p.find_all('a', href=True):
         if s==0:
           content += a.text+'\r\n'        
           content += str(a['href']).split('&sa')[0]+'\r\n\r\n'
           c = c+1
           s=1
 
   return content
def weather(str):
    url = 'https://works.ioa.tw/weather/api/all.json'
    res = requests.get(url)
    weather_list = []
    data = res.json()
    for s in data:  
             if s["name"] =="新竹":
                 if (s["name"] =="新竹"and s["name"] !=str):
                     for sc in s["towns"]:
                        print(sc["name"])
                        if (sc["name"].find(str) != -1 or str.find(sc["name"]) != -1):
                            print(sc["id"])
                            url2 = "https://works.ioa.tw/weather/api/weathers/"+s["id"]+".json"
                            res = requests.get(url2)
                            data_w = res.json()
                            weather_list.append(data_w["desc"])
                            weather_list.append(data_w["temperature"])
                            weather_list.append(data_w["at"])
                            weather_list.append("https://works.ioa.tw/weather/img/weathers/zeusdesign/"+data_w["img"])
                 else:
                     url2 = "https://works.ioa.tw/weather/api/weathers/"+s["id"]+".json"
                     res = requests.get(url2)
                     data_w = res.json()
                     weather_list.append(data_w["desc"])
                     weather_list.append(data_w["temperature"])
                     weather_list.append(data_w["at"])
                     weather_list.append("https://works.ioa.tw/weather/img/weathers/zeusdesign/"+data_w["img"])
    return weather_list

def demo(inp):
    ya = []
    with urllib.request.urlopen("http://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable?$format=JSON") as url:
        data = json.loads(url.read().decode())   
    
    for s in data:  
         # print(s["StopTimes"])
          a = 0
         # print ("-班次----------")
          l = []

          for se in s["StopTimes"]:
               if se["StationName"]["Zh_tw"] == "左營":
                    a = 1
                 #   print(se["StationName"]["Zh_tw"]," 到達時間: ",se["ArrivalTime"])
               if a == 1 :
                   l.append(se["StationName"]["Zh_tw"]+" 時間: "+se["ArrivalTime"])
                   #南港 台北 板橋 桃園 新竹 苗栗 台中 彰化 雲林 嘉義 台南 左營
          ya.append(l)   
    str_steps = "南港 台北 板橋 桃園 新竹 苗栗 台中 彰化 雲林 嘉義 台南 左營"
    check = 0
    outp = ""
    sts = []
    for stp in str_steps.split(" "):
        if inp.find(stp) != -1:
            check = check+1
            if check ==1:
            	start=stp
            if check ==2:
            	end = stp
    if check ==2:
        for ea in ya:
            if  ''.join(ea).find(start) != -1 &''.join(ea).find(end)!=-1:
                st=[]
           
                for step in ea:
                    if ''.join(step).find(start) !=-1 or ''.join(step).find(end) !=-1:
                        st.append(step)
                       # print(ea)
                       # print ("-班次----------")
                if len(st) >1:  
                    print (st[0],st[1])
                    outp = outp,st[0],st[1]
                    sts.append(st[0]+st[1])
                    print ("-班次----------")
            else:
                  False

	
    #sts_sort = sts.sort()
    sets = sorted(sts)
    set =  '\r\n'.join(sets)
    a =""
    return set
if __name__ == '__main__':
    app.run()
