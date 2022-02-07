# -*- coding:UTF-8 -*-
from PIL import Image,ImageFont,ImageDraw
import requests
import urllib
import urllib.request
import win32api,win32con,win32gui
import json
import os
import time,datetime,threading
from tkinter import Button,Tk,PhotoImage,Label,Text
import tkinter.messagebox


#http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/2019/01/05/131000_0_0.png

# TIMEDATA_URL = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json" THE PAGE IS NOT AVAILABLE

TIMEDATA_URL = "https://himawari8.nict.go.jp/img/FULL_24h/latest.json"
# EARTH_URL = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/{}/{}/{}/{}_0_0.png"
EARTH_URL = "https://himawari8.nict.go.jp/img/D531106/1d/550/{}/{}/{}/{}_0_0.png"
WTER_URL = "http://api.yytianqi.com/observe?city=CH010100&key=mu1lfn6pa8nibus8"
HITOKOTO_URL = "https://v1.hitokoto.cn"

tag = 0

get_earth_tag = 0
latest_earth_file_path = ""


def text_display(strs):
    text1.insert(1.0,strs+"\n")
    top.update()



def read_url(url_ok):
    """
    读取解析网址
    """
    web_html = ""
    try :
        web_html=urllib.request.urlopen(url_ok).read().decode('utf-8')
    except BaseException:
        text_display("error: reading url: "+url_ok)

    return web_html

def get_json(html):
    """
    将得到的信息解析为json格式
    """
    web_json = {}
    try :
        web_json=json.loads(html)
    except BaseException:
        text_display("error: parsing to json: "+html)

    return web_json

def url_provider(timedata,earthurl):
    earth_time = timedata.get("date")
    print(earth_time)
    year = earth_time[0:4]
    month = earth_time[5:7]
    day = earth_time[8:10]
    hms = str(earth_time[11:13]+earth_time[14:16]+earth_time[17:19])

    time_name = year+month+day+hms
    url = earthurl.format(year,month,day,hms)
    return url,time_name

def img_get(img_url,time_name):
    img = requests.get(img_url)
    f = open(time_name+".png",'ab')
    f.write(img.content)
    f.close()
    print("保存Pic:"+time_name+".png")
    return img

