from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value, arg=''):
    bad_words = ['badword1', 'badword2']  # Список слов, которые нужно заменить
    for word in bad_words:
        value = value.replace(word, '*' * len(word))
    return value
