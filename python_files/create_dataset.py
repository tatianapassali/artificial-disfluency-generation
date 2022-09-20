import nltk
import os
import pandas as pd
import numpy as np
from colorama import Fore
from python_files.disfluency_generation import LARD
import random
from colorama import init

init(autoreset=True)

FLUENT_PERC = [50, 30, 10, 10]
DISFLUENT_PERC = [50, 25, 25]
REPEAT_PERC = [40, 30, 30]
REPLACE_PERC = [20, 15, 20, 15, 20, 10]

lard = LARD()


def create_dataset(input_file_path,
                   column_text,
                   output_dir=None,
                   keep_fluent=False,
                   percentages=None,
                   percentages_with_fluent=None,
                   repetition_degrees_percentage=None,
                   replacement_types_percentage=None,
                   create_all_files=True,
                   concat_files=True):
    """
    This function is used to create multiple disfluencies (repetition, restarts and replacements) from fluent text
    from a .csv file.

    Args:
            input_file_path (`str`): The path of the input file. The input file must be formatted as
            a .csv file with one or more column and a least one text column that you want to generate
            the disfluencies. To see a sample data file, please refer to the data/sample_data directory.

            output_dir (`int`, *optional*, defaults to 'None'): The directory to store the created files.
            If it is not specified, the data are stored by default to ./data/output_data directory.

            column_text (`str`): The column that contains the fluent text.

            keep_fluent (`bool`, *optional*, defaults to False): Whether or not to keep some fluencies along
            with the disfluencies. If it is not specified, the default value is set to False.

            percentages (List[`int`], *optional*, defaults to 'None'): A list with the percentages of different types
            of disfluencies. The first value refers to the percentage of repetitions, the second value refers to the
            percentage of restarts and the third value refers to the percentage of replacements. All the values must
            sum to 100. If it is not specified, the default value is set to  [50, 25, 25], where 50% of the input
            text will be repetitions, 25% restarts and 25% replacements.

            percentages_with_fluent(List[`int`], *optional*, defaults to 'None'): A list with the percentages of
            different types of disfluencies, when keep_fluent = True. The first value refers to the percentage of
            fluencies, the second value refers to the percentage of repetitions, the third value refers to the
            percentage of restarts and the fourth value refers to the percentage of replacements. All the values
            must sum to 100.If it is not specified, the default value is set to [50, 30, 10, 10], where 50% of
            the input text will be fluencies, 30% will be repetitions, 10% restarts and 10% replacements.

            repetition_degrees_percentage (List[`int`], *optional*, defaults to 'None'): A list with the percentages
            of different types of repetitions. The first value refers to the percentage of first-degree repetitions,
            the second value refers to the percentage of second-degree repetitions and the third value refers to the
            percentage of  third-degree repetitions. All the values must sum to 100. If it is not specified, the default
            value is set to [40, 30, 30] where 450% of the repetition set will be first-degree repetitions, 30%  will be
            second-degree repetitions and 30% will be third-degree repetitions.

            replacement_types_percentage (List[`int`], *optional*, defaults to 'None'): A list with the percentages
            of different types of repetitions. The first value refers to the percentage of noun replacements with repair
            cue, the second value refers to the percentage of noun replacements without repair cue, the third value
            refers to the percentage of verb replacement with repair cue, the fourth value refers to the percentage
            of verb replacement without repair cue, the fifth value refers to the percentage of adjective replacement
            with repair cue and the sixth value refers to the percentage of adjective replacement without repair cue.
            All the values must sum to 100. If it is not specified, the default value is set to [20, 15, 20, 15, 20, 10],
            where 20% of replacement set are noun replacements with cue,
                  15% noun replacements without cue,
                  20% verb replacement with cue,
                  15% verb replacement without cue,
                  20% adjective replacement with cue,
                  10% adjective replacement without cue.

            create_all_files (`bool`, *optional*, defaults to True): Whether or not to save all different types of
            disfluencies. If not specified, the default value is set to True.

            concat_files (`bool`, *optional*, defaults to True): Whether or not to concat into a final file all
            the different types of disfluencies. If not specified, the default value is set to True.

    """

    final_df = pd.DataFrame()

    if input_file_path.lower().endswith(".csv"):
        fluent_data = pd.read_csv(input_file_path)
        if column_text is None:
            raise ValueError("You have to specify text column.")
    else:
        fluent_data = None
        print("You have to input a supported format input file. Supported formats: .csv or .json")

    if output_dir is None:
        output_dir = os.getcwd() + '/data/output_data'

    if keep_fluent:
        if percentages is not None:
            raise ValueError(
                "You have to specify percentages with fluent instead of percentages, when keep_fluent is set to True.")

        if percentages_with_fluent is None:
            # If not specified from user, set to default percentages
            print("Percentages were not specified from user.")
            print("Setting percentages to default values...")
            print("To change these values, please specify the percentages_with_fluent parameter.\n")
            percentages = FLUENT_PERC

        if percentages_with_fluent is not None:
            if sum(percentages_with_fluent) != 100:
                raise ValueError("The sum of percentages must be 100.")
            if len(percentages_with_fluent) != 4:
                raise ValueError("A list with length " + str(
                    len(percentages_with_fluent)) + " is passed. You have to input a list with length 4.")
            else:
                print("Setting percentages...\n")

            fluencies = percentages_with_fluent[0]
            repetitions = percentages_with_fluent[1]
            restarts = percentages_with_fluent[2]
            replacements = percentages_with_fluent[3]

            print("Fluencies: " + str(fluencies) + "%")
            print("Repetitions: " + str(repetitions) + "%")
            print("Restarts: " + str(restarts) + "%")
            print("Replacements: " + str(replacements) + "%\n")

            first_split = fluencies / 100
            second_split = first_split + repetitions / 100
            third_split = second_split + restarts / 100

            fluent_set, repetition_set, restart_set, replacement_set = np.split(fluent_data,
                                                                                [int(first_split * len(fluent_data)),
                                                                                 int(second_split * len(fluent_data)),
                                                                                 int(third_split * len(fluent_data))])

            fluent_set = create_disfluencies(fluent_set, column_text, 'fluency')

            if create_all_files:
                fluent_set.to_csv(output_dir + "/fluencies.csv", index=False)
                print(Fore.GREEN + u'\u2713' + " Saving to individual files completed")

            if concat_files:
                final_df = final_df.append(fluent_set, ignore_index=True)

            if repetition_degrees_percentage is None and percentages_with_fluent[1] != 0:
                print("Repetitions percentages were not specified from user.")
                print("Setting repetitions percentages to default values...")
                print("To change these values, please specify the percentages parameter.\n")

                repetition_degrees_percentage = REPEAT_PERC

            if repetition_degrees_percentage is not None and percentages_with_fluent[1] == 0:
                raise ValueError(
                    "The percentage of repetitions must be more than 0, when repetition_degrees_percentage is set.")

            if repetition_degrees_percentage is not None and percentages_with_fluent[1] != 0:
                if sum(repetition_degrees_percentage) != 100:
                    raise ValueError("The sum of percentages must be 100.")
                if len(repetition_degrees_percentage) != 3:
                    raise ValueError(
                        "A list with length " + str(
                            len(repetition_degrees_percentage)) + " is passed. You have to input a list with length 3.")
                else:
                    print("Setting percentages...\n")
            if percentages_with_fluent[1] != 0:
                one_reps = repetition_degrees_percentage[0]
                two_reps = repetition_degrees_percentage[1]
                three_reps = repetition_degrees_percentage[2]

                print("One-degree repetitions: " + str(one_reps) + "%")
                print("Second-degree repetitions: " + str(two_reps) + "%")
                print("Third-degree repetitions: " + str(three_reps) + "%")

                first_split = int(one_reps / 100)
                second_split = first_split + int(two_reps / 100)

                one_reps_set, two_reps_set, three_reps_set = np.split(repetition_set,
                                                                      [int(first_split * len(fluent_data)),
                                                                       int(second_split * len(
                                                                           fluent_data))])

                print("Creating repetitions...")

                one_reps_set = create_disfluencies(one_reps_set, column_text, 'repetition', degree=1)
                two_reps_set = create_disfluencies(two_reps_set, column_text, 'repetition', degree=2)
                three_reps_set = create_disfluencies(three_reps_set, column_text, 'repetition', degree=3)

                print(Fore.GREEN + u'\u2713' + " Creating repetition completed")
                repeat_frames = [one_reps_set, two_reps_set, three_reps_set]
                final_repeats = pd.concat(repeat_frames)

                if create_all_files:
                    print("Saving to individual files...")
                    final_repeats.to_csv(output_dir + "/repeat.csv", index=False)
                    print(Fore.GREEN + u'\u2713' + " Saving to individual files completed")

                if concat_files:
                    final_df = final_df.append(final_repeats, ignore_index=True)

            if percentages_with_fluent[2] != 0:
                print("Creating restarts...")
                restart_set = create_disfluencies(restart_set, column_text, 'restart')
                print(Fore.GREEN + u'\u2713' + " Creating restarts completed")

                if create_all_files:
                    print("Saving to individual files...")
                    restart_set.to_csv(output_dir + "/restarts.csv", index=False)

                if concat_files:
                    final_df = final_df.append(restart_set, ignore_index=True)

            if replacement_types_percentage is None and percentages_with_fluent[3] != 0:
                print("Replacements percentages were not specified from user.")
                print("Setting replacements percentages to default values...")
                print("To change these values, please specify the percentages parameter.\n")

                replacement_types_percentage = REPLACE_PERC

            if replacement_types_percentage is not None and percentages_with_fluent[3] == 0:
                raise ValueError(
                    "The percentage of replacements must be more than 0, when replacement_types_percentage is set.")

            if replacement_types_percentage is not None and percentages_with_fluent[3] != 0:
                if sum(replacement_types_percentage) != 100:
                    raise ValueError("The sum of percentages must be 100.")
                if len(replacement_types_percentage) != 6:
                    raise ValueError(
                        "A list with length " + str(
                            len(replacement_types_percentage)) + " is passed. You have to input a list with length 6.")
                else:
                    print("Setting percentages...\n")

            if percentages_with_fluent[3] != 0:
                noun_with_cue = replacement_types_percentage[0]
                noun_without_cue = replacement_types_percentage[1]
                verb_with_cue = replacement_types_percentage[2]
                verb_without_cue = replacement_types_percentage[3]
                adj_with_cue = replacement_types_percentage[4]
                adj_without_cue = replacement_types_percentage[5]

                print("Noun replacements with repair cue: " + str(noun_with_cue) + "%")
                print("Noun replacements without repair cue: " + str(noun_without_cue) + "%")
                print("Verb replacements with repair cue: " + str(verb_with_cue) + "%")
                print("Verb replacements without repair cue: " + str(verb_without_cue) + "%")
                print("Adjective replacements with repair cue: " + str(adj_with_cue) + "%")
                print("Adjective replacements without repair cue: " + str(adj_without_cue) + "%\n")

                first_split = noun_with_cue / 100
                second_split = first_split + noun_without_cue / 100
                third_split = second_split + verb_with_cue / 100
                fourth_split = third_split + verb_without_cue / 100
                fifth_split = fourth_split + adj_with_cue / 100

                
                noun_with_cue_set, noun_without_cue_set, \
                verb_with_cue_set, verb_without_cue_set, \
                adj_with_cue_set, adj_without_cue_set = np.split(replacement_set,
                                                                 [int(first_split * len(fluent_data)),
                                                                  int(second_split * len(fluent_data)),
                                                                  int(third_split * len(fluent_data)),
                                                                  int(fourth_split * len(fluent_data)),
                                                                  int(fifth_split * len(fluent_data))])

                print("Creating replacements...")
                print("Warning: This process might take a little longer, especially if you process a large dataset.")

                noun_with_cue_set = create_disfluencies(noun_with_cue_set, column_text, 'replacement', pos='NOUN',
                                                        condition="with_cue")
                noun_without_cue_set = create_disfluencies(noun_without_cue_set, column_text, 'replacement', pos='NOUN',
                                                           condition="without_cue")
                verb_with_cue_set = create_disfluencies(verb_with_cue_set, column_text, 'replacement', pos='VERB',
                                                        condition="with_cue")
                verb_without_cue_set = create_disfluencies(verb_without_cue_set, column_text, 'replacement', pos='VERB',
                                                           condition="without_cue")
                adj_with_cue_set = create_disfluencies(adj_with_cue_set, column_text, 'replacement', pos='ADJ',
                                                       condition="with_cue")
                adj_without_cue_set = create_disfluencies(adj_without_cue_set, column_text, 'replacement', pos='ADJ',
                                                          condition="without_cue")

                print(Fore.GREEN + u'\u2713' + " Creating replacements completed")

                replacement_frames = [noun_with_cue_set,
                                      noun_without_cue_set,
                                      verb_with_cue_set,
                                      verb_without_cue_set,
                                      adj_with_cue_set,
                                      adj_without_cue_set]

                final_replacements = pd.concat(replacement_frames)

                if create_all_files:
                    print("Saving to individual files...")
                    final_replacements.to_csv(output_dir + "/replacements.csv", index=False)
                    print(Fore.GREEN + u'\u2713' + " Saving to individual files completed")

                if concat_files:
                    final_df = final_df.append(final_replacements, ignore_index=True)

    if not keep_fluent:
        if percentages_with_fluent is not None:
            raise ValueError(
                "You have to specify percentages instead of percentages_with_fluent, when keep_fluent is set to False.")

        if percentages is None:
            # If not specified from user, set to default percentages
            print("Percentages were not specified from user.")
            print("Setting percentages to default values...")
            print("To change these values, please specify the percentages parameter.\n")
            percentages = DISFLUENT_PERC

        if percentages is not None:
            if sum(percentages) != 100:
                raise ValueError("The sum of percentages must be 100.")
            if len(percentages) != 3:
                raise ValueError(
                    "A list with length " + str(
                        len(percentages)) + " is passed. You have to input a list with length 3.")
            else:
                print("Setting percentages...")

        repetitions = percentages[0]
        restarts = percentages[1]
        replacements = percentages[2]
        print("Repetitions: " + str(repetitions) + "%")
        print("Restarts: " + str(restarts) + "%")
        print("Replacements: " + str(replacements) + "%")

        first_split = repetitions / 100
        second_split = first_split + restarts / 100

        repetition_set, restart_set, replacement_set = np.split(fluent_data, [int(first_split * len(fluent_data)),
                                                                              int(second_split * len(fluent_data))])

        if repetition_degrees_percentage is None and percentages[0] != 0:
            print("Repetitions percentages were not specified from user.")
            print("Setting repetitions percentages to default values...")
            print("To change these values, please specify the percentages parameter.\n")

            repetition_degrees_percentage = REPEAT_PERC

        if repetition_degrees_percentage is not None and percentages[0] == 0:
            raise ValueError(
                "The percentage of repetitions must be more than 0, when repetition_degrees_percentage is set.")

        if repetition_degrees_percentage is not None and percentages[0] != 0:
            if sum(repetition_degrees_percentage) != 100:
                raise ValueError("The sum of percentages must be 100.")
            if len(repetition_degrees_percentage) != 3:
                raise ValueError(
                    "A list with length " + str(
                        len(repetition_degrees_percentage)) + " is passed. You have to input a list with length 3.")
            else:
                print("Setting percentages...")

            one_reps = repetition_degrees_percentage[0]
            two_reps = repetition_degrees_percentage[1]
            three_reps = repetition_degrees_percentage[2]

            print("One-degree repetitions: " + str(one_reps) + "%")
            print("Second-degree repetitions: " + str(two_reps) + "%")
            print("Third-degree repetitions: " + str(three_reps) + "%\n")

            first_split = one_reps / 100
            second_split = first_split + two_reps / 100

            one_reps_set, two_reps_set, three_reps_set = np.split(repetition_set, [int(first_split * len(fluent_data)),
                                                                                   int(second_split * len(
                                                                                       fluent_data))])

            print("Creating repetitions...")
            one_reps_set = create_disfluencies(one_reps_set, column_text, 'repetition', degree=1)
            two_reps_set = create_disfluencies(two_reps_set, column_text, 'repetition', degree=2)
            three_reps_set = create_disfluencies(three_reps_set, column_text, 'repetition', degree=3)
            print(Fore.GREEN + u'\u2713' + " Creating repetition completed")
            repeat_frames = [one_reps_set, two_reps_set, three_reps_set]
            final_repeats = pd.concat(repeat_frames)

            if create_all_files:
                print("Saving to individual files...")

                final_repeats.to_csv(output_dir + "/repeat.csv", index=False)
                print(Fore.GREEN + u'\u2713' + " Saving to individual files completed")

            if concat_files:
                final_df = final_df.append(final_repeats, ignore_index=True)

        if percentages[1] != 0:
            print("Creating restarts...")
            restart_set = create_disfluencies(restart_set, column_text, 'restart')
            print(Fore.GREEN + u'\u2713' + " Creating restarts completed")

            if create_all_files:
                print("Saving to individual files...")
                restart_set.to_csv(output_dir + "/restarts.csv", index=False)

            if concat_files:
                final_df = final_df.append(restart_set, ignore_index=True)

        if replacement_types_percentage is None and percentages[2] != 0:
            print("Replacements percentages were not specified from user.")
            print("Setting replacements percentages to default values...")
            print("To change these values, please specify the percentages parameter.\n")

            replacement_types_percentage = REPLACE_PERC

        if replacement_types_percentage is not None and percentages[2] == 0:
            raise ValueError(
                "The percentage of replacements must be more than 0, when replacement_types_percentage is set.")

        if replacement_types_percentage is not None and percentages[2] != 0:
            if sum(replacement_types_percentage) != 100:
                raise ValueError("The sum of percentages must be 100.")
            if len(replacement_types_percentage) != 6:
                raise ValueError(
                    "A list with length " + str(
                        len(replacement_types_percentage)) + " is passed. You have to input a list with length 6.")
            else:
                print("Setting percentages...\n")

        if percentages[2] != 0:
            noun_with_cue = replacement_types_percentage[0]
            noun_without_cue = replacement_types_percentage[1]
            verb_with_cue = replacement_types_percentage[2]
            verb_without_cue = replacement_types_percentage[3]
            adj_with_cue = replacement_types_percentage[4]
            adj_without_cue = replacement_types_percentage[5]

            print("Noun replacements with repair cue: " + str(noun_with_cue) + "%")
            print("Noun replacements without repair cue: " + str(noun_without_cue) + "%")
            print("Verb replacements with repair cue: " + str(verb_with_cue) + "%")
            print("Verb replacements without repair cue: " + str(verb_without_cue) + "%")
            print("Adjective replacements with repair cue: " + str(adj_with_cue) + "%")
            print("Adjective replacements without repair cue: " + str(adj_without_cue) + "%\n")

            first_split = noun_with_cue / 100
            second_split = first_split + noun_without_cue / 100
            third_split = second_split + verb_with_cue / 100
            fourth_split = third_split + verb_without_cue / 100
            fifth_split = fourth_split + adj_with_cue / 100

            noun_with_cue_set, noun_without_cue_set, \
            verb_with_cue_set, verb_without_cue_set, \
            adj_with_cue_set, adj_without_cue_set = \
                np.split(replacement_set, [int(first_split * len(fluent_data)),
                                           int(second_split * len(fluent_data)),
                                           int(third_split * len(fluent_data)),
                                           int(fourth_split * len(fluent_data)),
                                           int(fifth_split * len(fluent_data))])
            print("Creating replacements...")
            print("Warning: This process might take a little longer, especially if you process a large dataset.")

            noun_with_cue_set = create_disfluencies(noun_with_cue_set, column_text, 'replacement', pos='NOUN',
                                                    condition="with_cue")
            noun_without_cue_set = create_disfluencies(noun_without_cue_set, column_text, 'replacement', pos='NOUN',
                                                       condition="without_cue")
            verb_with_cue_set = create_disfluencies(verb_with_cue_set, column_text, 'replacement', pos='VERB',
                                                    condition="with_cue")
            verb_without_cue_set = create_disfluencies(verb_without_cue_set, column_text, 'replacement', pos='VERB',
                                                       condition="without_cue")
            adj_with_cue_set = create_disfluencies(adj_with_cue_set, column_text, 'replacement', pos='ADJ',
                                                   condition="with_cue")
            adj_without_cue_set = create_disfluencies(adj_without_cue_set, column_text, 'replacement', pos='ADJ',
                                                      condition="without_cue")

            print(Fore.GREEN + u'\u2713' + " Creating replacements completed")

            replacement_frames = [noun_with_cue_set,
                                  noun_without_cue_set,
                                  verb_with_cue_set,
                                  verb_without_cue_set,
                                  adj_with_cue_set,
                                  adj_without_cue_set]

            final_replacements = pd.concat(replacement_frames)

            if create_all_files:
                print("Saving to individual files...")
                final_replacements.to_csv(output_dir + "/replacements.csv", index=False)
                print(Fore.GREEN + u'\u2713' + " Saving to individual files completed")

            if concat_files:
                final_df = final_df.append(final_replacements, ignore_index=True)

    if concat_files:
        print("Concatenating and saving to file...")
        final_df.to_csv(output_dir + "/final_disfluent_set.csv", index=False)
        print(Fore.GREEN + u'\u2713' + " Saving completed")


