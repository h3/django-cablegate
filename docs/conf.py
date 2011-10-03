import os, sys

sys.path.inser(0, os.path.abspath('../cablegate')

import settings
from django.core.management import setup_environ
setup_environ(settings)
