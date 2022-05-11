def test_return():
    return 1,2

a,b = test_return()
print(a,b)

import cv2
import pyzed.sl as sl
import time
import numpy as np
import imutils
BRIGHTNESS = sl.VIDEO_SETTINGS.BRIGHTNESS #亮度
CONTRAST = sl.VIDEO_SETTINGS.CONTRAST #对比度
HUE = sl.VIDEO_SETTINGS.HUE  #色调
SATURATION = sl.VIDEO_SETTINGS.SATURATION #饱和度
SHARPNESS = sl.VIDEO_SETTINGS.SHARPNESS #锐度
GAMMA = sl.VIDEO_SETTINGS.GAMMA #gamma
GAIN = sl.VIDEO_SETTINGS.GAIN #增益
EXPOSURE = sl.VIDEO_SETTINGS.EXPOSURE#曝光
AEC_AGC = sl.VIDEO_SETTINGS.AEC_AGC #AECUAGC定义增益和曝光是否处于自动模式。通过@Gain或@Exposure值设置增益或曝光将自动将该值设置为0。
AEC_AGC_ROI = sl.VIDEO_SETTINGS.AEC_AGC_ROI #AEC_AGC_ROI定义自动曝光/增益计算的感兴趣区域。与专用的@set_camera_settings_roi/@get_camera_settings_roi功能一起使用。
WHITEBALANCE_TEMPERATURE = sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE #白平衡温度定义色温值。设置一个值将自动将@WHITEBALANCE_AUTO设置为0。受影响的值应在2800和6500之间，步长为100。
WHITEBALANCE_AUTO = sl.VIDEO_SETTINGS.WHITEBALANCE_AUTO #白平衡\自动定义白平衡是否处于自动模式
LED_STATUS = sl.VIDEO_SETTINGS.LED_STATUS #LED_状态定义摄像头前LED的状态。设置为0可禁用灯光，设置为1可启用灯光。默认值为on。至少需要摄像头FW 1523

init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.VGA #672*376
init_params.camera_fps = 100
cam = sl.Camera()


if not cam.is_opened():
    print("Opening ZED Camera...")
status = cam.open(init_params)
if status != sl.ERROR_CODE.SUCCESS:
    print(repr(status))
    exit()

runtime = sl.RuntimeParameters()
left_image = sl.Mat()
key = ''
begin = time.time()
i=0

cam.set_camera_settings(BRIGHTNESS, 0)
cam.set_camera_settings(CONTRAST, 0)
cam.set_camera_settings(HUE, 0)
cam.set_camera_settings(SATURATION, 8)
cam.set_camera_settings(SHARPNESS, 0)
cam.set_camera_settings(GAMMA, 1)
cam.set_camera_settings(WHITEBALANCE_TEMPERATURE,4880)
cam.set_camera_settings(GAIN, 85)
cam.set_camera_settings(EXPOSURE, 1)

while key != 113:  # for 'q' keyq
    err = cam.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS:
        try:

            cam.retrieve_image(left_image, sl.VIEW.LEFT)
            left_image_data = left_image.get_data()
            cv2.imshow("ZED_L", left_image_data)
        except:
            print("miss")
        key = cv2.waitKey(5)
        if time.time()-begin >1:
            begin = time.time()
            print(i)
            i=0

        i+=1

    else:
        key = cv2.waitKey(5)
cv2.destroyAllWindows()

cam.close()
print("\nFINISH")