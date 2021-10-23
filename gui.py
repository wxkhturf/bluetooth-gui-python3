#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Master
import serial,threading
import tkinter as tk  # 使用Tkinter前需要先导入
#点击按钮的响应（点击之后会显示数据，否则不显示接收的数据，但是不影响小车运动界面是显示）
def hit_me():
    global on_hit
    global var
    if on_hit == False:
        on_hit = True
        var.set('bluetooth is working')
    else:
        on_hit = False
        var.set('')
#画运动轨迹
def drawLine(cor_list):
    global height
    x1=ini_x
    y1=ini_y
    for i in cor_list:
        temp_x=x1
        temp_y=y1
        print(i)
        x1=i[0]
        y1=height-i[1]
        print(x1)
        print(y1)
        x0=temp_x
        y0=temp_y
        print(x1-x0)
        print(y0-y1)
        canvas.create_line(x0,y0, x1,y1,tag="blue")
        canvas.move(rect, x1-x0, y1-y0) 
    canvas.pack()
#接收串口数据
def ReadUART():
    global rect
    while (True):
        try:
            idx = ser.read(dataSize)
            OutputText.insert(tk.END, int(idx))
            OutputText.insert(tk.END, ' ')
            print('idx is' +str(idx) )
            dif_x = int(idx[0:int(dataSize/2)])-500
            dif_y = int(idx[int(dataSize/2):dataSize])-500
            idx_x = cor_list[-1][0] + dif_x
            idx_y = cor_list[-1][1] + dif_y
            n= (idx_x, idx_y)
            #if n not in cor_list:
            print(n)
            cor_list.append(n)
            
            drawLine(cor_list)
            rect = canvas.create_rectangle(cor_list[0][0]-5, cor_list[0][1]+5, \
                (cor_list[0][0]+5), (cor_list[0][1]-5),fill='red',outline='red',tag="red")                  # 画矩形正方形 
            #print(idx, end='')
        except:
            print("There's something wrong")

#串口是COM4，若不同注意修改
ser = serial.Serial('COM4')
#设置波特率
ser.baudrate=9600      
#绘制运动的窗口大小  
height = 500               
width = 700 
#小车初始位置
ini_x = 300                
ini_y = 250 
#一次接收数据位数               
dataSize = 6
n1= (ini_x, ini_y)
#存储小车运动历程坐标的列表cor_list
cor_list=[]
cor_list.append(n1)
#按钮初始点击为False
on_hit=False
var = None
window = tk.Tk()
window.title('Bluetooth')
#gui整体界面大小
window.geometry('800x700')
var = tk.StringVar()
#Label控件
l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
l.pack()
on_hit = False 
#按钮
b = tk.Button(window, text='点击开始', font=('Arial', 12), width=10, height=1, command=hit_me)
b.pack()
ReadyToStart = True
write = tk.StringVar()
OutputText = tk.Text(window, wrap=tk.WORD, width=113, height=3)
OutputText.pack()
canvas = tk.Canvas(window, bg='white', height=height, width=width)
#绘制矩形
rect = canvas.create_rectangle(ini_x, ini_y, (ini_x+10), (ini_y-10),fill='red',outline='red',tag="red")                  # 画矩形正方形
drawLine(cor_list)
#采用多线程调用蓝牙通信函数
ReadUARTThread = threading.Thread(target=ReadUART)#多线程
ReadUARTThread.start()
#对gui界面进行循环
window.mainloop()

