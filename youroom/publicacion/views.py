from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import PublicacionForm
from .models import Publicacion, Etiqueta, Destacada
from usuario.models import UsuarioPerfil, Premium, ContadorVida
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core import serializers
from django.shortcuts import get_object_or_404, render

@method_decorator(login_required, name='dispatch')
class PublicacionView(TemplateView):
    template_name = 'publicacion/publicacion.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(PublicacionView, self).get_context_data(**kwargs)
            context['formulario_imagen'] = PublicacionForm()
            usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
            info_usuario = ContadorVida.objects.filter(perfil=usuario)
            data = serializers.serialize('json', info_usuario)
            context['info_usuario'] = data
            return context
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

@method_decorator(login_required, name='dispatch')
class SubirPublicacionView(FormView):
    form_class = PublicacionForm
    template_name = 'publicacion/publicacion.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        try:
            usuario_perfil = UsuarioPerfil.objects.get_or_create(user=self.request.user)[0]
            #Si es gratuito, comprobamos que tenga suficientes vidas, restando primero siempre las semanales gratuitas
            cont = ContadorVida.objects.get(perfil=usuario_perfil)
            #Creamos la variable para después decidir si puede publicar
            puede = False
            #Si el usuario es premium, puede publicar
            if not cont.estaActivo:
                puede = True
    
            #Tiene 1 vidas semanales disponibles
            elif cont.numVidasSemanales >=1:
                cont.numVidasSemanales-=1
                cont.save()
                puede = True
    
            #No tiene vidas semanales pero si compradas
            elif cont.numVidasCompradas >=1:
                cont.numVidasCompradas-=1
                cont.save()
                puede = True
            else:
                messages.info(self.request,'Necesitas 1 vida mínimo para poder publicar. Puedes comprarla en la tienda!')
    
            if puede:
                publicacion = Publicacion.objects.create(
                    usuario=usuario_perfil,
                    imagen=form.cleaned_data['imagen'],
                    categoria=form.cleaned_data.get('categoria'),
                    descripcion=form.cleaned_data.get('descripcion')
                )
                etiquetas = form.cleaned_data.get('etiquetas')
                if etiquetas != '':
                    etiquetas_list = etiquetas.split("|")
                    i = 1
                    for e in etiquetas_list:
                        etiqueta_elemento = e.split(",")
                        Etiqueta.objects.create(
                            nombre="e-" + str(publicacion.id) + "-" + str(i),
                            enlace=etiqueta_elemento[0],
                            coord_x=float(etiqueta_elemento[1]),
                            coord_y=float(etiqueta_elemento[2]),
                            publicacion=publicacion
                        )
            return super().form_valid(form)
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

@method_decorator(login_required, name='dispatch')
class DestacarPublicacionView(TemplateView):
    template_name = 'perfil/perfil.html'


    def get(self, request, publicacion_id):
        try:
            publicacion_id = publicacion_id
            publicacion = Publicacion.objects.get(id=publicacion_id)
            perfil = UsuarioPerfil.objects.get_or_create(user = self.request.user)[0]
            destacada_contador = Destacada.objects.filter(publicacion=publicacion).count()
    
            #Comprobaciones de perfil de usuario
            if (publicacion.usuario == perfil) and (destacada_contador == 0):
    
                #Si es premium, comprobamos que tenga 50 puntos y le restamos el 10% de sus puntos
                if Premium.objects.filter(perfil=perfil).exists():
                    if perfil.totalPuntos>=50:
                        perfil.totalPuntos = int(perfil.totalPuntos*0.9)
                        perfil.save()
                        messages.info(request,'Has perdido el 10% de tus puntos. Tranquilo, los recuperarás!')
                        destacada = Destacada.objects.create(es_destacada=True,publicacion=publicacion)
                    else:
                        messages.info(request,'Necesitas 50 puntos mínimo para poder destacar la publicación. ¡Sigue publicando :D!')
                else:
                    #Si es gratuito, comprobamos que tenga suficientes vidas, restando primero siempre las semanales gratuitas
                    cont = ContadorVida.objects.get(perfil=perfil)
    
                    #Caso 1: tiene 2 vidas semanales disponibles
                    if cont.numVidasSemanales >=2:
                        cont.numVidasSemanales-=2
                        cont.save()
                        messages.info(request,'Has destacado usando 2 vidas semanales. Tú sí que sabes!')
                        destacada = Destacada.objects.create(es_destacada=True,publicacion=publicacion)
    
                    #Caso 2: tiene 1 vida semanal y mínimo una vida comprada
                    elif cont.numVidasSemanales==1 and cont.numVidasCompradas >=1:
                        cont.numVidasSemanales-=1
                        cont.numVidasCompradas-=1
                        cont.save()
                        messages.info(request,'Has hecho uso de una vida gratuita y otra comprada. Aprovechando los recursos!')
                        destacada = Destacada.objects.create(es_destacada=True,publicacion=publicacion)
    
                    #No tiene vidas semanales pero si compradas
                    elif cont.numVidasCompradas >=2:
                        cont.numVidasCompradas-=2
                        cont.save()
                        destacada = Destacada.objects.create(es_destacada=True,publicacion=publicacion)
                        messages.info(request,'Has destadado la publicación con 2 vidas compradas. Enhorabuena!')
                    else:
                        messages.info(request,'Necesitas 2 vidas mínimo para poder destacar la publicación. Puedes comprarlas en la tienda!')
    
            return HttpResponseRedirect('/perfil/')
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(request, 'base/error.html', context)
        
