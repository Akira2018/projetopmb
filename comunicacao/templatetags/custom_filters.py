from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Verifica se o usuário pertence a um grupo"""
    return user.groups.filter(name=group_name).exists()

