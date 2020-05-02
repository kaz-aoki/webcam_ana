import cv2
import matplotlib.pyplot as plt

class webcam_gauge:
    """webcam_gauge class"""
    pass
    def __init__(self, filename ='e16hbdstand.jpg')->None:
        self.filename = filename
        self.img = cv2.imread(filename)
        self.img_gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.img_bin = cv2.bitwise_not(self.img_gray)
    def print(self):
        """print itself"""
        print('filename: {}'.format(self.filename))
    def show_img(self):
        img_RGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        plt.imshow(img_RGB)



    
