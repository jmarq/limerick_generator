import syllables as syl
import pronouncing
import random
import re


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




def parse_rhyme_pattern(rhyme_pattern):
    # "there once was a @4a, who @7a, and @4b, so @4b, @8a"
    # [(a,4),(a,7),(b,4),(b,4),(a,8)]
    # @4* could be any 4 syllable "phrase" TODO

    # find all the rhyme symbols in the pattern
    rhyme_symbols = re.findall("@[1-9]+[A-Za-z]", rhyme_pattern)
    phrase_formats = []

    for symbol in rhyme_symbols:
        symbol_id = symbol[-1]
        symbol_syllables = int(re.findall("[0-9]+", symbol)[0])
        phrase_formats.append((symbol_id, symbol_syllables))
    return phrase_formats


def generate_pattern_stats(phrase_formats):
    # [(a,4),(b,4),(a,2)]
    # a: max_syllables: 4, rhymes: 2, b: max_syllables: 4, rhymes: 1
    stats = {}
    symbols = list(set(map(lambda(f): f[0], phrase_formats)))
    for symbol in symbols:
        filtered = filter(lambda(f): f[0] == symbol, phrase_formats)
        count = len(filtered)
        max_syllables = max(map(lambda(f): f[1], filtered))
        stats[symbol] = {
            "max_syllables": max_syllables,
            "count": count
        }
    return stats


def generate_starting_words(pattern_stats):
    for symbol in pattern_stats.keys():
        symbol_stats = pattern_stats[symbol]
        symbol_stats["rhymes"] = starting_words(symbol_stats["count"], symbol_stats["max_syllables"])


def generate_poem(rhyme_pattern):
    phrase_formats = parse_rhyme_pattern(rhyme_pattern)
    pattern_stats = generate_pattern_stats(phrase_formats)
    generate_starting_words(pattern_stats)
    phrases = []
    for phrase in phrase_formats:
        rhyme_phrase = pattern_stats[phrase[0]]["rhymes"].pop()
        rhyme_phrase = fill_sentence(rhyme_phrase, phrase[1])
        phrases.append(rhyme_phrase)
    rhyme_pattern_template = re.sub("@[1-9]+[A-Za-z]", "%s", rhyme_pattern)
    return rhyme_pattern_template % tuple(phrases)

limerick_patterns = ["@8a\n@8a\n@5b\n@5b\n@8a", "@9a\n@9a\n@6b\n@6b\n@9a"]

if __name__ == "__main__":
    print generate_poem(limerick_patterns[0]+"\n-----------------")
    print generate_poem("@2a @2b, @2a @2b, @5c\n"*2+"-----------------")
    print "\n"
    print generate_poem("@1a @1b @1c @1d @1e\n"*2)
    print generate_poem(("@1a "*4+": @2b\n")*2)
