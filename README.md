This repisitory is designed for placing all control code for sentinel project

#opening a preview window for HQ camera. -t 0 means nonstop. tuning file is configuration of lens. focus is printed at the top of the windoes. 

#new Arducam preview window

  RPI zero

  rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx477_af.json --info-text "%focus"

  RPI 5

  rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/Arducam-477P-Pi5.json --info-text "%focus"

#for AI camera

  rpicam-hello -t 0 --tuning-file /usr/share/libcamera/ipa/rpi/pisp/imx500.json --info-text "%focus"




