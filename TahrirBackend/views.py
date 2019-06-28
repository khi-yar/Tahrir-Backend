import logging

from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_GET, require_POST

from TahrirBackend.models import EnToFaTranslation, FaToEnTranslation, Comment, PersianWord, EnglishWord

logger = logging.getLogger(__name__)


def _build_translation_response(translations):
    return {
        'translations':
            [
                {
                    'translation': t.translation.word,
                    'comments': [
                        {
                            'comment': c.comment,
                            'submitter_name': c.submitter_name,
                            'rating': c.rating
                        }
                        for c in t.comments.all()
                    ]
                }
                for t in translations
            ]
    }


@require_GET
def get_translation(request):
    word, lang = request.GET.get('word'), request.GET.get('lang')
    if not word or not lang:
        return HttpResponseBadRequest('Parameters "word" and "lang" not provided correctly')

    if lang == 'en':
        word = word.lower()
        translations = EnToFaTranslation.objects.filter(word__word=word, verified=True)
    elif lang == 'fa':
        translations = FaToEnTranslation.objects.filter(word__word=word, verified=True)
    else:
        return HttpResponseBadRequest('Invalid "lang" param')

    if len(translations) == 0:
        return HttpResponseNotFound('Translation not found')

    response = _build_translation_response(translations)
    return JsonResponse(response, status=200)


@require_POST
def create_translation(request):
    word, translation, lang = request.POST.get('word'), request.POST.get('translation'), request.POST.get('lang')
    if not word or not translation or not lang:
        return HttpResponseBadRequest('Parameters "word", "translation" and "lang" not provided correctly')

    submitter_name = request.POST.get('name')
    if lang == 'en':
        try:
            word = EnglishWord.objects.get(word=word.lower())
            translation = PersianWord.objects.get(word=translation)
        except (EnglishWord.DoesNotExist, PersianWord.DoesNotExist):
            return HttpResponseNotFound("Word/Translation pair not found")
        EnToFaTranslation.objects.create(word=word, translation=translation, submitter_name=submitter_name)
    elif lang == 'fa':
        try:
            word = PersianWord.objects.get(word=word)
            translation = EnglishWord.objects.get(word=translation.lower())
        except (EnglishWord.DoesNotExist, PersianWord.DoesNotExist):
            return HttpResponseNotFound("Word/Translation pair not found")
        FaToEnTranslation.objects.create(word=word, translation=translation, submitter_name=submitter_name)
    else:
        return HttpResponseBadRequest('Invalid "lang" param')

    return HttpResponse('Comment successfully created')


@require_POST
def create_comment(request):
    word, translation, lang = request.POST.get('word'), request.POST.get('translation'), request.POST.get('lang')
    if not word or not translation or not lang:
        return HttpResponseBadRequest('Parameters "word", "translation" and "lang" not provided correctly')

    try:
        if lang == 'en':
            translation = EnToFaTranslation.objects.get(word=word, translation=translation)
        elif lang == 'fa':
            translation = FaToEnTranslation.objects.get(word=word, translation=translation)
        else:
            return HttpResponseBadRequest('Invalid "lang" param')
    except (EnToFaTranslation.DoesNotExist, FaToEnTranslation.DoesNotExist):
        return HttpResponseNotFound('Translation not found')

    name, comment, rating = request.POST.get('name'), request.POST.get('comment'), require_POST.get('rating')
    if not name or not comment or not rating:
        return HttpResponseBadRequest('Parameters "name", "comment" and "rating" not provided correctly')

    Comment.objects.create(translation=translation, submitter_name=name, comment=comment, rating=rating)

    return HttpResponse('Comment successfully created')
