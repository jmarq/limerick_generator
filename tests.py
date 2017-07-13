import unittest
import syllables
import poem


class SyllablesTestCase(unittest.TestCase):
    def test_word_syllables(self):
        self.assertEquals(syllables.word_syllables("basketball"), 3)
        self.assertEquals(syllables.word_syllables(""), 0)

    def test_sentence_syllables(self):
        sentence = "Testing is fun"
        self.assertEquals(syllables.sentence_syllables(sentence), 4)


class PoemsTestCase(unittest.TestCase):
    def test_starting_words(self):
        num_syllables = 5
        num_rhymes = 3
        starting_words = poem.starting_words(num_rhymes=num_rhymes, num_syllables=num_syllables)
        # does the first starting word fit within the syllable limit?
        self.assertLessEqual(syllables.word_syllables(starting_words[0]), num_syllables)
        # does the second word rhyme with the first?
        self.assertTrue(starting_words[1] in poem.valid_rhymes(starting_words[0], num_syllables=num_syllables))
        # do we have enough rhymes?
        self.assertTrue(len(starting_words) == num_rhymes)


class RhymePatternTestCase(unittest.TestCase):
    def test_parse(self):
        pattern = "@2a @3b @5a"
        parsed_pattern = poem.parse_rhyme_pattern(pattern)
        self.assertEquals(parsed_pattern, [('a',2),('b',3),('a',5)])
    
    def test_pattern_stats(self):
        parsed_pattern = [('a',2),('b',3),('a',5)]
        pattern_stats = poem.generate_pattern_stats(parsed_pattern)
        self.assertEquals(pattern_stats['a']['max_syllables'], 5)
        self.assertEquals(pattern_stats['a']['count'], 2)


