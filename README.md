# Opening a Preview Window for HQ Camera｜打开 HQ 相机预览窗口

`-t 0` 表示预览持续运行（non-stop）。
`--tuning-file` 指定镜头与传感器的调校参数文件（ISP tuning）。
`%focus` 会在预览窗口顶部实时显示当前对焦数值。

`-t 0` means the preview runs continuously.
The tuning file defines lens and sensor configuration.
The focus value is printed at the top of the preview window.

```bash
rpicam-hello -t 0 \
  --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477_af.json \
  --info-text "%focus"
```

---

# Activate Python Virtual Environment｜激活 Python 虚拟环境

用于确保脚本运行在隔离、可复现的 Python 环境中。
Used to ensure scripts run in an isolated and reproducible Python environment.

```bash
source /home/yuyang/.venv/bin/activate
```

---

# Run Python Script｜运行 Python 脚本

## LTSC Version｜LTSC 稳定版

```bash
python3 /home/yuyang/scripts/capture.py
```

## Latest Version｜最新版

```bash
python3 /home/yuyang/Downloads/capture.py
```

---

# 自动捕捉识别指南｜Automatic Capture & Recognition Guide

## 初始系统连接｜Initial System Setup

* 系统初期需要 **显示器 + 键盘** 进行本地操作。

* 成功连接 **eduroam** 后，可移除显示器和键盘，改用 **VNC / SSH** 远程连接。

* During the initial stage, a **monitor and keyboard** are required.

* After connecting to **eduroam**, you can disconnect them and use **VNC or SSH**.

### 账号信息｜Account Information

* **Raspberry Pi 5**：密码请向 **Chris** 获取，通常通过云平台连接。

* **Raspberry Pi 5**: Ask **Chris** for the device password; cloud access is usually available.

* **Raspberry Pi 2W**：

  * 用户名 / Username：`我的名字，拼写不带姓氏`
  * 密码 / Password：`全名拼写`

---

## 系统更新｜System Update

在任何操作之前，必须将系统更新到最新状态。
Before doing anything else, update the system to the latest version.

```bash
sudo apt update
sudo apt upgrade
```

---

## 脚本目录导航｜Navigate to Script Directory

使用 `cd` 命令进入脚本所在目录。
Use `cd` to navigate to the script directory.

```bash
cd ~/scripts
```

---

## Neopixel 灯控制｜Neopixel LED Control

### 打开灯光｜Turn On LEDs

系统已预装 Python，只需运行脚本即可点亮灯光。
Python is already installed; simply run the script.

```bash
sudo python3 neopixel.py
```

* 灯光颜色可通过脚本中的 **RGBW** 参数进行调整。

* 灯可保持常亮状态。

* LED color can be adjusted via **RGBW** values in the script.

* The LEDs can remain on continuously.

### 关闭灯光｜Turn Off LEDs

* 运行 `neopixel_off.py` 或类似脚本。

* 或编辑 `green` 脚本实现关闭。

* Run `neopixel_off.py` (or similar).

* Alternatively, modify the `green` script.

### Raspberry Pi 5 注意事项｜Raspberry Pi 5 Notes

* 在 RPi 5 上使用 Neopixel 前，需要安装相关依赖库（如 `rpi_ws281x`）。

* 请自行搜索并安装对应库。

* On RPi 5, Neopixel dependencies (e.g. `rpi_ws281x`) must be installed manually.

* Refer to online documentation for installation steps.

---

## 电流与电压记录（INA219）｜Current & Voltage Logging (INA219)

* 使用 INA219 脚本采集电流、电压数据。

* 建议使用 `nohup` 使程序在后台长期运行。

* Use INA219 scripts to log current and voltage.

* `nohup` allows the process to run persistently in the background.

```bash
nohup python3 ina219.py &
```

---

## 图像捕捉与上传｜Image Capture & Upload

### 修改捕捉程序｜Modify Capture Script

* 捕捉逻辑位于 `capture-upload` 脚本中。

* 上传功能通过 Roboflow API 实现。

* Capture logic is implemented in `capture-upload`.

* Uploading is handled via the Roboflow API.

```python
# Initialize the Roboflow object with your API key
```

请替换为你自己的 API Key 与目标地址。
Replace this with your own API key and endpoint.

### 改变捕捉类型｜Change Capture Mode

* 修改 `saveImage` 函数中的 `subprocess` 调用：

  * `rpi-still`：静态图片
  * `rpicam-vid`：视频 / 动态捕捉

* Modify the `subprocess` call inside `saveImage`:

  * `rpi-still`: still images
  * `rpicam-vid`: video capture

官方参数文档｜Official documentation:
[https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/camera/rpicam_vid.adoc](https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/camera/rpicam_vid.adoc)

### 保存路径｜Save Path

* 文件保存路径定义在脚本顶部的 `filepath` 变量中。

* 可根据需要自行修改。

* The save directory is defined by the `filepath` variable at the top of the script.

### 上传与预测开关｜Upload & Predict Switches

* 在脚本底部，通过布尔值控制功能开关：

```python
Upload = True / False
Predict = True / False
```

---

## 对焦与最终执行｜Focus & Final Execution

### 对焦｜Focusing

运行 `focus` 脚本，或使用以下命令进行实时预览并调整相机位置。
Run the `focus` script or use the command below for live preview.

```bash
rpicam-hello -t 0 \
  --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477.json \
  --info-text "%focus"
```

### 正式运行｜Final Run

确认画面与对焦无误后，执行捕捉与上传脚本。
After confirming focus and framing, run the capture/upload script.

```bash
python3 capture_upload.py
```

---

## 文件下载｜File Retrieval

* 可使用 `scp` 将文件复制到本地电脑。

* 或上传至 GitHub 再下载。

* Use `scp` to copy files to your local machine.

* Alternatively, upload them to GitHub for retrieval.
