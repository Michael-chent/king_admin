#Time : 2017/9/7 9:03
#Author : Michael_chen

from king.service import v1
from app01 import models
from django.utils.safestring import mark_safe

class KingUserInfo(v1.BaseKingAdmin):

    def func(self,obj=None,is_header=False):
        if is_header:
            return '操作'
        else:
            from django.urls import reverse
            namespace = self.site.namespace
            app_name = self.model_class._meta.app_label
            model_name = self.model_class._meta.model_name
            edit_name = "{0}:{1}_{2}_change".format(namespace,app_name,model_name)
            edit_url = reverse(edit_name,args=(obj.pk,))
            del_name = "{0}:{1}_{2}_delete".format(namespace,app_name,model_name)
            del_url = reverse(del_name,args=(obj.pk,))
            return mark_safe("<a href='{0}'>编辑</a> | <a href='{1}'>删除</a>".format(edit_url,del_url))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选项'
        else:
            tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    # list_display = {'选项':checkbox,'ID':'id', '用户名':'username', '邮箱':'email', '操作':func}
    list_display = [checkbox,'id', 'username','email', func]

v1.site.register(models.UserInfo,KingUserInfo)


class KingRole(v1.BaseKingAdmin):
    list_display = ['id','name']

v1.site.register(models.Role,KingRole)
