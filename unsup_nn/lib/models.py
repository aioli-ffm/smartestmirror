import torch
import torch.nn as nn

class CAE(nn.Module):
    def __init__(self, batch_norm):
        super(CAE, self).__init__()

        self.batch_norm = batch_norm

        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, 8, stride=2, padding=1),
            nn.BatchNorm2d(64, eps=self.batch_norm),
            nn.ReLU(True),
            nn.Conv2d(64, 198, 8, stride=2, padding=1),
            nn.BatchNorm2d(198, eps=self.batch_norm),
            nn.ReLU(True),
            nn.Conv2d(198, 198, 5, stride=2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(198, 198, 5, stride=2),
            nn.BatchNorm2d(198, eps=self.batch_norm),
            nn.ReLU(True),
            nn.ConvTranspose2d(198, 64, 8, stride=2, padding=1),
            nn.BatchNorm2d(64, eps=self.batch_norm),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 3, 8, stride=2, padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


class VCAE(nn.Module):
    def __init__(self, batch_norm):
        super(VCAE, self).__init__()

        self.batch_norm = batch_norm

        self.conv1 = nn.Conv2d(3, 64, 8, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(64, eps=batch_norm)

        self.conv2 = nn.Conv2d(64, 128, 8, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(128, eps=batch_norm)

        self.conv31 = nn.Conv2d(128, 2, 5, stride=2)
        self.conv32 = nn.Conv2d(128, 2, 5, stride=2)

        self.conv4 = nn.ConvTranspose2d(2, 128, 5, stride=2)
        self.bn4 = nn.BatchNorm2d(128, eps=batch_norm)

        self.conv5 = nn.ConvTranspose2d(128, 64, 8, stride=2, padding=1)
        self.bn5 = nn.BatchNorm2d(64, eps=batch_norm)

        self.conv6 = nn.ConvTranspose2d(64, 3, 8, stride=2, padding=1)

        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def encode(self, x):
        h1 = self.relu(self.bn1(self.conv1(x)))
        h2 = self.relu(self.bn2(self.conv2(h1)))
        h31 = self.conv31(h2)
        h32 = self.conv32(h2)

        return h31, h32

    def reparameterize(self, mu, logvar):
        if self.training:
          std = logvar.mul(0.5).exp_()
          eps = torch.autograd.Variable(std.data.new(std.size()).normal_())
          return eps.mul(std).add_(mu)
        else:
          return mu

    def decode(self, z):
        h4 = self.relu(self.bn4(self.conv4(z)))
        h5 = self.relu(self.bn5(self.conv5(h4)))
        z = self.sigmoid(self.conv6(h5))

        return z

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar, z
