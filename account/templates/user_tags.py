from django import template

register = template.Library()

@register.filter
def get_initials(user):
    """Retourne les initiales de l'utilisateur"""
    if user.prenom and user.nom:
        return f"{user.prenom[0]}{user.nom[0]}".upper()
    elif user.prenom:
        return user.prenom[0].upper()
    return user.username[0].upper() if user.username else "?"