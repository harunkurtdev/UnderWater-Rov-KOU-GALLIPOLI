"""main controller."""
import time,base64
import pygame
import cv2
import numpy as np
from websocket import create_connection


size = [1280, 720]

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def location_print(self, screen, textString,x=size[0]-200,y=0):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [x, y])


    def title(self,screen):

        self.location_print(screen, "----Sağa-Sola Dönüş---", y=0)

        self.location_print(screen, "---Araç İleri-Geri Durumu---", y=30)

        """bu alanda biz ekranda göstermek istediğimiz aracın iniş ve yükselişine ait button bilgilerini göstermekteyiz"""

        self.location_print(screen,
                            "   ----Derinlik Durum----",
                            y=60)

        """ekrana Gripper Yazısı Bastırıyoruz"""
        self.location_print(screen,
                            "   ----Gripper Arm Durumu----",
                            y=90)

        """ekrana ışık bilgisi bastırıyoruz"""
        self.location_print(screen,
                            "   ----Işık Durum Bilgisi----",
                            y=120)

    """aracın derinliğini anlık olarak öğrenmek amaçlı bir fonksiyon"""
    def depth_button(self, screen,button_index,button_value):

        """burada sabit bir fonksiyon oluşturarak araç sabit fonksiyonu oluşturduk sürekli kullanmak için"""
        def vehicle_constant():
            self.print(screen, "Araç Sabit Durmakta.")



        """eğer ki aşağı iniş yukarı çıkışlardan birisine basılırsa button değeri 1 olursa ekrana yazı bastır"""
        if button_index == 4 or button_index==6:
            x=self.x
            if button_value==1:

                #self.print(screen, "Araç Yüzeye Çıkmakta." if button_index== 4 else "Araç Derine Doğru Dalmakta.")

                self.location_print(screen, ("Araç Yüzeye Çıkmakta." if button_value==1 else "Araç Sabit Durmakta.")
                if button_index== 4 else
                ("Araç Derine Doğru Dalmakta."if button_value==1 else "Araç Sabit Durmakta."),y=75)

            # elif button_value==0:
            #     self.location_print(screen, "" if button_value == 1 else "Araç Sabit Durmakta.", y=15)




    """gripper ı kontrol etmek için yapılmış bir fonksiyon """
    def gripper_arm(self, screen,button_index,button_value):


        """bu alanda biz ekranda göstermek istediğimiz arac kolunun açılış ve kapnışını kontrol ediyoruz ait button bilgilerini göstermekteyiz"""

        if button_index == 5 or button_index==7:
            x=self.x
            if button_value==1:

                #self.print(screen, "Araç Yüzeye Çıkmakta." if button_index== 4 else "Araç Derine Doğru Dalmakta.")

                self.location_print(screen, ("Kol açılıyor." if button_value==1 else "Araç Kolu Sabit Durmakta.")
                if button_index== 5 else
                ("Kol Kapanıyor."if button_value==1 else "Araç Kolu Sabit Durmakta."),y=105)



        # if button_index == 5 or button_index==7:
        #     if button_value==1:
        #         self.print(screen, "Kol açılıyor." if button_index== 7 else "Kol Kapanıyor.")
        #     else:
        #         vehicle_constant()

    def reset(self):
        self.x = 1150
        self.y = 10
        self.line_height = 40

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


camera = cv2.VideoCapture(0)
    #cameradan bilgi okuma

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



# Bu, ekrana yazdırmamıza yardımcı olacak basit bir sınıf
# Oyun çubuklarıyla hiçbir ilgisi yok, sadece
# bilgi.
pygame.init()

# Ekranın genişliğini ve yüksekliğini ayarlama [genişlik, yükseklik]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Joystick ile PC'den Kontrol")

# Kullanıcı kapat düğmesini tıklayana kadar bekleyin.
done = False

# Ekranın ne kadar hızlı güncelleneceğini yönetmek için kullanılır
clock = pygame.time.Clock()

# joystick kollarını başlat
pygame.joystick.init()

# Kamerayı başlat ve başlat
# pygame.camera.Camera.start()


textPrint = TextPrint()

