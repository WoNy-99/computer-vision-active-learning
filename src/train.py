import argparse
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def build_model(name: str, num_classes: int) -> nn.Module:
    if name == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model
    if name == "convnext_large":
        model = models.convnext_large(weights=models.ConvNeXt_Large_Weights.DEFAULT)
        model.classifier[2] = nn.Linear(model.classifier[2].in_features, num_classes)
        return model
    raise ValueError(f"Unsupported model: {name}")


def make_loaders(root: Path, batch_size: int):
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    eval_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    datasets_by_split = {
        "train": datasets.ImageFolder(root / "train", train_transform),
        "valid": datasets.ImageFolder(root / "valid", eval_transform),
        "test": datasets.ImageFolder(root / "test", eval_transform),
    }
    return {
        split: DataLoader(ds, batch_size=batch_size, shuffle=split == "train", num_workers=2)
        for split, ds in datasets_by_split.items()
    }


def run_epoch(model, loader, criterion, device, optimizer=None):
    training = optimizer is not None
    model.train(training)
    loss_sum = correct = count = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        if training:
            optimizer.zero_grad()
        with torch.set_grad_enabled(training):
            logits = model(images)
            loss = criterion(logits, labels)
            if training:
                loss.backward()
                optimizer.step()
        loss_sum += loss.item() * labels.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        count += labels.size(0)
    return loss_sum / count, 100 * correct / count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--model", choices=["resnet18", "convnext_large"], default="resnet18")
    parser.add_argument("--num-classes", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--output", type=Path, default=Path("checkpoints/best.pth"))
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaders = make_loaders(args.data_root, args.batch_size)
    model = build_model(args.model, args.num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    best_accuracy = -1.0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = run_epoch(model, loaders["train"], criterion, device, optimizer)
        val_loss, val_acc = run_epoch(model, loaders["valid"], criterion, device)
        print(f"epoch={epoch} train_loss={train_loss:.4f} train_acc={train_acc:.2f} "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.2f}")
        if val_acc > best_accuracy:
            best_accuracy = val_acc
            torch.save(model.state_dict(), args.output)

    model.load_state_dict(torch.load(args.output, map_location=device))
    test_loss, test_acc = run_epoch(model, loaders["test"], criterion, device)
    print(f"test_loss={test_loss:.4f} test_acc={test_acc:.2f}")


if __name__ == "__main__":
    main()

