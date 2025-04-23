from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# Regular expression to match words
WORD_RE = re.compile(r"[\w']+")

class WordCooccurrence(MRJob):

    def mapper(self, _, line):
        words = list(WORD_RE.findall(line.lower()))
        for i, word in enumerate(words):
            for j in range(i + 1, len(words)):
                if words[i] != words[j]:
                    yield (words[i], words[j]), 1

    def combiner(self, word_pair, counts):
        yield word_pair, sum(counts)

    def reducer(self, word_pair, counts):
        yield word_pair, sum(counts)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]

if __name__ == "__main__":
    WordCooccurrence.run()