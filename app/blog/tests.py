from django.test import TestCase

from .models import Widget


class AnimalTestCase(TestCase):
    def setUp(self):
        Widget.objects.create(title="Widget 1", content="Lorem ipsum dolor sit amor.")
        Widget.objects.create(title="Widget 1", content="Lorem ipsum dolor sit amor.")
        Widget.objects.create(title="Widget 1", content="Lorem ipsum dolor sit amor.")

    def test_widget_count(self):
        widgets = Widget.objects.all()
        self.assertEqual(widgets.count(), 3)

