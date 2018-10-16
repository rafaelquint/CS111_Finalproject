# Final Project
# finalproject.py

# Name: Rafael Quintero
# Email: rafaelq@bu.edu

# Partner's name: Justin Walsh
# Partner's email: justinrw@bu.edu

import math

class TextModel:
    """ a data type for objects that model a body of text
    """
    def __init__(self, model_name):
        """ constructor for new TextModel objects """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.preps = {}   # frequency of prepositions

    def __repr__(self):
        """ returns a string representation of a TextModel object """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of prepositions: ' + str(len(self.preps))
        return s

    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model.
        """
        split_words = s.split()
        sen_count = 0
        for a in range(len(split_words)):
            sen_count += 1
            if '.' in split_words[a] or \
               '!' in split_words[a] or \
               '?' in split_words[a]:
                if sen_count not in self.sentence_lengths:
                    self.sentence_lengths[sen_count] = 1
                    sen_count = 0
                else:
                    self.sentence_lengths[sen_count] += 1
                    sen_count = 0
        
        word_list = clean_text(s)

        for x in word_list:
            if x not in self.words:
                self.words[x] = 1
            else:
                self.words[x] += 1

        for w in word_list:
            current_len = len(w)
            if current_len not in self.word_lengths:
                self.word_lengths[current_len] = 1
            else:
                self.word_lengths[current_len] += 1
        
        for b in word_list:
            if stem(b) not in self.stems:
                self.stems[stem(b)] = 1
            else:
                self.stems[stem(b)] += 1

        # Additional feature: frequency of prepositions

        # Creates list of top 25 prepositions
        preps = ['of', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'about', 'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before', 'under', 'around', 'among']

        for c in word_list:
            if c in preps:
                if c not in self.preps:
                    self.preps[c] = 1
                else:
                    self.preps[c] += 1


    def add_file(self, filename):
        """ adds all of the text in the file indentified by filename to the model """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()

        self.add_string(text)

    def save_model(self):
        """ saves the TextModel object self by writing its various
            feature dictionaries to files
        """
        f = open(self.name + '_words', 'w')
        f.write(str(self.words))
        f.close()

        f = open(self.name + '_word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close()

        f = open(self.name + '_stems', 'w')
        f.write(str(self.stems))
        f.close()

        f = open(self.name + '_sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close()

        f = open(self.name + '_preps', 'w')
        f.write(str(self.preps))
        f.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object
            from their files and assigns them to the attributes of the
            called TextModel
        """
        f = open(self.name + '_words', 'r')
        d_str = f.read()
        f.close()
        self.words = dict(eval(d_str))

        f = open(self.name + '_word_lengths', 'r')
        d_str = f.read()
        f.close()
        self.word_lengths = dict(eval(d_str))

        f = open(self.name + '_stems', 'r')
        d_str = f.read()
        f.close()
        self.stems = dict(eval(d_str))

        f = open(self.name + '_sentence_lengths', 'r')
        d_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(d_str))

        f = open(self.name + '_preps', 'r')
        d_str = f.read()
        f.close()
        self.preps = dict(eval(d_str))

    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores
            measuring the similarity of self and other
        """
        score1 = compare_dictionaries(other.words, self.words)
        score2 = compare_dictionaries(other.word_lengths, self.word_lengths)
        score3 = compare_dictionaries(other.stems, self.stems)
        score4 = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        score5 = compare_dictionaries(other.preps, self.preps)
        
        sim_scores = [round(score1, 3), round(score2, 3), round(score3, 3), round(score4, 3), round(score5, 3)]

        return sim_scores

    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to 2 other
            "source" TextModel objects (source1 and source2) and
            determines which of these other TextModels is the more
            likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print('Scores for ' + source1.name + ': ' + str(scores1))
        print('Scores for ' + source2.name + ': ' + str(scores2))

        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1
            else:
                count2 += 1
        if count1 > count2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)


def clean_text(txt):
    """ inputs a string of text txt and returns a list containing
        the words in txt after punctuation has been removed
    """

    words = txt.lower().split()
    clean_words = []

    a = [w.replace('!','') for w in words]
    b = [w.replace('.','') for w in a]
    c = [w.replace('?','') for w in b]
    d = [w.replace(',','') for w in c]
    e = [w.replace(';','') for w in d]
    clean_words = [w.replace(':','') for w in e]
    
    return clean_words

def stem(s):
    """ accepts a string s as a parameter
        returns the stem of s
    """

    # suffixes
    if s[-2:] == 'es':
        s = s[:-2]
    if s[-1] == 's':
        s = s[:-1]
    if s[-2:] == 'ly':
        s = s[:-2]
    if s[-3:] == 'ing':
        if len(s) >= 5:
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
        else:
            s = s[:-3]
    if s[-2:] == 'er':
        s = s[:-2]
    if s[-2:] == 'ed':
        s = s[:-2]

    # prefixes
    if s[:2] == 'in':
        s = s[2:]
    if s[:2] == 'de':
        s = s[2:]
    if s[:2] == 'im':
        s = s[2:]
    if s[:2] == 're':
        s = s[2:]
    if s[:2] == 'un':
        s = s[2:]
    if s[:3] == 'non':
        s = s[3:]
    if s[:3] == 'dis':
        s = s[3:]

    return s

def compare_dictionaries(d1, d2):
    """ inputs 2 feature dictionaries d1 and d2
        computes and returns their log similarity score
    """
    score = 0
    total = 0

    for key in d1:
        total += d1[key]

    for key in d2:
        if key in d1:
            score += (math.log(d1[key] / total) * d2[key])
        else:
            score += (math.log(0.5 / total) * d2[key])

    return score

def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ your docstring goes here """
    source1 = TextModel('New York Times')
    source1.add_file('nyt1.txt')
    source1.add_file('nyt2.txt')
    source1.add_file('nyt3.txt')

    source2 = TextModel('Boston Globe')
    source2.add_file('globe1.txt')
    source2.add_file('globe2.txt')
    source2.add_file('globe3.txt')

    new1 = TextModel("Justin's WR 100 Paper")
    new1.add_file('wr100_justin.txt')
    new1.classify(source1, source2)

    new1 = TextModel("Rafael's WR 100 Paper")
    new1.add_file('wr100_rafael.txt')
    new1.classify(source1, source2)

    new1 = TextModel("Recode")
    new1.add_file('recode.txt')
    new1.classify(source1, source2)

    new1 = TextModel("CBS Boston")
    new1.add_file('cbsboston.txt')
    new1.classify(source1, source2)
