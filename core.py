#!/usr/bin/python3
import os
import time
import _thread
import subprocess
from slackclient import SlackClient
import requests
import re
import random
def videoanalyze(link):
  #<div class="watch-view-count">721,494 views</div>
  page = requests.get(link)
  pagefile=open("page.txt","w")
  print(page.text,file=pagefile)
  views = re.search("<div class=\"watch-view-count\">(\d*)(.*)(\d*)(.*)(\d*)", page.text)
  views = views.group(1)+views.group(2)+views.group(3)+views.group(4)+views.group(5)
  views=views.split()[0]
  textmessage="Bu videonun "+views+" izlenmesi var."
  return textmessage


def finduserbyid(id):
  a=sc.api_call("users.list")
  for user in a["members"]:
      if(user["id"]==str(id)):
        return user["name"]
def findchannelbyid(id):
    a=sc.api_call("channels.list")
    for channel in a["channels"]:
        if(channel["id"]==str(id)):
          return channel["name"]
def analyze(data):
  print(data)
  if(data["type"]=="message"):
    if("samaritan" in data["text"].lower()):
      dertli=0
      for elem in dertkeywords:
        if(elem in data["text"].lower()):
          textmessage=finduserbyid(data["user"])+", "+barmentavsiyeleri[random.randint(0,len(barmentavsiyeleri))]
          sc.rtm_send_message(data["channel"],textmessage)
          dertli=1
          break
      #print("Efendim , "+finduserbyid(data["user"]))
      if(finduserbyid(data["user"])!="ze0bot" and not dertli):
        textmessage="Efendim,  "+finduserbyid(data["user"])
        sc.rtm_send_message(data["channel"],textmessage)
      dertli=0
    elif(findchannelbyid(data["channel"])=="git"):
      try:
        if(data["bot_id"]==GITBOT):
          textmessage="Oooo commit alırım bi dal"
          sc.rtm_send_message("#botlamuhabbet",textmessage)
      except:
        pass

    elif("py-dev" in data["text"].lower()):
      codetex=data["text"].lstrip("py-dev")
      codetex=codetex.lstrip()
      codefile=open("code.py","w")
      print(codetex,file=codefile)
      codefile.close()
      pyproc= subprocess.Popen("python3 code.py",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
      (ans,error) = pyproc.communicate()
      print(ans)
      if(ans==b''):
        textmessage="Check your code !\n"+error.decode()
        sc.rtm_send_message(data["channel"],textmessage)
      else:
        textmessage="Output : \n"+ans.decode()
        sc.rtm_send_message(data["channel"],textmessage)
    elif("youtube.com" in data["text"]):
      textmessage=videoanalyze(data["text"].lstrip("<").rstrip(">"))
      sc.rtm_send_message(data["channel"],textmessage)


def listen():
  if sc.rtm_connect():
      while True:
          data=sc.rtm_read()
          if(data!=[]):
            try:
              print(data[0]["team"])
              if(data[0]["team"]==TEAM):
                #print("var böyle bi mesaj")
                _thread.start_new_thread(analyze,(data[0],))
            except:
              nothing=0
          time.sleep(1)
  else:
      print("Connection Failed, invalid token?")

random.seed()
conffile=open("slack.config","r")
SLACK_BOT_TOKEN=conffile.readline().lstrip("SLACK_BOT_TOKEN=").rstrip()
#print(SLACK_BOT_TOKEN)
TEAM=conffile.readline().lstrip("TEAM").rstrip()
TEAM=TEAM.lstrip("=")
#print(TEAM)
GITBOT=conffile.readline().lstrip("GITBOT=").rstrip()
#print(GITBOT)
sc = SlackClient(SLACK_BOT_TOKEN)
barmentavsiyeleri=["Ya bir yol bul, ya bir yol aç, ya da yoldan çekil","En büyük savunma savaştır","The beauty is just an illusion","Bazen tutmak, bırakmaktan daha çok acıtır","Senden iyisini mi bulacak","Akışına bırak","Zaman her şeyin ilacıdır","Emeklerinin karşılığını alacaksın","Bir gün sen de mutlu olacaksın","Öldürmeyen şey güçlendirir","Günün en karanlık anları tan ağarmadan önceki dakikalardır","Günün en karanlık anları tan ağarmadan önceki dakikalardır","Act without expectation","Hayat provası olmayan bir oyundur","Karanlığa söveceğine bir mum yak","Derin olan kuyu değil, kısa olan iptir","Marifet hiç düşmemek değil, her düştüğünde kalkabilmektir","Alfred why do we fall","l'amour fait mal","Yavaş yürüyene çelme takılmaz"]
dertkeywords=["dert","üzgünüm","üzgün","dertli","dertliyim","hüzün","hasret","acı"]
listen()