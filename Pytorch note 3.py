# -*- coding: utf-8 -*-
"""02_pytorch_neural_network_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-AeG41fiwF65bGT4zlHV6dch_5Xr_e-v
"""

#Binary Classification

"""
Classification that involves either thing a or thing b (classifies between 2 things)
Problem of predicting whether something is one thing or another (there can be multiple things as option)

"""

#Multiclass Classification

"""
Classification that involves more than 2 things, is it this that or the other? (classifies anything >2)
"""

#Multilabel Classification

"""
Multilabel,many labels of deep learning

Example:
could read text and bring out multiple categories from them

"""

#Images to tensors (Classification inputs and outputs)
"""
-Taking width and height and color channels of images, and thats the input
-Prediciton probabilities
  -There will be a table and within it you can have 0 or 1 or 0-1
  -Then it will give the answer between the different choices

  Dog | Cat
  0     1     ACTUAL ANSWER: Cat
  1     0     ACTUAL ANSWER: DOG
  0     1     ACTUAL ANSWER: DOG

What gets represented as a tensor:
  -batch_size
    -How many images to look at, at a time
  -color_channels
  -width
  -height
There is debate on the ordering of these


"""

import torch
from torch import nn
import sklearn
from sklearn.datasets import make_circles

#Make 1000 Samples
n_samples = 1000

#create circles

X,y = make_circles(n_samples,
                   noise = 0.03,
                   random_state = 42)

len(X), len(y)

print(f"first 5 samples of X: {X[:5]}")
print(f"first 5 samples of y: {y[:5]}")

#Make DataFrame of cricle data
import pandas as pd
circles = pd.DataFrame({"X1": X[:,0],
                        "X2" : X[:,1],
                        "label": y})
circles.head(10)

#Visualize
import matplotlib.pyplot as plt
plt.scatter(x= X[:,0],
            y= X[:,1],
            c= y,
            cmap = plt.cm.RdYlBu)

#Check input and output shapes
X.shape, y.shape

#We want to make it into PyTorch tensors, because we are working with pytorch

X_sample = X[0]
y_sample = y[0]

print(f"Values for one sample of X:{X_sample} and same for y {y_sample}")
print(f"Shapes for one sample of X: {X_sample.shape} and same for y {y_sample.shape}")

#Two features of x trying to predict one sample of y

##Turns data into tensors and create train and test splits

#Turn data into tensors
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)

X[:5], y[:5]

#Split data into training and test sets

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size = 0.2,  #0.2 = 20% of data will be test & 80% will be train
                                                    random_state = 42)

len(X_train), len(X_test), len(y_train), len(y_test)

#Lets build a classification model

"""
We want:

1. Setup device agnostic code, code will run on an accelerator
2. Contstruct a model (by suubclassing nn.Module)
3. Define a loss function and optimizer
4. Create a training and test loop

"""

from torch import nn

#Make device agnostic code

device = 'cuda' if torch.cuda.is_available() else 'cpu'
device

#now we've setup agnostic code lets create model
"""

1. Subclasses nn.module
2. Create 2 nn.Linear(), layers that are capable of handling shapes of our data
3. Define forward method, method that outlines forward pass
4. Instatiate an instance of our model class and send it to target device

"""

#1 Construct model nn.Module
class CircleModelV0(nn.Module):
  def __init__(self):
    super().__init__()
    #2 Create 2 nn.linear layers
    self.layer_1 = nn.Linear(in_features = 2, out_features = 5) #takes in 2 features and upscales to 5 features #rule of thumb in features, more oppurtunity to learn pattern in data
    self.layer_2 = nn.Linear(in_features = 5, out_features = 1) #takes in 5 features from layer 1 and outputs 1
  """
    self.two_linear_layers = nn.Sequential(
    nn.Linear(in_features=2, out_features=5),
    nn.Linear(in_features=5, out_features=1)
)"""

  #3 define forward method  that outlines forward pass
  def forward(self, x):
    return self.layer_2(self.layer_1(x)) #x-> layer_1 -> layer2 -> output
    #return two_linear_layers(x)

#4. Instantiate an instance of our model class and send it to target device
model_0 = CircleModelV0().to(device)
model_0

