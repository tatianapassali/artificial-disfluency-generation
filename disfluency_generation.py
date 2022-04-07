import string
import nltk
import random
import math
from colorama import Fore
from random import randrange
import utils
from utils import none_tuple
from colorama import init
init(autoreset=True)


class LARD:

    def create_repetitions(self, fluent_sentence, degree=None):
        """ Create repetitions.
        This function is used to create different degree repetitions in a fluent sequence.

        Args:
            fluent_sentence (`str`): A fluent text sequence

            degree (`int`, *optional*, defaults to 'None'): The degree of the repetition (1,2 or 3).
            If it is not specified the default value is set to None and the degree is randomly initialized
            inside the function.

        Returns:
            disfluent_sentence (`str`): The disfluent sentence with the corresponding repetition

            fluent_tokens (List[`str`]): List of fluent tokens of the fluent sequence

            disfluent_tokens (List[`str`]): List of disfluent tokens of the disfluent sequence

            annotations (List[`str`]): List of token-level annotations for the disfluent tokens
            (F: Fluent, D: Disfluent)
        """
        annotations = []
        disfluent_tokens = []

        if not fluent_sentence:
            raise TypeError('''A 'NoneType' object received while a 'str' object is required.''')
        else:
            # Tokenize the sentence
            fluent_tokens = nltk.word_tokenize(fluent_sentence)

        if len(fluent_tokens) == 1:
            if degree > 1:
                print("Warning! Only a first degree repetition can be created, because input sequence contains only one token.")
                print("Reseting ngram to 1...\n")

            # The only possible disfluency that we can create is first degree repetition
            disfluent_tokens.extend([fluent_tokens[0]] * 2)
            disfluent_sentence = " ".join(disfluent_tokens)
            annotations = ['D', 'F']
            degree = 1
            return disfluent_sentence, fluent_tokens, disfluent_tokens, annotations, degree

        elif len(fluent_tokens) == 2:
            if degree > 2:
                # We can create first or second degree repetitions
                degree = random.randint(1, 2)
                print(
                    "Warning! Only a first or second degree repetition can be created, because input sequence contains only one "
                    "token.")
                print("Degree is randomly reset to " + str(degree) + "...")

        # Finally, create repetitions
        # First-degree repetitions
        if degree == 1:
            try:
                random_repeat_idx = random.choice(
                    [idx for idx in range(len(fluent_tokens)) if fluent_tokens[idx] not in string.punctuation])
            except IndexError:
                print(
                    Fore.RED + "Warning: You try to pass an input sequence where there are not available candidate "
                               "tokens for creating a repetition.Ignoring this sequence...")
                return none_tuple

            disfluent_tokens = fluent_tokens[:random_repeat_idx]
            disfluent_tokens.append(fluent_tokens[random_repeat_idx])
            disfluent_tokens = disfluent_tokens + fluent_tokens[random_repeat_idx:]

            annotations = ["F"] * random_repeat_idx
            annotations.append("D")
            annotations.extend(["F"] * (len(fluent_tokens) - random_repeat_idx))

        # Second-degree repetitions
        if degree == 2:
            try:
                random_repeat_idx = random.choice([idx for idx in range(len(fluent_tokens) - 1) if
                                                   fluent_tokens[idx] not in string.punctuation and fluent_tokens[
                                                       idx + 1] not in string.punctuation])
            except IndexError:
                print(
                    Fore.RED + "Warning: You try to pass an input sequence where there are not available candidate "
                               "tokens for creating a repetition. Ignoring this sequence...")
                return none_tuple

            disfluent_tokens = fluent_tokens[:random_repeat_idx]
            disfluent_tokens.append(fluent_tokens[random_repeat_idx])
            disfluent_tokens.append(fluent_tokens[random_repeat_idx + 1])

            disfluent_tokens = disfluent_tokens + fluent_tokens[random_repeat_idx:]

            annotations = ["F"] * random_repeat_idx
            annotations.extend(["D"] * degree)
            annotations.extend(["F"] * (len(fluent_tokens) - random_repeat_idx))

        # Third-degree repetitions
        if degree == 3:
            try:
                random_repeat_idx = random.choice([idx for idx in range(len(fluent_tokens) - 2) if
                                                   fluent_tokens[idx] not in string.punctuation and fluent_tokens[
                                                       idx + 1] not in string.punctuation and fluent_tokens[
                                                       idx + 2] not in string.punctuation])
            except IndexError:
                print(
                    Fore.RED + "Warning: You try to pass an input sequence where there are not available candidate "
                               "tokens for creating a repetition.Ignoring this sequence...")
                return none_tuple

            disfluent_tokens = fluent_tokens[:random_repeat_idx]
            disfluent_tokens.append(fluent_tokens[random_repeat_idx])
            disfluent_tokens.append(fluent_tokens[random_repeat_idx + 1])
            disfluent_tokens.append(fluent_tokens[random_repeat_idx + 2])

            disfluent_tokens = disfluent_tokens + fluent_tokens[random_repeat_idx:]

            annotations = ["F"] * random_repeat_idx
            annotations.extend(["D"] * degree)
            annotations.extend(["F"] * (len(fluent_tokens) - random_repeat_idx))

        if len(annotations) != len(disfluent_tokens):
            print("Warning! Incompatible length between annotations and disfluent tokens.Ignoring this sequence...")
            return none_tuple

        disfluent_sentence = " ".join(disfluent_tokens)

        return disfluent_sentence, fluent_tokens, disfluent_tokens, annotations, degree

    def create_restarts(self, fluent_sentence_1, fluent_sentence_2):
        """ Create restarts.
                This function is used to create restarts, given two different fluent sequences.

                Args:
                    fluent_sentence_1 (`str`): A fluent text sequence

                    fluent_sentence_2 (`str`): A fluent text sequence, different from fluent_sentence_1

                Returns:
                    disfluent_sentence (`str`): The disfluent sentence with the corresponding restart

                    fluent_tokens (List[`str`]): List of fluent tokens of the fluent sequence

                    disfluent_tokens (List[`str`]): List of disfluent tokens of the disfluent sequence

                    annotations (List[`str`]): List of token-level annotations for the disfluent tokens
                    (F: Fluent, D: Disfluent)
                """
        if not fluent_sentence_1 or not fluent_sentence_2:
            raise TypeError('''A 'NoneType' object received while a 'str' object is required.''')
        else:
            # Tokenize both sentences
            fluent_for_disfluent_tokens = nltk.word_tokenize(fluent_sentence_1)
            fluent_tokens = nltk.word_tokenize(fluent_sentence_2)

        disfl_type = 'restart'

        # For creating a realistic restart we need sequences with 4 tokens or more
        if len(fluent_for_disfluent_tokens) < 4 or len(fluent_tokens) < 4:
            print("Warning! For creating a restart, we need sentences with 4 or more tokens. Ignoring this sequence...")
            return none_tuple

        # Select the position of restart (We opt for creating restarts in the beginning of the sentence)
        random_location_idx = randrange(2, math.ceil(len(fluent_for_disfluent_tokens) / 2) + 2)

        if all(fluent_for_disfluent_tokens[i] == fluent_tokens[i] for i in range(random_location_idx)):
            print("Warning! Same sequence is detected, aborted to avoid creating a repetition instead of restart...")
            return none_tuple

        else:
            discarded_tokens = fluent_for_disfluent_tokens[:random_location_idx]

        if discarded_tokens[0].lower() == fluent_tokens[0].lower():
            print(
                "Warning! First token of correction is the same with the first token of the disfluency, aborted to avoid "
                "creating "
                "a replacement instead of restart...")
            return none_tuple

        elif discarded_tokens[-1].lower() == fluent_tokens[0].lower():
            print("Warning! Consecutive tokens are detected, aborted to avoid creating a repetition instead of restart...")
            return none_tuple

        disfluent_tokens = fluent_for_disfluent_tokens[:random_location_idx] + fluent_tokens
        annotations = ["D"] * random_location_idx
        annotations.extend(["F"] * (len(fluent_tokens)))

        disfluent_sentence = " ".join(disfluent_tokens)

        if len(annotations) != len(disfluent_tokens):
            print("Warning! Incompatible length between annotations and disfluent tokens.")
            print("Ignoring this sequence...\n")
            return none_tuple

        return disfluent_sentence, fluent_tokens, disfluent_tokens, annotations, disfl_type

    def create_replacements(self, fluent_sentence, candidate_pos=None, with_cue=True):
        """ Create restarts.
                 This function is used to create replacements, given two different fluent sequences.

                 Args:
                     fluent_sentence (`str`): A fluent text sequence

                     candidate_pos (`str`, *optional*, defaults to None): The desired candidate part of speech
                     to create the replacement. Supported values VERB, NOUN, ADJ for verb, noun and adjective.
                     If not specified the default value is set to None and the candidate pos is randomly
                     initialized inside the function.

                     with_cue (`bool`, *optional*, defaults to True): Whether or not to create replacement with
                     repair cue. If not specified the default value is set to True.

                 Returns:
                     disfluent_sentence (`str`): The disfluent sentence with the corresponding replacement

                     fluent_tokens (List[`str`]): List of fluent tokens of the fluent sequence

                     disfluent_tokens (List[`str`]): List of disfluent tokens of the disfluent sequence

                     annotations (List[`str`]): List of token-level annotations for the disfluent tokens
                     (F: Fluent, D: Disfluent)
                 """

        if not fluent_sentence:
            raise TypeError('''A 'NoneType' object received while a 'str' object is required.''')
        else:
            # Tokenize the sentence
            fluent_tokens = nltk.word_tokenize(fluent_sentence)
            if len(fluent_tokens) < 2:
                print("Warning! We need at least two tokens to create a replacement. Ignoring this sequence...")
                return none_tuple
            # Find pos tag for each token
            pos_tags = nltk.pos_tag(fluent_tokens)

        if with_cue:
            disfl_type = candidate_pos.lower() + "_with_cue"
        else:
            disfl_type = candidate_pos.lower() + "_without_cue"

        # Create list for all possible replacement candidates
        candidates = []

        # If pos is in the tag list keep the corresponding token as a candidate
        for i in range(len(pos_tags)):
            for t in utils.extract_pos_format(candidate_pos):
                if pos_tags[i][1] == t:
                    candidates.append((pos_tags[i][0], i, t))


        # If there is no possible candidate for replacement in the input sentence
        if len(candidates) == 0:
            print("Warning! There is no possible replacement in this sentence. Ignoring this sequence...")
            return none_tuple

        # Select randomly a candidate token to replace
        random_candidate_idx = randrange(len(candidates))
        # Extract pos
        non_formatted_pos = candidates[random_candidate_idx][2]
        # Revert pos to the right form for NLTK library
        formatted_pos = utils.revert_pos_format(non_formatted_pos)

        # Find synonyms and antonyms
        synonyms, antonyms = utils.extract_syns_ants(candidates[random_candidate_idx][0], formatted_pos)

        possible_replacements = synonyms + antonyms

        if len(possible_replacements) > 0:
            try:
                replaced_candidate = random.choice(
                    [possible_replacements[idx] for idx in range(len(possible_replacements)) if
                     possible_replacements[idx].lower() != candidates[random_candidate_idx][0].lower()])
            except IndexError:
                print(Fore.RED + "Warning: You try to pass an input sequence where there are not available "
                                 "repair tokens for creating a replacement. Ignoring this sequence...")
                return none_tuple

            degree_range = len(fluent_tokens) - random_candidate_idx
            random_degree = random.randrange(0, degree_range)

            # Ensure that the random degree is valid
            if candidates[random_candidate_idx][1] - random_degree < 0:
                return none_tuple

            # Fill the new sentence and annotate until the begging of reparandum
            disfluent_tokens = fluent_tokens[:candidates[random_candidate_idx][1]]
            annotations = ["F"] * (candidates[random_candidate_idx][1] - random_degree)

            # Some tokens are returned with "_" so we split them to get the actual tokens
            replaced_candidate = replaced_candidate.split("_")

            # If the last token of the replaced candidate is the same with repair return empty lists
            # (to ensure no conflict with repeats)
            if replaced_candidate[-1].lower() == candidates[random_candidate_idx][0].lower():
                print("Warning! Consecutive words detected, aborted to avoid creating "
                      "a repetition instead of replacement...")

            # We begin to annotate
            # Create the annotations based on the degree of replace
            if random_degree == 0:
                if len(replaced_candidate) == 1:
                    annotations.append("D")
                    disfluent_tokens.append(replaced_candidate[0])

                if len(replaced_candidate) == 2:
                    annotations.extend(["D"] * 2)
                    annotations.append(replaced_candidate[0])
                    annotations.append(replaced_candidate[1])

                elif len(replaced_candidate) > 2:
                    annotations.append("D")

                    for i in range(len(replaced_candidate)):
                        disfluent_tokens.append(replaced_candidate[i])

                    annotations.extend(["D"] * (len(replaced_candidate)))

            if random_degree >= 1:
                annotations.extend(["D"] * random_degree)

                for i in range(len(replaced_candidate)):
                    annotations.append("D")
                    disfluent_tokens.append(replaced_candidate[i])

                annotations[-1] = "D"

            # If we want to add repair cues between RM and RP
            if with_cue:
                random_repair_cue_idx = randrange(len(utils.REPAIR_CUES))

                disfluent_tokens.append(utils.REPAIR_CUES[random_repair_cue_idx][0])

                for i in range(utils.REPAIR_CUES[random_repair_cue_idx][1]):
                    annotations.append("D")

            annotations.extend(["F"] * (random_degree + 1))

            # Continue filling the sentence and the annotations with the rest tokens
            disfluent_tokens = disfluent_tokens + fluent_tokens[candidates[random_candidate_idx][1] - random_degree:]
            rest = len(fluent_tokens) - candidates[random_candidate_idx][1]
            annotations.extend(["F"] * (rest - 1))

            # Join sentence tokens
            disfluent_sentence = " ".join(disfluent_tokens)

            disfluent_tokens = nltk.word_tokenize(disfluent_sentence)

        else:
            print("Warning! No available candidates for creating a replacement. Ignoring this sequence...")
            return none_tuple

        if len(annotations) != len(disfluent_tokens):
            print("Warning! Incompatible length between annotations and disfluent tokens. Ignoring this sequence...")
            return none_tuple

        return disfluent_sentence, fluent_tokens, disfluent_tokens, annotations, disfl_type
