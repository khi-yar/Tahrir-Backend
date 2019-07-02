from django.contrib import admin
from TahrirBackend.models import (Comment, EnglishWord, EnToFaTranslation,
                                  FaToEnTranslation, PersianWord)


@admin.register(EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):
    ordering = ['word']
    list_editable = ('suggested_to_translate', )
    list_display = ('word', 'is_approved', 'suggested_to_translate')
    list_filter = ('is_approved', 'suggested_to_translate')
    search_fields = ['word']


@admin.register(PersianWord)
class PersianWordAdmin(admin.ModelAdmin):
    ordering = ['word']
    list_editable = ('suggested_to_translate', )
    list_display = ('word', 'is_approved', 'suggested_to_translate')
    list_filter = ('is_approved', 'suggested_to_translate')
    search_fields = ['word']


@admin.register(EnToFaTranslation)
class EnToFaAdmin(admin.ModelAdmin):
    ordering = ['word']
    autocomplete_fields = ['word', 'translation']
    list_editable = ('verified', )
    list_display = ('word', 'translation', 'verified')
    list_filter = ('verified', )
    search_fields = ['word__word']


@admin.register(FaToEnTranslation)
class FaToEnAdmin(admin.ModelAdmin):
    ordering = ['word']
    autocomplete_fields = ['word', 'translation']
    list_editable = ('verified', )
    list_display = ('word', 'translation', 'verified')
    list_filter = ('verified', )
    search_fields = ['word__word']


admin.site.register(Comment)
