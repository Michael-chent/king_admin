#Time : 2017/9/7 9:23
#Author : Michael_chen

from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse

class BaseKingAdmin(object):
    list_display = '__all__'
    add_or_edit_model_form = None

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            # 对象由类创建，类由type创建
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"
            _m = type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
            MyModelForm = type('MyModelForm',(ModelForm,),{'Meta':_m})
            return MyModelForm


    @property
    def urls(self):
        from django.conf.urls import url,include
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$',self.changelist_view,name='%s_%s_changelist'%info),
            url(r'^add/$',self.add_view,name='%s_%s_add'%info),
            url(r'^(.+)/delete/$',self.delete_view,name='%s_%s_delete'%info),
            url(r'^(.+)/change/$',self.change_view,name='%s_%s_change'%info),
        ]
        return urlpatterns

    def changelist_view(self,request):
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
        if request.method == 'GET':
            model_form_obj = self.get_add_or_edit_model_form()()
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            if model_form_obj.is_valid():
                # 添加成功，进行跳转
                model_form_obj.save()
                # 反向生成跳转URL
                base_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace,self.app_label,self.model_name))
                list_url = '{0}?{1}'.format(base_list_url,request.GET.get('_changelistfilter'))
                return redirect(list_url)
        context = {
            'form':model_form_obj,
        }

        return render(request,'kg/add.html',context)

    def delete_view(self,request,pk):
        """
        删除数据
        :param request:
        :return:
        """
        self.model_class.objects.filter(pk=pk).delete()
        base_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label, self.model_name))
        list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changelistfilter'))
        return redirect(list_url)

    def change_view(self,request,pk):
        """
        修改数据
        :param request:
        :return:
        """
        # 1.获取_changelistfilter中传递的参数
        # request.GET.get('_changelistfilter')
        # 2.页面显示并提供默认值ModelForm
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('ID不存在')
        if request.method == 'GET':
            model_form_obj = self.get_add_or_edit_model_form()(instance=obj)
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES,instance=obj)
            # instance=obj 没有这个就会创建一条新数据，而不是修改
            if model_form_obj.is_valid():
                model_form_obj.save()
                # base_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace,self.app_label,self.model_name))
                # list_url = '{0}?{1}'.format(base_list_url,request.GET.get('_changelistfilter'))
                base_list_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label, self.model_name))
                list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)
        # 3.返回页面
        context = {
            'form':model_form_obj,
        }
        return render(request,'kg/edit.html',context)


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
            ret.append(url(r'^%s/%s/'%(app_label,model_name),include(kg_admin_obj.urls)))

        return ret

    @property
    def urls(self):
        return self.geturls(),self.app_name,self.namespace

    def login(self,request):
        return HttpResponse('login')


site = KingSite()



