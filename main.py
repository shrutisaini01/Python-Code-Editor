#Day1- 14th May, 2024- GUI PART

from tkinter import *
from tkinter import filedialog,messagebox
import subprocess
font_size=10
path=''

def saveas(event=None):
    global path
    path=filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py")],defaultextension="*.py")
    if path != '':
        file = open(path, "w")
        file.write(textArea.get(1.0, END))
        file.close()

def openfile(event=None):
    path=filedialog.askopenfilename(filetypes=[("Python Files", "*.py")],defaultextension="*.py")
    if path != '':
        file = open(path, 'r')
        data = file.read()
        textArea.delete('1.0', END)
        textArea.insert(1.0, data)
        highlight_syntax()
        file.close()

def save(event=None):
    if path == '':
        saveas()
    else:
        result = messagebox.askyesno('Confirm', 'Do you want to save the file with the same name?')
        if result:
            file = open(path, "w")
            file.write(textArea.get(1.0, END))
            file.close()
        else:
            saveas()


def newFile(event=None):
    global path
    path=''
    textArea.delete('1.0', END)
    outputArea.delete('1.0', END)
    highlight_syntax()

def iexit(event=None):
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def theme():
    if check.get()=='light':
        textArea.config(bg='white',fg='black')
        outputArea.config(bg='white',fg='black')
    elif check.get()=='dark':
        textArea.config(bg='#3D3B40',fg='white')
        outputArea.config(bg='#3D3B40',fg='white')

def clear():
    textArea.delete('1.0', END)
    outputArea.delete('1.0', END)

def run():
    if path=='':
        messagebox.showerror('Error','Please save the file before running')
    else:
        command = f'python {path}'
        runFile=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output,error=runFile.communicate()
        outputArea.delete('1.0', END)
        outputArea.insert(1.0,output)
        outputArea.insert(1.0,error)

def font_inc(event=None):
    global font_size
    font_size+=1
    textArea.config(font=('arial',font_size,'bold'))
    outputArea.config(font=('arial', font_size, 'bold'))

def font_dec(event=None):
    global font_size
    font_size-=1
    textArea.config(font=('arial', font_size, 'bold'))
    outputArea.config(font=('arial', font_size, 'bold'))

def highlight_syntax():
    keywords = ['if', 'else', 'for', 'while', 'def', 'class', 'import', 'from', 'as', 'return', 'in', 'range', 'print']
    operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']
    for keyword in keywords:
        textArea.tag_config(keyword, foreground='#2E97A7')
    for operator in operators:
        textArea.tag_config(operator, foreground='#EA168E')
    text = textArea.get("1.0", "end")
    for keyword in keywords:
        start = '1.0'
        while True:
            start = textArea.search(keyword, start, stopindex=END)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            textArea.tag_add(keyword, start, end)
            start = end

    for operator in operators:
        start = '1.0'
        while True:
            start = textArea.search(operator, start, stopindex=END)
            if not start:
                break
            end = f"{start}+{len(operator)}c"
            textArea.tag_add(operator, start, end)
            start = end

#start
root = Tk()

#to hold the window we will use mainloop
#add width and height using geometry
root.geometry('1270x670+0+0')
#title
root.title("Python Editor")

check=StringVar()
check.set('light')

myMenu=Menu()
fileMenu=Menu(myMenu,tearoff=False)
fileMenu.add_command(label="New",accelerator="Ctrl+N",command=newFile)
fileMenu.add_command(label="Open",accelerator="Ctrl+O",command=openfile)
fileMenu.add_command(label="Save",accelerator="Ctrl+S",command=save)
fileMenu.add_command(label="Save As",accelerator="Ctrl+A",command=saveas)
fileMenu.add_command(label="Exit",accelerator="Ctrl+Q",command=iexit)
myMenu.add_cascade(label='File',menu=fileMenu)

#themes
themeMenu=Menu(myMenu,tearoff=False)
themeMenu.add_radiobutton(label="Light",variable=check,value='light',command=theme)
themeMenu.add_radiobutton(label="Dark",variable=check,value='dark',command=theme)
myMenu.add_cascade(label='Theme',menu=themeMenu)

#clear
myMenu.add_command(label='Clear',command=clear)

#run
myMenu.add_command(label='Run',command=run)

#text area and scroll bar
editFrame=Frame(root,bg='white')
editFrame.place(x=0,y=0,height=500,relwidth=1)
scrollBar=Scrollbar(editFrame, orient=VERTICAL)
scrollBar.pack(side=RIGHT,fill=Y)
textArea=Text(editFrame,font=('arial', font_size, 'bold'),yscrollcommand=scrollBar.set)
textArea.pack(side=LEFT,fill=BOTH,expand=True)
scrollBar.config(command=textArea.yview)
highlight_syntax()

#output area
outputFrame=LabelFrame(root,text='Output',font=('arial',font_size,'bold'))
outputFrame.place(x=0,y=500,relwidth=1,height=170)

scrollBar2=Scrollbar(outputFrame, orient=VERTICAL)
scrollBar2.pack(side=RIGHT,fill=Y)
outputArea=Text(outputFrame,font=('arial',font_size,'bold'),yscrollcommand=scrollBar.set)
outputArea.pack(side=LEFT,fill=BOTH,expand=True)
scrollBar2.config(command=outputArea.yview)

textArea.bind('<KeyRelease>', lambda event: highlight_syntax())
root.config(menu=myMenu)


root.bind('<Control-n>',newFile)
root.bind('<Control-s>',save)
root.bind('<Control-o>',openfile)
root.bind('<Control-q>',iexit)
root.bind('<Control-a>',saveas)
root.bind('<Control-p>',font_inc)
root.bind('<Control-m>',font_dec)
#end
root.mainloop()


