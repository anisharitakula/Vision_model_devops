import torch
import torch.optim as optim
import os

#import torchvision.transforms as transforms
import torch.nn.functional as F

from model import Net
from azureml.core import Run
from load.load_data import data_loading

#ADDITIONAL CODE: get AML run from the current context
run=Run.get_context()


def train_data():
    torch.manual_seed(0)
    trainloader=data_loading()
    

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

    # Define the path where you want to save the model
    model_name = "pytorch_model.pth"

    # Save the PyTorch model
    torch.save(net.state_dict(), model_name)

    # Upload the model file explicitly into artifacts
    run.upload_file(name="./outputs/" + model_name, path_or_stream=model_name)
    print("Uploaded the model {} to experiment {}".format(model_name, run.experiment.name))

    print("Following files are uploaded ")
    print(run.get_file_names())
    run.complete()

if __name__=="__main__":
    train_data()
    