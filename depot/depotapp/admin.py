from django.contrib import admin

# Register your models here.
from .models import depot

class BaseAdmin(admin.ModelAdmin):
	list_displa=('name','price')#指定要显示的字段
	search_fields=('name',)#指定要搜索的字段，将会出现一个搜索框让管理员搜索关键字
	list_filter=('name',)
	'''指定列表过滤器，右边将出现一个快捷的日期过滤选项，
	以便开发人员快速定位想要的数据，同样你也可以指定非日期类的字段
	'''
	'''
	#分组表单,当有多个表单相关联时可以使用这个属性
	fieldsets=(
	()，
	)
	'''
admin.site.register(depot.Product,BaseAdmin)