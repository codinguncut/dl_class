import torch
# Making sure we can find the data loader
import sys
sys.path.append('..')
from data import load
import torch.utils.tensorboard as tb
import logging
import numpy as np
from tqdm.notebook import trange, tqdm

def train(model, log_dir, batch_size=128, resize=(32,32), device="cpu", n_epochs=100):
    logging.warning("loading dataset")
    train_data, train_label = load.get_dogs_and_cats_data(resize=(32,32))
    valid_data, valid_label = load.get_dogs_and_cats_data(split='valid', resize=(32,32))
    logging.warning("loading done")
    input_size = 32*32*3
    to_image = load.to_image_transform()
    
    train_data, train_label = train_data.to(device), train_label.to(device)
    valid_data, valid_label = valid_data.to(device), valid_label.to(device)
    model = model.to(device)

    train_logger = tb.SummaryWriter(log_dir+'/deepnet1/train', flush_secs=1)
    valid_logger = tb.SummaryWriter(log_dir+'/deepnet1/valid', flush_secs=1)
      
    # Create the optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
    
    # Create the loss
    loss = torch.nn.BCEWithLogitsLoss()
    
    # Start training
    global_step = 0
    for epoch in trange(n_epochs):
        # Shuffle the data
        permutation = torch.randperm(train_data.size(0))
        
        # Iterate
        train_accuracy = []
        for it in range(0, len(permutation)-batch_size+1, batch_size):
            batch_samples = permutation[it:it+batch_size]
            batch_data, batch_label = train_data[batch_samples], train_label[batch_samples]
            
            # Compute the loss
            o = model(batch_data)
            loss_val = loss(o, batch_label.float())
            
            train_logger.add_scalar('train/loss', loss_val, global_step=global_step)
            # Compute the accuracy
            train_accuracy.extend(((o > 0).long() == batch_label).cpu().detach().numpy())
            
            optimizer.zero_grad()
            loss_val.backward()
            optimizer.step()
            
            # Increase the global step
            global_step += 1
        
        # Evaluate the model
        valid_pred = model(valid_data) > 0
        valid_accuracy = float((valid_pred.long() == valid_label).float().mean())
        
        train_logger.add_scalar('train/accuracy', np.mean(train_accuracy), global_step=global_step)
        valid_logger.add_scalar('valid/accuracy', valid_accuracy, global_step=global_step)