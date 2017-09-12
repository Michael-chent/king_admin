#Time : 2017/9/11 10:54
#Author : Michael_chen

from django.template import Library
from django.forms.models import ModelChoiceField
from django.urls import reverse
from king.service import v1

register = Library()

def add_content(form):
    form_list = []
    for item in form:
        row = {'is_popup':False,'item':None,'popup_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = '{0}:{1}_{2}_add'.format(v1.site.namespace,target_app_label,target_model_name)
            row['popup_url'] = '{0}?_popup={1}'.format(reverse(url_name),item.auto_id)
            row['is_popup'] = True
            row['item'] = item
        else:
            row['item'] = item
        form_list.append(row)
    return form_list

@register.inclusion_tag('kg/add_edit_form.html')
def show_add_edit_form(form):
    context = {
        'form':add_content(form)
    }
    return context











