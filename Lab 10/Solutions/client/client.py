import socketio
import asyncio
import time
import openapi_client
from pprint import pprint
from openapi_client.api import default_api
from openapi_client.model.inline_response200 import InlineResponse200
import tkinter as tk
import requests
import json
sio = socketio.Client()
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)
user_ID = 0
chat_text = ""
USERS = []
other_user = 0

class User:
    Id = -1
    Name = 'None'
    Status = 'ND'
    Unread = 0

    def __init__(self,Id,Name,Status,Unread):
        self.Id = Id
        self.Name = Name
        self.Status = Status
        self.Unread = Unread

def InitialDraw(root):
    Clear(root)
    widg = tk.Label(root,text="Enter your user ID")
    widg.pack()
    login_text = tk.Entry(root)
    login_text.pack()
    password_text = tk.Entry(root)
    password_text.pack()
    widg = tk.Button(root,text="Enter",command=lambda: Login(login_text,password_text))
    widg.pack()

def Login(login,password):
    log = str(login.get())
    psw = str(password.get())
    global user_ID
    response = requests.get(f'http://localhost:5000/login/{log}/{psw}')
    data = json.loads(response.text)
    if data["status"] == 1:
        user_ID = data["id"]
        connect_websocket()
        root.title(log)
        MainDraw(root)
    else:
        user_ID = 0
        InitialDraw(root)  
def connect_websocket():
    sio.connect('http://localhost:5000')
def Clear(root):
    print("Updating UI")
    for widget in root.winfo_children():
        widget.destroy()
def MainDraw(root):
    Clear(root)
    DrawChat()

    input_field = tk.Entry(root)
    input_field.grid(row=11,sticky="WS")
    send_button = tk.Button(root,text="Wyślij",command=lambda: send_message(input_field.get()))
    send_button.grid(row=11,sticky="S")
    
    DrawUsers()
def DrawChat():
    if len(USERS) <= 0:
        text = tk.Label(root,text="Select user and start chatting")
        text.grid(row=0,sticky="W")
        return
    print(other_user) 
    response = requests.get(f'http://localhost:5000/get_messages/{user_ID}/{USERS[other_user].Id}')
    data = json.loads(response.text)
    x = 0
    for msg in data:
        if user_ID != msg["From"]:
            text = tk.Label(root,text=f'{msg["SendDate"]}:{msg["Content"]}',bg="grey")
            text.grid(row=x,sticky="W")
        else:
            text = tk.Label(root,text=f'{msg["Content"]}:{msg["SendDate"]}',bg="white")
            text.grid(row=x,sticky="E")
        x = x+1
def DrawUsers():
    response = requests.get(f'http://localhost:5000/get_user_list/{user_ID}')
    data = json.loads(response.text)
    UserButton.Count = 0
    USERS.clear()
    for x in data:
        print(x)
    data = sorted(data,key=lambda item:item["Status"],reverse=True)
    for x in data:
        print(x)
    for user in data:
        u = User(user["Id"],user["Name"],user["Status"],user["Unread"])
        USERS.append(u)
        print(f"{len(USERS)} users found")
        UserButton(user["Name"],user["Status"],user["Unread"])
class UserButton:
    Count = 0
    def __init__(self,name,status,unread):
        self.id = UserButton.Count
        user_button = tk.Button(root,text=f'{name} {status} {unread}',command=lambda:self.change_focus(self.id))
        user_button.grid(row=self.id,column=2,sticky="e")
        UserButton.Count=UserButton.Count+1
    def change_focus(self,focus):
        global other_user
        other_user = focus
        MainDraw(root)
def send_message(msg):
    requests.get(f'http://localhost:5000/send_message/{user_ID}/{USERS[other_user].Id}/{msg}')
    MainDraw(root)
@sio.event
def update_list():
    MainDraw(root)
@sio.event
def update_data():
    print("data updated xD")
def main():
    global root
    root = tk.Tk()
    root.geometry("800x350")
    for i in range(2):
        root.columnconfigure(i, weight=1)
    InitialDraw(root)
    root.mainloop()
if __name__ == "__main__":
    main()
    pass

