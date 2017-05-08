import syllables as syl
import pronouncing 
import random

pronouncing.init_cmu()
valid_words = pronouncing.lookup.keys()
valid_words.sort()

# make lists of words that are 8 syllables or less, 7 syllables or less, 6 or less, etc down to 1
# store as variables so we don't have to run that regex over and over
n_syllables_or_less = {}
for i in range(1, 10):
    regex = "^[A-Z\s]*(([A-Z]{2}[0-9])[\sA-Z]*){,%d}$" % i 
    n_syllables_or_less[i] = pronouncing.search(regex)


def valid_rhymes(word, num_syllables=8):
    word_rhymes = pronouncing.rhymes(word)
    word_valid_rhymes = filter(lambda(w): w in n_syllables_or_less[num_syllables], word_rhymes)
    return word_valid_rhymes


def choose_from_rhymes(rhymes):
    choice = random.choice(rhymes)
    rhymes.remove(choice)
    return choice


def starting_words(num_rhymes=3, num_syllables=8):
    # num_rhymes is the number of total words returned
    done = False
    word = ""
    word_valid_rhymes = []
    while not done:
        word = random.choice(n_syllables_or_less[num_syllables])
        word_valid_rhymes = valid_rhymes(word, num_syllables)
        if len(word_valid_rhymes) >= num_rhymes:
            done = True
    # "word" is the starting word
    words = [word]
    while len(words) < num_rhymes:
        words.append(choose_from_rhymes(word_valid_rhymes))
    return words
    # find word less than or equal to 8 syllables that has rhymes that are 8 syllables or less
    # make a list of those valid rhymes
    # choose 2 distinct words from that list
    # find word less than or equal to 5 syllables that has rhymes that are 5 syllables or less
    # make a list of those valid rhymes
    # choose 1 word from that list


def prepend_sentence(sentence, max_syllables):
    current_syllables = syl.sentence_syllables(sentence)
    needed_syllables = max_syllables - current_syllables
    new_word = random.choice(n_syllables_or_less[needed_syllables])
    prepended_sentence = new_word+" "+sentence
    return prepended_sentence


def fill_sentence(sentence, max_syllables):
    while syl.sentence_syllables(sentence) < max_syllables:
        sentence = prepend_sentence(sentence, max_syllables)
    return sentence


def generate_limerick(triplet_syllables=8, doublet_syllables=5):
    starting_triplet = starting_words(num_rhymes=3, num_syllables=triplet_syllables)
    starting_doublet = starting_words(num_rhymes=2, num_syllables=doublet_syllables)
    triplet = []
    doublet = []
    for i in range(0, 3):
        sentence = starting_triplet[i]
        sentence = fill_sentence(sentence, triplet_syllables)
        # while syl.sentence_syllables(sentence) < triplet_syllables:
        #     sentence = prepend_sentence(sentence, triplet_syllables)
        triplet.append(sentence)
    for i in range(0, 2):
        sentence = starting_doublet[i]
        sentence = fill_sentence(sentence, doublet_syllables)
        # while syl.sentence_syllables(sentence) < doublet_syllables:
        #     sentence = prepend_sentence(sentence, doublet_syllables)
        doublet.append(sentence)
    limerick_list = [triplet[0], triplet[1], doublet[0], doublet[1], triplet[2]]
    limerick = "\n".join(limerick_list)
    return limerick


if __name__ == "__main__":
    for i in range(100):
        print "______________________"
        print generate_limerick(9, 6)
        print "\n"