def create_disfluencies(set, column_text, disfl_type, degree=None, pos=None, condition=None):
    if len(set) != 0:
        if disfl_type == 'repetition':
            set[['disfluent_sentence', 'fluent_tokens', 'disfluent_tokens',
                 'annotations', 'degree']] = set.apply(lambda row: lard.create_repetitions(row[column_text], degree),
                                                       axis=1,
                                                       result_type='expand')
            set['label'] = 1
            set['disfl_type'] = 'repetition'

        if disfl_type == 'replacement':
            if condition == 'with_cue':
                set[['disfluent_sentence', 'fluent_tokens', 'disfluent_tokens',
                     'annotations', 'disfl_type']] = set.apply(
                    lambda row: lard.create_replacements(row[column_text], pos, with_cue=True),
                    axis=1,
                    result_type='expand')
                set['label'] = 2
                set['degree'] = 'N/A'
            if condition == "without_cue":
                set[['disfluent_sentence', 'fluent_tokens', 'disfluent_tokens',
                     'annotations', 'disfl_type']] = set.apply(
                    lambda row: lard.create_replacements(row[column_text], pos, with_cue=False),
                    axis=1,
                    result_type='expand')
                set['label'] = 2
                set['degree'] = 'N/A'
        if disfl_type == 'fluency':
            set['fluent_tokens'] = set[column_text].apply(lambda x: nltk.word_tokenize(x))
            set['disfluent_tokens'] = set['fluent_tokens']

            set['disfluent_sentence'] = set[column_text]
            set['annotations'] = set.apply(lambda row: len(row['fluent_tokens']) * ["F"], axis=1)
            set['disfl_type'] = 'fluency'
            set['label'] = 0
            set['degree'] = 'N/A'

        if disfl_type == 'restart':
            disfluent_sentence = []
            fluent_tokens = []
            disfluent_tokens = []
            annotations = []
            disfl_type = []

            fluent_text = set[column_text].values.tolist()
            for i in range(len(fluent_text)):
                fluent_sentence_1 = random.choice(fluent_text)
                fluent_sentence_2 = fluent_text[i]

                if fluent_sentence_1 != fluent_sentence_2:
                    tmp_disfluent_sentence, tmp_fluent_tokens, tmp_disfluent_tokens, tmp_annotations, tmp_disfl_type = lard.create_restarts(
                        fluent_sentence_1, fluent_sentence_2)

                else:
                    tmp_disfluent_sentence, tmp_fluent_tokens, tmp_disfluent_tokens, tmp_annotations, tmp_disfl_type = None, None, None, None, None

                disfluent_sentence.append(tmp_disfluent_sentence)
                fluent_tokens.append(tmp_fluent_tokens)
                disfluent_tokens.append(tmp_disfluent_sentence)
                annotations.append(tmp_annotations)
                disfl_type.append(tmp_disfl_type)

            set['disfluent_sentence'] = disfluent_sentence
            set['fluent_tokens'] = fluent_tokens
            set['disfluent_tokens'] = disfluent_tokens
            set['annotations'] = annotations
            set['disfl_type'] = disfl_type
            set['degree'] = 'N/A'
            set['label'] = 3

        set = set.dropna()

        return set
