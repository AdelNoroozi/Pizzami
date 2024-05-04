from django_elasticsearch_dsl import Document, fields, Index

from .models import Profile

PUBLISHER_INDEX = Index("pizzami_profiles")
PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
)


@PUBLISHER_INDEX.doc_type
class ProfilesDocument(Document):
    id = fields.IntegerField(attr="id")
    public_name = fields.TextField(
        fields={
            "raw": {
                "type": "keyword"
            }
        }
    )
    bio = fields.TextField(
        fields={
            "raw": {
                "type": "keyword"
            }
        }
    )

    class Django(object):
        model = Profile
