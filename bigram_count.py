from mrjob.job import MRJob
import re
import string

WORD_REGEX = re.compile(r"[\w']+")

class BigramCount(MRJob):
    '''
        Input: List of lines containing sentences (possibly many sentences per line)
        Output: A generated list of key/value tuples:
            Key: A bigram separated by a comma (i.e. "the,cat")
            Value: The number of occurences of that bigram (integer)
    '''

    def mapper(self, key, val):

               
        exclude = set(string.punctuation)
        val = ''.join(ch for ch in val if ch not in exclude)

        lines = val.splitlines()
        bigrams = [bigr for line in lines for bigr in zip(line.split(" ")[:-1], line.split(" ")[1:])]

        for big in bigrams:
            big = ",".join(big)
            yield (big, 1)

    def reducer(self, key, vals):
        sum = 0 

        for _ in vals:
            sum += 1 

        yield key, sum

if __name__ == '__main__':
    BigramCount.SORT_VALUES = True
    BigramCount.run()