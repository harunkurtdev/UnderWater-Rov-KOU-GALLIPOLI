import serial
import time
import json
def pythonSerial():
    # burada portumuzu okuyoruz...
    port = serial.Serial("COM5"  # com girilmesi gerekli
                         , baudrate=115200  # baund rate
                         , timeout=0.101
                         , parity=serial.PARITY_NONE,
                         bytesize=serial.EIGHTBITS,
                         stopbits=serial.STOPBITS_ONE
                         )  # zaman aşım

    #port_okunan = port.readline()[:-2]  # readline ile veriyi okuyup barçalıyoruz
    #print("Mpu dan okunan X derecesi : {}".format(port_okunan.decode("ascii")))  # format ile ekrana veriyi bastıroyruz aynı zamanda ise
    # decode diyerek parçalama işlemi yapıyoruz...

    while True:
        if port.readline():
            if port.readline()!=b'':
                jsonSerial=json.loads(port.readline().decode("utf-8"))
                print(jsonSerial["x_eksen"])

        port.flush()

        if 0xFF==ord("q"):
            print("cıkıs yapılıyor")
            break

if __name__=="__main__":
    pythonSerial()
