import torch
import torch.nn as nn
import torch.nn.functional as F

class SpatioTemporalModel(nn.Module):
    def _init_(self, input_size, output_size, d_model, nhead, num_encoder_layers, num_decoder_layers, dropout_rate=0.1):
        super(SpatioTemporalModel, self)._init_()

        # Convolutional layers
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
#         self.bn1 = nn.BatchNorm2d(16)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
#         self.bn2 = nn.BatchNorm2d(32)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Calculate the flattened size after convolutional layers
        self.flattened_size = (input_size[1] // 4) * (input_size[2] // 4) * 32  # Dividing by 4 due to two pooling layers
        # Bottleneck layer to adjust the dimensionality to d_model
        self.bottleneck = nn.Linear(self.flattened_size, d_model)

        # Transformer layers
        self.transformer = nn.Transformer(
            d_model=d_model,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dropout=dropout_rate
        )

        # Linear layer for prediction
        self.fc1 = nn.Linear(d_model, d_model//2)
        self.fc2 = nn.Linear(d_model//2, d_model//4)
        self.fc3 = nn.Linear(d_model//4, output_size)

        self.fcpred2 = nn.Linear(output_size, output_size)
        self.fcpred3 = nn.Linear(output_size, output_size)
        self.fcpred4 = nn.Linear(output_size, output_size)
        self.fcpred5 = nn.Linear(output_size, output_size)

    def forward(self, x):
        # Convolutional layers
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))

        # Flattening
        x = x.view(x.size(0), -1)
        x = self.bottleneck(x)

        # Transformer layers
        x = x.unsqueeze(0)
        x = self.transformer(x, x)
        x = x.squeeze(0)

        # Linear layer for prediction
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x1 = self.fc3(x)
        x2 = self.fcpred2(x1)
        x3 = self.fcpred3(x2)
        x4 = self.fcpred4(x3)
        x5 = self.fcpred5(x4)

        return x1, x2, x3, x4, x5

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_run_model():
    return torch.load('models/runmodel.pth', map_location=device)

def load_dwell_model():
    return torch.load('models/dwellModel.pth', map_location=device)