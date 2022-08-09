from django import template


register = template.Library()


@register.inclusion_tag('utilities/render_field.html')
def render_field(field, bulk_nullable=False, css=None):
    """
    Render a single form field from template
    """
    return {
        'field': field,
        'bulk_nullable': bulk_nullable,
    }


@register.inclusion_tag('utilities/render_custom_fields.html')
def render_custom_fields(form):
    """
    Render all custom fields in a form
    """
    return {
        'form': form,
    }


@register.inclusion_tag('utilities/render_form.html')
def render_form(form):
    """
    Render an entire form from template
    """
    return {
        'form': form,
    }


@register.filter(name='widget_type')
def widget_type(field):
    """
    Return the widget type
    """
    if hasattr(field, 'widget'):
        return field.widget.__class__.__name__.lower()
    elif hasattr(field, 'field'):
        return field.field.widget.__class__.__name__.lower()
    else:
        return None


@register.inclusion_tag('utilities/render_item_image.html')
def render_item_image(image, thumbnail=True, max_y_size=300):
    """
    Render an item image, assuring it's size
    """
    if thumbnail:
        max_y_size = 100
    return {
        'image': image,
        'max_y_size': max_y_size,
    }