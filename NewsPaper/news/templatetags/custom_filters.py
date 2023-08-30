from django import template


register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Фильтр только для строк')
    words = value.split()
    for i, word in enumerate(words):
        if word[1:].islower():
            pass
        else:
            words[i] = word[0] + '*' * len(word[1:])

    return ' '.join(words)
