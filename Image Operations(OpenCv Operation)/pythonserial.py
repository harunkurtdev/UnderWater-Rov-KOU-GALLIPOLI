import serial
import time
import json
def pythonSerial():
    # burada portumuzu okuyoruz...
    port = serial.Serial("COM14"  # com girilmesi gerekli
                         , baudrate=19200  # baund rate
                         , timeout=0
                         , parity=serial.PARITY_NONE,
                         bytesize=serial.EIGHTBITS,
                         stopbits=serial.STOPBITS_ONE
                         )  # zaman aşım

    #port_okunan = port.readline()[:-2]  # readline ile veriyi okuyup barçalıyoruz
    #print("Mpu dan okunan X derecesi : {}".format(port_okunan.decode("ascii")))  # format ile ekrana veriyi bastıroyruz aynı zamanda ise
    # decode diyerek parçalama işlemi yapıyoruz...

    while True:
        if port.isOpen():
            port.write("a".encode("ascii"))
            b=port.read()
            if b!=b'':
                print(b.decode("ascii"))
        port.flush()

        if 0xFF==ord("q"):
            print("cıkıs yapılıyor")
            break

if __name__=="__main__":
    pythonSerial()
