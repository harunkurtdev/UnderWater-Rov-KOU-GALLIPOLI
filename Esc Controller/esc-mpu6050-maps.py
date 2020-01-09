"""Burada ki asıl amaç Raspberry pi de Mpu dan aldıgımız denge oranına göre motorlara güç vermektir...
aşağıda ki fonk ise arduino daki map fonksiyonun matematiksel halidir...
"""
def mpu6050map(x,in_min,in_max,out_min,out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min) + out_min)

if __name__ == '__main__':
   a= mpu6050map(1023,0,1023,0,160)
   print(a)