#Time : 2017/9/7 16:06
#Author : Michael_chen

from django.template import Library
from types import FunctionType

register = Library()

def table_body(result_list,list_display,kgadmin_obj):
    for row in result_list:
        yield [name(kgadmin_obj,row) if isinstance(name,FunctionType) else getattr(row,name) for name in list_display.values()]

def table_head(list_display):
    title_list = []
    for item in list_display:
        if isinstance(item,FunctionType):
            title_list.append(item.__name__)
        else:
            title_list.append(item)
        print("&&&&&&&",title_list)
    return title_list

@register.inclusion_tag('kg/md.html')
def func(result_list,list_display,kgadmin_obj):
    v = table_body(result_list,list_display,kgadmin_obj)
    h = table_head(list_display)
    # for item in list_display:
    #     if isinstance(item,FunctionType):
    #         print(item.__name__.title())
    #     else:
    #         print(item)
    return {'content':v,'head_list':h}