def img_edit(img,time_name,timedata,wterdata,hitokoto_json):
    #新建一个背景图层,其分辨率符合用户桌面分辨率,然后将重合两个图片
    screenX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screenY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    bg_img = Image.new('RGBA', (screenX,screenY), (0,0,0,255))#新建壁纸背景
    earth_img = Image.open(time_name+".png")#打开得到的地球图片
    bg_img.paste(earth_img,(screenX//2-550//2,screenY//2-550//2))#重合
    logo = Image.open('logo.png')
    bg_img.paste(logo,(screenX-250,screenY//2))

    # 时间转换,进行加8小时,得到东八区区时
    # 将str格式的时间转换为datetime格式
    chinaTime = datetime.datetime.strptime(timedata.get('date'), '%Y-%m-%d %H:%M:%S')
    # 将datetime格式的时间转换成时间戳格式,再加上八小时的毫秒数
    chinaTime = int(time.mktime(chinaTime.timetuple())) + 8 * 60 * 60
    # 时间戳转为datetime
    chinaTime = datetime.datetime.fromtimestamp(chinaTime)
    text_display("零时区的时间:"+timedata.get('date'))
    text_display("东八区区时:"+str(chinaTime))

    hitokoto_str = hitokoto_json.get("hitokoto") + "   ——" + hitokoto_json.get("from")

    fontFolder = r'C:\Windows\Fonts'
    # fontFolder = r'\\'
    blackFont1 = ImageFont.truetype(os.path.join(fontFolder, 'msyh.ttc'), size=20)
    blackFont2 = ImageFont.truetype(os.path.join(fontFolder, 'msyh.ttc'), size=90)
    blackFont3 = ImageFont.truetype(os.path.join(fontFolder, 'msyh.ttc'), size=30)
    blackFont80 = ImageFont.truetype(os.path.join(fontFolder, 'msyh.ttc'), size=80)
    # blackFont1 = ImageFont.truetype(os.path.join(fontFolder, 'DENGGB.TTF'), size=20)
    # blackFont2 = ImageFont.truetype(os.path.join(fontFolder, 'DENGGB.TTF'), size=90)
    # blackFont3 = ImageFont.truetype(os.path.join(fontFolder, 'DENGGB.TTF'), size=30)
    # blackFont80 = ImageFont.truetype(os.path.join(fontFolder, 'DENGGB.TTF'), size=80)
    tx_time = ImageDraw.Draw(bg_img)
    tx_time.text((screenX-250+12,screenY//2+55), str(chinaTime), fill='white', font=blackFont1)

    try :
        tx_wter_qw = ImageDraw.Draw(bg_img)
        tx_wter_du = ImageDraw.Draw(bg_img)
        tx_wter_tq = ImageDraw.Draw(bg_img)
        tx_wter_ct = ImageDraw.Draw(bg_img)
        wter_qw = str(wterdata.get('data').get('qw'))

        tx_hitokoto = ImageDraw.Draw(bg_img)


      # wter_tq = int(str(wterdata.get('data').get('numtq')))
      # print(wter_tq)
      #
      # if wter_tq == 2:
      #   tqlogo = Image.open('02.png')
      #   bg_img.paste(tqlogo, (screenX - 500, screenY // 2))
 #90大小的最优间隔 65px,所以就有了下面三行的位置的算法
      # tx_wter_qw.text((screenX - 250 + 12, screenY -650), wter_qw, fill='white', font=blackFont2)
      # tx_wter_du.text((screenX - 250 + len(wter_qw)*65, screenY - 630),  "°", fill='white',font=blackFont3)
      # tx_wter_tq.text((screenX - 250 + len(wter_qw)*65, screenY - 587), str(wterdata.get('data').get('tq')), fill='white', font=blackFont3)
      # tx_wter_ct.text((screenX - 250 + 16, screenY - 540), "桂林市", fill='white', font=blackFont1)
        tx_wter_qw.text((screenX * 0.84 , screenY * 0.2), wter_qw, fill='white', font=blackFont2)
        tx_wter_du.text((screenX * 0.92, screenY * 0.22), "°", fill='white', font=blackFont3)
        tx_wter_tq.text((screenX * 0.92, screenY * 0.313), str(wterdata.get('data').get('tq')),
                        fill='white', font=blackFont3)
        tx_wter_ct.text((screenX * 0.843, screenY * 0.323), "北京市", fill='white', font=blackFont1)


        tx_hitokoto.text((screenX * 0.5 - 10*len(hitokoto_str), screenY * 0.08), hitokoto_str, fill='white', font=blackFont1)



    except AttributeError:
        text_display("获取天气集合失败,也许是没Money了...")
    bg_img.save('bg_img.bmp')

def wallpaperSet():
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, os.getcwd() + r'\bg_img.bmp',1 + 2)  # os.getcwd()返回此文件所在目录

def startCallBack():
    global tag
    tag = 0
    t = threading.Thread(target=starting, name='StartingThread')
    t.setDaemon(True)
    t.start()

def endCallBack():
   global tag
   tag = 1
   tkinter.messagebox.showinfo("操作状态", "执行成功!")
def infoCallBack():
    tkinter.messagebox.showinfo("关于...", "地球日记 By:Soulter \n QQ:905617992 \n如何设置自启动? 将本程序放入Windows的'启动'文件夹中" )

def diyBtnCallBack():
    diySettingsWindow = Tk()
    l1 = tkinter.Label(diySettingsWindow, text='目标网址(目前仅支持json)', bg='green', width=30, height=2)
    apiInput = tkinter.Entry(diySettingsWindow)
    l2 = tkinter.Label(diySettingsWindow, text='更新频率(毫秒ms)', bg='green', width=30, height=2)
    ctimeInput = tkinter.Entry(diySettingsWindow)
    l3 = tkinter.Label(diySettingsWindow, text='坐标x', bg='green', width=30, height=2)
    posxInput = tkinter.Entry(diySettingsWindow)
    l4 = tkinter.Label(diySettingsWindow, text='坐标y', bg='green', width=30, height=2)
    posyInput = tkinter.Entry(diySettingsWindow)
    l5 = tkinter.Label(diySettingsWindow, text='键', bg='green', width=30, height=2)
    target_arg = tkinter.Entry(diySettingsWindow)
    # btn = Button(diySettingsWindow, text="确定", command=lambda: dsw_set_diy_style(apiInput.get(), ctimeInput.get(), posxInput.get(), posyInput.get(), target_arg.get()))
    l1.pack()
    apiInput.pack()
    l2.pack()
    ctimeInput.pack()
    l3.pack()
    posxInput.pack()
    l4.pack()
    posyInput.pack()
    l5.pack()
    target_arg.pack()
    # btn.pack()
    diySettingsWindow.mainloop()
    

def dsw_parsingApiCallback(url):
    html = read_url(url)
    print(html)

def starting():
    while 1:
        global tag
        if tag == 1:
            print("STOP...")
            break
        text_display(
            "-------------------------\n作者:Soulter QQ:905617992\ngithub.com/soulter\n-------------------------")
        timedata_html = read_url(TIMEDATA_URL)
        timedata_json = get_json(timedata_html)

        wterdata_html = read_url(WTER_URL)
        wterdata_json = get_json(wterdata_html)

        hitokoto_html = read_url(HITOKOTO_URL)
        hitokoto_json = get_json(hitokoto_html)

        text_display("得到时间数据文件:" + str(timedata_json))
        text_display("得到文件city=25.266443,110.157113 天气:" + str(wterdata_json))

        # global get_earth_tag
        url, time_name = url_provider(timedata_json, EARTH_URL)
        # latest_earth_file_path = time_name
        img = img_get(url, time_name)
        img_edit(img, time_name, timedata_json, wterdata_json, hitokoto_json)
        get_earth_tag = 0

        # Set Windows Wallpaper
        wallpaperSet()

        text_display("sleep5分钟-v-!!!")
        time.sleep(5 * 60)


top = Tk()
get_earth_tag = 0
text1 = Text(top,width=50,height=20)

text1.insert(1.0, "Waiting your order:)")
text1.pack()

top.title("地球日记 | EarthDiary")
top.iconbitmap('mainlogo.ico')
B = Button(top, text ="运行", command=startCallBack)
B2 = Button(top, text ="停止", command=endCallBack)
B3 = Button(top, text ="关于作者...", command=infoCallBack)
# textInput = tkinter.Entry(top)
diyBtn = Button(top, text= "个性化(beta)", command=diyBtnCallBack)

# photo=PhotoImage(file="guibg.gif")
# label=Label(top,image=photo)  #图片
# label.pack()
B.pack()
B2.pack()
B3.pack()
# textInput.pack()
diyBtn.pack()
top.mainloop()






