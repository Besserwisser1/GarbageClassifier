import torch
import torch.nn as nn
from torchvision import models, transforms
import os
from PIL import Image
import numpy as np
#import matplotlib.pyplot as plt
import os.path


class GarbageClassifier:
  def __init__(self, modelDir=None, dictDir=None, class_names=None):
    self.device = torch.device("cpu")
    if class_names is None:
        self.class_names = ['cardboard-paper', 'metal-plastic-glass', 'organic', 'trash']
    else:
        self.class_names = class_names
    self.output_ftrs = len(self.class_names)
    if class_names is None:
        self.dictDir = r'models/resnet101/weights/resnet101_ft.pt'
    else:
        self.dictDir = dictDir
    if modelDir is None:
        self.modelDir = r"models/resnet101/model/resnet101_ft_oldtorch.pth"
    else:
        self.modelDir = modelDir
    self.modelURL = r"https://download.pytorch.org"
    self.model_ft = None
    # self.test_image_dir = ''

  def pil_loader(self, path):
    with open(path, 'rb') as f:
      img = Image.open(f)
      return img.convert('RGB')

  def load_model(self):
    try:
      if self.checkNet() == False:
        raise Exception("No internet connection")
      self.model_ft = models.resnet101(pretrained=True)
      num_ftrs = self.model_ft.fc.in_features
      self.model_ft.fc = nn.Sequential(
        nn.Flatten(),
        nn.Linear(num_ftrs, 512),
        nn.Dropout(0.5),
        nn.Linear(512, self.output_ftrs)
      )
      self.model_ft = self.model_ft.to(self.device)
      if os.path.exists(self.dictDir):
        self.model_ft.load_state_dict(torch.load(self.dictDir, map_location=self.device))
    except OSError as e:
      print("Check weights directory, exception:\n" + str(e))
    except Exception as e:
      print("Exception:\n")
    # finally:
    #   return

  def init_model(self, source='local'):
    try:
      if source == 'local':
        if os.path.isfile(self.modelDir):
          self.model_ft = torch.load(self.modelDir, map_location=self.device)
        else:
          print("Model does not exist\nStarted loading model")
          self.load_model()
      elif source == 'internet':
        self.load_model()
    except Exception as e:
      print("Exception:\n")

  def run_model(self, img):
    preprocess = transforms.Compose([
      transforms.Resize((256,256)),
      # transforms.CenterCrop(224),
      transforms.Grayscale(3),
      transforms.ToTensor(),
      transforms.Normalize(mean=[0.5,], std=[0.5,])
    ])
    input = preprocess(img).to(self.device)

    # self.imshow(input)
    res = self.model_ft(input[None, ...])
    return res

  def test_model(self, test_image_dir):
    self.init_model()
    image = self.pil_loader(test_image_dir)
    # fig = plt.figure()
    # plot = plt.imshow(image)
    # plt.show()

    out, preds = torch.max(self.run_model(image), 1)
#     print(self.run_model(image))
#     print(preds)
#     print(out)
    return self.class_names[preds]

#   def output_img(self, img):
#     fig = plt.figure()
#     ax = fig.subplot(111)
#     plot = plt.imshow(img)
#     tens = self.run_model(self, img)

#   def imshow(self, inp, title=None):
#     """Imshow for Tensor."""
#     inp = inp.numpy().transpose((1, 2, 0))
#     mean = np.array([0.5,])
#     std = np.array([0.5, ])
#     inp = std * inp + mean
#     inp = np.clip(inp, 0, 1)
#     plt.imshow(inp)
#     if title is not None:
#       plt.title(title)
#     # plt.show()


  def checkNet(self):
    import requests
    try:
        requests.head("http://www.google.com/", timeout=1)
        return True
    except requests.ConnectionError:
        return False

