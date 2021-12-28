import socket
import threading
import struct
import  msvcrt
import time
import random



tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
team_name = f"saja {random.randint(0,10)}"


def client_listen(broadcast_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enable broadcasting mode
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", broadcast_port))
    while True:
        global tcp_socket
        tcp_socket = socket.socket()
        msg, addr = client.recvfrom(1024)
        invitation_port=struct.unpack('!IBH',msg)
        
        port=invitation_port[2] # socket server port number
        

        hostIp = addr[0]  # (eth1, 172.1.0/24) is for development , (eth2, 172.99.0/24) is to test your work

        print(addr)
        msg =f"Received offer from {hostIp}, attempting to connect..."
        
        client_connect(hostIp, port)
        print("\nServer disconnected, listening for offer requests...")


def client_connect(hostip, port):

   # tcp_socket.settimeout(10)  # 10 sec
    try:
        tcp_socket.connect((hostip, port))  # connect to the server
        tcp_socket.setblocking(False)
    except socket.error as err:
        print ("Error while trying to connect to server : "+str(err))
        return

    try:
        tcp_socket.send(team_name.encode())
    except socket.error as err:
        print("Error at sending the team name : "+str(err))
        tcp_socket.close()
        return
    tcp_socket.settimeout(socket.getdefaulttimeout())
   
    
    clientGame()


def clientGame():
   
    try:
        welcome_message = tcp_socket.recv(1024).decode()
        print(welcome_message)
        #getAnswer=threading.Thread(target=char_Answer)
        #getAnswer.start()
        t = time.time()+10
        while t>time.time():
            try:
                print("sss")
                data = tcp_socket.recv(1024).decode()  # receive response
                print("s2")
                if not data:
                    print(data)
                    break
            except socket.error:
                print("s3")
                pass
            print("check!!!!")
            if msvcrt.kbhit():#check if press any key
                tcp_socket.send(msvcrt.getch())#send to the server

                print("you pressed",msvcrt.getch(),"so now i will quit")


        tcp_socket.close()  # close the connection
    except socket.error as err:
        print("Error during the game : "+str(err))
        
        tcp_socket.close()
        return

# def char_Answer(): ## Key Board Listener Thread -  to  catch user answer
    
#     answer=msvcrt.getch()
#     answer=answer.decode('utf-8')
    
#     tcp_socket.send(answer.encode())
  
#     answer=None
    


if __name__ == '__main__':
    broadcastPort = 13117
    print("Client started, listening for offer requests...")
    client_listen(broadcastPort)
