from django.shortcuts import render
from django.shortcuts import redirect
from ..models.user import *
from ..models.url import *
from ..src.authenticator import Authenticator
from ..src.id_generator import IdGenerator
from django.contrib import messages
from ..src.hasher import Hasher
from django.core.mail import send_mail

class ActivateView:

    def activate_view(request,lenguage,hash):

        error_password = 'Incorrect Password'
        error_user = 'User dows not exists'
        activate = 'hound-eng/reactivate_account.html'
        email_url = '/email/0/'

        if int(lenguage) == 1:
            error_password = 'Contraseña incorrecta'
            error_user = 'El usuario no existe'
            activate = 'hound-esp/reactivate_account.html'
            email_url = '/email/1/'


        if Url.objects.filter(url = hash,expires__gte=datetime.datetime.now()).exists():
            formActivate = ActivateForm()
            if request.method == 'POST':
                formActivate = ActivateForm(request.POST)
                if formActivate.is_valid():
                    email = formActivate.cleaned_data['email']
                    if User.objects.filter(email=email).exists():
                        user =  User.objects.get(email=email)
                        tmp_password = formActivate.cleaned_data['tmp_password']
                        tmp_password = Authenticator.authenticate(email,tmp_password)
                        if user.password == tmp_password:
                            if user.active == False:
                                user.active = True
                                user.save()
                                Url.objects.get(url=hash).delete()
                                return redirect(email_url)
                        else:
                            return render(request,'hound-eng/error.html',{'error':error_password})

                    else:
                        return render(request,'hound-eng/error.html',{'error':error_user})


                else:
                    messages.error(request,formActivate.errors)
            return render(request,activate,{'formActivate':formActivate,'hash':hash})
        else:
            Url.objects.get(url=hash).delete()
            return render(request,'hound-eng/not_found.html')

    def activate(request,lenguage):

        email = '/email/0/'
        msg =  "url: http://hound.ziiodek.com/url_activate/0/" + hash + '/'
        header = 'Hound reactivate request'
        error = 'Error processing request'

        if int(lenguage) == 1:
            email = '/email/1/'
            msg = "url: http://hound.ziiodek.com/url_activate/1/" + hash + '/'
            header = 'Hound solicitud de reactivación de cuenta'
            error = 'Error procesando solicitud'

        hash = Hasher.encode(IdGenerator.generate_token_key(IdGenerator))
        status = send_mail(
            header,
            msg,
            'settings.EMAIL_HOST_USER',
            [request.session['tmp']],
            #['reyes.yahaira.a@gmail.com'],
            fail_silently=False,
        )
        if status > 0:
            url = Url.create(hash)
            url.save()
            return redirect(email)
        else:
            return render(request, 'hound-eng/error.html', {'error': error})



