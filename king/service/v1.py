#Time : 2017/9/7 9:23
#Author : Michael_chen

from django.shortcuts import render,HttpResponse
from django.urls import reverse

class BaseKingAdmin(object):
    list_display = '__all__'

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    @property
    def urls(self):
        from django.conf.urls import url,include
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$',self.changelist_viwe,name='%s_%s_changelist'%info),
            url(r'^add/$',self.add_view,name='%s_%s_add'%info),
            url(r'^(.+)/delete/$',self.delete_view,name='%s_%s_delete'%info),
            url(r'^(.+)/change/$',self.change_view,name='%s_%s_change'%info),
        ]
        return urlpatterns

    def changelist_viwe(self,request):
        """
        查看列表
        :param request:
        :return:
        """
        # 生成页面上：添加按钮
        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True) #mutable默认为False，意思为禁止修改，强行修改会报错
        if request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()
        base_add_url = reverse('{0}:{1}_{2}_add'.format(self.site.namespace,self.app_label,self.model_name))
        add_url = '{0}?{1}'.format(base_add_url,param_dict.urlencode())

        self.request = request
        result_list = self.model_class.objects.all()
        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'kgadmin_obj':self,
            'add_url':add_url
        }
        return render(request,'kg/change_list.html',context)

    def add_view(self,request):
        """
        添加数据
        :param request:
        :return:
        """
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        data = "%s_%s_add"%info
        return HttpResponse(data)

    def delete_view(self,request,pk):
        """
        删除数据
        :param request:
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_add" % info
        return HttpResponse(data)

    def change_view(self,request,pk):
        """
        修改数据
        :param request:
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = "%s_%s_add" % info
        return HttpResponse(data)


class KingSite(object):
    def __init__(self):
        self._registry = {}
        self.namespace = 'king'
        self.app_name = 'king'

    def register(self,model_class,base_obj=BaseKingAdmin):
        self._registry[model_class] = base_obj(model_class,self)

    def geturls(self):
        from django.conf.urls import url,include
        ret = []
        for model_cls,kg_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            print(app_label,model_name)
            ret.append(url(r'^%s/%s/'%(app_label,model_name),include(kg_admin_obj.urls)))

        return ret

    @property
    def urls(self):
        return self.geturls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse('login')


site = KingSite()



