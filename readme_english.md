# ROS node on Windows
[GitHub repo.](https://github.com/Wei1234c/ROS_node_on_Windows)  

Wei Lin  
2018-03-16  

![chatters](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/string_telephone.jpg)  


## [Why this]
---
Recently I started to learn [ROS](http://www.ros.org/) and found it interesting. The architecture is similar to a lot of decentralized frameworks. There is a master or broker, and nodes Communicate through the topics/publish/subscribe mechanism, there is also a service mechanism for RPC, the official website has a good [description](http://wiki.ros.org/ROS/Technical%20Overviewl):  

![ROS architecture](http://wiki.ros.org/ROS/Technical%20Overview?action=AttachFile&do=get&target=master-node-example.png)  



At first glance, I think the most important feature of ROS is the exchange of messages. Inspite of master, the data is ultimately passed directly between nodes. It does not need to go through master or broker. This is similar to [Dask](https://dask.pydata.org/en/latest/), which is more suitable for delivering larger chunk of data than [MQTT](http://mqtt.org/) .  

ROS nodes communicate through the topics/publish/subscribe mechanism. It is also because of the need for integration. Different packages developed by different companies and different development teams can communicate with each other by following a common message standard. This [paragraph](http://www.ros.org/core-components/) explains it very well:
> ... Another benefit of using a message passing system is that it forces you to implement clear interfaces between the nodes in your system, nearest improvement encapsulation and promoting code reuse.  

However, if you want to connect a Windows computer to a ROS network, you will need another Linux computer to run a bridge package (for example, [rosbridge](http://wiki.ros.org/rosbridge_suite)). Not so convenient.  

The Windows ecosystem also has a lot of resources. If Windows can be easily connected to a ROS network, the integration will be great. For example:
- On a Windows computer, I can collect data from a remote ROS system and use the software specific to the Windows platform to analyze and process it.
- When you need to control some Linux/ROS platform specific resources, you can send instructions to do that.

## [Thinking]
---
- Python considerably keeps the operating system abstract. The same Python code may run on both Linux and Windows.
- Therefor, we may copy the dependent *.py codes to Windows and it may be able to run.
- For the simplest test, use [chatter experiment on ROS tutorials](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29) as an example and see if we can get a Windows computer directly connect to ROS's topics/publish/subscribe network.  

## [How]
---

### ROS node's workflow
In `talker.py`, `listener.py` must:
- First create a ROS client
- Create XMLRPC client, server
- Registration with the ROS master through the XMLRPC protocal
- Then create publisher or subscriber, register to master, and start sending and receiving messages

This process can be seen from the contents of the `talker.py`, `listener.py` log file:  

Talker's log:
```
[rospy.client][INFO] 2018-03-16 21:17:00,447: init_node, name[/talker_5428_1521206220442], pid[5428]
[xmlrpc][INFO] 2018-03-16 21:17:00,448: XML-RPC server binding to 0.0.0.0:0
[xmlrpc][INFO] 2018-03-16 21:17:00,449: Started XML-RPC server [http://DESKTOP-M4SP11C:53279/]
[rospy.impl.masterslave][INFO] 2018-03-16 21:17:00,449: _ready: http://DESKTOP-M4SP11C:53279/
[rospy.registration][INFO] 2018-03-16 21:17:00,450: Registering with master node http://192.168.43.124:11311
[xmlrpc][INFO] 2018-03-16 21:17:00,450: xml rpc node: starting XML-RPC server
[rospy.init][INFO] 2018-03-16 21:17:00,459: ROS Slave URI: [http://DESKTOP-M4SP11C:53279/]
[rospy.init][INFO] 2018-03-16 21:17:00,459: registered with master
[rospy.rosout][INFO] 2018-03-16 21:17:00,459: initializing /rosout core topic
[rospy.rosout][INFO] 2018-03-16 21:17:00,496: connected to core topic /rosout
[rospy.simtime][INFO] 2018-03-16 21:17:00,522: /use_sim_time is not set, will not subscribe to simulated time [/clock] topic
[rosout][INFO] 2018-03-16 21:17:00,838: hello world 1521206220.8385267
[rosout][INFO] 2018-03-16 21:17:00,938: hello world 1521206220.9387927
[rosout][INFO] 2018-03-16 21:17:01,039: hello world 1521206221.0385587
[rospy.internal][INFO] 2018-03-16 21:17:01,055: topic[/rosout] adding connection to [/rosout], count 0
[rosout][INFO] 2018-03-16 21:17:01,143: hello world 1521206221.1438384
[rosout][INFO] 2018-03-16 21:17:01,252: hello world 1521206221.252839
[rosout][INFO] 2018-03-16 21:17:01,338: hello world 1521206221.3388672
[rosout][INFO] 2018-03-16 21:17:01,438: hello world 1521206221.4389257
```

### Dependent modules (packages)
In order for `talker.py` and `listener.py` to perform the above process smoothly, the dependent modules (packages) must still be copied from ROS/Linux and placed onto a Windows computer. After that, just make sure `talker.py`. , `listener.py` can refer to those modules.  


The dependent modules (packages) are as below (the items below the "ros" folder):  
![dependent modules](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/dependants.jpeg)

### Setting up the environment
I added one line of code at the beginning of `talker.py`, `listener.py`
```
Import config_ros_win
```

This will reference [config_ros_win.py](https://github.com/Wei1234c/ROS_node_on_Windows/blob/master/codes/my_ws/src/ros_win/scripts/config_ros_win.py), and its main purpose is:
- Set the values of some environment variables required by the ROS node
- Append paths to PYTHONPATH so that ROS node's python code can find the required modules

## [Test the idea]
---

### 1. Start ROS core
Start ROS core on a Linux machine and record its IP address (for example: `192.168.43.124`)  

### 2. Download the sample
Copy the contents of [GitHub repo.](https://github.com/Wei1234c/ROS_node_on_Windows) into a folder (eg C:\temp\)  

### 3. Set the ROS master's URI
Find the file `config_ros_win.py` and set the `ROS_MASTER_URI` variable in it:
```
os.environ['ROS_MASTER_URI'] = 'http://192.168.43.124:11311'
```

### 4. Start Listener
Open a terminal window, cd to the `...scripts` folder (where `listener.py` is located) and execute `python listener.py`
```
C:\...\ROS node on Windows\codes\my_ws\src\ros_win\scripts> python listener.py
```

### 5. Start Talker
Open another window of terminal, cd to the `...scripts` folder (where `talker.py` is located) and run `python talker.py`
```
C:\...\ROS node on Windows\codes\my_ws\src\ros_win\scripts> python talker.py
```

Talker should start sending messages to listener.  

## [Result]
---
I use two Windows Home edition computers to do [chatter](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29) via ROS network
- The ROS core runs on the Raspberry Pi Zero W in the middle
- ROS node on the left computer runs "Listener"
- ROS node on the right computer runs "Talker"

Messages can be smoothly delivered and received  

[![ROS chatters on Windows](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/youtube.jpeg)](https://youtu.be/SJJreMgJbx0)  


## [Possible Applications]
---
- Build an IoT system with ROS
- Create a chat room with ROS
- Build a parallel/distributed system with ROS to handle big data
- Integration with software systems on other Windows platforms

...

## [Notes]
---
- At this moment, only the simple `chatter` example has been tested. If other message types or functions are involved and depending on the native C code, this may not work.
- The above is purely personal experiment, stability not guaranteed .
