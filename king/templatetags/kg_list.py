#Time : 2017/9/7 16:06
#Author : Michael_chen

from django.template import Library
from types import FunctionType
from django.urls import reverse

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











