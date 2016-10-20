# -*- encoding: UTF-8 -*-
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class HomepageView(TemplateView):
    '''
    HomePage
    '''
    template_name = 'shop/homepage/index.html'
