from django import template


register = template.Library()


@register.filter
def pluralize(value, arg="комментарий, комментария, комментариев"):
    args = arg.split(", ")
    number = abs(int(value))
    x = number % 10
    y = number % 100

    if x == 1 and y != 11:
        return args[0]
    elif 4 >= x >= 2 and (y < 10 or y >= 20):
        return args[1]
    else:
        return args[2]
