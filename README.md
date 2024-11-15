#opening a preview window for HQ camera. -t 0 means nonstop. tuning file is configuration of lens. focus is printed at the top of the windoes. 

rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477.json --info-text "%focus"

#for AI camera

rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx500.json --info-text "%focus"

#activate virtual environment

source /home/yuyang/.venv/bin/activate

#run python script
#LTSC
python3 /home/yuyang/scripts/capture.py
#latest ver
python3 /home/yuyang/Downloads/capture.py

#new Arducam

rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477_af.json --info-text "%focus"
rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/Arducam-477P-Pi5.json --info-text "%focus"
