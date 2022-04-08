from python_files.disfluency_generation import LARD


if __name__ == "__main__":

    # Initialize lard tool
    lard = LARD()

    # Generate repetitions
    fluent_sentence = "Hello are you up for a coffee this friday ?"
    # This is a first-degree repetition
    disfluency = lard.create_repetitions(fluent_sentence, 1)
    print(disfluency[0])

    # This is a second-degree repetition
    disfluency = lard.create_repetitions(fluent_sentence, 2)
    print(disfluency[0])

    #  Generate replacements
    fluent_sentence = "Yes, I am going to visit my family for a week"
    disfluency = lard.create_replacements(fluent_sentence)
    print(disfluency[0])

    fluent_sentence = "i prefer to drink coffee without sugar"
    disfluency = lard.create_replacements(fluent_sentence)
    print(disfluency[0])

    # Generate restarts
    fluent_sentence_1 = "where can i find a pharmacy near me ?"
    fluent_sentence_2 = "what time do you close ?"
    disfluency = lard.create_restarts(fluent_sentence_1, fluent_sentence_2)
    print(disfluency[0])



