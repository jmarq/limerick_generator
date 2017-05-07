from limerick import starting_words, prepend_sentence
import syllables
import re


def parse_rhyme_pattern(rhyme_pattern):
    # "there once was a @4a, who @7a, and @4b, so @4b, @8a"
    # [(a,4),(a,7),(b,4),(b,4),(a,8)]
    # @4* could be any 4 syllable "phrase"

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
    symbols = list(set(map(lambda(f):f[0],phrase_formats)))
    for symbol in symbols:
        filtered = filter(lambda(f):f[0]==symbol,phrase_formats)
        count = len(filtered)
        max_syllables = max(map(lambda(f):f[1],filtered))
        stats[symbol] = {
            "max_syllables": max_syllables,
            "count": count
        }
    return stats


def generate_starting_words(pattern_stats):
    for symbol in pattern_stats.keys():
        symbol_stats = pattern_stats[symbol]
        symbol_stats["rhymes"] = starting_words(symbol_stats["count"],symbol_stats["max_syllables"])


def fill_sentence(sentence, max_syllables):
    while syllables.sentence_syllables(sentence) < max_syllables:
        sentence = prepend_sentence(sentence, max_syllables)
    return sentence


def generate_poem(rhyme_pattern):
    phrase_formats = parse_rhyme_pattern(rhyme_pattern)
    pattern_stats = generate_pattern_stats(phrase_formats)
    generate_starting_words(pattern_stats)
    phrases = []
    for phrase in phrase_formats:
        rhyme_phrase = pattern_stats[phrase[0]]["rhymes"].pop()
        rhyme_phrase = fill_sentence(rhyme_phrase,phrase[1])
        phrases.append(rhyme_phrase)
    rhyme_pattern_template = re.sub("@[1-9]+[A-Za-z]", "%s", rhyme_pattern)
    return rhyme_pattern_template % tuple(phrases)



if __name__ == "__main__":
    print generate_poem("@8a\n@8a\n@5b\n@5b\n@8a\n-----------------")
    print generate_poem("@2a @2b, @2a @2b, @5c\n"*2+"-----------------")
    print "\n"
    print generate_poem("@1a @1b @1c @1d @1e\n"*2)
    print generate_poem(("@1a "*4+": @2b\n")*2)
