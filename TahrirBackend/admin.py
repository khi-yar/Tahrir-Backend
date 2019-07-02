from django.contrib import admin
from TahrirBackend.models import (Comment, EnglishWord, EnToFaTranslation,
                                  FaToEnTranslation, PersianWord)


@admin.register(EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):
    ordering = ['word']
    list_display = ('word', 'is_approved', 'suggested_to_translate')
    list_filter = ('is_approved', 'suggested_to_translate')
    search_fields = ['word']


@admin.register(PersianWord)
class PersianWordAdmin(admin.ModelAdmin):
    ordering = ['word']
    list_display = ('word', 'is_approved', 'suggested_to_translate')
    list_filter = ('is_approved', 'suggested_to_translate')
    search_field = ['word']


@admin.register(EnToFaTranslation)
class EnToFaAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'verified')
    list_filter = ('verified', )
    search_field = ['word', 'translation']


@admin.register(FaToEnTranslation)
class FaToEnAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'verified')
    list_filter = ('verified', )
    search_field = ['word', 'translation']


admin.site.register(Comment)