"""
#Lets replicate using nn.Sequential()
model_0 = nn.Sequential(
    nn.Linear(in_features=2, out_features=5),
    nn.Linear(in_features=5, out_features=1)
).to(device)
model_0
"""

#Make predictions
with torch.inference_mode():
  untrained_preds = model_0(X_test.to(device))
print(f"Length of predictions {len(untrained_preds)}, Shape: {untrained_preds.shape}")
print(f"Length of test samples: {len(X_test)}, Shape: {X_test.shape}")
print(f"\nFirst 10 predictions:\n{untrained_preds[:10]}")
print(f"\nFirst 10 labels:\n {y_test[:10]}")

#Setting up loss function and optimizer

"""
Previously used regression, with classification it won't work.

You should use binary crossentropy or categorical cross entropy
"""

loss_fn = nn.BCEWithLogitsLoss() #Sigmoid activation function is built into this
#loss_fn = nn.BCELoss = requires inputs to have gone through sigmoid activation prior to input to BCELoss

optimizer = torch.optim.SGD(params = model_0.parameters(),
                            lr = 0.1)

#Calculate accuracy - out of 100 examples, what percantage is correct?
def accuracy_fn(y_true, y_pred):
  correct = torch.eq(y_true, y_pred).sum().item()
  acc = (correct/len(y_pred))*100
  return acc

#Train model

"""
Forward pass
Calculate Loss
Optimize zero grad
Loss Backward
Optimizer step
"""

#Going from raw logits -> prediction probaiblities -> prediction labels
"""
The model outputs are going to be raw logits

We can cover the logits into prediction probabilities by passing them to
some kind of activation function (sigmoid, BCE, softmax for multiclass classification)
Sigmoid is good for Binary and softmax is good for multiclass classification

Then model prediction probaiblities can be converted to prediction labels by either rounding them or taking the argmax()
"""

#View first 5 outputs (of forward pass on test data)
model_0.eval()
with torch.inference_mode():
  y_logits = model_0(X_test.to(device))[:5]
y_logits

#use sigmoid activation on model logits to turn them into prediction probabilities
y_pred_probs = torch.sigmoid(y_logits)
y_pred_probs

#For the prediction probaiblity values, a range style rounding must be performed on them
"""
y_pred_probs >= 0.5, y = 1
y_pred_probs < 0.5, y = 0
"""

#Find predicted labels
y_preds = torch.round(y_pred_probs)

#in FUll (logits -> pred probs-> pred labels)
y_pred_labels = torch.round(torch.sigmoid(model_0(X_test.to(device))[:5]))

#Check for equality
print(torch.eq(y_preds.squeeze(), y_pred_labels))

#Get rid of extra dimension
y_preds.squeeze()

y_test[:5]

#Building a training and testing loop
torch.manual_seed(42)
torch.cuda.manual_seed(42)

#set epochs
epochs = 100

#Put data tp target device
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

#Build training and evaluation loop
for epoch in range(epochs):
  #Training
  model_0.train()

  #Forward pass
  y_logits = model_0(X_train).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) #turn logits -> pred pobs -> pred labels

  #Calculate loss/accuracy
  """
  loss = loss_fn(torch.sigmoid(y_logits, #nn.BCELoss expects prediction probabilities as inputs
                               y_train)) """
  loss = loss_fn(y_logits, #nn.BCEWithLogitsLoss expects raw logits as input
                 y_train)
  acc =accuracy_fn(y_true=y_train,
                   y_pred=y_pred)

  #Optimizer Zero grad
  optimizer.zero_grad()

  #4Loss backward (backpropagation)
  loss.backward()

  #Optimizer step (gradient descent)
  optimizer.step()

  #Testing
  model_0.eval()
  with torch.inference_mode():
    #forward pass
    test_logits = model_0(X_test).squeeze()
    test_pred = torch.round(torch.sigmoid(test_logits))

    #Caculate test loss/acc
    test_loss = loss_fn(test_logits,
                        y_test)
    test_acc = accuracy_fn(y_true=y_test,
                           y_pred=test_pred)

#Print whats happening
  if epoch % 10 == 0:
    print(f"Epoch: {epoch} | Loss: {loss:.5f}, Acc; {acc:.2f}% | Test loss: {test_loss:.5f}, Test acc: {test_acc:.2f}")

#Make predictions and evaluate model

