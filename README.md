#opening a preview window for HQ camera. -t 0 means nonstop. tuning file is configuration of lens. focus is printed at the top of the windoes. 

rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477.json --info-text "%focus"


#activate virtual environment

source /home/yuyang/.venv/bin/activate

#run python script
#LTSC
python3 /home/yuyang/scripts/capture.py
#latest ver
python3 /home/yuyang/Downloads/capture.py

自动捕捉识别指南：
系统连接在初期阶段要通过显示器和键盘。连接eduroam后就可以拔下键盘和显示器，利用VNC或者ssh功能进行连接。
RPI 5设备的密码可以找Chris要，平时可以通过云平台来连接。 RPI2W的账号是yuyang，密码yuyangzhang。

首先，在一切之前，我们需要将系统更新到最新版
通过终端里sudo apt update 或者 sudo apt upgrade来完成更新。

更新结束后，我们利用导航命令cd， 导航至script的文件夹。

首先要运行neopixel这个文件。我们已经在本地装好了python。因此只需要将灯打开就行
sudo python3 neopixel.py
开灯后我们就可以将这个放在那里即可。灯的颜色可以自己在脚本里通过调整RGBW值调节。
需要关灯的时候应该有一个neopixel_off或者类似的脚本，执行即可。编辑一下green的脚本也可以。
需要换到树莓派5的情况下，需要先安装neopixel的一系列依赖。Google会教你如何安装neopixel库的，。
需要记录电流电压的情况下，使用INA219的程序，利用Nohup来运行，使得程序可以在后台持续运作。
需要捕捉图片的情况下，改动capture-upload这一程序.
捕捉到的图片如果需要上传，请改动# Initialize the Roboflow object with your API key之下的部分。将其替换成你自己的地址和api就好
需要改变捕捉类型的时候，请改动saveImage里subprocess之中的函数，rpi-still是捕捉静态图片。需要捕捉动态图片请根据rpicam-vid的各种关键词改变句柄。
保存位置在最上端的filepath中，可以将其改成自己的路径。

