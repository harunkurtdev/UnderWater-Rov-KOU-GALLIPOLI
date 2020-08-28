import asyncio
import websockets
import json
import numpy as np
import serial
import  time
from serial_asyncio import create_serial_connection

# port = serial.Serial("COM1"  # com girilmesi gerekli
#                          , baudrate=115200  # baund rate
#                          , timeout=0
#                          ,parity=serial.PARITY_NONE,
#                          bytesize=serial.EIGHTBITS,
#                          stopbits=serial.STOPBITS_ONE
#                      )  # zaman aşım

class RoboSocketCom:

    def __init__(self,serverHost=None,serverPort=None,clientHost=None,clientPort=None):
        "gelen bilgiler atanmakta..."
        self.serverHost=serverHost
        self.serverPort=serverPort
        self.clientHost=clientHost
        self.clientPort=clientPort


        "socket bağlantılarını başlat"
        self.socketRun()

    def socketRun(self):
         
        """asyncio ile fonksiyonu başlatılmasını isteyerek burada fonksiyonu çağrıyoruz 
        ve bölyelikle rahatlıkla socket bağlantımızın başlatılmasını sağlıyoruz ve istenilen bağlantı yapılmış
        oluyor...
        self.startRoboServer() yerine 
        self.startserver da yazılabilirdi ancak fonksiyonu başlatmak gerekli...
        """

        "serverhost ve serverPort dolu ise server başlasın"
        if self.serverHost==None and self.serverPort==None :
            pass
        else : 
            asyncio.get_event_loop().run_until_complete(self.startRoboServer())
            "clientHost ve clientPort dolu ise bağlanma işlemi başlasın"
            # self.loop= asyncio.get_event_loop()
            # self.coro =create_serial_connection(self.loop, Output, 'COM5', baudrate=115200)

            asyncio.get_event_loop().run_forever()
            
        if self.clientHost==None and self.clientPort==None :
            pass
        else: 
            "client bilgilerini burada doldurabilir connect işlemini başlatılabilir ancak hata alınmakta"
            pass
            #asyncio.get_event_loop().run_until_complete(self.startRoboServerConnect())



    def startRoboServer(self,serverHost=None,serverPort=None):
        "server ın başlatılması gerektiğini dile getiyoruz gelen verileri roboResponse da yakalamamız gerektiğini istoyruz"
        if self.serverHost==None or self.serverPort==None:
            self.serverHost=serverHost
            self.serverPort=serverPort

        self.startserver=websockets.serve(self.roboServer,self.serverHost,self.serverPort)
        print("server başladı")
        return self.startserver

    async def roboServer(self,websockets,path):
        """
        Burada bir algoritma üreterek ancak send veri gönderebiliriz... gelen verileri buradan
        recv ile yakalarız...
        """
        self.roboServerWebSocket= websockets
        
        """
        send() fonksiyonu ile gelen mesajlara karşılık verebiliriz...
        """
        # await websockets.send("server dan giden mesaj roboServerWebSocket")
        
        """gelen mesajları bu fonksiyon içerisinde recv() ile yakalayıp 
        ekrana basabiliriz...
        """

        self.message = await websockets.recv()
        "json.loads methodunu kullanmak zorundasın aksi halde hata alırsın"
        value = json.loads(self.message)

        try:
            #print("client ten gelen : ",self.message)
            direction="0"

            if value!=None:
                if(float(value["motor_x_axis"])==-1.0):
                    direction="1"
                    #direction="front"
                    # speed= map(-value["motor_x_axis"],0.0,1.0,0,2000)
                elif(float(value["motor_x_axis"])==0.999969482421875):
                    direction="2"
                    #direction="back"
                    # speed = map(value["motor_x_axis"], 0.0,0.999969482421875,0, 2000)

                if (float(value["motor_y_axis"]) ==0.999969482421875):
                    direction = "4"
                    # direction="goright"
                    # speed = map(value["motor_y_axis"], 0.0, 0.999969482421875, 0, 2000)
                elif (float(value["motor_y_axis"]) ==-1.0):
                    direction="3"
                    #direction="goleft"
                    # speed = map(-value["motor_y_axis"], 0.0, 1.0, 0, 2000)

                if (int(value["robot_arm_x_positive"])> 0):
                    direction="5"
                    #direction="turnright"
                    # speed = 1000

                if (int(value["robot_arm_x_negative"])> 0):
                    direction="6"
                    #direction="turnleft"
                    # speed = 1000

                if (int(value["robot_arm_z_negative"])> 0):
                    direction="7"
                    #direction="turnleft"
                    # speed = 1000


                print(direction)

                # line = await reader.readline()
                # print(str(line, 'utf-8'))
                #
                # # # port.open()
                # if port.isOpen():
                #     try:
                #         print(direction)
                #         port.write(str(direction).encode("utf-8"))
                #         incoming = port.readline().decode("utf-8")
                #
                #         print(incoming)
                #     except Exception as e:
                #         print(e)
                #         pass
                # else:
                #     print("opening error")
                # # port.close()


            # try:
            #
            #     self.port.write(str(value).encode("utf-8"))
            #     #print(str(value).encode("utf-8"))
            #     # array = []
            #     # for i in range(4):
            #     #     port_okunan_x = self.port.readline()[:-2].decode("utf-8")  # readline ile veriyi okuyup barçalıyoruz
            #     #
            #     #     array.append(port_okunan_x)
            #     #
            #     # print("Mpu dan okunan: {}-{}-{}".format(array[0],array[1],array[2]))
            #
            #     print(self.port.readlines())
            # except Exception as exp:
            #     print("port açılırken sorun oldu ",exp)
            #print(self.port.read())

            
            
            await websockets.send("server dan giden mesaj- roboServerWebSocket")
            
        except Exception as exp:
            pass
            print("roboServer bölümünde veriler gelirken bir hata oluştu hata kodu : ",exp)
        finally:
            print(value)
    async def startRoboServerConnect(self,clientHost=None,clientPort=None,sendMessage=None):
        "Server a diğer araçta ki server a bağlanma durumunu buradan ele alarak yapacağız"
        
        if self.clientHost==None or self.clientPort==None:
            self.clientHost=clientHost
            self.clientPort=clientPort
        
        """
        websocket bağlantısı açılmaktadır ve bu açılma işlemi ile verileri transfer işlemi yapmaktayız...
        
        """
        async with websockets.connect("ws://"+str(self.clientHost)+":"+str(self.clientPort)) as roboClientWebSocket:
            
            "hata alınmaz ise verileri aktarma bölümü..."
            try :
                self.roboClientWebSocket= roboClientWebSocket
                """
                farklı bir foknsiyon içerisinde verilerimizi transfer işlemi yapmaya çalışmaktayız...
                ancak verileri transfer ederken bir sorun almaktayız ----düzeltimesi gerekiyor----
                ------ Hatalı bölüm-----------
                #asyncio.get_event_loop().run_until_complete(self.roboSendMessage(roboClientWebSocket=self.roboClientWebSocket,sendMessage=sendMessage))
                """ 
                
                " foksiyon sayesinde alınan veriyi socket üzerinden server a transfer etme işlemi"
                await self.roboClientWebSocket.send(sendMessage)

                "server dan gelen veriyi dinleme işlemi"
                print(await self.roboClientWebSocket.recv())
                return self.roboClientWebSocket
            except Exception as hata:
                print("startRoboServerConnect bölümünde veriler iletilirken bir hata ile karışılaşıldı hata kodu : ",hata)

    async def roboSendMessage(self,roboClientWebSocket=None,sendMessage=None):
        "buradan bir mesaj gönderme işlemi yapılmaktadır..."
        #self.roboClientWebSocket=await self.startRoboServerConnect()
        
        if sendMessage==None:
            pass
        else: 
            try: 
                await self.roboClientWebSocket.send(sendMessage)
                print(await self.roboClientWebSocket.recv())
                
            except Exception as exp:
                print("roboSendMessage bölümünde veriler iletilirken bir hata ile karşılaşıldı hata kodu : ",exp)
        #self.roboClientWebSocket.close()

if __name__ == '__main__':
    robosocket=RoboSocketCom(serverHost="0.0.0.0",serverPort=5000)
    #robosocketclient=RoboSocketCom(clientHost="127.0.0.1",clientPort=5000)
    #robosocketclient.startRoboServerConnect()
    #robosocketclient.socketRun()
    

