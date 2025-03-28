import re
from django import template

register = template.Library()

# Список нежелательных слов (отредактируйте по необходимости)
BANNED_WORDS = ['плохое', 'нежелательное', 'некрасивое']

@register.filter(name='censor')
def censor(value):
    """
    Фильтр для замены нежелательных слов на строку из '*' той же длины.
    """
    if not isinstance(value, str):
        return value

    def replace(match):
        word = match.group()
        return '*' * len(word)

    # Проходим по всем запрещённым словам и заменяем их независимо от регистра
    for banned in BANNED_WORDS:
        pattern = re.compile(re.escape(banned), re.IGNORECASE)
        value = pattern.sub(replace, value)
    return value
