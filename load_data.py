import torch


def load_data(zip_file_path):
    # Your data loading logic here
    # Example: Assume you have a dataset with 100 samples, each with 10 features
    num_samples = 100
    num_features = 10

    # Generate random data for simulation
    inputs = torch.randn(num_samples, num_features)
    targets = torch.randn(num_samples, 1)

    # Assume you have a DataLoader
    data_loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(inputs, targets), batch_size=32, shuffle=True
    )

    return data_loader
