import numpy as np
import cv2
import math
from PIL import Image
import random
import serial
# import json
# import board
# import busio
# import adafruit_mpu6050

brown = (19, 69, 139)
blue = (255, 255, 0)
#
# i2c = busio.I2C(board.SCL, board.SDA)
# mpu = adafruit_mpu6050.MPU6050(i2c)

class Display:
    width = 700
    height = 700
    radius = 250
    angle = 85
    previous = -1

    def rotate_image(self, image, angle):
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        return cv2.warpAffine(image, M, (w, h))

    def make_compass(self, azimuth):
        height = int(self.height)
        width = int(self.width * 0.75)
        radius = int(self.radius * 0.75)
        center_x = width // 2 - 10
        center_y = height // 2
        drop = radius * math.sin(math.radians(self.angle))
        x_c = math.sqrt(math.pow(radius, 2) - math.pow(drop, 2))
        image = np.zeros((height, width, 3), np.uint8)
        lower_left = [int(center_x - x_c), int(center_y + drop - 10)]
        lower_right = [int(center_x + x_c), int(center_y + drop - 10)]
        top_left = [int(center_x - x_c), int(center_y - drop + 60)]
        top_right = [int(center_x + x_c), int(center_y - drop + 60)]
        pts = np.array([lower_left, lower_right, top_right, top_left], np.int32)
        square = pts.reshape((-1, 1, 2))
        cv2.fillPoly(image, [square], (0, 255, 0))
        top_image = [int(center_x), int(center_y - radius + 10)]
        triangle = np.array([top_left, top_right, top_image], np.int32)
        triangle = triangle.reshape(-1, 1, 2)
        cv2.fillPoly(image, [triangle], (0, 255, 0))
        image = self.rotate_image(image, azimuth)
        # cv2.circle(image, (center_x, center_y), radius, (128, 128, 128), -1)
        cv2.circle(image, (center_x, center_y), radius, (255, 0, 0), thickness=10)
        image = self.make_compass_marks(image, center_x, center_y, azimuth, radius)
        return image

    def make_compass_line(self, image, x, y, value, radius, make_red=False):
        bound = 45
        display_angle = (value - 90) % 360
        center_y = int(y - radius * math.sin(math.radians(value)))
        shift_x = radius * math.cos(math.radians(value))
        center_x = int(x + shift_x)
        display_angle = abs(display_angle)
        radius = radius + 10
        copy_y = int(y - radius * math.sin(math.radians(value)))
        shift_x = radius * math.cos(math.radians(value))
        copy_x = int(x + shift_x)
        pt1 = (center_x, center_y)
        pt2 = (copy_x, copy_y)
        thick = 1
        if display_angle % bound == 0 or make_red:
            thick = 5
            if not make_red:
                text_point = (copy_x, copy_y)
                if display_angle == 0:
                    text_point = (copy_x, copy_y - 5)
                elif copy_x <= x and copy_y <= y:
                    text_point = (copy_x - 25, copy_y - 10)
                elif copy_x <= x and copy_y >= y:
                    text_point = (copy_x - 25, copy_y + 25)
                elif copy_x >= x and copy_y >= y:
                    text_point = (copy_x + 5, copy_y + 25)
                cv2.putText(image, str(display_angle), text_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
        color = (255, 255, 255)
        if make_red:
            color = (0, 0, 255)
        cv2.line(image, pt1, pt2, color, thickness=thick)

    def make_compass_marks(self, image, x, y, azimuth, radius):
        for angle in range(0, 360, 15):
            self.make_compass_line(image, x, y, angle, radius)
        self.make_compass_line(image, x, y, azimuth + 90, radius, make_red=True)
        return image

    def make_line(self, image, x, y, value, make_red=False):
        bound = 15
        display_angle = value - 90
        center_y = int(y - self.radius * math.sin(math.radians(value)))
        shift_x = self.radius * math.cos(math.radians(value))
        center_x = int(x + shift_x)
        display_angle = abs(display_angle)
        radius = self.radius + 20
        copy_y = int(y - radius * math.sin(math.radians(value)))
        shift_x = radius * math.cos(math.radians(value))
        copy_x = int(x + shift_x)
        pt1 = (center_x, center_y)
        pt2 = (copy_x, copy_y)
        thick = 1
        if display_angle % bound == 0 or make_red:
            thick = 5
            if not make_red:
                text_point = (copy_x + 5, copy_y - 10)
                if value > 90:
                    text_point = (copy_x - 35, copy_y - 5)
                if copy_y > y:
                    text_point = (copy_x - 60, copy_y + 20)
                    if copy_x > x:
                        text_point = (copy_x + 5, copy_y + 20)
                cv2.putText(image, str(display_angle), text_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
        color = (255, 255, 255)
        if make_red:
            color = (0, 0, 255)
        cv2.line(image, pt1, pt2, color, thickness=thick)

    def indicate_bank(self, image, x, y, bank, bank_range):
        bank_val = 90 + bank
        bank_start = 90 - bank_range
        bank_end = 95 + bank_range
        for angle in range(bank_start, bank_end, 5):
            self.make_line(image, x, y, angle)
        self.make_line(image, x, y, bank_val, make_red=True)
        return image

    def draw_marks(self, image, pitch_range, x, y, limit):
        start = int((8.0 / 9.0) * pitch_range)
        x = int(x)
        end = int(-1 * start)
        count = 0
        while (start >= end):
            center_y = int(y - self.radius * (1.0 * start) / pitch_range)
            thick = 1
            if count % 4 == 0:
                cv2.line(image, (x - 50, center_y), (x + 50, center_y), (255, 255, 255), thickness=5)
                color = (255, 255, 255)
                if (center_y < limit):
                    color = (255, 0, 255)
                cv2.putText(image, str(int(start)), (x + 55, center_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            else:
                cv2.line(image, (x - 10, center_y), (x + 10, center_y), (255, 255, 255), thickness=1)
            start -= (1.0 / 18.0) * pitch_range
            count += 1

    def make_image(self, phi, theta, psi, pitch_range=180, bank_range=150):
        bank = -1 * phi
        pitch = -theta / pitch_range
        azimuth = psi
        image = np.zeros((self.height, self.width, 3), np.uint8)
        x = int(self.width / 2)
        y = int(self.height / 2)
        shift = pitch * self.radius
        center_y = int(y + shift)
        shift = abs(shift)
        value = (1.0 * shift) / self.radius
        x_r = math.sqrt(math.pow(self.radius, 2) - math.pow(shift, 2))
        first_angle = math.degrees(math.asin(value))
        second_angle = 180 - first_angle
        x_r = self.radius * math.cos(math.radians(first_angle))
        x_min = int(x - x_r)
        x_max = int(x + x_r)
        pts = np.array([[x, y], [x_min, center_y], [x_max, center_y]], np.int32)
        triangle = pts.reshape((-1, 1, 2))
        if pitch <= 0:
            first_angle += 180
            second_angle += 180
            cv2.ellipse(image, (x, y), (self.radius, self.radius), 0, first_angle, second_angle, blue, -1)
            cv2.ellipse(image, (x, y), (self.radius, self.radius), 0, second_angle - 360, first_angle, brown, -1)
            cv2.polylines(image, [triangle], True, brown, thickness=3)
            cv2.fillPoly(image, [triangle], brown)
        else:
            cv2.ellipse(image, (x, y), (self.radius, self.radius), 0, first_angle, second_angle, brown, -1)
            cv2.ellipse(image, (x, y), (self.radius, self.radius), 0, second_angle, first_angle + 360, blue, -1)
            cv2.polylines(image, [triangle], True, blue, thickness=3)
            cv2.fillPoly(image, [triangle], blue)
        # cv2.line(image, (x_min, center_y), (x_max, center_y), (147, 196, 70), thickness= 4)
        cv2.circle(image, (x, y), self.radius + 10, (128, 128, 128), thickness=25)
        self.draw_marks(image, pitch_range, x, y, center_y)
        if (bank != 0):
            image = self.rotate_image(image, bank)
        image = self.indicate_bank(image, x, y, bank, bank_range)
        compass = self.make_compass(azimuth)
        image_h, image_w, im_ch = image.shape
        compass_h, compass_w, compass_ch = compass.shape
        factor = (1.0 * self.height) / compass_h
        compass = cv2.resize(compass, None, fx=factor, fy=factor)
        image_all = np.hstack((image, compass))
        '''
        display = "Pitch:" + str(theta) + "    Bank:" + str(bank)+ "    Azimuth:" + str(azimuth)
        image = cv2.copyMakeBorder(image, 0, 100, 0, 0, cv2.BORDER_CONSTANT, value = (0, 0, 0))
        height, width, channels = image.shape
        factor = 1.25
        cv2.putText(image, display, (10, int(height - 35 * factor)), cv2.FONT_HERSHEY_SIMPLEX, factor, (255, 255, 255), 1)
        '''
        width_percent = 80
        height_percent = 80
        width = int(image.shape[0] * width_percent / 100)
        height = int(image.shape[1] * height_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return image
        # cv2.imshow("Display", image)


def main():
    dis = Display()
    phi = 0
    theta = 0
    psi = 0
    while (True):
        k = cv2.waitKey(1) & 0xFF

        """
        port_okunan = port.readline()[:-2].decode("utf-8")  # readline ile veriyi okuyup barçalıyoruz
        print("Mpu dan okunan X derecesi : {}".format(
            port_okunan))  # -"ascii"- format ile ekrana veriyi bastıroyruz aynı zamanda ise
        # decode diyerek parçalama işlemi yapıyoruz...
        """
        # array = []
        # for i in range(4):
        #     port_okunan_x = port.readline()[:-2].decode("utf-8") # readline ile veriyi okuyup barçalıyoruz
        #
        #     array.append(port_okunan_x)
        #
        # print("Mpu dan okunan: {}-{}".format(
        #     array[0],
        #     array[1]))  # format ile ekrana veriyi bastıroyruz aynı zamanda ise
        # # decode diyerek parçalama işlemi yapıyoruz...

        if k == ord('q'):
            break
        if k == ord('w'):
            theta += 18
        elif k == ord('s'):
            theta -= 18
        if k == ord('a'):
            phi -= 18
        if k == ord('d'):
            phi += 18
        if k == ord('n'):
            psi -= 18
        if k == ord('m'):
            psi += 18

        # try:
        #     if port.readline():
        #         print("girdi 0")
        #         if port.readline() != b'':
        #             print("girdi 1")
        #             jsonSerial = json.loads(port.readline().decode("utf-8"))
        #             print(jsonSerial)
        #
        #             phi = int(jsonSerial["x_eksen"])
        #             # phi =int(array[0])
        #             theta =int(jsonSerial["y_eksen"])
        #
        #             if(theta<=360 and theta>=200):
        #                 print("girdi 3")
        #                 theta=int(jsonSerial["y_eksen_asagi"])
        #             elif(theta<=160 and theta>=0):
        #                 print("girdi 4")
        #
        #                 theta=int(jsonSerial["y_eksen_yukari"])
        #             else :
        #                 theta=0
        #             # print(type(theta))
        #
        #             port.flush()
        #             cv2.destroyAllWindows()
        #             print("girdi 2")
        #
        #     # phi=0
        # except ValueError as val:
        #     print("hata" + str(val))
        #     pass
        # phi = int(15)
        # port.cancel_read()
        # 
        # phi, theta, psi=mpu.acceleration
        cv2.imshow("display",dis.make_image(phi, theta, psi))
        # # dis.make_image()
        # print(f"phi {phi} - theta {theta} - psi {psi}")



if __name__ == "__main__":
    main()
