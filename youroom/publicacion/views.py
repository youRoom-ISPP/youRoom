import time
from datetime import datetime
from django.urls import reverse
from publicacion.models import Publicacion
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from publicacion.forms import FormularioPublicacion

class PublicacionView(TemplateView):
    
    def create_formulario_publicacion(request):
        if request.method == 'POST':
            PublicacionView.create_publicacion(request)
            return redirect('/publicacion_realizada/')
        else:
            form = FormularioPublicacion()
            return render(request, 'publicacion/form_publicacion.html', {'form':form})


    def create_publicacion(request):
        form = FormularioPublicacion(request.POST)
        if form.is_valid():
            errors = []
            descripcion = form.cleaned_data.get('descripcion')

            if not descripcion:
                errors.append('La descripción no puede estar vacía')
                return render(request, 'publicacion/form_publicacion.html', {'form':form, 'errors':errors})

            categoria = form.cleaned_data.get('categoria')
            hora_actual = datetime.now()

            publicacion = Publicacion.objects.get_or_create(
                descripcion=descripcion,
                categoria=categoria,
                fecha_publicacion=hora_actual
            )
            
        else:
            return render(request, 'publicacion/form_publicacion.html', {'form':form})

    def publicado_exito(request):
        return render(request, 'publicacion/exito.html')


