from users.models import VoicesUser


def create_user(email):
    return VoicesUser.objects.create_user(email)
