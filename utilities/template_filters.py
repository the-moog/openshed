from django import template

register = template.Library()


@register.filter(is_safe=True)
def format_img_src(img_ur, size):
    return img_ur
