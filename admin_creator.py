from django.contrib.auth import get_user_model

user_model = get_user_model()

if not user_model.objects.filter(username='admin').exists():
    user = user_model.objects.create_user('admin', password='admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()