# -------- Main Program Loop -----------
# cam=cv2.VideoCapture(0)
try:

    while True:

        # ETKİNLİK İŞLEME ADIMI
        for event in pygame.event.get():  # Kullanıcı bir şey yaptı
            if event.type == pygame.QUIT:  # Kullanıcı kapat'ı tıkladıysa
                done = True  # Yaptığımız işaret, bu döngüden çıkalım
                pygame.quit()
                cv2.destroyAllWindows()

        # ÇİZİM ADIM
        # İlk olarak, ekranı beyaza temizleyin. Bunun üzerine başka çizim komutları
        # koymayın, aksi takdirde bu komutla silinirler.

        screen.fill(WHITE)

        # ret, frame = camera.read()

        ws = create_connection("ws://127.0.0.1:5001")
        ws.send("Hello, World")
        result = ws.recv()
        ws.close()
        im_bytes = base64.b64decode(result.decode("utf-8"))
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        # cv2.imshow("Resim", img)
        img = img
        frame = img.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.array(frame)
        # yüzdelik değere göre büyültme ve küçültme yap
        width_percent = 100
        height_percent = 80
        width = int(frame.shape[1] * width_percent / 100)
        height = int(frame.shape[1] * height_percent / 100)
        dim = (width, height)

        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (100, 100))

        # pygame.display.update()

        # Sayımını al joysticks
        joystick_count = pygame.joystick.get_count()

        # textPrint.print(screen, "joysticks kolu sayısı : {}".format(joystick_count))
        # textPrint.indent()
        # pilotInput = [0 for]
        # For each joystick:
        for i in range(joystick_count):

            """ekrana title bilgilerini basıtıyoruz"""
            textPrint.title(screen)

            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            # textPrint.print(screen, "Joystick {}".format(i))
            # textPrint.indent()

            # Denetleyici için işletim sisteminden adı alın/joystick
            name = joystick.get_name()

            # Genellikle eksen çiftler halinde çalışır, biri için yukarı / aşağı ve diğeri için sola / sağa.
            axes = joystick.get_numaxes()

            for i in range(axes):
                axis = joystick.get_axis(i)

                if i == 0:

                    if axis == -1.0:
                        # textPrint.print(screen, "Sola Hareket Etmekte.")
                        textPrint.location_print(screen, "Sola Hareket Etmekte.", y=15)

                    elif axis == 0.999969482421875:
                        # textPrint.print(screen, "Sağa Hareket Etmekte.")
                        textPrint.location_print(screen, "Sağa Hareket Etmekte.", y=15)
                    else:
                        #  textPrint.print(screen, "Sağa - Sola Hareket etmiyor.")
                        textPrint.location_print(screen, "Sağa - Sola Hareket etmiyor.", y=15)
                elif i == 1:

                    if axis == -1.0:
                        # textPrint.print(screen, "Araç İleri Doğru Gitmekte.")
                        textPrint.location_print(screen, "Araç İleri Doğru Gitmekte.", y=45)

                    elif axis == 0.999969482421875:
                        # textPrint.print(screen, "Araç Geri Doğru Gitmekte.")
                        textPrint.location_print(screen, "Araç Geri Doğru Gitmekte.", y=45)

                    else:
                        # textPrint.print(screen, "Araç Sabit Durmakta.")
                        textPrint.location_print(screen, "Araç Sabit Durmakta.", y=45)

            buttons = joystick.get_numbuttons()

            for i in range(buttons):
                button = joystick.get_button(i)

                if i == 0:
                    textPrint.location_print(screen, "Araç Önü Aydınlatılıyor." if button == 1 else "", y=135)
                elif i == 1:
                    pass
                elif i == 2:
                    pass
                elif i == 3:
                    pass
                elif i == 4:
                    """derinlik yüzeye çıkış"""
                    textPrint.depth_button(screen, i, button)

                elif i == 6:
                    """derinlik aşağı iniş"""
                    textPrint.depth_button(screen, i, button)
                elif i == 5:
                    """gripper """
                    # textPrint.gripper_arm(screen,i,button)
                    textPrint.location_print(screen, "Araç Kol Ağzı Açılıyor." if button == 1 else "", y=105)

                elif i == 7:
                    """grippyer"""
                    # textPrint.gripper_arm(screen, i, button)
                    textPrint.location_print(screen, "Araç Kol Ağzı Kapanıyor." if button == 1 else "", y=105)

            textPrint.reset()

            # Şapka anahtarı. Yön için ya hep ya hiç, joystick gibi değil.
            # Değer bir dizide geri gelir.
            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)

            # async with websockets.connect("ws://127.0.0.1:5553") as socket:

            # await socket.send(str(message_list))#message gönder

        # BU YORUMUN ÜZERİNDEN ÇİZMEK İÇİN TÜM KOD

        # Devam edin ve ekranı çizdiklerimizle güncelleyin.
        pygame.display.flip()

        # Saniyede 20 kare ile sınırlandır
        clock.tick(24)
except KeyboardInterrupt as SystemExit:
    pygame.quit()
    cv2.destroyAllWindows()
# Pencereyi kapatın ve çıkın.
# Bu satırı unutursanız, program 'askıda kalacaktır'
# IDLE'den çalışıyorsa çıkışta.
pygame.quit()



