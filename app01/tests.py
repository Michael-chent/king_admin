from django.test import TestCase


# class Foo(object):
#     _instance = None
#
#     def __init__(self):
#         pass
#
#     @classmethod
#     def get_instance(cls):
#         if cls._instance:
#             return cls._instance
#         else:
#             obj = cls()
#             cls._instance = obj
#             return obj
#
# obj1 = Foo.get_instance()
# obj2 = Foo.get_instance()


# class Foo(object):
#     _instance = None
#
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instance:
#             return cls._instance
#         else:
#             obj = object.__new__(cls,*args,**kwargs)
#             cls._instance = obj
#             return obj
#
# obj1 = Foo()
# obj2 = Foo()
#
# print(id(obj1))
# print(id(obj2))
# print(obj1 == obj2)
# print(obj1 is obj2)

class FilterList(object):
    def __init__(self,option,data_list):
        self.option = option
        self.data_list =data_list

    def show(self):
        self.option.nick()

    def __iter__(self):
        yield "全部 ："
        for i in self.data_list:
            yield "<a href='{0}'>{1}</a>".format(i,self.option.bs+i)

class FilterOption(object):
    def __init__(self,brand,output):
        self.brand = brand
        self.output = output

    def nick(self):
        tpl = self.brand + str(self.output)
        return tpl

    @property
    def bs(self):
        if self.output > 300:
            return "大"
        else:
            return "小"

obj_list = [
    FilterList(FilterOption('春风',650),['拉力','街车','越野','沙滩']),
    FilterList(FilterOption('铃木',250),['拉力','街车','越野','沙滩']),
    FilterList(FilterOption('本田',150),['拉力','街车','越野','沙滩']),
    FilterList(FilterOption('川崎',650),['拉力','街车','越野','沙滩']),
]

for obj in obj_list:
    for item in obj:
        print(item,end="  ")
    else:
        print()



































