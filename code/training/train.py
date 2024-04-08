import torch
import torch.optim as optim
import os

#import torchvision.transforms as transforms
import torch.nn.functional as F
import sys
sys.path.append('/code/training')

from model import Net
from azureml.core import Run
import load_data

#ADDITIONAL CODE: get AML run from the current context
run=Run.get_context()


def train_data():
    torch.manual_seed(0)
    trainloader=load_data.data_loading()
    

    net=Net()
    criterion=torch.nn.CrossEntropyLoss()
    lr=0.001
    optimizer=optim.SGD(net.parameters(),lr=lr,momentum=0.9)
    #ADDITIONAL CODE: log loss metric to AML
    run.log('learning_rate',lr)

    epoch_batch_loss=[]
    #train the network
    for epoch in range(2):

        running_loss=0.0
        for i,data in enumerate(trainloader,0):
            #unpack the data
            inputs, labels=data

            #Zero the parameter gradients
            optimizer.zero_grad()

            #Forward + Backward + Optimize
            outputs=net(inputs)
            loss= criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            #print statistics
            running_loss+=loss.item()
            if i%2000==1999:
                loss=running_loss/2000
                #ADDITIONAL CODE: log loss metric to AML
                run.log('loss',loss)
                print(f"epoch={epoch+1},batch={i+1:5}: loss {loss:.2f}")
                running_loss=0.0
                epoch_batch_loss.append([epoch,loss])
    print(f"Finished training")
    #print(epoch_batch_loss)

    #Save model state
    #os.makedirs('./models', exist_ok=True)
    #torch.save(net.state_dict(),'./models/model_1.pth')
    
if __name__=="__main__":
    print(sys.path)
    train_data()
    