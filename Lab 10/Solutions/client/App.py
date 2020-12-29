import tkinter as tk
import threading
import requests
import json

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.InitialDraw()

        self.root.mainloop()
    def InitialDraw(self):
        widg = tk.Label(self.root,text="Enter your user ID")
        widg.pack()
        login_text = tk.Entry(self.root)
        login_text.pack()
        password_text = tk.Entry(self.root)
        password_text.pack()
        widg = tk.Button(self.root,text="Enter")
        widg.pack()

    def Clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def MainDraw(self):
        self.Clear()

        input_field = tk.Entry(self.root)
        input_field.grid(row=11,sticky="WS")
        send_button = tk.Button(self.root,text="Wyślij")
        send_button.grid(row=11,sticky="S")
        response = requests.get(f'http://localhost:5000/get_user_list/0')
        data = json.loads(response.text)
    

app = App()
print('Now we can continue running code while mainloop runs!')

for i in range(10000):
    print(i)
app.MainDraw()
for i in range(10000):
    print(1000-i)