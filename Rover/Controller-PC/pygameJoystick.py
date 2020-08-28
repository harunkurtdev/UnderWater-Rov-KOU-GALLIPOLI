import pygame
import time

class pyGameJoystick:
    
    "construckda pygame modülü istiyoruz..."
    def __init__(self,pyGame):
        self.pyGame=pyGame
        try:
            for event in self.pyGame.event.get(): # Kullanıcı bir şey yaptı
                if event.type == pygame.QUIT: # Kullanıcı kapat'ı tıkladıysa
                    break # Yaptığımız işaret, bu döngüden çıkalım

                # Olası kumanda kolu eylemleri: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick kolu düğmesine basıldı.")
                    #serArduino.write(b"1");
                if event.type == pygame.JOYBUTTONUP:
                    print("Kumanda kolu düğmesi serbest bırakıldı.")
            
            "pygame başlatıldı..."
            self.pyGame.init()
            "pygame içerisinde ki joystick modülü çalıştırıldı..."
            self.pyGame.joystick.init()
            "pygame üzerine zaman mödülü alıyoryz"
            self.clock=pyGame.time.Clock()
            #print("başladı")            
        except Exception as exp:
            print("pygame veya joystick başlatılırken bir sorun oluştu hata : ",exp)

    def joystick_Count(self):
        "pygame başlatılıp başlatılmayacağı sorgulanıyor..."
        if self.pyGame.joystick.get_init()==True:
            "pygame.joystick içerisinden başlatılmış ise joystick sayısını bize göster"
            self.joystickCount=self.pyGame.joystick.get_count()
            #print(self.joystickCount)
            return self.joystickCount
        else :
            print("Pygame başlatılmadı...")

    def joystickIdName(self,id=None):
        self.joystickNumber=self.joystick_Count()
        if id==None:
            for index in range(self.joystickNumber):
                "istenilen joystciği aldık..."
                self.joystick=self.pyGame.joystick.Joystick(index)
                "joystik kolunu başlatıyoruz"
                self.joystick.init()
                axes = self.joystick.get_numaxes()
                "joystick id sini alıyoruz"
                self.joystickId=self.joystick.get_id()
                "joysctik ismini alıyoruz"
                self.joystickName=self.joystick.get_name()
                #print("joystick : " ,self.joystick )
                #print("joystick number : ",index," joystick : ",joystick," joystickId : " , self.joystickId, " joystickName : ",self.joystickName)
                return self.joystick,self.joystickId,self.joystickName
        else:
            "istenilen joystciği aldık..."
            self.joystick=self.pyGame.joystick.Joystick(id)
            "joystik kolunu başlatıyoruz"
            #self.joystick.init()
            "joystick id sini alıyoruz"
            self.joystickId=self.pyGame.joystick.Joystick(id).get_id()
            "joysctik ismini alıyoruz"
            self.joystickName=self.pyGame.joystick.Joystick(id).get_name()
            #print("joystickId : " , self.joystickId, " joystickName : ",self.joystickName)
            "param 1 joystickId  param 2 joystickName"
            return self.joystick,self.joystickId,self.joystickName
    
    def joysctikNumAxes(self,index=None):
        self.pyGame.event.get()
        "foksiyondan gelen joystik id name gibi bigiler alıyoruz"
        self.joystick,_,_=self.joystickIdName()
        #print("gelen joystick : ",joystick)
        "kol üzerinde ki axes sayısını alıyoruz"
        self.joystickNumberAxes=self.joystick.get_numaxes()
        "eğer ki verilen index boş ise "
        #print("joystickNumberAxes : ", self.joystickNumberAxes)
        if index==None:
            self.joystick_axis=[]
            for index in range(self.joystickNumberAxes):
                "burada joystick sayılarını indexsinden axislarını çekiyoruz..."
                #print(index ,self.joystick.get_axis(index))
                self.joystick_axis.append(self.joystick.get_axis(index))
                "param 1 index param 2 joystick_axis"
            
            # print(self.joystick_axis)
            return self.joystick_axis
        else :
            "verilen index boş değil ise..."
            self.joystick_axis=self.joystick.get_axis(index)
            print(self.joystick_axis)
            "param 1 joystick_axis"
            return self.joystick_axis
    
    def joysctikNumBalls(self,index=None):
        "foksiyondan gelen joystik id name gibi bigiler alıyoruz"
        self.joystick,_,_=self.joystickIdName()
        "kol üzerinde ki top  sayısını alıyoruz"
        self.joysctikNumberBalls=self.joystick.get_numballs()
        "eğer ki verilen index boş ise "
        data=[]
        if index==None:
            for index in range(self.joysctikNumberBalls):
                "burada joystick sayılarını indexsinden axislarını çekiyoruz..."
                data.append(self.joystick.get_ball(index))
                print(data)
                "param 1 index param 2 self.joystick_ballx param 3 self.joystick_bally"
            return data
        else :
            "verilen index boş değil ise..."
            self.joystick_ballx,self.joystick_bally=self.joystick.get_ball(index)
            print(self.joystick_ballx,self.joystick_bally)
            "param 1 self.joystick_ballx param2 self.joystick_bally"
            return self.joystick_ballx,self.joystick_bally

    def joysctikNumButtons(self,index=None):
        "foksiyondan gelen joystik id name gibi bigiler alıyoruz"
        self.joystick,_,_=self.joystickIdName()
        "kol üzerinde ki top  sayısını alıyoruz"
        self.joysctikNumberButtons=self.joystick.get_numbuttons()
        "eğer ki verilen index boş ise "
        if index==None:
            indexButtonValue=[]
            for index in range(self.joysctikNumberButtons):
                "burada joystick sayılarını indexsinden axislarını çekiyoruz..."
                self.joystick_button=self.joystick.get_button(index)
                indexButtonValue.append(self.joystick_button)
                # print("button index {} button value {}".format(index,self.joystick_button))
            # print(indexButtonValue)
            "param 1 index param 2 self.joystick_button param 3 indexButtonValue[]"
            return index,self.joystick_button,indexButtonValue
        else :
            "verilen index boş değil ise..."
            self.joystick_button=self.joystick.get_button(index)
            print(self.joystick_button)
            "param 1 self.joystick_button"
            return self.joystick_button
    
    def joysctikNumHat(self,index=None):
        "foksiyondan gelen joystik id name gibi bigiler alıyoruz"
        self.joystick,_,_=self.joystickIdName()
        "kol üzerinde ki top  sayısını alıyoruz"
        self.joysctikNumberHat=self.joystick.get_numhats()
        "eğer ki verilen index boş ise "
        if index==None:
            for index in range(self.joysctikNumberHat):
                "burada joystick sayılarını indexsinden axislarını çekiyoruz..."
                self.joystick_hat=self.joystick.get_hat(index)
                print(index,self.joystick_hat)
                "param 1 index param 2 self.joystick_hat"
                return index,self.joystick_hat
        else :
            "verilen index boş değil ise..."
            self.joystick_hat=self.joystick.get_hat(index)
            print(self.joystick_hat)
            "param 1 self.joystick_hat"
            return self.joystick_hat


if __name__ == '__main__':
    pygame.init()
    while 1 :
        pystart=pyGameJoystick(pyGame=pygame)
        pystart.joysctikNumBalls()