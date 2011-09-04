import re
from operator import itemgetter

from django.db import models

WORDS_IGNORED = (
    'after', 'that', 'with', 'which', 'into', 'when', 'than', 'them', 'there', 'threw',
)


class Cable(models.Model):
    id              = models.AutoField(primary_key=True)
    date            = models.DateTimeField(blank=True, null=True)
    refid           = models.CharField(max_length=250)
    classification  = models.CharField(max_length=250)
    origin          = models.CharField(max_length=250)
    destination     = models.TextField(blank=True, null=True)
    header          = models.TextField(blank=True, null=True)
    content         = models.TextField(blank=True, null=True)

    def count_words(self, minlen=4, mincount=3):
        "Count the number of times each word has appeared."
        # http://code.google.com/p/nltk/source/browse/trunk/nltk/examples/school/words.py
        wordcounts = {}
        out = {}
        words = re.split('\W+', self.content)
        for word in words:
            if len(word) > minlen and word not in WORDS_IGNORED:
                if word not in wordcounts:
                     wordcounts[word] = 0
                wordcounts[word] += 1

        for word in wordcounts:
            if wordcounts[word] >= mincount:
                out[word] = wordcounts[word]

        return out 

    def freq_words(self, num=25):
        "Print the words and their counts, in order of decreasing frequency."
        # http://code.google.com/p/nltk/source/browse/trunk/nltk/examples/school/words.py
        counts = self.count_words()
        total  = sum(counts.values())
        cumulative = 0.0
        sorted_word_counts = sorted(counts.items(), key=itemgetter(1), reverse=True)
        for i in range(num):
            word, count = sorted_word_counts[i]
            cumulative += count * 100.0 / total
            print "%3d %3.2d%% %s" % (i, cumulative, word)

    class Meta:
        db_table = u'cable'


class CableMetadata(models.Model):
    cable           = models.OneToOneField(Cable)
    # Stats
    words_dist      = models.TextField(blank=True, null=True)
    keywords        = models.TextField(blank=True, null=True)
    names           = models.TextField(blank=True, null=True)
    # Geo
    origin_lat      = models.CharField(max_length=250, blank=True, null=True)
    origin_lon      = models.CharField(max_length=250, blank=True, null=True)
    destination_lat = models.CharField(max_length=250, blank=True, null=True)
    destination_lon = models.CharField(max_length=250, blank=True, null=True)
