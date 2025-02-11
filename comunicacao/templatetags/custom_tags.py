from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Verifica se o usuário pertence a um grupo específico."""
    return user.groups.filter(name=group_name).exists()
