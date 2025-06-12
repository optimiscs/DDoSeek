import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from model import ConvNet
from tqdm import tqdm
import config
from utils import (
    save_checkpoint,
    load_checkpoint,
    get_loaders,
    check_class_accuracy,
    plt_pictures,
)


def train_fn(train_loader, model, optimizer, criterion, epoch):
    loop = tqdm(train_loader, leave=True)
    count = 0
    correct = 0
    losses = 0
    acc = []
    for batch_idx, (x, y) in enumerate(loop):
        count += 1
        x = x.to(config.DEVICE)
        y = y.to(config.DEVICE)
        x = x.unsqueeze(dim=1)

        out = model(x)

        loss = criterion(out, y)
        losses += loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        y = y.unsqueeze(dim=1)
        out = F.log_softmax(out, dim=1).max(1, keepdim=True)[1]
        correct += (y == out).sum()
        # update progress bar
        mean_loss = losses / count
        cur_acc = 100. * correct / (config.BATCH_SIZE * count)
        loop.set_description(f"Epoch {epoch}/{config.EPOCHS}")
        loop.set_postfix(loss=mean_loss, acc=cur_acc)
        if (batch_idx + 1) % 100 == 0:
            acc.append(cur_acc)

    plt_pictures(acc, './pic/pic%s.png' % epoch)
    return 100. * correct / (config.BATCH_SIZE * count)


def main():
    model = ConvNet().to(config.DEVICE)
    optimizer = optim.Adam(
        model.parameters(), lr=config.LEARNING_RATE, weight_decay=config.WEIGHT_DECAY
    )
    criterion = nn.CrossEntropyLoss()
    train_loader, test_loader = get_loaders(
        train_csv_path=config.TRAIN_DIR, test_csv_path=config.TEST_DIR
    )
    test_acc = []
    train_acc = []

    epoch = 0
    if config.LOAD_MODEL:
        epoch = load_checkpoint(
            config.CHECKPOINT_FILE, model, optimizer, train_acc, test_acc,
        )

    for epoch in range(epoch + 1, config.EPOCHS + 1):
        train_acc.append(train_fn(train_loader, model, optimizer, criterion, epoch))

        test_acc.append(check_class_accuracy(model, test_loader, criterion, epoch))

        if config.SAVE_MODEL:
            save_checkpoint(model, optimizer, epoch, train_acc, test_acc)

    print("首先绘制测试集准确率图像")
    plt_pictures(test_acc, './pic/pic-test-acc.png')
    print("绘制训练集准确率图像")
    plt_pictures(train_acc, './pic/pic-train-acc.png')


if __name__ == "__main__":
    main()
