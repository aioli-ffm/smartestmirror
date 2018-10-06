import torch
import shutil
import matplotlib.pyplot as plt


class AverageMeter(object):
    """
    Computes and stores the average and current value
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def save_checkpoint(state, is_best, file_path, file_name='checkpoint.pth.tar'):
    """
    Saves the current state of the model. Does a copy of the file
    in case the model performed better than previously.

    Parameters:
        state (dict): Includes optimizer and model state dictionaries
        is_best (bool): True if model is best performing model
        file_path (str): Path to save file
        file_name (str): File name with extension (default: checkpoint.pth.tar)
    """

    save_path = file_path + '/' + file_name
    torch.save(state, save_path)
    if is_best:
        shutil.copyfile(save_path, file_path + '/model_best.pth.tar')


def plot_kernels(tensor, file_path, num_cols=6):
    if not tensor.ndim==4:
        raise Exception("assumes a 4D tensor")
    if not tensor.shape[-1]==3:
        raise Exception("last dim needs to be 3 to plot")
    num_kernels = tensor.shape[0]
    num_rows = 1+ num_kernels // num_cols
    fig = plt.figure(figsize=(num_cols,num_rows))
    for i in range(tensor.shape[0]):
        ax1 = fig.add_subplot(num_rows,num_cols,i+1)
        ax1.imshow(tensor[i]*255, interpolation='none')
        ax1.axis('off')
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])

    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.savefig(file_path)