from django.test import TestCase

from TahrirBackend.models import EnglishWord


class EnglishTestCase(TestCase):
    """Documentation for EnglishTestCase

    """

    def setUp(self):
        self.word = 'bozanghare'
        self.word_object = EnglishWord.objects.create(word=self.word)

    def test_suggested(self):
        self.word_object.suggested_to_translate = True
        self.word_object.save()
        another_word_object = EnglishWord.objects.get(word=self.word)
        self.assertEqual(another_word_object.suggested_to_translate, True)
