from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
    contex = {
    'productos': 'productos',
    'usuario': request.user,
    }
    return render(request, 'index/principal.html', contex)

@login_required(login_url='/login/')
def err_permisos(request):
    contex = {
    'productos': 'productos',
    'usuario': request.user,
    }
    return render(request, 'index/error_permisos.html', contex)