import torch
import torch.nn as nn

# image size doesn't matter as long as
# minimum size of images is 32 x 32.
# So far, best results in terms of accuracy vs. computation trade-off
# seem to be achieved at 96 x 96 patch size

class CAE(nn.Module):
    def __init__(self, batch_norm):
        super(CAE, self).__init__()

        self.batch_norm = batch_norm

        self.conv1 = nn.Conv2d(3, 32, 8, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32, eps=self.batch_norm)
        self.act1 = nn.ReLU(True)

        self.conv2 = nn.Conv2d(32, 7, 8, stride=2)

        self.dconv1 = nn.ConvTranspose2d(7, 32, 8, stride=2)
        self.dbn1 = nn.BatchNorm2d(32, eps=self.batch_norm)
        self.dact1 = nn.ReLU(True)

        self.dconv2 = nn.ConvTranspose2d(32, 3, 8, stride=2, padding=1)

        self.dact2 = nn.Sigmoid()

    def encode(self, x):
        h1 = self.act1(self.bn1(self.conv1(x)))
        h2 = self.conv2(h1)

        return h2

    def decode(self, x):
        dh1 = self.dact1(self.dbn1(self.dconv1(x)))
        dh2 = self.dact2(self.dconv2(dh1))
        return dh2

    def forward(self, x):
        x = self.encode(x)
        x = self.decode(x)
        return x


class VCAE(nn.Module):
    # TODO: Doesn't seem to work very well yet!
    def __init__(self, batch_norm):
        super(VCAE, self).__init__()

        self.batch_norm = batch_norm

        self.conv1 = nn.Conv2d(3, 32, 8, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32, eps=self.batch_norm)

        self.conv21 = nn.Conv2d(32, 7, 8, stride=2)
        self.conv22 = nn.Conv2d(32, 7, 8, stride=2)

        self.dconv1 = nn.ConvTranspose2d(7, 32, 8, stride=2)
        self.dbn1 = nn.BatchNorm2d(32, eps=self.batch_norm)

        self.dconv2 = nn.ConvTranspose2d(32, 3, 8, stride=2, padding=1)

        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def encode(self, x):
        h1 = self.relu(self.bn1(self.conv1(x)))
        h21 = self.conv21(h1)
        h22 = self.conv22(h1)

        return h21, h22

    def reparameterize(self, mu, logvar):
        if self.training:
            std = logvar.mul(0.5).exp_()
            eps = torch.autograd.Variable(std.data.new(std.size()).normal_())
            return eps.mul(std).add_(mu)
        else:
            return mu

    def decode(self, z):
        dh1 = self.relu(self.dbn1(self.dconv1(z)))
        z = self.sigmoid(self.dconv2(dh1))

        return z

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)

        return self.decode(z), mu, logvar, z
