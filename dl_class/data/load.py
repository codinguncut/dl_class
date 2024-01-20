import torch
from torchvision import datasets, transforms
import pathlib
import random

def get_dogs_and_cats(*args, **kwargs):
    return get_dogs_and_cats_data(*args, **kwargs)

def get_dogs_and_cats_data(split="train", resize=(32,32), n_images=None, batch_size=None, is_resnet=False, **kwargs):
    if resize is None:
        resize = (256, 256)
        
    transform = transforms.Compose([
        transforms.Resize(size=resize),
        transforms.ToTensor(),
    ])

    folder = pathlib.Path(__file__).resolve().parent / "dogs_and_cats" / split
    dataset = datasets.ImageFolder(folder, transform=transform)
    
    if is_resnet:
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, **kwargs)
        return dataloader
    else:
        sampler = None
        if n_images:
            sampler = random.sample(list(range(len(dataset))), n_images)
        batch_size = n_images if n_images else len(dataset)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, sampler=sampler, **kwargs)
        return next(iter(dataloader))

def to_image_transform():
    return transforms.ToPILImage()

