import torch
import config
# import albumentations as A
# from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dataset import SDNDataset


# transform = A.Compose(
#     [
#         ToTensorV2(),
#     ]
# )


def save_checkpoint(model, optimizer, epoch, train_acc, test_acc, filename=config.CHECKPOINT_FILE):
    print("=> Saving checkpoint")
    checkpoint = {
        "state_dict": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "epoch": epoch,
        "train_acc": train_acc,
        "test_acc": test_acc,
    }
    torch.save(checkpoint, filename)


def load_checkpoint(checkpoint_file, model, optimizer, train_acc, test_acc):
    print("=> Loading checkpoint")
    checkpoint = torch.load(checkpoint_file, map_location=config.DEVICE)
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    train_acc.extend(list(checkpoint["train_acc"]))
    test_acc.extend((checkpoint["test_acc"]))
    return checkpoint["epoch"]


def get_loaders(train_csv_path, test_csv_path):
    train_dataset = SDNDataset(
        csv_file=train_csv_path,
    )
    test_dataset = SDNDataset(
        csv_file=test_csv_path,
    )
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=True,
        drop_last=True,
    )
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=False,
        drop_last=True,
    )

    return train_loader, test_loader


def check_class_accuracy(model, loader, criterion, epoch):
    model.eval()

    loss = 0
    count = 0
    correct = 0
    for idx, (x, y) in enumerate(loader):
        count += 1
        x = x.to(config.DEVICE)
        y = y.to(config.DEVICE)
        x = x.unsqueeze(dim=1)
        with torch.no_grad():
            out = model(x)
        loss += criterion(out, y)
        y = y.unsqueeze(dim=1)
        out = F.log_softmax(out, dim=1).max(1, keepdim=True)[1]  # torch.Size([1, 1])
        correct += (y == out).sum()

    acc = 100. * correct / (config.BATCH_SIZE * count)
    print('Train Epoch: {},Loss: {:.6f}, Accuracy: {} / {} ({:.4f}%)'.format(
        epoch, loss / count, correct, count * config.BATCH_SIZE, acc))
    model.train()
    return acc


def plt_pictures(acc, pic_name):
    plt.figure()
    plt.plot(acc, c='red', label='pred')
    plt.ylabel('acc')
    plt.xlabel('number')
    plt.rcParams['figure.dpi'] = 300  # 设置图片分辨率为 1800*1200
    plt.rcParams['savefig.dpi'] = 300
    plt.savefig(pic_name)
    plt.show()
