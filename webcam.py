import cv2
import matplotlib.pyplot as plt
import numpy as np

class webcam_gauge:
    """webcam_gauge class"""
    pass
    def __init__(self, filename ='e16hbdstand.jpg')->None:
        self.filename = filename
        self.img = cv2.imread(filename)
        if self.img is None :
            print('Cannot read the file :{}'.format(filename))
            raise ValueError
        self.img_gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.img_rev = cv2.bitwise_not(self.img_gray)

    def print(self):
        """print itself"""
        print('filename: {}'.format(self.filename))

    def show_img(self):
        """display the original figure."""
        img_RGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        plt.imshow(img_RGB)
        plt.show()

    def put_mask_circle(self,img,x1,y1,r):
        copied = img.copy()
        mask = np.zeros_like(copied)
        cv2.circle(mask,(x1,y1),r,color=(1,1,1),thickness=-1)
        copied = copied*mask
        return copied

    def calc_angle(self,x1,y1,x2,y2):
        if x2==x1 :
            return -np.pi/2.
        else:
            angle = np.arctan((y2-y1)/(x2-x1))
            return angle - np.pi
    
    def read_gauge(self,gauge : str):
        g = webcam_subgauge(gauge)
        x1,y1 = g.get_center()
        r = g.get_radius()
        copied = self.put_mask_circle(self.img_rev,x1,y1,r)
        copied2 = copied[y1-r:y1+r,x1-r:x1+r]

        lines = cv2.HoughLinesP(copied2,rho=1,
                                theta=np.pi/360,
                                threshold = 10,
                                minLineLength = 20,
                                maxLineGap = 20)
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(copied2,(x1,y1),(x2,y2),color=(120,120,120),thickness =1)
            angle = self.calc_angle(x1,y1,x2,y2)
            print ('angle {}'.format(angle))
            press = g.angle_pressure(angle)
            print ('pressure {}'.format(press))

        

        
##################################################################
#
##################################################################
class webcam_subgauge:
    """webcam_subgage stores information needed to image processing"""
    def __init__(self, gauge : str):
        if gauge == 'B' or gauge == "b" :
            self.center = 171,109
            self.radius = 16
            self.ticks = -2.86, -2.04, -1.12, -0.31
        elif gauge == "A" or gauge == 'a' :
            self.center = 96,101
            self.radius = 17
            self.ticks = 1.55-2*np, 2.61-2*np.pi, -2.65, -1.73
        else:
            print ('gauge identification invalid: {}'.format(gauge))
            raise ValueError
    def get_center(self):
        return self.center

    def get_radius(self):
        return self.radius

    def angle_pressure(self,angle):
        p = [0,5,10,15]
        if angle < self.ticks[0] or self.ticks[3] < angle:
            return -1
        return np.interp(angle,self.ticks,p)
    



