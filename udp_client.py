import logging
import socket
import _thread
import time
#import sys
#from util import *

logger = logging.getLogger()


def main(host='127.0.0.1', port=9999):
    
    host = 'ec2-13-233-141-155.ap-south-1.compute.amazonaws.com'
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('',port))
    sock.sendto(b'0', (host, port))
    data, addr = sock.recvfrom(1024)
    print('client received: {} {}'.format(addr, data))
    addr = msg_to_addr(data)
    #switching port
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('',8080))
    #addr = ('192.168.0.101', port)
    sock.settimeout(1)
    msgCount = 0
    _thread.start_new_thread(recv,(sock, ))
    while True:
        #print(addr)
        sock.sendto(bytes(str(msgCount)+"Hello"  ,'utf-8'), addr)
        time.sleep(1)
        msgCount = msgCount + 1


def recv(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(addr[0] +" "+ data.decode('utf-8'))
            
        except Exception as e:
            print(e) 
            

def msg_to_addr(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return (ip, int(port))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
main()
