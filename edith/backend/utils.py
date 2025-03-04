import os
import random
import shutil
from datetime import datetime

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import models
from torchvision import transforms
from torchvision.datasets import ImageFolder


def get_time():
    return datetime.now().strftime('%H:%M:%S')


def split_image_folder(in_dir, out_dir, train_size=0.8):
    """Split dataset into train and val.

    Args:
        in_dir: path to raw dataset folder.
        out_dir: path to processed folder.
        train_size: the proportion of the dataset to include in the train split.
    """
    class_names = os.listdir(in_dir)
    images_per_class = min([len(os.listdir(os.path.join(in_dir, class_name)))
                            for class_name in class_names])

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    for class_name in class_names:
        os.makedirs(os.path.join(out_dir, 'train', class_name))
        os.makedirs(os.path.join(out_dir, 'val', class_name))

        img_list = os.listdir(os.path.join(in_dir, class_name))[:images_per_class]
        random.shuffle(img_list)
        num_images = len(img_list)
        num_train = int(num_images * train_size)

        train_images = img_list[:num_train]
        val_images = img_list[num_train:]
        for image in train_images:
            shutil.copy2(os.path.join(in_dir, class_name, image),
                         os.path.join(out_dir, 'train', class_name))
        for image in val_images:
            shutil.copy2(os.path.join(in_dir, class_name, image),
                         os.path.join(out_dir, 'val', class_name))


def get_device():
    return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def get_net(model_name, mode, device, pretrained=False, num_classes=2, checkpoint_path=None):
    """Returns a torchvision model.

    Args:
        model_name (str): name of model.
        mode (str): train or val.
        device (torch.device): where data and model will be put on.
        pretrained (bool): If True, returns a model pre-trained on COCO train2017.
        num_classes (int): how many classes will be classified.
        checkpoint_path (str): path to checkpoint.

    Returns:
        net: model instance.
    """
    if model_name == "mobilenet" or model_name == "mobilenet_v2":
        net = models.mobilenet_v2(pretrained)
        in_features = net.classifier[1].in_features
        net.classifier[1] = nn.Linear(in_features, num_classes)
    elif model_name == "resnet":
        net = models.resnet18(pretrained)
        in_features = net.fc.in_features
        net.fc = nn.Linear(in_features, num_classes)

    if checkpoint_path is not None:
        checkpoint_dict = torch.load(checkpoint_path, map_location=device)
        net.load_state_dict(checkpoint_dict['model_state_dict'])

    if mode == 'train':
        net.train()  # Set model to training mode
    elif mode == 'val':
        net.eval()  # Set model to evaluate mode

    return net.to(device)


def get_result(frame, classes, net, device):
    """Returns class name of a frame captured by cv2.

    Args:
         frame: frame captured by cv2.
         classes (tuple): ('Cyclone', 'Wildfire', 'Flood', 'Earthquake').
         net: torchvision model instance.
         device (torch.device): device that net is put on.
    Returns:
        result (str): class name of the frame.
    """
    # Pre-processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_tensor = preprocess_image(frame_rgb, mode='inference')
    frame_tensor = frame_tensor.to(device)

    with torch.no_grad():
        prediction = net(frame_tensor)
        # result = get_prediction_class(prediction, idx_to_class)
        _, result_idx = torch.max(prediction, 1)
        result = classes[result_idx]

    return result


def load_checkpoint(model, path, optimizer=None):
    """Loads checkpoint from path.

    Args:
        model: model instance.
        path: path to the checkpoint.
        optimizer: optimizer instance (only needed during training).

    Returns:
        model: model instance loading checkpoint.
        optimizer: optimizer instance loading checkpoint.
        epoch: epoch at which to start training (useful for resuming a previous training run).
        loss: best loss.
    """
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']

    return model, optimizer, epoch, loss


