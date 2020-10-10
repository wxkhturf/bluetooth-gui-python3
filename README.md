# bluetooth-gui-python3
该python文件运行在PC端，需要打开对应的串口，然后PC接收UART接收的数据，数据为6位，格式为bytes，前三位代表横坐标，后三位代表纵坐标。
由于没有采用极坐标形式，所以为简便，对于正负数的表示采用以500为零点，如600代表100，300代表-200等
## python3环境
安装serial、tkinter等包即可
