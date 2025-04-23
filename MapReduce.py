from mrjob.job import MRJob
import re

# Regular expression to match words
WORD_RE = re.compile(r"\b\w+\b")

class MRWordCount(MRJob):

    # Mapper function to split words and emit (word, 1)
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    # Reducer function to sum occurrences of each word
    def reducer(self, word, counts):
        yield word, sum(counts)

if __name__ == "__main__":
    MRWordCount.run()
