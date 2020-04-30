from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from aplicaciones.web.models import Marca, Catalagos, Promocion, Evento, RegistroExpo, Vacante, Postulacion
from aplicaciones.web.forms import CooreoForm, IncribirForm, PostulacionForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.
class Home(TemplateView):
    template_name="web/index.html"

    def get_context_data(self, **kwargs): 
        context = super(Home, self).get_context_data(**kwargs)
        # context['galeria_list'] = Galeria.objects.all()
        # context['form_correo'] = CorreoForm()
        # context['even_nombre'] = Evento.objects.all()
        context['marca_list'] = Marca.objects.all()
        context['catagolo_list'] = Catalagos.objects.all()[:8]
        context['promo_list'] = Promocion.objects.all()
        context['evento_list'] = Evento.objects.all()
        context['msn_ccs'] = CooreoForm()
        return context
    def post(self, request, *args, **kwargs):
        form = CooreoForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje guardado correctamente')
        else:
            messages.warning(request, 'Error al guardar')
        url=reverse('web:inicio')
        url=url+'#contact'
        return redirect(url)


class IncribirCreate(CreateView):
    template_name = 'form_create.html'
    model = RegistroExpo
    form_class = IncribirForm
    def get_success_url(self):
        url=reverse('web:inicio')
        url=url+'#expos'
        messages.success(self.request, 'Inscrito guardado correctamente')
        return url
    
    def get_context_data(self, **kwargs): 
        context = super(IncribirCreate, self).get_context_data(**kwargs)
        context['detalle_object'] = Evento.objects.get(id=self.request.GET.get('codex'))
        return context



class VacanteView(ListView):
    template_name = "web/vacantes.html"
    model = Vacante


class PostularCreate(CreateView):
    template_name = 'form_create.html'
    model = Postulacion
    form_class = PostulacionForm
    def get_success_url(self):
        url=reverse('web:vacantes')
        messages.success(self.request, 'Postulacion exitosa, si cumple con los requisitos un agente de RH se comunicara con usted.')
        return url