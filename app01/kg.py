#Time : 2017/9/7 9:03
#Author : Michael_chen

from king.service import v1
from app01 import models
from django.utils.safestring import mark_safe

class KingUserInfo(v1.BaseKingAdmin):

    def func(self,obj):
        from django.urls import reverse
        namespace = self.site.namespace
        app_name = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        name = "{0}:{1}_{2}_change".format(namespace,app_name,model_name)
        url = reverse(name,args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self,obj):
        tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)

    list_display = {'选择':checkbox,'ID':'id', '用户名':'username', '邮箱':'email', '操作':func}

v1.site.register(models.UserInfo,KingUserInfo)


class KingRole(v1.BaseKingAdmin):
    list_display = ['id','name']

v1.site.register(models.Role,KingRole)
