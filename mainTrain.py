import cv2
import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import normalize
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense
from keras.utils import to_categorical

image_directory = 'dataset/melanoma_cancer_dataset/train'
no_cancer_images = os.listdir(os.path.join(image_directory, 'benign'))
yes_cancer_images = os.listdir(os.path.join(image_directory, 'malignant'))

dataset = []
label = []
Input_size=64


for image_name in no_cancer_images:
    if image_name.endswith('.jpg'):
        image = cv2.imread(os.path.join(image_directory, 'benign', image_name))
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = image.resize((Input_size, Input_size))
        dataset.append(np.array(image))
        label.append(0)

for image_name in yes_cancer_images:
    if image_name.endswith('.jpg'):
        image = cv2.imread(os.path.join(image_directory, 'malignant', image_name))
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = image.resize((Input_size, Input_size))
        dataset.append(np.array(image))
        label.append(1)

# print(len(dataset))
# print(len(label))

dataset=np.array(dataset)
label=np.array(label)

x_train, x_test, y_train, y_test = train_test_split(dataset,label,test_size=0.2,random_state=0)
# Reshape=(n,image_width, image_height, n_channel)

# print(x_train.shape)
# print(y_train.shape)

# print(x_test.shape)
# print(y_test.shape)

x_train=normalize(x_train,axis=1)
x_test=normalize(x_test,axis=1)


# y_train=to_categorical( y_train,num_classes=2)
# y_test=to_categorical( y_train,num_classes=2)

# Model Bulding
model= Sequential()

model.add(Conv2D(32,(3,3),input_shape=(Input_size,Input_size,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3),kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3),kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])


# Binary CrossEntropy =1,sigmoid
# cross entropy =1, softmax
class_weights = {0: 1.0, 1: 2.0}  # Adjust the weights as needed
history = model.fit(x_train, y_train, 
                    batch_size=16, 
                    verbose=1, 
                    epochs=20, 
                    validation_data=(x_test, y_test), 
                    shuffle=False,
                    class_weight=class_weights)

print("Training loss:", history.history['loss'])
print("Training accuracy:", history.history['accuracy'])
print("Validation loss:", history.history['val_loss'])
print("Validation accuracy:", history.history['val_accuracy'])

model.save('skincancer10epocs.h5')

# # # Assuming the model has been trained and saved
# model = keras.models.load_model('skincancer10epocs.h5')

# # Evaluate the model on the test set
# eval_results = model.evaluate(x_test, y_test, verbose=1)

# # Print the evaluation results
# print("Test Loss:", eval_results[0])
# print("Test Accuracy:", eval_results[1])

# # Make predictions on the test set
# y_pred = model.predict(x_test)

# # Assuming binary classification, you can convert probabilities to binary predictions
# y_pred_binary = (y_pred > 0.5).astype(int)

# # Importing scikit-learn for additional evaluation metrics
# from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# # Print classification report and confusion matrix
# print("Classification Report:\n", classification_report(y_test, y_pred_binary))
# print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_binary))

# # Print ROC-AUC score
# roc_auc = roc_auc_score(y_test, y_pred)
# print("ROC-AUC Score:", roc_auc)

# # 