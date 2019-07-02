import json
import logging

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from TahrirBackend.models import (Comment, EnglishWord, EnToFaTranslation,
                                  FaToEnTranslation, PersianWord)

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
    body = {}

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Please fill a json object')

    word, translation, lang = body.get('word'), body.get(
        'translation'), body.get('lang')

    if not word or not translation or not lang:
        return HttpResponseBadRequest(
            'Parameters "word", "translation" and "lang" not provided correctly'
        )

    submitter_name = body.get('name')
    if lang == 'en':
        try:
            word = EnglishWord.objects.get(word=word.lower())
            translation = PersianWord.objects.get(word=translation)
        except EnglishWord.DoesNotExist:
            return HttpResponseNotFound("Word not found")
        except PersianWord.DoesNotExist:
            translation = PersianWord(word=translation)
            translation.save()
        try:
            EnToFaTranslation.objects.create(word=word,
                                             translation=translation,
                                             submitter_name=submitter_name)
        except Exception:
            return HttpResponse('Translation exists')
    elif lang == 'fa':
        try:
            word = PersianWord.objects.get(word=word)
            translation = EnglishWord.objects.get(word=translation.lower())
        except PersianWord.DoesNotExist:
            return HttpResponseNotFound("Word not found")
        except EnglishWord.DoesNotExist:
            translation = EnglishWord(word=translation.lower())
            translation.save()
        try:
            FaToEnTranslation.objects.create(word=word,
                                             translation=translation,
                                             submitter_name=submitter_name)
        except Exception:
            return HttpResponse('Translation exists')
    else:
        return HttpResponseBadRequest('Invalid "lang" param')

    return HttpResponse('Translation successfully created')


@require_POST
@csrf_exempt
def create_comment(request):
    body = {}

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Please fill a json object')

    word, translation, lang = body.get('word'), body.get(
        'translation'), body.get('lang')

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
                return HttpResponseNotFound("Word not in DB")
            translation = EnToFaTranslation.objects.get(
                word=word, translation=translation)
        elif lang == 'fa':
            try:
                word = PersianWord.objects.get(word=word)
                translation = EnglishWord.objects.get(word=translation.lower())
            except (EnglishWord.DoesNotExist, PersianWord.DoesNotExist):
                return HttpResponseNotFound("Word not in DB")
            translation = FaToEnTranslation.objects.get(
                word=word, translation=translation)
        else:
            return HttpResponseBadRequest('Invalid "lang" param')
    except (EnToFaTranslation.DoesNotExist, FaToEnTranslation.DoesNotExist):
        return HttpResponseNotFound('Translation not found')

    name, comment, rating = body.get('name'), body.get('comment'), body.get(
        'rating')

    if not name or not comment or not rating:
        return HttpResponseBadRequest(
            'Parameters "name", "comment" and "rating" not provided correctly')

    Comment.objects.create(translation=translation,
                           submitter_name=name,
                           comment=comment,
                           rating=rating)

    return HttpResponse('Comment successfully created')
