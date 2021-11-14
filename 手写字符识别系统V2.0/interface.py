#界面V2.0
from tkinter import *
import tkinter as tk
from multiprocessing import Process
from PIL import Image, ImageTk
import os
import time
import threading

from Mouse import Mouse
import Train as tr
import Train_A_J as taj


def creat_image():
    mn = Mouse()
    mn.create_image()

class Face(tk.Frame):     
        
    def __init__(self,root):
        super().__init__(root)
        root.geometry("630x150+600+600")  
        root.title('手写字符识别系统')
        
        label = Label(root,text='欢迎使用手写字符识别系统！')
        label.pack(side = TOP,anchor = CENTER)
        label.update()
        time.sleep(3)
        label.config(text='首次使用系统需初始化')
        
        label2 = Label(root,text='系统正在初始化……请稍等')
        label2.pack(side = TOP,anchor = CENTER)
        
        label3 = Label(root, text='初始化进度:', )
        label3.place(x=30, y=60)
        label3.update()
        canvas = tk.Canvas(root, width=465, height=22, bg="white")
        canvas.place(x=110, y=60)
        
        process=Process(target=tr.main)
        process2 = Process(target = taj.main)
        process.start()
        process2.start()
        
        fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for i in range(x):
            n = n + 465 / x
            canvas.coords(fill_line, (0, 0, n, 60))
            root.update()
            time.sleep(0.43)  # 控制进度条流动的速度

        # 清空进度条
        fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        
        if not os.path.exists('./only.png'):
            image_new = Image.new('RGB',(200,200),'black')
            image_new.save('only.png')
        
        label2.update()
        label2.config(text = '初始化完成！正在进入系统……')
        label2.update()
        label.config(text='')
        
        time.sleep(2)
        canvas.place_forget()
        label3.config(text='')
        label2 .config(text='')
        
        app2=App(root)
        
        root.quit()

class App(tk.Frame):
    
    def __init__(self, root):
        super().__init__(root)
        root.geometry("500x500+700+400")  
        root.title('手写字符识别系统')
        
        w = tk.Canvas(root,width=500,height=20)
        w.pack()

        Label(root, text='欢迎使用手写识别系统，以下为使用说明').pack(side=TOP)
        Label(root, text='1、点击生成手写图片按钮，摁下m切换到手写状态，点击鼠标左键，进行手写操作。').pack(side=TOP, anchor=W)
        Label(root, text='2、手写完成后，摁下w进行切图操作，点击鼠标左键，选择截取数字区域').pack(side=TOP, anchor=W)
        Label(root, text='3、完成上述操作后，摁q退出手绘区').pack(side=TOP, anchor=W)
        Label(root, text='4、点击刷新按钮，回显截图').pack(side=TOP, anchor=W)
        Label(root, text='5、点击数字/字母识别按钮，识别截图中数字/字母').pack(side=TOP, anchor=W)
        Label(root, text='识别到的数字/字母是：').place(x=100,y=180)
        self.numLabel = Label(root, text='', relief=RAISED,fg="red", font=("黑体", 30, "bold"))
        self.numLabel.pack(side=TOP, anchor=CENTER)
        Label(root, text='').pack(side=TOP, anchor=W)

        fm = Frame(root)
        # Button是一种按钮组件，与Label类似，只是多出了响应点击的功能
        Button(fm, text='生成手写图片', command=creat_image).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='刷新', command=self.changeImage).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='数字识别', command=self.recognition).pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(fm, text='字母识别', command = self.recognition_A_J).pack(side=TOP, anchor=W, fill=X, expand=YES)

        fm.pack(side=LEFT, fill=BOTH, expand=YES, padx=20)  
        
        self.pilImage = Image.open("only.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.label = Label(root, image=self.tkImage)
        self.label.pack()
        
        root.quit()

    def changeImage(self):
        self.png = tk.PhotoImage(file="only.png")  # 需要储存为实例属性，否则会被垃圾回收
        self.label.configure(image=self.png)
        
    def recognition(self):
        result = tr.main()
        self.numLabel.configure(text=str(result))
    
    def recognition_A_J(self):
        result = taj.main()
        self.numLabel.configure(text=str(result))

if __name__ == '__main__':
    if not os.path.exists('./NotMnist_model/checkpoint') or not os.path.exists('./Mnist_model/checkpoint'):
        root=Tk()
        app = Face(root)
    else:
        root=Tk()
        app = App(root)
    root.mainloop()
