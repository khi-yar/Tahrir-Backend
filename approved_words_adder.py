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
        p = PersianWord.objects.get(word=farsi)
    except PersianWord.DoesNotExist:
        p = PersianWord(word=farsi)
        p.save()
    try:
        e = EnglishWord.objects.get(word=english.lower())
    except EnglishWord.DoesNotExist:
        e = EnglishWord(word=english)
        e.save()

    fte, etf = None, None
    try:
        fte = FaToEnTranslation.objects.get(word=p,
                                            translation=e,
                                            verified=True,
                                            submitter_name='ADMIN')
    except FaToEnTranslation.DoesNotExist:
        fte = FaToEnTranslation(word=p,
                                translation=e,
                                verified=True,
                                submitter_name='ADMIN')
        fte.save()
    try:
        etf = EnToFaTranslation.objects.get(word=e,
                                            translation=p,
                                            verified=True,
                                            submitter_name='ADMIN')
    except Exception:
        etf = EnToFaTranslation(word=e,
                                translation=p,
                                verified=True,
                                submitter_name='ADMIN')
        etf.save()
