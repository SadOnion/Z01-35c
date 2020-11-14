import tkinter as tk
import calc

root = tk.Tk()
expression = ""
def DrawMainLayout():

    global mainLabel 
    mainLabel= tk.Label(root,text="",font=("Helvetica", 36),relief="raised",anchor="e")
    mainLabel.grid(row=0,columnspan=4,sticky="EW")
    AddButton(root,1,0,"**")
    button = tk.Button(root,text="x!",font=("Helvetica", 16),command=lambda:AddToExpression("factorial("))
    button.grid(row=1,column=1,sticky="nesw")
    button = tk.Button(root,text="sqrt(x)",font=("Helvetica", 16),command=lambda:AddToExpression("sqrt("))
    button.grid(row=1,column=2,sticky="nesw")

    AddButton(root,2,0,"1")
    AddButton(root,2,1,"2")

    AddButton(root,2,2,"3")

    AddButton(root,3,0,"4")


    AddButton(root,3,1,"5")

    AddButton(root,3,2,"6")

    AddButton(root,4,0,"7")

    AddButton(root,4,1,"8")

    AddButton(root,4,2,"9")

    
    AddButton(root,1,3,"+")

    AddButton(root,2,3,"-")


    AddButton(root,3,3,"*")

    AddButton(root,4,3,"/")


    AddButton(root,5,0,"(")
    AddButton(root,5,1,")")
    button = tk.Button(root,text="mod(x)",font=("Helvetica", 16),command=lambda:AddToExpression("%"))
    button.grid(row=5,column=2,sticky="nesw")
    button = tk.Button(root,text="log(x)",font=("Helvetica", 16),command=lambda:AddToExpression("log("))
    button.grid(row=5,column=3,sticky="nesw")
    
    button = tk.Button(root,text="=",font=("Helvetica", 16),command=Solve)
    button.grid(row=6,column=0,columnspan=2,sticky="nesw")
    button = tk.Button(root,text="<--",font=("Helvetica", 16),command=RemoveOneChar)
    button.grid(row=6,column=2,sticky="nesw")
    button = tk.Button(root,text="C",font=("Helvetica", 16),command=RemoveAll)
    button.grid(row=6,column=3,sticky="nesw")

    button = tk.Button(root,text=".",font=("Helvetica", 16),command=lambda:AddToExpression("."))
    button.grid(row=7,column=0,columnspan=2,sticky="nesw")

    button = tk.Button(root,text="0",font=("Helvetica", 16),command=lambda:AddToExpression("0"))
    button.grid(row=7,column=2,columnspan=2,sticky="nesw")

def AddButton(root,ro,col,bText):
    button = tk.Button(root, text=bText,font=("Helvetica", 16),command=lambda:AddToExpression(bText))
    button.grid(row=ro,column=col,sticky="nsew")

def Solve():
    global expression
    try:
        expression = str(calc.evaluate(expression))
        mainLabel["text"] = expression
    except:
        mainLabel["text"] = "ERROR"
        expression = ""
def RemoveAll():
    global expression
    expression = ""
    mainLabel["text"] = expression
def RemoveOneChar():
    global expression
    expression = expression[:-1]
    mainLabel["text"] = expression
    
def AddToExpression(txt):
    global expression
    expression += txt
    mainLabel["text"] = expression

if __name__ == "__main__":
    
    root.geometry("500x650")
    root.resizable(height = False, width = False)
    DrawMainLayout()
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)
    root.grid_columnconfigure(2,weight=1)
    root.grid_columnconfigure(3,weight=1)

    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.grid_rowconfigure(2,weight=1)
    root.grid_rowconfigure(3,weight=1)
    root.grid_rowconfigure(4,weight=1)
    root.grid_rowconfigure(5,weight=1)
    root.grid_rowconfigure(6,weight=1)
    root.grid_rowconfigure(7,weight=1)
    root.mainloop()