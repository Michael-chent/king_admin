#Time : 2017/9/7 16:06
#Author : Michael_chen

from django.template import Library
from types import FunctionType
from django.urls import reverse
from django.forms.models import ModelChoiceField
from king.service import v1

register = Library()

def table_body(result_list,list_display,kgadmin_obj):
    for row in result_list:
        if list_display == '__all__':
            yield [str(row),]
        else:
            yield [name(kgadmin_obj,obj=row) if isinstance(name,FunctionType) else getattr(row,name) for name in list_display]

def table_head(list_display,kgadmin_obj):
    if list_display == '__all__':
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item,FunctionType):
                yield item(kgadmin_obj,is_header=True)
            else:
                yield kgadmin_obj.model_class._meta.get_field(item).verbose_name
    # 另一种方法
    # title_list = []
    # for item in list_display:
    #     if isinstance(item,FunctionType):
    #         title_list.append(item.__name__)
    #     else:
    #         title_list.append(item)
    # return title_list

@register.inclusion_tag('kg/md.html')
def func(result_list,list_display,kgadmin_obj):
    v = table_body(result_list,list_display,kgadmin_obj)
    h = table_head(list_display,kgadmin_obj)
    return {'content':v,'head_list':h}

def add_content(form):
    for item in form:
        row = {'popup':False,'item':item,'popup_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            row['popup'] = True
            opt = item.field.queryset.model._meta
            url_name = '{0}:{1}_{2}_add'.format(v1.site.namespace,opt.app_label,opt.model_name)
            row['popup_url'] = '{0}?_popup={1}'.format(reverse(url_name),item.auto_id)
        yield row

@register.inclusion_tag('kg/add_form.html')
def show_form(form):
    context = {
        'form':add_content(form)
    }
    return context







