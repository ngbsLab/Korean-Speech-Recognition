"""
-*- coding: utf-8 -*-
"""

import queue
import torch.nn as nn
import torch.optim as optim
import random
import torch
import time
import os
from models.speller import Speller
from models.listener import Listener
from models.listenAttendSpell import ListenAttendSpell
from package.dataset import split_dataset
from package.definition import *
from package.evaluator import evaluate
from package.config import Config
from package.loader import load_data_list, load_targets, load_pickle, MultiLoader, BaseDataLoader
from package.loss import LabelSmoothingLoss
from package.trainer import supervised_train
from package.utils import save_epoch_result


if __name__ == '__main__':
    ##os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # if you use Multi-GPU, delete this line
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    logger.info("device : %s" % torch.cuda.get_device_name(0))
    logger.info("CUDA is available : %s" % (torch.cuda.is_available()))
    logger.info("CUDA version : %s" % (torch.version.cuda))
    logger.info("PyTorch version : %s" % (torch.__version__))

    config = Config(
        use_bidirectional = True,
        use_attention = True,
        use_label_smooth = True,
        input_reverse = True,
        use_augment = True,
        use_pickle = False,
        use_pyramidal = False,
        use_cuda = True,
        pack_by_length = False,
        augment_ratio = 1.0,
        hidden_size = 256, #256
        dropout = 0.5,
        listener_layer_size = 5,
        speller_layer_size = 3,
        batch_size = 2, #6
        worker_num = 4, #1
        max_epochs = 200, #50
        use_multistep_lr = False,
        init_lr = 0.0001, #0.0001
        high_plateau_lr = 0.0003, #0.0003
        low_plateau_lr = 0.00001,
        teacher_forcing = 0, #0.9
        seed = 1,
        max_len = 151
    )

    random.seed(config.seed)
    torch.manual_seed(config.seed)
    torch.cuda.manual_seed_all(config.seed)
    cuda = config.use_cuda and torch.cuda.is_available()
    device = torch.device('cuda' if cuda else 'cpu')

    listener = Listener(
        in_features = 80,
        hidden_size = config.hidden_size,
        dropout_p = config.dropout,
        n_layers = config.listener_layer_size,
        bidirectional = config.use_bidirectional,
        rnn_cell = 'gru',
        use_pyramidal = config.use_pyramidal,
        device=device
    )
    speller = Speller(
        class_num = len(char2id),
        max_len = config.max_len,
        k = 8,
        hidden_size = config.hidden_size << (1 if config.use_bidirectional else 0),
        sos_id = SOS_TOKEN,
        eos_id = EOS_TOKEN,
        n_layers = config.speller_layer_size,
        rnn_cell = 'gru',
        dropout_p = config.dropout,
        use_attention = config.use_attention,
        device = device
    )
    model = ListenAttendSpell(listener, speller, use_pyramidal = config.use_pyramidal)

    model.flatten_parameters()
    model = nn.DataParallel(model).to(device)

    optimizer = optim.Adam(model.module.parameters(), lr=config.init_lr)
    if config.use_label_smooth:
        criterion = LabelSmoothingLoss(len(char2id), ignore_index = PAD_TOKEN, smoothing = 0.1, dim = -1).to(device)
    else:
        criterion = nn.CrossEntropyLoss(reduction='sum', ignore_index=PAD_TOKEN).to(device)

    audio_paths, label_paths = load_data_list(data_list_path=TRAIN_LIST_PATH, dataset_path=DATASET_PATH)

    if config.use_pickle:
        target_dict = load_pickle(TARGET_DICT_PATH, "load all target_dict using pickle complete !!")
    else:
        target_dict = load_targets(label_paths)

    total_time_step, train_dataset_list, valid_dataset = split_dataset(
        config = config,
        audio_paths = audio_paths,
        label_paths = label_paths,
        valid_ratio = 0.2,
        target_dict = target_dict,
    )

    logger.info('start')
    train_begin = time.time()

    for epoch in range(config.max_epochs):
        train_queue = queue.Queue(config.worker_num << 1)

        for train_dataset in train_dataset_list:
            train_dataset.shuffle()

        train_loader = MultiLoader(train_dataset_list, train_queue, config.batch_size, config.worker_num)
        train_loader.start()
        train_loss, train_cer = supervised_train(
            model = model,
            total_time_step = total_time_step,
            config = config,
            queue = train_queue,
            criterion = criterion,
            epoch = epoch,
            optimizer = optimizer,
            device = device,
            train_begin = train_begin,
            worker_num = config.worker_num,
            print_time_step = 10,
            teacher_forcing_ratio = config.teacher_forcing
        )
        train_loader.join()

        torch.save(model, "./data/weight_file/epoch%s.pt" % str(epoch))
        logger.info('Epoch %d (Training) Loss %0.4f CER %0.4f' % (epoch, train_loss, train_cer))

        valid_queue = queue.Queue(config.worker_num << 1)
        valid_loader = BaseDataLoader(valid_dataset, valid_queue, config.batch_size, 0)
        valid_loader.start()

        valid_loss, valid_cer = evaluate(model, valid_queue, criterion, device)
        valid_loader.join()

        logger.info('Epoch %d (Evaluate) Loss %0.4f CER %0.4f' % (epoch, valid_loss, valid_cer))
        logger.info('Epoch %d Training result saved as a csv file complete !!' % epoch)

        save_epoch_result(train_result=[train_dict, train_loss, train_cer], valid_result=[valid_dict, valid_loss, valid_cer])
