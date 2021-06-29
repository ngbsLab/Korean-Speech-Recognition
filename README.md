# ***Korean Speech Recognition***  
  
### Character-unit based End-to-End Korean Speech Recognition  
   
[<img src="https://github.com/gentaiscool/end2end-asr-pytorch/raw/master/img/pytorch-logo-dark.png" height=18>](https://pytorch.org/) <img src="https://img.shields.io/badge/License-Apache--2.0-yellow" height=20> [<img src="https://img.shields.io/badge/chat-on%20gitter-4fb99a" height=20>](https://gitter.im/Korean-Speech-Recognition/community)
    
  
###### ( **CRR** : Character Recognition Rate )  

## Installation
This project recommends Python 3.7 or higher.   
We recommend creating a new virtual environment for this project (using virtual env or conda).  

### Prerequisites
  
* Numpy: `pip install numpy` (Refer [here](https://github.com/numpy/numpy) for problem installing Numpy).
* PyTorch: Refer to [PyTorch website](http://pytorch.org/) to install the version w.r.t. your environment.
* Pandas: `pip install pandas` (Refer [here](https://github.com/pandas-dev/pandas) for problem installing Pandas)  
* librosa: `pip install librosa` (Refer [here](https://github.com/librosa/librosa) for problem installing librosa)
* tqdm: `pip install tqdm` (Refer [here](https://github.com/tqdm/tqdm) for problem installing tqdm)  
  
### Install from source
Currently we only support installation from source code using setuptools. Checkout the source code and run the   
following commands:  
```
pip install -r requirements.txt
```
```
python setup.py build
python setup.py install
```
  
## Get Started
### Preparation before Training

The above document is written in Korean.  
We will also write a document in English as soon as possible, so please wait a little bit.  
  
If you already have another dataset, please modify the data set path to [definition.py] as appropriate.  

### Train and Test
if you want to start training, you should run [train.py]
or after training, you want to start testing, you should run [test.py] 
  
you can set up a configuration [config.py]
  

### Code Style
We follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) for code style. Especially the style of docstrings is important to generate documentation.  
    
### Reference   
[[1] 「Listen, Attend and Spell」  Paper](https://arxiv.org/abs/1508.01211)   
[[2] 「State-of-the-art Speech Recognition with Sequence-to-Sequence Models」   Paper](https://arxiv.org/abs/1712.01769)  
[[3] 「A Simple Data Augmentation Method for Automatic Speech Recognition」  Paper](https://arxiv.org/abs/1904.08779)     
[[4] 「Voice Recognition Using MFCC Algorithm」  Paper](https://ijirae.com/volumes/vol1/issue10/27.NVEC10086.pdf)        
[[5]    IBM pytorch-seq2seq](https://github.com/IBM/pytorch-seq2seq)   
[[6]    A.I Hub Korean Voice Dataset](http://www.aihub.or.kr/aidata/105)   
  
### License
```
Copyright (c) 2020 Kai.Lib

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
