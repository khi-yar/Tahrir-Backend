from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError


class PersianWord(models.Model):
    word = models.CharField(max_length=50, unique=True)


class EnglishWord(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super(EnglishWord, self).save(*args, **kwargs)


class Comment(models.Model):
    comment = models.TextField()
    submitter_name = models.CharField(max_length=50)

    rating = models.PositiveSmallIntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    translation = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self.rating > 5 or self.rating < 1:
            raise ValidationError('Rating outside valid range.')
        super(Comment, self).save(*args, **kwargs)

class FaToEnTranslation(models.Model):
    word = models.ForeignKey(PersianWord, on_delete=models.CASCADE)
    translation = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)
    submitter_name = models.CharField(max_length=50)

    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('word', 'translation')


class EnToFaTranslation(models.Model):
    word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    translation = models.ForeignKey(PersianWord, on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)
    submitter_name = models.CharField(max_length=50)

    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('word', 'translation')