"""
Models test acc is about 50/50, so its just guessing,
to inspect it we need to make predictions visual

Import a function called plot_decision_boundary()

"""

import requests
from pathlib import Path

#Download helper functions from learn PyTorch repo (if not already downloaded)

if Path("helper_functions.py").is_file():
  print("helper_functions.py already exists, skipping download")
else:
  print("Download help_functions.py")
  request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py")
  with open("helper_functions.py","wb") as f:
    f.write(request.content)

from helper_functions import plot_predictions, plot_decision_boundary

#plot decision boundary of model
plt.figure(figsize = (12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_0, X_train, y_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_0, X_test, y_test)

#Improving model

"""
Add more layers, give more chances to learn about patterns in data
Add more hidden units
Fit for longer
Changing activation functions
change learning rate
change loss function

These options are all from a models perspective because they deal directly with the model rather than the data

Try improving model by:
adding more hidden units: 5-> 10
Increase number of layers 2-> 3
increase number of layers 100-> 1000
"""
class CircleModelV1(nn.Module):
  def __init__(self):
    super().__init__()
    self.layer_1 = nn.Linear(in_features =2, out_features = 10)
    self.layer_2 = nn.Linear(in_features = 10, out_features = 10)
    self.layer_3 = nn.Linear(in_features = 10, out_features = 1)

  def forward(self, x):
    """
    z = self.layer_1(x)
    z = self.layer_2(z)
    z = self.layer_3(z)

    return z
    This is the same as the return statement below
    """
    return self.layer(self.layer_2(self.layer_1(x))) #This makes things faster behind the scenes


model_1 = CircleModelV1().to(device)

model_1

#Not working I don't know why
"""
#Create a loss function
loss_fn = nn.BCEWithLogitsLoss()

#Create an optimizer
optimizer = torch.optim.SGD(params=model_1.parameters(),
                               lr = 0.1)

#Write a training and evaluation loop for model_1
torch.manual_seed(42)
torch.cuda.manual_seed(42)

#Training longer
epochs = 1000

#Put data on target device
X_train_V1, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

for epoch in range(epochs):
  #training
  model_1.train()
  #Forward pass
  y_logits = model_1(X_train_V1).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) #logits -> pred probabilities -> predictions

  #Calculate loss
  loss = loss_fn(y_logits, y_train)
  acc = accuracy_fn(y_true = y_train,
                    y_pred = y_pred)

  #3 optimizer zero grad
  optimizer.zero_grad()

  #4 Loss backward (backwardpropogation)
  loss.backward()

  #5 Optimizer step (gradient descent)
  optimizer.step()

  #Testing
  model_1.eval()
  with torch.inference_mode():
    #1 forward pass
    test_logits = model_1(X_test).squeeze()
    test_pred = torch.round(torch.sigmoid(test_logits))
    #Calculate loss
    test_loss = loss_fn(test_logits,
                           y_test)
    test_acc = accuracy_fn(y_true = y_test,
                           y_pred = test_pred)

  #Print out whats happening
  if epoch % 100 == 0:
    print(f"Epoch {epoch} | Loss: {loss:.5f}, Acc: {acc:.2f} | Test loss {test_loss:.5f}, Test acc: {test_acc:.2f}%")
 """

"""
This is a model used for linear regression, and our data is a circle so this won't ever have worked no matter what experimentation is done

So we will fix this using non-linear functions
"""

#Non-Linearity

"""
What patterns could be drawn if given infinite amount of straight and non-straight lines

In machine learning linear, and non-linear functions?
"""
#Recreating non-linear data

#make and plot data
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
n_samples = 1000

X, y = make_circles(n_samples,
                    noise=0.03,
                    random_state = 42)

plt.scatter(X[:, 0], X[:, 1], c=y, cmap =plt.cm.RdYlBu);

#convert data to tensors and then to train and test splits

from sklearn.model_selection import train_test_split

#turn data into tensors
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)

#Split into train and test sets

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size = 0.2,
                                                    random_state =42)

X_train[:5], y_train[:5]

#Building a model with non-linearity

"""

"""
class CircleModelV2(nn.Module):
  def __init__(self):
    super().__init__()
    self.layer_1 = nn.Linear(in_features = 2, out_features = 10)
    self.layer_2 = nn.Linear(in_features = 10, out_features = 10)
    self.layer_3 = nn.Linear(in_features = 10, out_features = 1)
    self.relu = nn.ReLU() #Non-Linear activation function
    #self.sigmoid = nn.Sigmoid()

  def forward(self,x):
    return self.layer_3(self.relu(self.layer_2(self.relu(self.layer_1(x)))))

