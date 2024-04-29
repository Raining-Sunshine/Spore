#openi9ng a preview window for HQ camera. -t 0 means nonstop. tuning file is configuration of lens. focus is printed at the top of the windoes. 

rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477.json --info-text "%focus"


#activate virtual environment

source /home/yuyang/.venv/bin/activate

#run python script
#LTSC
python3 /home/yuyang/scripts/capture.py
#latest ver
python3 /home/yuyang/Downloads/capture.py
