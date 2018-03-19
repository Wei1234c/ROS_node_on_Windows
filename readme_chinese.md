
# ROS node on Windows
[GitHub repo.](https://github.com/Wei1234c/ROS_node_on_Windows)

Wei Lin  
2018-03-16  

![chatters](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/string_telephone.jpg)  


## [緣由]
---
最近開始接觸 [ROS](http://www.ros.org/)，覺得很有趣，架構上來說和很多分散式的 frameworks 都很類似，有一個 master 或 broker 來做仲介，nodes 之間則是透過 topics/publish/subscribe 的機制來溝通，也有 service 的機制可以做 RPC，官網上有很好的[描述](http://wiki.ros.org/ROS/Technical%20Overviewl):  

![ROS architecture](http://wiki.ros.org/ROS/Technical%20Overview?action=AttachFile&do=get&target=master-node-example.png)  



初看之下，我覺得 ROS 最大的特點是 訊息的交換 雖然是由 master 牽成，但資料最終卻是由 node 和 node 之間直接傳遞的，不需經過 master 或 broker。這點和 [Dask](https://dask.pydata.org/en/latest/) 比較像，比起 [MQTT](http://mqtt.org/) 來說更適合傳遞比較大的資料包。  

ROS 透過 topics/publish/subscribe 的機制來溝通，也是因為整合上的需求，不同公司，不同開發團隊所發展出來的套件，只要遵循共同的訊息標準，就可以互相傳遞訊息整合在一起，[官網上這段話](http://www.ros.org/core-components/) 我覺得很有道理：  
>  ... Another benefit of using a message passing system is that it forces you to implement clear interfaces between the nodes in your system, thereby improving encapsulation and promoting code reuse.  

但是目前 Windows 的電腦如果想要連上 ROS 網路，都必須透過裝在另外一台 Linux 電腦上的仲介軟體(例如 [rosbridge](http://wiki.ros.org/rosbridge_suite))，不是很方便。Windows 生態圈也是有很多資源與需求，如果可以容易地連接到 ROS 網路，整合上就會更順暢一些，例如，我們就可以在 Windows 電腦上收集遠端 ROS 系統中的資料，使用 Windows 平台上特有的軟體來分析與處理，需要指揮一些 Linux/ROS 平台特有資源的時候，也可以發送指令去做一些控制。  

## [想法]
---
- Python 相當程度地把作業系統抽象化了，同樣一段 Python 程式碼在 Linux 和 Windows 上面或許都可以跑。
- 那麼，把相依的 *.py 碼都複製到 Windows 上面來，或許就可以跑。
- 從最簡單的試試看，就以 [ROS tutorials 上的 chatter 實驗](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29) 作為範例，看看能不能讓 Windows 電腦直接連上 ROS 的 topics/publish/subscribe 網路。

## [原理與作法]
---

### ROS node 主要流程
而 `talker.py`, `listener.py` 中 都須:
- 先建立一個 ROS client
- 建立 XMLRPC client, server
- 透過 XMLRPC 協定，向 ROS master 註冊
- 然後再建立 publisher 或者 subscriber，向 master 報備，然後開始收發 messages

這個流程可以從 `talker.py`, `listener.py` 的 log 檔內容看得出來:  

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

### 相依的 modules (packages)
為了讓 `talker.py`, `listener.py`能順利執行上述流程，相依的 modules (packages) 還是得從 Linux 上的 ROS 中複製出來 放到 Windows 電腦上，再來只要讓 `talker.py`, `listener.py`能引用到就好了。  


相依的 modules (packages) 有這些 (下圖 "ros" 資料夾之下的項目):  
![相依的 modules](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/dependants.jpeg)  

### 環境的建立
我在 `talker.py`, `listener.py` 的前面 加了一行程式
```
import config_ros_win
```

這會引用 [config_ros_win.py](https://github.com/Wei1234c/ROS_node_on_Windows/blob/master/codes/my_ws/src/ros_win/scripts/config_ros_win.py)，而其作用主要是:
- 設定一些 ROS node 需要的 環境變數的值
- 建立 PYTHONPATH 的路徑，讓 ROS node 的 python 程式碼可以找到需要的 modules

## [實驗步驟]
--- 

### 1. 啟動 ROS core
在某一台 Linux 的機器上 啟動 ROS core，並記錄其 IP 位址 (例如: `192.168.43.124`)

### 2. 下載範例
將 [GitHub repo.](https://github.com/Wei1234c/ROS_node_on_Windows) 的內容 複製到某個資料夾中 (例如 C:\temp\)

### 3. 設定好 ROS master 的 URI
找到檔案 config_ros_win.py，在其中設定好 `ROS_MASTER_URI` 變數:
```
os.environ['ROS_MASTER_URI'] = 'http://192.168.43.124:11311'
```

### 4. 啟動 Listener
開啟一個 terminal 的視窗，cd 到 `...scripts` 資料夾 (`listener.py` 所在之處)，執行 `python listener.py`
```
C:\...\ROS node on Windows\codes\my_ws\src\ros_win\scripts> python listener.py
```

### 5. 啟動 Talker
開啟另一個 terminal 的視窗，cd 到 `...scripts` 資料夾 (`talker.py` 所在之處)，執行 `python talker.py`
```
C:\...\ROS node on Windows\codes\my_ws\src\ros_win\scripts> python talker.py
```

這樣應該就可以開始發送 messages 給 listener。  

## [效果]
---
我用兩台 Windows Home版 的電腦透過 ROS network 做 [chatter](http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29) 實驗。  

- ROS core 跑在中間的那台 Raspberry Pi Zero W 上面
- 左側電腦上的 ROS node 運行 "Listener"
- 右側電腦上的 ROS node 運行 "Talker"

messages 可以順利傳遞與接收  

[![ROS chatters on Windows](https://raw.githubusercontent.com/Wei1234c/ROS_node_on_Windows/master/jpgs/youtube.jpeg)](https://youtu.be/SJJreMgJbx0)  


## [其他可能之應用]
---
- 用 ROS 建立一個 IoT 系統
- 用 ROS 建立一個 聊天室
- 用 ROS 建立一個 併行系統 處理大數據
- 與其他 Windows 平台上的軟體系統整合

...

## [Notes]
---
- 目前只有測試過簡單的 `chatter` 範例，如果牽涉到其他的 message type 或功能，相依於原生的 C 碼，可能就不能這樣做了。 
- 以上純屬個人試驗，不保證其穩定性。
