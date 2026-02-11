import factory

from .. import models


class ContentfulDemoItemFactory(factory.django.DjangoModelFactory):
    id = factory.Faker("uuid4")
    fields: dict = {}
    is_published = True

    class Meta:
        model = models.DemoItem
