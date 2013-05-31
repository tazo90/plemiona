from django.shortcuts import render, render_to_response
from django.template import RequestContext

def index(request):
    return render(request, "home.html")    
