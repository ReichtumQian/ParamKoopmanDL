import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_device(device):
  global DEVICE
  DEVICE = device


def print_device():
  print(DEVICE)


if __name__ == "__main__":
  print(DEVICE)
