
import time
import openapi_client
from pprint import pprint
from openapi_client.api import default_api
from openapi_client.model.inline_response200 import InlineResponse200
import tkinter as tk
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)
user_ID = 0
chat_text = ""

def UpdateMessages():
    print("prt")
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)

        try:
            print("upadat")
            api_response = api_instance.get_user_id_get(user_ID)
            for x in api_response["messages"]:
                chat['text'] = chat['text'] + x
        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_user_id_get: %s\n" % e)

def SendMessage():
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = default_api.DefaultApi(api_client)
        try:
            user_id = int(send_to.get())
            message = new_message.get("1.0",tk.END)
            chat['text'] = chat['text'] +"Your message: "+message
            api_instance.send_user_id_message_post(user_id,message)
            new_message.delete("1.0",tk.END)

        except openapi_client.ApiException as e:
            print("Exception when calling DefaultApi->get_user_id_get: %s\n" % e)
def InitialDraw(root):
    widg = tk.Label(root,text="Enter your user ID")
    widg.pack()
    global id_text
    id_text = tk.Entry(root)
    id_text.pack()
    widg = tk.Button(root,text="Enter",command=lambda: MainDraw(root))
    widg.pack()

def MainDraw(root):
    global user_ID
    user_ID = int(id_text.get())
    print(user_ID)
    for widget in root.winfo_children():
        widget.destroy()
    global chat
    chat = tk.Label(root,text=chat_text,width=70,height=20,anchor="sw")
    chat.grid(row=0,column=0)
    btn = tk.Button(root,text="Update",command=UpdateMessages)
    btn.grid(row=1,column=0)
    global new_message
    new_message = tk.Text(root,width=15,height=5)
    new_message.grid(row=0,column=1)
    btn = tk.Button(root,text="Send",command=SendMessage)
    btn.grid(row=1,column=1)
    lbl = tk.Label(root,text="to user ")
    lbl.grid(row=1,column=2)
    global send_to
    send_to = tk.Entry(root)
    send_to.grid(row=1,column=3)
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x350")
    InitialDraw(root)
    root.mainloop()
    pass