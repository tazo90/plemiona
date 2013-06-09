from django import template
from ..models import Osada

register = template.Library()

def show_status_bar(context):
    user_profile = context['request'].user.profile
    osada = Osada.objects.filter(user=user_profile)
    if osada:
        osada = osada[0]
        
    return {'osada': osada}

register.inclusion_tag('lpp_app/status_bar.html', takes_context=True)(show_status_bar)
