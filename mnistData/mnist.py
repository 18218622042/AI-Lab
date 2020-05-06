import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import time

transform = transforms.Compose([transforms.ToTensor(),])

#训练集
trainset = torchvision.datasets.MNIST(root='/Data', train=True,download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,shuffle=True, num_workers=2)

#测试集
testset = torchvision.datasets.MNIST(root='/Data', train=False,download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,shuffle=False, num_workers=2)

class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=10, kernel_size=3)
        self.conv2 = nn.Conv2d(in_channels=10, out_channels=32, kernel_size=3)
        self.fc1 = nn.Linear(in_features=12 * 12 * 32, out_features=100)  
        self.fc2 = nn.Linear(in_features=100, out_features=10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, (2,2))
        x = x.view(x.size(0),-1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = F.log_softmax(x, dim=1)
        return x

convNet = ConvNet()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(convNet.parameters(), lr=0.001, momentum=0.9)



def train(model,trainloader,optimizer,epoch):
	model.train()
	running_loss = 0.0
	for i, data in enumerate(trainloader, 0):
	    imgs, labels = data
	    optimizer.zero_grad() 
	    outputs = model(imgs)
	    loss = criterion(outputs, labels)
	    loss.backward()
	    optimizer.step()
	    running_loss += loss.item()
	print(epoch,running_loss)
	

def test(model,testloader):
	model.eval()
	r = 0
	for i, data in enumerate(testloader, 0):
	    imgs, labels = data
	    outputs = model(imgs)
	    r += (torch.max(outputs, 1)[1] == labels).sum()
	print(int(r)/10000)
	return r

r = 0
for epoch in range(1, 51):
    train(convNet,trainloader,optimizer,epoch)
    r = test(convNet,testloader)

filename = '/Data/model/' + time.ctime() + ('_mnist_%s.pkl' % str(int(r)/10000))

#保存模型
torch.save(convNet, filename)  
