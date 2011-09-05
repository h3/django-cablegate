from django.core.management.base import BaseCommand, CommandError
from cablegate.cable.models import Cable, CableMetadata

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    #help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for cable in Cable.objects.filter(cablemetadata=None):
            meta = CableMetadata()
            meta.cable_id = cable.id
            meta.save()
            # Update cache
            meta.get_words_count()
            meta.get_words_freqdist()

        self.stdout.write('Done\n')
