import torch
import torch.utils.data
import torchvision.datasets as datasets
import torchvision.transforms as transforms


class CUSTOM:
    """
    CUSTOM dataset using ImageFolder for any data-loading.
    Preprocessing is calculated using the preprocessing class.

    Parameters:
        args (dict): Dictionary of (command line) arguments.
            Needs to contain batch_size (int), workers(int),
            patch_size (int) defining image size and
            a path to_data (str)
        is_gpu (bool): True if CUDA is enabled.
            Sets value of pin_memory in DataLoader.

    Attributes:
        data_dir (str): Path to dataset as required by
            torchvision.datasets.ImageFolder
        transforms (torchvision.transforms): Composition of transforms
            including conversion to Tensor, horizontal flips, scaling of
            shorter edge to patch_size.
        trainset (torch.utils.data.TensorDataset): trainset wrapper.
        train_loader (torch.utils.data.DataLoader): trainset loader.
    """

    def __init__(self, is_gpu, args):
        self.datadir = args.data_dir

        self.transforms = self.__get_transforms(args.patch_size)

        self.train_set = self.get_dataset()
        self.train_loader = self.get_dataset_loader(args.batch_size, args.workers, is_gpu)

    def __get_transforms(self, patch_size):
        train_transforms = transforms.Compose([
            transforms.Scale(patch_size),
            transforms.CenterCrop(patch_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            #transforms.Lambda(lambda x: x.narrow(0, 0, 1)),  #one (not so nice) way of going to gray-scale
            ])

        return train_transforms

    def get_dataset(self):
        """
        Uses torchvision.datasets.ImageFolder to load dataset.

        Returns:
             torch.utils.data.TensorDataset: dataset
s        """

        trainset = datasets.ImageFolder(self.datadir, self.transforms)

        return trainset

    def get_dataset_loader(self, batch_size, workers, is_gpu):
        """
        Defines the dataset loader for wrapped dataset

        Parameters:
            batch_size (int): Defines the batch size in data loader
            workers (int): Number of parallel threads to be used by data loader
            is_gpu (bool): True if CUDA is enabled so pin_memory is set to True

        Returns:
             torch.utils.data.TensorDataset: data_loader
        """

        train_loader = torch.utils.data.DataLoader(
            self.train_set,
            batch_size=batch_size, shuffle=True,
            num_workers=workers, pin_memory=is_gpu, sampler=None)

        return train_loader
