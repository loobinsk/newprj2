from ..models import User


def get_or_create_user_from_order(data):
    """
        data :param dict which contain order payload
        (user, is_create) :return
        If user exists function returns (existing_user, False)
        If user does not exist function returns (new_user, True)
    """

    existing_user = User.objects.filter(phone=data['phone']).first()
    if existing_user:
        return existing_user, False

    new_user = User()
    new_user.phone = data['phone']
    new_user.name = data['name']
    new_user.save()

    return new_user, True

