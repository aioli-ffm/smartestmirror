import time
import torch
from lib.utility import AverageMeter
from torchvision.utils import save_image
from torch.nn import functional as F
from lib.utility import plot_kernels


def train_unsup(train_loader, model, criterion, epoch, optimizer, is_gpu, args):
    """
    Trains/updates the model for one epoch on the training dataset.

    Parameters:
        train_loader (torch.utils.data.DataLoader): The trainset dataloader
        model (torch.nn.module): Model to be trained
        criterion (torch.nn.criterion): Loss function
        epoch (int): Continuous epoch counter
        optimizer (torch.optim.optimizer): optimizer instance like SGD or Adam
        is_gpu (bool): True if CUDA is enabled so pin_memory is set to True
        args (dict): Dictionary of (command line) arguments.
            Needs to contain learning_rate (float), momentum (float),
            weight_decay (float), print_freq (int), batch_size (int)
            and patch_size (int).
    """

    def vae_loss_function(recon_x, x, mu, logvar, batch_size, patch_size):
        BCE = F.binary_cross_entropy(recon_x, x)

        # see Appendix B from VAE paper:
        # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
        # https://arxiv.org/abs/1312.6114
        KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        # Normalise by same number of elements as in reconstruction
        KLD /= batch_size * 3 * patch_size * patch_size

        return BCE + KLD

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    # switch to train mode
    model.train()

    end = time.time()

    c = 1 # counter for saved_images

    for i, (input, _) in enumerate(train_loader):
        # measure data loading time
        data_time.update(time.time() - end)

        if is_gpu:
            input = input.cuda()

        input_var = torch.autograd.Variable(input)
        target_var = torch.autograd.Variable(input)

        # compute output
        if args.variational:
            output, mu, logvar, z = model(input_var)
            loss = vae_loss_function(output, input_var, mu, logvar,
                                     args.batch_size, args.patch_size)
        else:
            output = model(input_var)
            loss = criterion(output, target_var)

        # record loss
        losses.update(loss.data[0], input.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        # logging and visualization
        if i % args.print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})'.format(
                   epoch, i, len(train_loader), batch_time=batch_time,
                   data_time=data_time, loss=losses))

            # TODO: bad path hard-coding here
            # TODO: do not print every mini-batch?
            save_image(output.cpu().data.view(args.batch_size, 3, args.patch_size, args.patch_size),
                       'tmp/recon_epoch_' + str(epoch) + '_' + str(c) + '.png')
            c += 1

    """
    # Removing this temporarily because of need for sequential containers in inference 
    # in order to differentiate between encoder and decoder
    # TODO: Plotting should be correct, but weights look off. Find fix.
    # visualization of first layer's filters
    conv1weight = model.conv1.weight.data
    if is_gpu:
        conv1weight = conv1weight.cpu()
    plot_kernels(conv1weight.transpose(1, 3).numpy(), 'tmp/weights_epoch_' + str(epoch) + '.png')
    """

    return losses.avg