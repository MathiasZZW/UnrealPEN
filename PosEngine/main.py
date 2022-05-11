import cv2
import pyzed.sl as sl
import time
import numpy as np
import imutils
import socket
# 1. 创建套接字
X =0
Y =0
Z=0
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

standard_distance_camera  = 0.12#米
standard_distance_horizontal = 672
standard_distance_depth = standard_distance_horizontal/2/np.sqrt(3)
standard_distance_vertical = 376
standard_ver_d_depth = 10/10

#乒乓球hsv阈值
greenUpper = np.array([131, 255, 255])
greenLower = np.array([38, 24, 114])

#镜头参数设置
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

time_c=time.time()

#设置方法
#cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)
def find_ball(frame):
    global time_c

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    # print(len(cnts))
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #print(x,y)

        #M = cv2.moments(c)

        # only proceed if the radius meets a minimum size
        if radius > 1:
            # center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) #求重心，即颜色最深处
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
            text = "center x: " + str(int(x)) + "   center y: " + str(int(y))
            cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)

            time_d = (time.time()-time_c)*1000
            cv2.putText(frame, str(time_d)[:5]+"ms; FPS:100", (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)


    return x,y
def cal_xyz(lx,ly,rx,ry):
    # 如果在中线左边
    print(lx,ly,rx,ry)
    global X,Y,Z
    if lx < standard_distance_horizontal / 2:
        angle1 = np.pi / 2 + np.arctan((standard_distance_horizontal / 2 - lx) / standard_distance_depth)
    else:
        angle1 = np.pi / 2 - np.arctan((lx - standard_distance_horizontal / 2) / standard_distance_depth)
    if rx<standard_distance_horizontal/2:
        angle2 = np.pi/2+np.arctan((standard_distance_horizontal/2-rx)/standard_distance_depth)
    else:
        angle2 = np.pi/2-np.arctan((rx-standard_distance_horizontal/2)/standard_distance_depth)
    X = 0.12/(1-np.tan(angle1)/np.tan(angle2))-0.06
    Z = np.tan(angle1)*(X+0.06)

    Y =Z/(standard_distance_vertical/2/standard_ver_d_depth/(((ly+ry)/2)-standard_distance_vertical/2))
    X*=1000
    Y*=-1000
    Z*=1000


def main():
    global time_c

    #初始化摄像头
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

    cam.set_camera_settings(BRIGHTNESS, 0)
    cam.set_camera_settings(CONTRAST, 0)
    cam.set_camera_settings(HUE, 0)
    cam.set_camera_settings(SATURATION, 8)
    cam.set_camera_settings(SHARPNESS, 0)
    cam.set_camera_settings(GAMMA, 1)
    cam.set_camera_settings(WHITEBALANCE_TEMPERATURE, 4880)
    cam.set_camera_settings(GAIN, 95)
    cam.set_camera_settings(EXPOSURE, 1)

    runtime = sl.RuntimeParameters()
    left_image = sl.Mat()
    right_image = sl.Mat()
    key = ''
    begin = time.time()
    i=0
    while key != 113:  # for 'q' keyq
        time_c = time.time()
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            try:
                cam.retrieve_image(left_image, sl.VIEW.LEFT)
                cam.retrieve_image(right_image, sl.VIEW.RIGHT)
                left_image_data = left_image.get_data()
                right_image_data = right_image.get_data()
                lx,ly = find_ball(left_image_data)
                rx,ry = find_ball(right_image_data)
                cal_xyz(lx, ly, rx, ry)
                a = str(round(X,2))+"_"+str(round(Y,2))+"_"+str(round(Z,2))
                print(a)
                udp_socket.sendto(a.encode(), ("255.255.255.255", 9999))
                cv2.imshow("ZED_L", left_image_data)
                cv2.imshow("ZED_R", right_image_data)
            except:
                print("miss")
                a = str(round(X, 2)) + "_" + str(round(Y, 2)) + "_" + str(round(Z, 2))
                udp_socket.sendto(a.encode(), ("255.255.255.255", 9999))
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
if __name__ == "__main__":
    main()

