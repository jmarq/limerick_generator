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

    def test_vowel_phones(self):
        phrase = "slow motion"
        vowel_phones = syllables.vowel_phones_for_phrase(phrase)
        self.assertEquals(len(vowel_phones), 3)

    def test_rhyme_syllables_match(self):
        phrases = ["at my house", "a sly mouse"]
        match = syllables.rhyme_and_syllables_match(phrases, num_syllables=2)
        self.assertTrue(match)
        phrases2 = ['four syllables' , 'a six syllable phrase']
        match2 = syllables.rhyme_and_syllables_match(phrases2, num_syllables=2)          
        self.assertFalse(match2)

    def test_same_number_of_syllables(self):
        phrases = ['my code can always get better', 'a dog thought about his limits']
        self.assertTrue(syllables.same_number_of_syllables(phrases))



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


    def test_generate_poem(self):
        poem_pattern = "@2a::@2a::@2a"
        new_poem = poem.generate_poem(poem_pattern)
        poem_syllables = syllables.sentence_syllables(new_poem.replace("::"," "))
        self.assertEquals(poem_syllables, 6)
        rhyme_groups = new_poem.split("::")
        self.assertTrue(syllables.rhyme_and_syllables_match(rhyme_groups, num_syllables=1))


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


