import socket
# 1. 创建套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# 2. 绑定一个本地信息
localaddr = ("0.0.0.0", 8888)
udp_socket.bind(localaddr)
a = "dwdawdawd"


def recv_message():
    # 3. 接收数据
    recv_data = udp_socket.recvfrom(9999)
    recv_msg = recv_data[0]
    send_addr = recv_data[1]
    msg=""
    for i in recv_msg:
        msg+=str(chr(i))
    data = list(map(int,msg.split('1073645562')[:-1]))
    # 4. 打印接收到的信息
    print(data,len(data))
    # print(recv_msg)
    # print(send_addr)
    return data

    # 5. 关闭套接字
    # udp_socket.close()
print('start')
while(1):

    dataArray=recv_message()
        # Roll = ((dataArray[25] << 8) | dataArray[24]) / 32768 * 180;
        # Pitch = ((dataArray[27] << 8) | dataArray[26]) / 32768 * 180;
        # Yaw = ((dataArray[29] << 8) | dataArray[28]) / 32768 * 180;
        # print("ROll: "+str(Roll)[:5]+" Pitch: "+str(Pitch)[:5]+" Yaw: "+str(Yaw)[:5])


    # udp_socket.sendto(a.encode(),("255.255.255.255",8888))