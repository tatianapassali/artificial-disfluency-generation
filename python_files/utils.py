import nltk
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

REPAIR_CUES = [("no", 1), ("no wait", 2), ("no sorry", 2), ("I meant", 2), ("I mean", 2), ("sorry", 1),
               ("I am sorry", 3), ("no i meant to say", 5), ("actually no", 2), ("wait", 1),
               ("well I actually mean", 4), ("well I actually meant", 4),
               ("wait a minute", 3),
               ("no wait a minute", 4)]


none_tuple = (None, None, None, None, None)


def extract_syns_ants(word, pos):
    synsets = wordnet.synsets(word, pos=getattr(wordnet, pos))

    synonyms = [lemma.name() for synset in synsets for lemma in synset.lemmas()]
    antonyms = [lemma.antonyms()[0].name() for synset in synsets for lemma in synset.lemmas() if lemma.antonyms()]

    return synonyms, antonyms


def are_same(lst):
    return all(x.lower() == lst[0].lower() for x in lst)


def extract_pos_format(candidate_pos):
    if candidate_pos is not None:
        if candidate_pos == 'NOUN':
            possible_tag_format = ['NN', 'NNS']
        elif candidate_pos == 'VERB':
            possible_tag_format = ['VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP']
        elif candidate_pos == "ADJ":
            possible_tag_format = ['JJ', 'JJR', 'JJS']
        else:
            print("You need to specify a valid POS identifier. Supported POS: NOUN, VERB or ADJ")
            return None
    else:
        possible_tag_format = ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'JJ', 'JJR', 'JJS']

    return possible_tag_format


def revert_pos_format(pos):
    if pos in ['NN', 'NNS']:
        candidate_pos = 'NOUN'
    elif pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP']:
        candidate_pos = 'VERB'
    elif pos in ['JJ', 'JJR', 'JJS']:
        candidate_pos = 'ADJ'
    else:
        candidate_pos = ''

    return candidate_pos