model_2 = CircleModelV2().to(device)
model_2

#Setup loss and optimizer

loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model_2.parameters(),
                            lr = 0.1)

#Training model with non-linearity


#Random seed
torch.manual_seed(42)
torch.cuda.manual_seed(42)

#Put all data on target device
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

#Loop data
epochs = 1000

for epoch in range(epochs):
  #train
  model_2.train()

  #1 forward pass
  y_logits = model_2(X_train).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) #logits -> prediction prob -> prediction labels

  #calculate loss
  loss = loss_fn(y_logits, y_train) #BCEWithLogitsLoss(takesi nlogits as first input)
  acc = accuracy_fn(y_true = y_train,
                    y_pred = y_pred)

  #Optimizer
  optimizer.zero_grad()

  #loss backward
  loss.backward()

  #Step the optimizer
  optimizer.step()

  #testing
  model_2.eval()
  with torch.inference_mode():
    test_logits = model_2(X_test).squeeze()
    test_pred = torch.round(torch.sigmoid(test_logits))

    test_loss = loss_fn(test_logits, y_test)
    test_acc = accuracy_fn(y_true = y_test,
                           y_pred = test_pred)

  #print whats happening
  if epoch % 100 == 0:
    print(f"Epoch {epoch} | Loss: {loss:.4f}, Acc: {acc:.2f} | Test loss {test_loss:.4f}, Test acc: {test_acc:.2f}%")

#Evaluating

#make predictions
model_2.eval()
with torch.inference_mode():
  y_preds = torch.round(torch.sigmoid(model_2(X_test))).squeeze()
y_preds[:10], y_test[:10]

#plot decision boundaries
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_2, X_train, y_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_2, X_test, y_test)

from sklearn.datasets import make_blobs

NUM_CLASSES = 4
NUM_FEATURES = 2
RANDOM_SEED = 42

#Create multiclass bdata
X_blob, y_blob = make_blobs(n_samples = 1000,
                            n_features = NUM_FEATURES,
                            centers = NUM_CLASSES,
                            cluster_std=1.5, #mix clusters up a bit
                            random_state = RANDOM_SEED)

#Turn data into tensors
X_blob = torch.from_numpy(X_blob).type(torch.float)
y_block = torch.from_numpy(y_blob).type(torch.float)

#Split into train and test
X_blob_train, X_blob_test, y_blob_train, y_blob_test = train_test_split(X_blob,
                                                                        y_blob,
                                                                        test_size=0.2,
                                                                        random_state=RANDOM_SEED)
#Plot data
plt.figure(figsize=(10,7))
plt.scatter(X_blob[:,0], X_blob[:,1], c=y_blob, cmap=plt.cm.RdYlBu)

#Building multi-class classification model in Pytorch
device = 'cuda' if torch.cuda.is_available() else 'cpu'

#Build multi-class classification model
class BlobModel(nn.Module):
  def __init__(self, input_features, output_features, hidden_units=8):
    #Initializes multi-class classification model

    super().__init__()
    self.linear_layer_stack = nn.Sequential(
        nn.Linear(in_features=input_features, out_features=hidden_units),
        nn.ReLU(),
        nn.Linear(in_features=hidden_units, out_features=hidden_units),
        nn.ReLU(),
        nn.Linear(in_features=hidden_units, out_features=output_features)
    )

    def forward(self, x):
      return self.linear_layer_stack(x)

#Create instance of BlobModel
model_4 = BlobModel(input_features= 2,
                    output_features=10,
                    hidden_units=8)
model_4

X_train.shape, y_blob_train[:5]

#Create a loss function for a multi-class classification model

"""
We're gonna use cross entropy loss
"""

loss_fn = nn.CrossEntropyLoss()

#Optimizer
optimizer = torch.optim.SGD(params=model_4.parameters(),
                            lr=0.1)

#Predictions predictions
model_4.eval()
with torch.inference_mode():

  y_preds = model_4(X_blob_test.to(device))
y_preds[:10]

next(model_4.parameters()).device