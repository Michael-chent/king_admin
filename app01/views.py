from django.shortcuts import render,HttpResponse
from app01 import models

def test(request):
    user_group_list = models.UserGroup.objects.all()
    return render(request,'test.html',{'user_group_lilst':user_group_list})

def add_test(request):
    if request.method == 'GET':
        return render(request,'add_test.html')
    else:
        popid = request.GET.get('popup')
        if popid:
            title = request.POST.get('title')
            obj = models.UserGroup.objects.create(title=title)
            return render(request,'popup_response.html',{'id':obj.id,'title':obj.title,'popid':popid})
        else:
            title = request.POST.get('title')
            models.UserGroup.objects.create(title=title)
            return HttpResponse('重定向到列表页面')












