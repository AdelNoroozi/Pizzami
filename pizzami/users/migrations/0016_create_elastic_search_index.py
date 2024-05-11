from django.db import migrations
from elasticsearch import Elasticsearch

from pizzami.users.documents import ProfilesDocument


def create_elastic_search_profile_index(apps, schema_editor):
    ProfilesDocument.init()


def remove_elastic_search_profile_index(apps, schema_editor):
    es = Elasticsearch('http://elasticsearch:9200')
    es.indices.create(index='pizzami_profiles')


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0015_alter_address_phone_number'),
    ]

    operations = [
        migrations.RunPython(create_elastic_search_profile_index, reverse_code=remove_elastic_search_profile_index)
    ]
