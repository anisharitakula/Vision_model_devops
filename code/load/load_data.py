import torch
import numpy as np
import torchvision


def worker_init_fn(id):
    return np.random.seed(id)

#download CIFAR 10 data
def data_loading():
    torch.manual_seed(0)
    trainset=torchvision.datasets.CIFAR10(root='./data',train=True,download=True,
                                        transform=torchvision.transforms.ToTensor(),)

    trainloader= torch.utils.data.DataLoader(trainset,batch_size=4,shuffle=True,num_workers=2,
                                            worker_init_fn = worker_init_fn)
    return trainloader
