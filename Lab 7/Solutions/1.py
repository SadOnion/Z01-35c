import json
from tkinter import *
from PIL import Image,ImageTk
import io
import requests
import datetime as dt
import matplotlib.pyplot as plt

image_request = "http://openweathermap.org/img/wn/Y@4x.png"#"https://www.metaweather.com/static/img/weather/png/X.png"

apicall = "https://api.openweathermap.org/data/2.5/onecall?lat=X&lon=Y&exclude=minutealy,current,alerts&units=metric&lang=pl&appid=5f9b4267233d1f8f081dac5100a478f3"
weather = []
def_lat = "51"
def_lon = "17"

with open("city.list.json",'r',encoding='utf-8') as j:
    json_data = json.load(j)

def GetApiCall(lat = def_lat,lon = def_lon):
    return json.loads(requests.get(apicall.replace('Y',str(lon)).replace('X',str(lat))).text)

def GetImage(state):
    raw_data = requests.get(image_request.replace("Y",state)).content
    im = Image.open(io.BytesIO(raw_data))
    im = im.resize((128,128))
    photo = ImageTk.PhotoImage(im)
    return photo
def AddDay(root,day):

    

    photo = GetImage(weather["daily"][day]["weather"][0]["icon"])

    date = dt.date.today()
    
    date = date + dt.timedelta(days=day)
    label = Label(root, text=date.strftime('%A'))
    label.grid(row=0,column=day, padx=75,pady=5)

    labelim = Label(root, image=photo)
    labelim.grid(row=1,column=day)
    labelim.image = photo
    
    label = Label(root, text="Min: "+"{:.2f}".format(weather["daily"][day]["temp"]["min"])+" °C")
    label.grid(row=2,column=day,pady=5)

    label = Label(root, text="Max: "+"{:.2f}".format(weather["daily"][day]["temp"]["max"])+" °C")
    label.grid(row=3,column=day,pady=5)

    label = Label(root, text="Air pressure: "+"{:.2f}".format(weather["daily"][day]["pressure"])+" hPa")
    label.grid(row=4,column=day,pady=5)

    label = Label(root, text="Humidity: "+"{:.2f}".format(weather["daily"][day]["humidity"])+" %")
    label.grid(row=5,column=day,pady=5)

    button = Button(root,text="Hourly",command=lambda:ShowHourly(day))
    button.grid(row=6,column=day,pady=5)
def ShowHourly(day):
    hours = []
    data = GetTempData(day)
    first = 0
    last = 24
    if day == 0:
        first = data.pop()
    elif day == 1:
        first = 0
        data.pop()
    else:
        last = data.pop() 
    for x in range(first,last):
        hours.append(x)
    print(hours,data)
    plt.bar(hours,data)
    plt.show()
def Draw(root):
    for x in range(3):
        AddDay(root, x)
    inp = Entry(root)
    inp.grid(row=2,column=3)
    btn = Button(root,text="Apply",command=lambda:Update(root,inp.get()))
    btn.grid(row=3,column=3)

def Update(root,newLocation):
    global weather
    for widget in root.winfo_children():
        widget.destroy()

    for x in json_data:
        if x["name"] == newLocation:
            coord = x["coord"]
            weather = GetApiCall(lat=coord["lat"],lon=coord["lon"])
            break
    Draw(root)
def GetTempData(day):
    hourly_data = weather["hourly"]
    data = []
    date = dt.datetime.today() + dt.timedelta(days=day)
    first = int(dt.datetime.fromtimestamp(hourly_data[0]["dt"]).today().strftime("%H"))

    for x in hourly_data:
        if date.strftime('%d') == dt.datetime.fromtimestamp(x["dt"]).strftime('%d'):
            data.append(x["temp"])
    data.append(first)
    return data
if __name__ == "__main__":
       

    root = Tk()
    weather = GetApiCall()
    root.geometry("800x350")
    root.resizable(height = False, width = False)
    
    Draw(root)
    
    root.mainloop()
    
   
