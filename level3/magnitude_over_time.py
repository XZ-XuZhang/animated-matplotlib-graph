import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import time
import paho.mqtt.client as mqtt

import socket
socket.setdefaulttimeout(3)


temp=[]
fig=plt.figure()
plt.ylim(0,10)
plt.xlim([0,19])
value=[]
label=[]
count=-10
average=[]



def setup_mqtt():
	client=mqtt.Client("movement_level3")
	client.on_connect=OnConnect
	client.on_message=OnMessage
	client.connect("192.168.4.1",1883,120)
	return client

def OnConnect(client,userdata,flags,rc):
	#client.subscribe("test1/message")
	client.subscribe("test/accdata1")
	
		
	
def OnMessage(client,userdata,msg):
    global temp
    if msg.topic =="test/accdata1":
        temp.append(msg.payload.decode())
        time.sleep(1)
        
def assign_value():
    global count
    global value
    global label
    global temp
    global average
    local_temp=temp
    threading.Timer(10.0,assign_value).start()
    for item in local_temp:
        if float(item)<0.4:
            average.append(0)
        else:
            average.append(float(item))
    print(average)
            
    value.append(np.average(average))
    temp.clear()
    average.clear()
    count +=10
    label.append(str(count))
    print(label)
        
        
def animate(i):
    global value
    global label
    plt.clf()
    plt.ylim(0,10)
    plt.xlim([0,19])
    plt.title("magnitude over 3 minutes period", fontsize=15)
    plt.bar(label,value)
    

while True:
    try:
        client = setup_mqtt()
        client.loop_start()
        print("mqtt connected")
        break
    except:
        print("Still waiting for mqtt connection")
        time.sleep(1)
        
assign_value()

def aniChecking():
    global count
    global ani
    global value
    global label
    while True:
        if count>=190:
            count=0
            value.clear()
            label.clear()
            value.append(0)
            label.append("0")
            ani= animation.FuncAnimation(fig, animate, frames=18, interval=10000,repeat=False)
            

aniCheck = threading.Thread(target=aniChecking,daemon=True)
aniCheck.start()

ani= animation.FuncAnimation(fig, animate, frames=18, interval=10000,repeat=False)
plt.show()

