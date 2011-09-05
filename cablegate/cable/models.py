import re
from operator import itemgetter

from django.utils import simplejson
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

    def __str__(self):
        return '<cable object #%s %s %s %s>' % (self.pk, self.date, self.classification, self.origin)

    def __unicode__(self):
        return '%s - %s - %s' % (self.date, self.classification.lower(), self.origin)

    class Meta:
        db_table = u'cable'


class CableMetadata(models.Model):
    cable           = models.OneToOneField(Cable)
    # Stats
    words_freqdist  = models.TextField(blank=True, null=True)
    words_count     = models.TextField(blank=True, null=True)
    keywords        = models.TextField(blank=True, null=True)
    names           = models.TextField(blank=True, null=True)

    # Geo
    origin_lat      = models.CharField(max_length=250, blank=True, null=True)
    origin_lon      = models.CharField(max_length=250, blank=True, null=True)
    destination_lat = models.CharField(max_length=250, blank=True, null=True)
    destination_lon = models.CharField(max_length=250, blank=True, null=True)


    def get_words_count(self, minlen=4, mincount=3):
        """
        Count the number of times each word has appeared.
        Based on http://code.google.com/p/nltk/source/browse/trunk/nltk/examples/school/words.py
        """
       #if not self.words_count:
        wordcounts = {}
        out = []
        words = re.split('\W+', self.cable.content.lower())
        # Calculate
        for word in words:
            if len(word) > minlen and word not in WORDS_IGNORED:
                if word not in wordcounts:
                     wordcounts[word] = 0
                wordcounts[word] += 1


        # Skim
        for word in wordcounts:
            if wordcounts[word] >= mincount:
                out.append((word, wordcounts[word]))

        out = sorted(out, key=lambda i: i[1], reverse=True)

        self.words_count  = simplejson.dumps(out)
        self.save()
        return simplejson.loads(self.words_count)

    def get_words_freqdist(self, num=25):
        """
        Returns the words and their counts, in order of decreasing frequency.
        Based on http://code.google.com/p/nltk/source/browse/trunk/nltk/examples/school/words.py
        """
        if not self.words_freqdist:
            out = {}
            counts = self.get_words_count()
            total  = sum(counts.values())
            cumulative = 0.0
            sorted_word_counts = sorted(counts.items(), key=itemgetter(1), reverse=True)
            for i in range(len(counts.values())):
                word, count = sorted_word_counts[i]
                cumulative += count * 100.0 / total
                out[i] = [word, '%3.2d%%' % cumulative]
               #print "%3d %3.2d%% %s" % (i, cumulative, word)
            self.words_freqdist = out
            self.save()
        return self.words_freqdist
