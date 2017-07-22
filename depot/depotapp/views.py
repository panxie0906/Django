from django.shortcuts import render

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

# app specific files

from .models import *
from .forms import *


def base_product(request):
    return HttpResponse(request,'depotapp\base_product.html')

def create_product(request):
    
    form = ProductForm(request.POST or None)
    #if request.method == 'POST':        
    #   form = ProductForm(request.POST)
    if form.is_valid():
        form.save()
        form = ProductForm()

    #t = get_template('depotapp/create_product.html')
    #c = RequestContext(request,locals())
    return render(request,'depotapp\create_product.html',{'item':form})#HttpResponse(t.render(c))

def list_product(request):
    list_items = Product.objects.all().values('name','price')
    paginator = Paginator(list_items,5)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
        
    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)
        
    return render(request,'depotapp\list_product.html',{'items':list_items})
    
'''
def list_product(request):
  
    list_items = Product.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depotapp/list_product.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_product(request, id):
    product_instance = Product.objects.get(id = id)

    t=get_template('depotapp/view_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_product(request, id):

    product_instance = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance = product_instance)

    if form.is_valid():
        form.save()

    t=get_template('depotapp/edit_product.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
    '''