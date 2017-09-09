import pymysql
from time import time
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.user import *
from ..models.reset import *
from ..models.url import *
from django.contrib import messages
from ..src.authenticator import Authenticator
from ..src.hasher import Hasher
from ..src.id_generator import IdGenerator
from ..src.validator import Validator
from django.views.decorators.http import require_POST


class AuthenticationView:

    atemps = 1
    current_time = 0
    view_time = 0
    view_state = 0

    def version(request):
        return render(request,'hound-eng/select_version.html')

	
    def home_page_eng(request):
        return render(request,'hound-eng/home_page.html')

    def home_page_esp(request):
        return render(request,'hound-esp/home_page.html')	

    def email_auth(request,lenguage):

        template_email = 'hound-eng/email.html'
        template_activation = 'hound-eng/activate_notice.html'
        template_confirmation = 'hound-eng/confirmation_notice.html'
        error = "The user name does not exists, please create an account"
        password = '/password/0/'
        drivers = '/drivers/0/0/'

        if int(lenguage) == 1:
            template_email = 'hound-esp/email.html'
            template_activation = 'hound-esp/activate_notice.html'
            template_confirmation = 'hound-esp/confirmation_notice.html'
            error = "El nombre de usuario no existe, porfavor cree una cuenta"
            password = '/password/1/'
            drivers = '/drivers/1/0/'


        if Validator.validate_view(request):
            return redirect(drivers)

        if request.session.get('tmp') != None:
            request.session['tmp'] = ''

        emailForm = EmailForm()



        if request.method == 'POST':
            emailForm = EmailForm(request.POST)

            if emailForm.is_valid():
                email = emailForm.cleaned_data['email']

                if Authenticator.validate_email_form(email) != '':
                    messages.error(request, Authenticator.validate_email_form(email))
                    return render(request, template_email, {'emailForm': emailForm})

                if Validator.get_user_status(email) != None:
                    if Validator.get_user_status(email) == False:
                        request.session['tmp'] = email
                        return render(request,template_activation)

                if Validator.get_confirmation(email) != None:
                    if Validator.get_confirmation(email) == False:
                        request.session['confirm'] = email
                        return render(request,template_confirmation)

                if User.objects.filter(email = email).exists():
                    request.session['tmp'] = email
                    request.session['tmp_tmp'] = email
                    request.session.modified = True
                    return redirect(password)
                else:
                    messages.error(request,error)
            else:
                messages.error(request,emailForm.errors)
        return render(request,template_email,{'emailForm':emailForm})

    def password_auth(request,lenguage):

        email = '/email/0/'
        drivers = 'drivers/0/0/'
        template_activation = 'hound-eng/activate_notice.html'
        error = "You have exceded the number of allowed atemps"
        password_template = 'hound-eng/password.html'
        incorrect_password = "Incorrect password"

        if int(lenguage) == 1:
            email = '/email/1/'
            template_activation = 'hound-esp/activate_notice.html'
            error = "Has excedido el numero de intentos permitidos"
            password_template = 'hound-esp/password.html'
            incorrect_password = "Contraseña incorrecta"
            drivers = 'drivers/1/0/'

        if request.session.get('tmp') == None:
            return redirect(email)



        if Validator.get_user_status(request.session.get('tmp')) != None:
            if Validator.get_user_status(request.session.get('tmp')) == False:
                return render(request, template_activation)

        if Validator.validate_view(request):
            return redirect(drivers)


        passwordForm = PasswordForm()



        if AuthenticationView.current_time != 0:
            t = time()
            if t >= AuthenticationView.current_time + 40000:
                AuthenticationView.reset_atemps(AuthenticationView)
                request.session.flush()
                response = redirect(email)
                response.delete_cookie('user_location')
                return response
            else:
                messages.error(request, error)
                return render(request, password, {'passwordForm': passwordForm})

        if AuthenticationView.atemps == 5:
            AuthenticationView.current_time = time()
            AuthenticationView.atemps =6

        if AuthenticationView.atemps == 6:
            AuthenticationView.view_state = 0
            AuthenticationView.view_time = 0
        else:
            if AuthenticationView.view_state == 0:
                AuthenticationView.view_state = 1

        if AuthenticationView.view_state == 1:
            AuthenticationView.view_time = time()
            AuthenticationView.view_state = 2



        if AuthenticationView.view_state == 2:

            print (AuthenticationView.view_state)
            print (AuthenticationView.view_time+300)
            view_t = time()
            if view_t >= AuthenticationView.view_time + 300:
                request.session.flush()
                AuthenticationView.view_state = 0
                AuthenticationView.view_time = 0
                response = redirect(email)
                response.delete_cookie('user_location')
                return response


        if request.method == 'POST':

            if AuthenticationView.view_state == 2:
                view_t = time()
                if view_t > AuthenticationView.view_time + 30:
                    request.session.flush()
                    AuthenticationView.view_state = 0
                    AuthenticationView.view_time = 0
                    response = redirect(email)
                    response.delete_cookie('user_location')
                    return response

            passwordForm = PasswordForm(request.POST)
            if passwordForm.is_valid():
                password = passwordForm.cleaned_data['tmp_password']
                if User.objects.filter(email = request.session['tmp']).exists():
                    user = User.objects.get(email = request.session['tmp'])
                    hash = Authenticator.authenticate(request.session['tmp'],password)
                    if user.password == hash:
                        request.session.flush()
                        request.session['id'] = user.user_id

                        AuthenticationView.reset_atemps(AuthenticationView)
                        return redirect(drivers)
                    else:

                        AuthenticationView.atemps += 1
                        messages.error(request,incorrect_password)
            else:
                messages.error(request,passwordForm.errors)
        return render(request,password_template,{'passwordForm':passwordForm})

    def registration(request,lenguage):

        if int(lenguage) == 0:
            template = 'hound-eng/registration.html'
            confirm_template = '/confirm_email/0/'

        elif int(lenguage) == 1:
            template = 'hound-esp/registration.html'
            confirm_template = '/confirm_email/1/'
        else:
            return render(request,'hound-eng/error.html',{'error':'Invalid option'})

        registrationForm = RegistrationForm()

        if request.method == 'POST':
            registrationForm = RegistrationForm(request.POST)
            print(registrationForm.is_valid())
            if registrationForm.is_valid():
                email = registrationForm.cleaned_data['email']
                if not User.objects.filter(email=email).exists():
                    if Authenticator.validate_email(email) == False:

                        if Authenticator.validate_email_form(email) != '':
                            messages.error(request, Authenticator.validate_email_form(email))
                            return render(request, template, {'registrationForm': registrationForm})

                        password = registrationForm.cleaned_data['tmp_password']
                        retype = registrationForm.cleaned_data['retype']
                        if retype != password:
                            messages.error(request, 'Passwords do not match')
                            return render(request, template, {'registrationForm': registrationForm})

                        user = registrationForm.save(commit=False)
                        error = Authenticator.validate_password(password)
                        if error == '':
                            user.password = Authenticator.hashPassword(email,password)
                            user.user_id = IdGenerator.generate_user_id(IdGenerator)
                            user.save()
                        else:
                            messages.error( request, error )
                            return render( request, template, {'registrationForm': registrationForm} )

                        request.session['confirm'] = email

                        msn = "Registration was done successfully"
                        if int(lenguage) == 1:
                            msn = "Registro realizado exitosamente"

                        return render(request, 'hound-eng/alert.html', {'msn': msn, 'view':  confirm_template})

                        #return redirect('/email/')
                    else:
                        error = "Email address already exists"
                        if int(lenguage) == 1:
                            error = "El correo electrónico ya existe"
                        messages.error( request, error )
            else:
                messages.error(request,registrationForm.errors)
        return render(request,template,{'registrationForm':registrationForm})


    def log_out(request,lenguage):
        request.session.flush()
        response = redirect('/email/0/')

        if int(lenguage) == 1:
            response = redirect('/email/1/')

        response.delete_cookie('user_location')

        return response



    def reset_view(request,lenguage,hash):
        email_template = '/email/0/'
        reset_password = 'hound-eng/reset_password.html'
        error_passwords = 'Paswords do not match'
        alert = 'Your password has been successfully reseted'
        error_user = 'User does not exists'
        error_token = 'Invalid token'
        if int(lenguage) == 1:
            email_template = '/email/1/'
            reset_password = 'hound-esp/reset_password.html'
            error_passwords = 'Las contraseñas no coinciden'
            alert = 'Tu contraseña ha sido cambiada exitosamente'
            error_user = 'El nombre de usuario no existe'
            error_token = 'Token invalido'

        if request.session.get('tmp_tmp') == None:
            return redirect(email_template)

        if Url.objects.filter(url = hash,expires__gte=datetime.datetime.now()).exists():
            formReset = ResetForm()
            if request.method == 'POST':
                formReset = ResetForm(request.POST)
                if formReset.is_valid():
                    if Reset.objects.filter(token = formReset.cleaned_data['tmp_token']).exists():
                        reset = Reset.objects.get(token = formReset.cleaned_data['tmp_token'])
                        email = reset.email
                        if User.objects.filter(email=email).exists():
                            user = User.objects.get(email = email)
                            password = formReset.cleaned_data['password']
                            retype = formReset.cleaned_data['retype']
                            if retype != password:
                                messages.error(request, error_passwords)
                                return render(request, reset_password, {'formReset': formReset,'hash':hash})
                            error = Authenticator.validate_password(password)
                            if error == '':
                                user.password =  Authenticator.hashPassword(email,password)
                                user.save()
                                Reset.objects.get(token = reset.token).delete()
                                Url.objects.get(url = hash).delete()
                                request.session.flush()
                                return render(request, 'hound-eng/alert.html',{'msn': alert, 'view': email_template})
                                #return redirect('/email/')

                        else:
                            Reset.objects.get(token=reset.token).delete()
                            Url.objects.get(url=hash).delete()
                            request.session.flush()
                            return render(request,reset_password,{'error':error_user})


                    else:
                        messages.error(request, error_token)
                else:
                    messages.error(request,formReset.errors)
            return render(request,reset_password,{'formReset':formReset,'hash':hash})
        else:
            Reset.objects.get(email=request.session['tmp_tmp']).delete()
            Url.objects.get(url=hash).delete()
            request.session.flush()
            return render(request,'hound-eng/not_found.html')

    def reset(request,lenguage):
        email = '/email/0/'
        if int(lenguage) == 1:
            email = '/email/1/'


        if request.session.get('tmp') == None:
            return redirect(email)

        token = IdGenerator.generate_token_key(IdGenerator)
        hash = Hasher.encode(IdGenerator.generate_token_key(IdGenerator))
        alert = 'An email with a link to reset your password has been sent'

        msg =  "Use the token to reset your password\n Token:"+token+"\n url: http://hound.ziiodek.com/url/0/"+hash+'/'
        header = 'Hound reset password request'
        error = 'Error processing request'

        if int(lenguage) == 1:
            msg =  "Usa el siguiente token para cambiar tu contraseña\n Token:"+token+"\n url: http://hound.ziiodek.com/url/1/"+hash+'/'
            header = 'Hound solicitud de cambio de contraseña'
            alert = 'Un mensage de correo electrónico ha sido enviado para cambiar tu contraseña'
            error = 'Error procesando la solicitud'
        status = send_mail(
            header,
            msg,
            'settings.EMAIL_HOST_USER',
            [request.session['tmp']],
            #['reyes.yahaira.a@gmail.com'],
            fail_silently=False,
        )
        if status > 0 :
            reset = Reset.create(token,request.session['tmp'])
            reset.save()
            url = Url.create(hash)
            url.save()
            return render(request, 'hound-eng/alert.html',{'msn': alert, 'view': email})
            #return redirect('/email/')
        else:
            return render(request, 'hound-eng/error.html', {'error': error})


    def confirm_view(request,lenguage,hash):
        error_confirm = 'Error trying to generate confirmation email'
        error_user = 'User does not exists'
        email = '/email/0/'
        alert = 'Your email address has been confirmed'

        if int(lenguage) == 1:
            error_confirm = 'Error generando correo electrónico de confirmación'
            email = '/email/1/'
            alert = 'Tu dirección de correo electrónico ha sido confirmada'
            error_user = 'El nombre de usuario no existe'

        if request.session.get('confirm') == None:
            return render(request, 'hound-eng/error.html', {'error': error_confirm})

        if Url.objects.filter(url = hash,expires__gte=datetime.datetime.now()).exists():
            if User.objects.filter(email = request.session['confirm']).exists():
                user = User.objects.get(email=request.session['confirm'])
                user.confirmed = True
                user.save()
                Url.objects.get(url=hash).delete()
                request.session.flush()
                return render(request, 'hound-eng/alert.html',
                              {'msn': alert, 'view': email})

            else:
                Url.objects.get(url=hash).delete()
                request.session.flush()
                return render(request,'hound-eng/error.html',{'error':error_user})

        else:
            Url.objects.get(url=hash).delete()
            request.session.flush()
            return render(request,'hound-eng/not_found.html')


    def confirm(request,lenguage):

        error_confirm = 'Error trying to generate confirmation email'
        error_request = 'Error processing request'
        email = '/email/0/'
        alert = 'An email with a link to confirm your email address has been sent'

        if int(lenguage) == 1:
            error_confirm = 'Error generando correo electrónico de confirmación'
            email = '/email/1/'
            error_request = 'Error procesando solicitud'


        if request.session.get('confirm') == None:
            return render(request,'hound-eng/error.html',{'error':error_confirm})

        hash = Hasher.encode(IdGenerator.generate_token_key(IdGenerator))

        header = 'Hound confirm email address request'
        msg =  "url: http://hound.ziiodek.com/confirm/0/" + hash + '/'
        if int(lenguage) == 1:
            header = 'Hound solicitud de confirmación de correo'
            msg = "url: http://hound.ziiodek.com/confirm/1/" + hash + '/'
            alert = 'Un mensaje de correo electrónico ha sido enviado para confirmar tu dirección de correo electrónico'

        status = send_mail(
            header,
            msg,
            'settings.EMAIL_HOST_USER',
            [request.session['confirm']],
            # ['reyes.yahaira.a@gmail.com'],
            fail_silently=False,
        )
        if status > 0:
            url = Url.create(hash)
            url.save()
            return render(request, 'hound-eng/alert.html',
                          {'msn': alert, 'view': email})
            # return redirect('/email/')
        else:
            return render(request, 'hound-eng/error.html', {'error': error_request})

    def reset_atemps(self):
        AuthenticationView.atemps = 0
        AuthenticationView.current_time = 0

    def activate(request,lenguage):
        template = 'hound-eng/activate_notice.html'
        if int(lenguage) == 1:
            template = 'hound-esp/activate_notice.html'
        return render(request,template)







