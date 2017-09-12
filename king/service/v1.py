#Time : 2017/9/7 9:23
#Author : Michael_chen

import copy

from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse


class BaseKingAdmin(object):
    list_display = '__all__'
    add_or_edit_model_form = None
    action_list = []
    filter_list = []

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
        from django.conf.urls import url
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
        # 分页开始
        condition = {}
        from king.utils.pager import PageInfo
        all_count = self.model_class.objects.filter(**condition).count() #筛选条件下，共有多少数据
        base_page_url = reverse("{0}:{1}_{2}_changelist".format(self.site.namespace,self.app_label,self.model_name))
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True
        page_obj = PageInfo(request.GET.get('page'),all_count,base_page_url,page_param_dict)
        result_list = self.model_class.objects.filter(**condition)[page_obj.start:page_obj.end]
        # 分页结束

        # get请求，显示下拉框
        action_list = []
        for item in self.action_list:
            tpl = {'name':item.__name__,'text':item.text}
            action_list.append(tpl)
        if request.method == 'POST':
            # 获取action
            func_name_str = request.POST.get('action')
            print("***",func_name_str)
            ret = getattr(self,func_name_str)(request)
            action_page_url = reverse("{0}:{1}_{2}_changelist".format(self.site.namespace,self.app_label,self.model_name))
            if ret :
                action_page_url = "{0}?{1}".format(action_page_url,request.GET.urlencode())
            return redirect(action_page_url)

        # ################ 组合搜索操作 ##################
        from king.utils.filter_code import FilterList
        filter_list = []
        for option in self.filter_list:
            if option.is_func:
                data_list = option.field_or_func(self,option,request)
            else:
                from django.db.models import ForeignKey,ManyToManyField
                field = self.model_class._meta.get_field(option.field_or_func)

                # 因为OneToOneField 继承 ForeignKey,如果有OneToOne字段，一定要写在ForeignKey的前面
                # if isinstance(field,OneToOneField):
                #     data_list = field.rel.model.objects.all()
                if isinstance(field,ForeignKey):
                    # data_list = field.rel.model.objects.all() # UserGroup 表
                    data_list = FilterList(option,field.rel.model.objects.all(),request)
                elif isinstance(field,ManyToManyField):
                    # data_list = field.rel.model.objects.all() # Role 表
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                else:
                    # data_list = field.model.objects.all()
                    data_list = FilterList(option, field.model.objects.all(), request)
            filter_list.append(data_list)

        context = {
            'filter_list':filter_list,
            'result_list':result_list,
            'list_display':self.list_display,
            'kgadmin_obj':self,
            'add_url':add_url,
            'page_str':page_obj.pager(),
            'action_list':action_list
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
                obj = model_form_obj.save()
                # 如果是popup
                popid = request.GET.get('popup')
                if popid:
                    return render(request,'kg/popup_response.html',{'data_dict':{'pk':obj.pk,'text':str(obj),'popid':popid}})
                else:
                    # 添加成功，进行跳转
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



