import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv1d(in_channels=in_channels, out_channels=out_channels, **kwargs)
        self.gelu = nn.GELU()
        # self.bn = nn.BatchNorm1d(out_channels)

    def forward(self, x):
        return self.gelu(self.conv(x))


class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        # input_size batch_size,1,23
        self.conv1 = ConvBlock(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=0)
        self.conv2 = ConvBlock(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=0)
        self.conv3 = ConvBlock(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=0)
        self.conv4 = ConvBlock(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=0)
        # batch_size,128,16
        self.lstm1 = nn.LSTM(input_size=3, hidden_size=48, num_layers=2, batch_first=True)  # 11/4
        # self.gru1 = nn.GRU(input_size=3, hidden_size=48,
        #                    num_layers=2, batch_first=True)
        self.maxpool = nn.MaxPool1d(kernel_size=2, ceil_mode=True)
        self.avgpool = nn.AvgPool1d(kernel_size=2, ceil_mode=True)
        # self.fc1 = nn.Linear(49152, 256)
        self.fc1 = nn.Linear(6144, 128)
        # self.fc2 = nn.Linear(256, 8)
        self.fc2 = nn.Linear(128, 8)
        self.softmax = nn.Softmax(dim=1)
        self.dropout1 = nn.Dropout(p=0.25)
        self.dropout2 = nn.Dropout(p=0.5)
        self.gelu = nn.GELU()

    def forward(self, x):
        batch_size = x.size(0)
        x = self.conv1(x)
        x = self.conv2(x)

        x = self.maxpool(x)

        x = self.conv3(x)
        x = self.conv4(x)

        x = self.maxpool(x)

        out, (h, c) = self.lstm1(x)
        # out, h = self.gru1(x)
        # Flatten()
        out = out.contiguous().view(batch_size, -1)

        x = self.dropout1(out)
        x = self.fc1(x)
        # x = self.gelu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        # x = self.gelu(x)
        out = self.softmax(x)
        return out
