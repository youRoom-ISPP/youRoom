from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView as auth_view
from django.contrib.auth.models import User
from .models import UsuarioPerfil, ContadorVida
from .forms import RegistroForm
from django.urls import reverse_lazy

class LoginView(auth_view):
    template_name = 'usuario/login.html'
    redirect_authenticated_user=True

class RegistroView(FormView):
    form_class = RegistroForm
    template_name = 'usuario/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form, **kwargs):
        try:
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            descripcion = form.cleaned_data['descripcion']
            if password1 == password2:
                if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                    print('LLego aqui')
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    perfil = UsuarioPerfil(user=user, descripcion=descripcion)
                    perfil.save()
                    cv = ContadorVida(perfil=perfil)
                    cv.save()
                    return super().form_valid(form)
                else:
                    context = self.get_context_data(form=form)
                    return self.render_to_response(context)
            else:
                context = self.get_context_data(form=form)
                return self.render_to_response(context)
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)