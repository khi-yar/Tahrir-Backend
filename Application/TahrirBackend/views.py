import json
import logging

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

from TahrirBackend.models import (Comment, EnglishWord, EnToFaTranslation,
                                  FaToEnTranslation, PersianWord)
from TahrirBackend.weak_login import login_required_here

logger = logging.getLogger(__name__)


def _build_translation_response(translations):
    return {
        'translations': [{
            'translation':
            t.translation.word,
            'comments': [{
                'comment': c.comment,
                'submitter_name': c.submitter_name,
                'rating': c.rating
            } for c in t.comments.all()]
        } for t in translations]
    }


@require_http_methods(['GET', 'POST'])
@csrf_exempt
def echo(request):
    if request.method == 'GET':
        return JsonResponse(request.GET)
    elif request.method == 'POST':
        decoded_body = request.body.decode('utf-8')
        return JsonResponse({'Data': decoded_body})
    else:
        return JsonResponse({'Not valid!'})


@require_GET
def get_translation(request):
    word, lang = request.GET.get('word'), request.GET.get('lang')
    if not word or not lang:
        return HttpResponseBadRequest(
            'Parameters "word" and "lang" not provided correctly')

    if lang == 'en':
        word = word.lower()
        translations = EnToFaTranslation.objects.filter(word__word=word,
                                                        verified=True)
    elif lang == 'fa':
        translations = FaToEnTranslation.objects.filter(word__word=word,
                                                        verified=True)
    else:
        return HttpResponseBadRequest('Invalid "lang" param')

    if len(translations) == 0:
        return HttpResponseNotFound('Translation not found')

    response = _build_translation_response(translations)
    return JsonResponse(response, status=200)


@require_POST
@csrf_exempt
def create_translation(request):
    word, translation, lang = request.POST.get('word'), request.POST.get(
        'translation'), request.POST.get('lang')

    if not word or not translation or not lang:
        return HttpResponseBadRequest(
            'Parameters "word", "translation" and "lang" not provided correctly'
        )

    submitter_name = request.POST.get('name')
    if lang == 'en':
        try:
            word = EnglishWord.objects.get(word=word.lower())
            translation, _ = PersianWord.objects.get_or_create(
                word=translation)
        except EnglishWord.DoesNotExist:
            return HttpResponseNotFound("English word ({}) not found".format(
                word.lower()))
        etf, created = EnToFaTranslation.objects.get_or_create(
            word=word, translation=translation)
        if not created:
            return HttpResponse('Translation exists')
        else:
            etf.submitter_name = submitter_name
            etf.save()
    elif lang == 'fa':
        try:
            word = PersianWord.objects.get(word=word)
            translation, _ = EnglishWord.objects.get_or_create(
                word=translation.lower())
        except PersianWord.DoesNotExist:
            return HttpResponseNotFound(
                "Persian word ({}) not found".format(word))

        fte, created = FaToEnTranslation.objects.get_or_create(
            word=word, translation=translation)
        if not created:
            return HttpResponse('Translation exists')
        else:
            fte.submitter_name = submitter_name
            fte.save()
    else:
        return HttpResponseBadRequest('Invalid "lang" param')
    return HttpResponse('Translation successfully created')


@require_POST
@csrf_exempt
def create_comment(request):
    word, translation, lang = request.POST.get('word'), request.POST.get(
        'translation'), request.POST.get('lang')

    if not word or not translation or not lang:
        return HttpResponseBadRequest(
            'Parameters "word", "translation" and "lang" not provided correctly'
        )

    try:
        if lang == 'en':
            try:
                word = EnglishWord.objects.get(word=word.lower())
                translation = PersianWord.objects.get(word=translation)
            except (EnglishWord.DoesNotExist, PersianWord.DoesNotExist):
                return HttpResponseNotFound("Word not found in DB")
            translation = EnToFaTranslation.objects.get(
                word=word, translation=translation)
        elif lang == 'fa':
            try:
                word = PersianWord.objects.get(word=word)
                translation = EnglishWord.objects.get(word=translation.lower())
            except (EnglishWord.DoesNotExist, PersianWord.DoesNotExist):
                return HttpResponseNotFound("Word not found in DB")
            translation = FaToEnTranslation.objects.get(
                word=word, translation=translation)
        else:
            return HttpResponseBadRequest('Invalid "lang" param')
    except (EnToFaTranslation.DoesNotExist, FaToEnTranslation.DoesNotExist):
        return HttpResponseNotFound('Translation not found')

    name, comment, rating = request.POST.get('name'), request.POST.get(
        'comment'), request.POST.get('rating')

    if not name or not comment or not rating:
        return HttpResponseBadRequest(
            'Parameters "name", "comment" and "rating" not provided correctly')

    comment = Comment.objects.create(translation=translation,
                                     submitter_name=name,
                                     comment=comment,
                                     rating=rating)
    return HttpResponse('Comment successfully created')


@require_GET
def get_report(request):
    persian_suggesteds = [
        word_object.word for word_object in PersianWord.objects.filter(
            is_approved=True, suggested_to_translate=True)
    ]
    english_suggesteds = [
        word_object.word for word_object in EnglishWord.objects.filter(
            is_approved=True, suggested_to_translate=True)
    ]
    return JsonResponse({'fa': persian_suggesteds, 'en': english_suggesteds})


@require_POST
@csrf_exempt
def create_report(request):
    word, lang = request.POST.get('word'), request.POST.get('lang')
    if not word or not lang:
        return HttpResponseBadRequest('Not a valid request.')
    if lang == 'en':
        word, created = EnglishWord.objects.get_or_create(word=word.lower())
    elif lang == 'fa':
        word, created = PersianWord.objects.get_or_create(word=word)
    else:
        return HttpResponseBadRequest('Language is not correctly specified')
    word.suggested_to_translate = True
    word.save()
    return HttpResponse('The word is now suggested.')
