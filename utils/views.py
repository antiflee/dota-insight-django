from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def slides(request):
    return HttpResponseRedirect('https://docs.google.com/presentation/d/1YrbU6vBK0_jchzj-x7RPRLyQJft8U83qO6RziF-5Ijw/edit#slide=id.p')

def sourceCode(request):
    return HttpResponseRedirect('https://github.com/antiflee/InsightDEProject/')
