import sys
from django.core import serializers
from cablegate.cable.models import Cable

def migrate(model, size=500, start=0):
    count = model.objects.using('default').count()
    print "%s objects in model %s" % (count, model)
    for i in range(start, count, size):
        print i,
        sys.stdout.flush()
        original_data = model.objects.using('default').all()[i:i+size]
        original_data[0].content = unicode(original_data[0].content)
        original_data_json = serializers.serialize("json", original_data)
        new_data = serializers.deserialize("json", original_data_json, 
                                           using='mysql')
        for n in new_data:
            n.save(using='mysql')

migrate(Cable)
