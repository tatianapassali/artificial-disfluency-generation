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


## Generating disfluencies 




## Create disfluencies from text file
If you have a file that contains fluent text, you can easily 
create disfluencies, specify the percentages 