def preprocess_image(image_np, mode='train'):
    """Returns prediction from image.

    Args:
        image_np: numpy image.
        mode: train or val.

    Returns:
        input_tensor: processed image.
    """
    data_transforms = get_data_transforms()[mode]
    input_tensor = data_transforms(image_np)
    input_tensor.unsqueeze_(dim=0)
    return input_tensor


def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


def visualize_model(model, dataloaders, num_images=6):
    class_names = dataloaders['val'].dataset.classes
    device = get_device()
    was_training = model.training
    model.eval()

    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['val']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, predictions = torch.max(outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images // 2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[predictions[j]]))
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)


# def get_prediction_class(prediction, idx_to_class):
#     """Returns class of prediction.
#     Args:
#         prediction(Tensor): a vector of probabilities.
#         idx_to_class(dict): a dict maps keys to the corresponding names. For example:
#         {0: 'cat', 1:'dog'}
#     Returns:
#         target_name: class of the prediction.
#     """
#     target_idx = torch.argmax(prediction).item()
#     target_name = idx_to_class[target_idx]
#     return target_name


def get_metadata(path):
    """Returns dataset metadata.
    Args:
        path: PATH to dataset folder.

    Returns:
        dataset_sizes: number of total images.
        num_classes:
        idx_to_class: A dict mapping labels to the corresponding class_names.
        {'drooling-face': 0,
         'face-savouring-delicious-food': 1,
         'face-with-cowboy-hat': 2,
         ...}
    """
    dataset = ImageFolder(path)
    dataset_size = len(dataset)

    class_names = dataset.classes
    num_classes = len(class_names)

    class_to_idx = dataset.class_to_idx
    idx_to_class = {value: key for key, value in class_to_idx.items()}
    return dataset_size, num_classes, idx_to_class


def get_data_loader(path, batch_size=2, mode='train', num_workers=2):
    """Returns data_loader.

    Args:
        path: path to dataset folder.
        batch_size: number of samples per gradient update.
        mode: train or val.
        num_workers: how many sub-processes to use for data loading.

    Returns:
        data_loader
    """
    data_transform = get_data_transforms()[mode]
    dataset = ImageFolder(root=path, transform=data_transform)
    data_loader = DataLoader(
        dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    return data_loader


def get_data_transforms():
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(30, resample=Image.NEAREST),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ]),
        'inference': transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
    }
    return data_transforms


def matplotlib_imshow(img, one_channel=False):
    if one_channel:
        img = img.mean(dim=0)
    img = img / 2 + 0.5  # unnormalize
    img_np = img.cpu().numpy()
    if one_channel:
        plt.imshow(img_np, cmap="Greys")
    else:
        plt.imshow(np.transpose(img_np, (1, 2, 0)))


def images_to_probs(net, images):
    """
    Generates predictions and corresponding probabilities from a trained
    network and a list of images.
    """
    output = net(images).cpu()
    # convert output probabilities to predicted class
    _, preds_tensor = torch.max(output, 1)
    preds = np.squeeze(preds_tensor.numpy())
    return preds, [F.softmax(el, dim=0)[i].item() for i, el in zip(preds, output)]


def plot_classes_preds(net, class_names, images, labels):
    """
    Generates matplotlib Figure using a trained network, along with images
    and labels from a batch, that shows the network's top prediction along
    with its probability, alongside the actual label, coloring this
    information based on whether the prediction was correct or not.
    Uses the "images_to_probs" function.
    """
    preds, probs = images_to_probs(net, images)
    # plot the images in the batch, along with predicted and true labels
    fig = plt.figure(figsize=(12, 48))
    for idx in np.arange(4):
        ax = fig.add_subplot(1, 4, idx + 1, xticks=[], yticks=[])
        matplotlib_imshow(images[idx], one_channel=False)
        ax.set_title("{0}, {1:.1f}%\n(label: {2})".format(
            class_names[preds[idx]],
            probs[idx] * 100.0,
            class_names[labels[idx]]),
            color=("green" if preds[idx] == labels[idx].item() else "red"))
    return fig
