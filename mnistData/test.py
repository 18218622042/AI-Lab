import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose([transforms.ToTensor(),])
#测试集
testset = torchvision.datasets.MNIST(root='/Data', train=False,download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=1,shuffle=False, num_workers=2)

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
convNet = torch.load('/Data/model/Wed May  6 10:29:49 2020_mnist_0.9909.pkl')  #载入模型

def test(model,testloader):
	model.eval()
	r = 0
	for i, data in enumerate(testloader, 0):
	    imgs, labels = data
	    outputs = model(imgs)
	    r += (torch.max(outputs, 1)[1] == labels).sum()
	print('识别率:%s%%' % str(int(r)/100))
	return r

test(convNet,testloader)

