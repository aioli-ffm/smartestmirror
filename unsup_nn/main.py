# System libraries
import os
from time import gmtime, strftime

# Torch libraries
import torch
import torch.nn as nn

# From custom library
import lib.models as architectures
import lib.datasets as datasets
from lib.cmdparser import parser
from lib.initialization import WeightInit
from lib.train import train_unsup
from lib.utility import save_checkpoint


def main():
    # Command line options
    args = parser.parse_args()
    print("Command line options:")
    for arg in vars(args):
        print(arg, getattr(args, arg))

    # Check whether GPU is available and can be used
    # if CUDA is found then set flag to True
    is_gpu = torch.cuda.is_available()

    # Dataset loading
    # There's only one dataset loader right now, but it can be extended
    data_init_method = getattr(datasets, 'CUSTOM')
    dataset = data_init_method(is_gpu, args)

    # Construct the network
    net_init_method = getattr(architectures, args.architecture)
    model = net_init_method(args.batch_norm)

    # Initialize the weights of the model
    print("Initializing network with: " + args.weight_init)
    WeightInitializer = WeightInit(args.weight_init)
    WeightInitializer.init_model(model)

    if is_gpu:
        # CUDNN
        import torch.backends.cudnn as cudnn
        model = model.cuda()
        cudnn.benchmark = True

    print(model)

    # Define optimizer and loss function (criterion)
    criterion = nn.BCELoss()

    if is_gpu:
        criterion = criterion.cuda()

    # autoencoders also work with SGD but it is much harder to find the correct parameters
    # TODO: expose this to cmd line eventually
    if args.optimizer == 'ADAM':
        optimizer = torch.optim.Adam(model.parameters(),
                                     lr=args.learning_rate,
                                     betas=(args.momentum, 0.999))
    else:
        optimizer = torch.optim.SGD(model.parameters(), args.learning_rate,
                                    momentum=args.momentum,
                                    weight_decay=args.weight_decay)

    save_path = 'runs/' + strftime("%Y-%m-%d_%H:%M:%S", gmtime()) + \
                ';' + args.architecture
    os.mkdir(save_path)

    epoch = 1
    best_loss = 100000000  # some arbitrarily large initial number

    while epoch <= args.epochs:

        model.train()
        loss = train_unsup(dataset.train_loader, model, criterion, epoch, optimizer, is_gpu, args)

        # remember best prec@1 and save checkpoint
        is_best = loss < best_loss
        best_loss = min(loss, best_loss)
        save_checkpoint({
            'epoch': epoch,
            'arch': args.architecture,
            'state_dict': model.state_dict(),
            'best_loss': best_loss,
            'optimizer': optimizer.state_dict(),
        }, is_best, save_path)

        # increment epoch counter
        epoch += 1

if __name__ == '__main__':
    main()