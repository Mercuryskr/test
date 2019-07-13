from socket import *

udpsocket = socket(AF_INET, SOCK_DGRAM)


for i in range(999):
     udpsocket.sendto(b"1:1238605487:yangjifeng:yangjifeng-pc:32:wojiu shi huangzefan",("192.168.36.86", 2425))