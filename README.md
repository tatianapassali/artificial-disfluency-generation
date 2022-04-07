# artificial-disfluency-generation
LARD: A tool to generate easily and promptly artificial disfluencies from fluent text

This repository contains the code for paper: LARD: Large-scale Artificial Disfluency Generation

## Requirements
`Python>=3.8`  
`nltk>=3.5`  
`numpy>=1.19.2`  
`pandas>=1.1.3`  
`colorama>=0.4.4`

## Installation 
To use the LARD tool, you need to clone the repository locally and 
install the necessary library dependencies from requirements.txt
```
git clone https://github.com/tatianapassali/topic-controllable-summarization.git
cd artificial-disfluency-generation
pip3 install -r requirements.txt
```

Alternatively, you can create a python virtual environment (venv) using the virtualenv tool.
Just make sure that you run Python 3.8 or more. After cloning the repository, as shown above,
you have to initialize and activate the virtual enviroment.
```
virtualenv artificial-disfluency-generation
source myproject/venv/bin/activate
pip3 install -r requirements.txt
```

## How to use 
You can use the LARD tool to auto-generate disfluencies such as repetitions, restarts, and replacements.

### Initialize tool
```python
>>> from disfluency_generation import LARD
>>> lard = LARD
```

### Generate repetitions
You can generate repetitions of different degrees specifying the degree parameter (1-3). For example, you can generate 
a first-degree repetition like this:
```python
>>> fluent_sentence = "Hello are you up for a coffee this friday ?"
# This is a first-degree repetition
>>> disfluency = lard.create_repetitions(fluent_sentence, 1)
>>> print(disfluency[0])
'Hello are you up for a coffee this this friday ?'
```
or a second-degree repetition like this:
```python
>>> fluent_sentence = "Hello are you up for a coffee this friday ?"
# This is a second-degree repetition
>>> disfluency = lard.create_repetitions(fluent_sentence, 2)
>>> print(disfluency[0])
'Hello are you are you up for a coffee this friday ?'
```

### Generate replacements
You can generate replacements with different criteria. An example of usage for the replacement is shown below:

```python
>>> fluent_sentence = "Yes, I am going to visit my family for a week ."
>>> disfluency = lard.create_replacements(fluent_sentence)
>>> print(disfluency[0])
'Yes, I am go no I am going to visit my family for a week .'
```
You can also specify the part-of-speech candidate for replacement from noun, verb or adjective and chose whether or not
a repair cue will be included in the disfluent sequence. Note that if you don't specify any of these,
a random part-of speech will be selected along with a repair cue by default. 

```python
>>> fluent_sentence = "I prefer to drink coffee without sugar."
>>> disfluency = lard.create_replacements(fluent_sentence)
>>> print(disfluency[0])
'I prefer to drink chocolate well I actually meant drink coffee without sugar .'
```

### Generate restarts 
Similarly, you can generate restarts. Note that you need two fluent
sequences to generate a restart like this:

```python
>>> fluent_sentence_1 = "Where can i find a pharmacy near me?"
>>> fluent_sentence_1 = "What time do you close?"
>>> disfluency = lard.create_restarts(fluent_sentence_1, fluent_sentence_2)
>>> print(disfluency[0])
'I prefer to drink chocolate well I actually meant drink coffee without sugar .'
```


## Generate multiple disfluencies from text file
You can also use the LARD tool to generate multiple types of disfluencies from a text file using the create_dataset
function.

```python
from create_dataset import create_dataset

create_dataset(INPUT_FILE_PATH,
                   OUTPUT_DIR,
                   column_text=column_text,
                   keep_fluent=False,
                   create_all_files=True,
                   concat_files=True)
```

You can also specify the fractions of fluencies, repetitions, replacements and restarts. Please read the 
whole documentation of create_dataset.py for more information about the parameters of this function.

**NOTE**: The input file must be formatted as a.csv file with one or more columns. You also need to specify the text column for the generation of the
disfluencies. A sample .csv file can be found at sample_data directory. 

## LARD Dataset
We create our own disfluent dataset bulding upon [Schema-Guided Dialogue (SGD)](https://arxiv.org/pdf/1801.04871.pdf). 

**Dataset Summary**

LARD dataset contains 95,992 examples of utterances with 71,994 artificial inserted disfluencies using the LARD method. We use the [Schema-Guided Dialogue (SGD) ](https://arxiv.org/pdf/1801.04871.pdf) dataset as a base to construct the synthetic disfluencies. The LARD dataset contains three different types of disfluencies: repetitions, replacements and restarts.

**Data Instances:**
The dataset consists of three Comma-Separated Values (CSV) files (train.csv, validation.csv, test.csv)

**Data Fields:** Each row of the dataset has the following columns:

`original text`: The original fluent natural language utterance (String)

`disfluent_text`: The utterance with the inserted synthetic disfluency. If no disfluency is added, the disfluent text is the same as the original text. (String)

`tokenized_disfluent_text`: A list of tokens of the disfluent utterance (list)

`binary_label`: 1 if disfluency exists, 0 if no disfluency exists.

`mutliclass_label`: The type of difsluency, if exists (0: no disfluency, 1: repetition, 2:replacement, 3:restart)

`token_tags`: A list with the tag for each token of the tokenized disfluent text (0: fluent token, D: disfluent token).

**Data Splits**: The dataset is split into train, validation and test split as follows:

|                            | Training   | Validation |  Test   |
| -----                      | --------   | ---------- | ------- | 
| # Examples                 | 57,595     | 19,198     | 19,199  |


**Language:** English (`en`)

**Source data**: [Schema-Guided Dialogue (SGD) ](https://arxiv.org/pdf/1801.04871.pdf)

**License:** The dataset is released under [![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/).

You can download the dataset from [here.](https://bit.ly/LARDdataset) 