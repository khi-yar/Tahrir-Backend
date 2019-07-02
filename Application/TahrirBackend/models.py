from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class PersianWord(models.Model):
    word = models.CharField(max_length=60, unique=True)
    suggested_to_translate = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.word


class EnglishWord(models.Model):
    word = models.CharField(max_length=60, unique=True)
    suggested_to_translate = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super(EnglishWord, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


class Comment(models.Model):
    comment = models.TextField()
    submitter_name = models.CharField(max_length=50)

    rating = models.PositiveSmallIntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    translation = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if int(self.rating) > 5 or int(self.rating) < 1:
            raise ValidationError('Rating outside valid range.')
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.comment


class FaToEnTranslation(models.Model):
    word = models.ForeignKey(PersianWord, on_delete=models.CASCADE)
    translation = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)
    submitter_name = models.CharField(max_length=50, blank=True, null=True)

    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('word', 'translation')
        verbose_name = 'Farsi To English'
        verbose_name_plural = 'Farsi To English'


class EnToFaTranslation(models.Model):
    word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    translation = models.ForeignKey(PersianWord, on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)
    submitter_name = models.CharField(max_length=50, blank=True, null=True)

    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('word', 'translation')
        verbose_name = 'English To Farsi'
        verbose_name_plural = 'English To Farsi'
