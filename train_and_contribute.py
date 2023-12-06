import torch
import torch.nn as nn
import torch.optim as optim
from load_data import load_data
from train_model import train_model
import os


class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)


def train_and_contribute(miner_id, zip_file_path, folder):
    # Simulate loading data from the processed zip file
    data_loader = load_data(zip_file_path)

    # Initialize the model
    model = SimpleModel()

    # Train the model
    train_model(model, data_loader)

    # Check if gradients are not None
    if any(param.grad is None for param in model.parameters()):
        print(f"Miner {miner_id} failed to compute gradients.")
        return

    # Get model gradients
    destination_folder = "./Destination"
    gradients = [param.grad.data.numpy().tolist() for param in model.parameters()]
    gradients_folder = os.path.join(destination_folder, folder)
    os.makedirs(gradients_folder, exist_ok=True)

    # Save gradient in a .pth file for each minor inside the gradients folder
    torch.save(
        model.state_dict(),
        os.path.join(gradients_folder, f"{miner_id}.pth"),
    )
    return gradients
