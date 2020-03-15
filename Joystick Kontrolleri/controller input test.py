# kodu pygame örneğinden toplandı ve sonra değiştirildi
import serial
import pygame
import numpy as np
#import pygame.base
#import Drive
# Arduino için seri bağlantı noktasını tanımlama
#serArduino = serial.Serial("COM3")

# Bazı renkleri tanımla
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# Bu, ekrana yazdırmamıza yardımcı olacak basit bir sınıf
# Oyun çubuklarıyla hiçbir ilgisi yok, sadece
# bilgi.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 1250
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    

pygame.init()

# Ekranın genişliğini ve yüksekliğini ayarlama [genişlik, yükseklik]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Joystik deneme")

# Kullanıcı kapat düğmesini tıklayana kadar bekleyin.
done = False

# Ekranın ne kadar hızlı güncelleneceğini yönetmek için kullanılır
clock = pygame.time.Clock()

# joystick kollarını başlat
pygame.joystick.init()


#Kamerayı başlat ve başlat
#pygame.camera.Camera.start()


# Yazdırmaya hazır olun
textPrint = TextPrint()

message_list = np.array([[0,1,2,3],[0,1,2,3,4,5,6,7,8,9,10,11]])

print(message_list)
# -------- Main Program Loop -----------
while done==False:
    # ETKİNLİK İŞLEME ADIMI
    for event in pygame.event.get(): # Kullanıcı bir şey yaptı
        if event.type == pygame.QUIT: # Kullanıcı kapat'ı tıkladıysa
            done=True # Yaptığımız işaret, bu döngüden çıkalım

        # Olası kumanda kolu eylemleri: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick kolu düğmesine basıldı.")
            #serArduino.write(b"1");
        if event.type == pygame.JOYBUTTONUP:
            print("Kumanda kolu düğmesi serbest bırakıldı.")
            #serArduino.write(b"0");

    # ÇİZİM ADIM
    # İlk olarak, ekranı beyaza temizleyin. Bunun üzerine başka çizim komutları
    # koymayın, aksi takdirde bu komutla silinirler.
    screen.fill(WHITE)
    textPrint.reset()

    # Sayımını al joysticks
    joystick_count = pygame.joystick.get_count()


    textPrint.print(screen, "joysticks kolu sayısı : {}".format(joystick_count) )
    textPrint.indent()
    #pilotInput = [0 for]
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Denetleyici için işletim sisteminden adı alın/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )

        # Genellikle eksen çiftler halinde çalışır, biri için yukarı / aşağı ve diğeri için sola / sağa.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Eksen sayısı: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            message_list[0][i]=axis
            textPrint.print(screen, "Eksen {} değeri: {:>6.2f}".format(i, axis) )
        textPrint.unindent()


        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Düğme sayısı: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            message_list[1][i]=button
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()

        print(message_list)

        # Şapka anahtarı. Yön için ya hep ya hiç, joystick gibi değil.
        # Değer bir dizide geri gelir.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()
        
        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

    # BU YORUMUN ÜZERİNDEN ÇİZMEK İÇİN TÜM KOD

    # Devam edin ve ekranı çizdiklerimizle güncelleyin.
    pygame.display.flip()

    # Saniyede 20 kare ile sınırlandır
    clock.tick(20)
    

# Pencereyi kapatın ve çıkın.
# Bu satırı unutursanız, program 'askıda kalacaktır'
# IDLE'den çalışıyorsa çıkışta.
pygame.quit ()
