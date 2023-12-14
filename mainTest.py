import cv2
from keras.models import load_model
from PIL import Image
import numpy as np

model=load_model('skincancer10epocs.h5')
# model=load_model('skin cancer model.pkl')
image=cv2.imread('/home/binam/Desktop/project/newproject/scds/dataset/melanoma_cancer_dataset/test/benign/melanoma_9610.jpg')

img=Image.fromarray(image)
img=img.resize((64,64))

img=np.array(img)
input_img=np.expand_dims(img,axis=0)

result = model.predict(input_img)
print(result)