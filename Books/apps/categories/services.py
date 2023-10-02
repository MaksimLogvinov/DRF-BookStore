from datetime import date

from django.db.models import Q
from django.template.defaultfilters import register


def categories(model, user=None, data=None):
    today = date.today()
    prod = model
    if not user.is_anonymous and user.user_profile.birth_date:
        birth_date = user.user_profile.birth_date
        user_age = (
                today.year - birth_date.year -
                ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        prod = prod.filter(prod_age_restriction__lte=user_age)
    if data:
        prod = prod.filter(
            Q(prod_title__icontains=data) or Q(slug__icontains=data)
        )
    return prod


@register.filter
def rating(dict_data, key):
    return dict_data[key]
