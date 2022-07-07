import cv2


class Cam:
    def __init__(self, default_image_dir):
        self.cap = cv2.VideoCapture(0)
        self.default_image_dir = default_image_dir + "/testImage.png"

    def __del__(self):
        del(self.cap)
        
    def getPhoto(self, image_dir_=None):
        _, image = self.cap.read()
        if image_dir_ is None:
            image_dir = self.default_image_dir
        else:
            image_dir = image_dir_ + "/testImage.png"
        cv2.imwrite(image_dir, image)
        return image_dir
