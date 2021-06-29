
# If you haven't read https://sh951011.github.io/Korean-Speech-Recognition/notes/Preparation.html
# please read it first before setting define.py

DATASET_PATH = "/home/nextgen/Desktop/mjh/325/augmentdata/augment_data/" # set by your data path
SAMPLE_DATASET_PATH = "./data/sample/"
TRAIN_LIST_PATH = "./data/data_list/augmentdata_train_list.csv"
TEST_LIST_PATH = "./data/data_list/mytest_list.csv"
SAMPLE_LIST_PATH = "./data/data_list/debug_list.csv"
TARGET_DICT_PATH = "./data/pickle/new_target_dict.bin"
TRAIN_RESULT_PATH = "./data/train_result/train_result.csv"
VALID_RESULT_PATH = "./data/train_result/eval_result.csv"
TRAIN_STEP_RESULT_PATH = "./data/train_result/train_step_result.csv"
import logging, sys
logger = logging.getLogger('root')
FORMAT = "[%(asctime)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
logger.setLevel(logging.INFO)
from package.loader import load_label
char2id, id2char = load_label('./data/label/mytest_labels.csv', encoding='utf-8') # 2,040
# if you want to use total character label
# change => char2id, id2char = load_label('./data/label/test_labels.csv', encoding='utf-8') # 2,337
SOS_TOKEN = int(char2id['<s>'])
EOS_TOKEN = int(char2id['</s>'])
PAD_TOKEN = int(char2id['_'])
train_dict = {'loss': [], 'cer': []}
valid_dict = {'loss': [], 'cer': []}
