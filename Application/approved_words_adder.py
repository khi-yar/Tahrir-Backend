import pickle

from TahrirBackend.models import (EnglishWord, EnToFaTranslation,
                                  FaToEnTranslation, PersianWord)

init_data = {}

with open('./en2fa.pkl', 'rb') as pickle_file:
    init_data = pickle.load(pickle_file)

for english, farsi in init_data.items():
    # print(english.lower(), farsi)
    p, e = None, None
    try:
        p = PersianWord.objects.get(word=farsi,
                                    suggested_to_translate=False,
                                    is_approved=True)
    except PersianWord.DoesNotExist:
        p = PersianWord(word=farsi,
                        suggested_to_translate=False,
                        is_approved=True)
        p.save()
    try:
        e = EnglishWord.objects.get(word=english.lower(),
                                    suggested_to_translate=False,
                                    is_approved=True)
    except EnglishWord.DoesNotExist:
        e = EnglishWord(word=english.lower(),
                        suggested_to_translate=False,
                        is_approved=True)
        e.save()

    fte, etf = None, None
    try:
        fte = FaToEnTranslation.objects.get(word=p,
                                            translation=e,
                                            verified=True,
                                            submitter_name='Farhangestan')
    except FaToEnTranslation.DoesNotExist:
        fte = FaToEnTranslation(word=p,
                                translation=e,
                                verified=True,
                                submitter_name='Farhangestan')
        fte.save()
    try:
        etf = EnToFaTranslation.objects.get(word=e,
                                            translation=p,
                                            verified=True,
                                            submitter_name='Farhangestan')
    except Exception:
        etf = EnToFaTranslation(word=e,
                                translation=p,
                                verified=True,
                                submitter_name='Farhangestan')
        etf.save()
