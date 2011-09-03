from django.db import models

class Cable(models.Model):
    id              = models.AutoField(primary_key=True)
    date            = models.DateTimeField(blank=True, null=True)
    refid           = models.CharField(max_length=250)
    classification  = models.CharField(max_length=250)
    origin          = models.CharField(max_length=250)
    destination     = models.TextField(blank=True, null=True)
    header          = models.TextField(blank=True, null=True)
    content         = models.TextField(blank=True, null=True)

    class Meta:
        db_table = u'cable'

