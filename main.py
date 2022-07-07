from GarbageClassifier import GarbageClassifier
from CameraControl import Cam
from Controls import Controls


test_image_dir = r"test images/recyclable_003899_photo.jpg"
defaul_photo_dir = r"tmp"
class_names = ['cardboard-paper', 'metal-plastic-glass', 'organic', 'trash']
boxes_order = [2,4,1,3]
cam = Cam(defaul_photo_dir)
gc = GarbageClassifier()
controls = Controls()

def RunSmartBin():
    
    photo_dir = cam.getPhoto()
    photo_class = gc.test_model(photo_dir)
    print(photo_class)
    
    class_index = -1
    for index, elem in enumerate(class_names):
        if elem.find(photo_class) != -1:
            class_index = index
#     if class_index != -1:
#         controls.move_box(boxes_order[class_index])
    controls.move_box(0)

#controls.move_box(0)
RunSmartBin()

