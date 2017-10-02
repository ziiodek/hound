import pymysql
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.user import *
from ..models.profile import *
from ..models.url import *
from ..src.authenticator import Authenticator
from ..src.id_generator import IdGenerator
from ..models.reset import ChangePasswordForm
from ..src.database import Database
from ..static.hound.data.uploader import Uploader
from ..src.validator import Validator
from django.contrib import messages
from ..src.hasher import Hasher
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.http import HttpResponse

class SettingsView:
    atemps = 1

    def settings(request,lenguage):
        email = '/email/0/'
        error_user = 'User does not exists'
        settings = 'hound-eng/settings.html'
        error_email = 'Email address already exists'
        alert = 'Information updated successfully'
        settings_url = '/settings/0/'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_user = 'El usuario no existe'
            settings = 'hound-esp/settings.html'
            error_email = 'El correo electronico ya existe'
            alert = 'Informacion actualizada exitozamente'
            settings_url = '/settings/1/'
        if not Validator.validate_view(request):
            return redirect(email)

        formProfile = ProfileForm()
        profile = SettingsView.load_tmp_profile(request.session['id'])


        if User.objects.filter(user_id=request.session['id']).exists():
            user = User.objects.get(user_id=request.session['id'])

        else:
            return render(request,'hound-eng/error.html',{'error',error_user})

        formSettings = SettingsForm(request.POST or None, instance=user)

        if request.method == 'POST':
            formSettings = SettingsForm(request.POST)
            if formSettings.is_valid():
                tmp = formSettings.save(commit=False)
                error = ''

                if Validator.check_pattern(tmp.name) == True:
                    error = 'Name must not have symbols'
                    if int(lenguage) == 1:
                        error = 'Nombre no debe de contener symbolos'

                    messages.error(request,error)
                    return render(request, settings, {'formSettings': formSettings,
                                                      'formProfile': formProfile,
                                                      'profile': profile})

                if Validator.check_pattern(tmp.last_name) == True:
                    error = 'Lastname must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Apellido no debe de contener simbolos'

                    messages.error(request,error)
                    return render(request, settings, {'formSettings': formSettings,
                                                      'formProfile': formProfile,
                                                      'profile': profile})


                user = User.objects.get(user_id=request.session['id'])
                user.name = tmp.name
                user.last_name = tmp.last_name
                user.company = tmp.company

                if tmp.email != user.email and User.objects.filter(email = tmp.email).exists():
                    messages.error(request,error_email)
                else:
                    user.email = tmp.email
                    user.save()
                    SettingsView.save_profile(request.session['id'])
                    Database.clear_profile(request.session['id'], 'logo')
                    return render(request, 'hound-eng/alert.html',
                                  {'msn': alert, 'view': settings_url})

            else:
                messages.error(request,formSettings.errors)

        return render(request,settings,{'formSettings':formSettings,
                                                         'formProfile':formProfile,
                                                         'profile':profile})



    def load_tmp_profile(user_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select path from hound_profile where user_id='%s' and type='%s';" % (user_id, 'logo'))
        if cursor.rowcount <= 0:
            cursor.execute("select profile_img from hound_user where user_id='%s';" % (user_id))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                try:
                    cursor.execute(
                        "insert into hound_profile (user_id, type,path) values('%s','%s','%s');" % (
                            user_id, 'logo', data[0]))
                    database.commit()
                except:
                    database.rollback()
                src = data[0]
            else:
                try:
                    cursor.execute(
                        "insert into hound_profile (user_id, type,path) values('%s','%s','%s');" % (
                            user_id, 'trailer', 'hound/images/default.jpg'))
                    database.commit()
                except:
                    database.rollback()
        else:
            data = cursor.fetchone()
            src = data[0]
        database.close()
        return src

    @require_POST
    def upload_profile(request,lenguage):

        email_template = '/email/0/'
        settings_template = '/settings/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            settings_template = '/settings/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':

            if Profile.objects.filter(user_id=request.session['id']).filter(type='logo'):
                profile = Profile.objects.get(user_id=request.session['id'], type='logo')
                formProfile = ProfileForm(request.POST or None, request.FILES, instance=profile)
            else:
                formProfile = ProfileForm(request.POST, request.FILES)

            if formProfile.is_valid():
                file = request.FILES['profile']
                profile = formProfile.save(commit=False)
                fs = FileSystemStorage()
                url = request.session['id'] + '/logo/' + file.name
                if not fs.exists(request.session['id'] + '/logo/'  + file.name):
                    filename = fs.save(request.session['id'] + '/logo/'  + file.name, file)
                    url = fs.url(filename)

                Uploader.create_directory('/' + request.session['id'] + '/logo/')
                Uploader.clear_directory('/' + request.session['id'] + '/logo')
                Uploader.move_file('/system/hound/images/' + url,
                                   '/' + request.session['id'] + '/logo/'  + file.name)
                profile.type = 'logo'
                profile.path = 'hound/data/' + request.session['id'] + '/logo/'  + file.name
                profile.user_id = request.session['id']
                profile.save()
                Uploader.clear_tmp_dir('/system/hound/images/')

                return redirect(settings_template)

    def save_profile(user_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' ;" % (user_id, 'logo'))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            try:
                cursor.execute("select profile_img from hound_user where user_id='%s';" % (user_id))
                if cursor.rowcount > 0:
                    cursor.execute("update hound_user set profile_img='%s' where user_id='%s';" % (data[0], user_id))
                    database.commit()
                else:
                    cursor.execute("insert into hound_user (user_id_id,profile_img) values('%s','%s');" % (user_id, data[0]))
                    database.commit()
            except:
                database.rollback()
        database.close()

    def change_view(request,lenguage,hash):
        email = '/email/0/'
        error_atemps = 'You have exceded the number of allowed atemps'
        alert = 'Your password has been successfully changed'
        error_match = 'Passwords do not match'
        error_passwords = 'Incorrect Password'
        change_password = 'hound-eng/change_password.html'
        settings = '/settings/0/'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_atemps = 'Has excedido el numero de intentos permitidos'
            alert = 'Tu contraseña ha sido cambiada exitosamente'
            error_match = 'Las contraseñas no coinciden'
            error_passwords = 'Contraseña incorrecta'
            change_password = 'hound-esp/change_password.html'
            settings = '/settings/1/'

        if not Validator.validate_view(request):
            if Url.objects.filter(url=hash).exists():
                Url.objects.get(url=hash).delete()
            return redirect(email)

        if SettingsView.atemps == 5:
            SettingsView.atemps = 0
            Url.objects.get(url=hash).delete()
            return render(request,'hound-eng/error.html',error_atemps)

        if Url.objects.filter(url = hash,expires__gte=datetime.datetime.now()).exists():
            formChangePassword = ChangePasswordForm()
            if request.method == 'POST':
                formChangePassword = ChangePasswordForm(request.POST)
                if formChangePassword.is_valid():
                    old_password = formChangePassword.cleaned_data['old_password']
                    user = User.objects.get(user_id = request.session['id'])
                    old_password = Authenticator.authenticate(user.email,old_password)
                    if user.password == old_password:
                        new_password = formChangePassword.cleaned_data['new_password']
                        retype = formChangePassword.cleaned_data['retype']
                        if new_password == retype:
                            error = Authenticator.validate_password(new_password)
                            if error == '':
                                user.password = Authenticator.hashPassword(user.email,new_password)
                                user.save()
                                Url.objects.get(url=hash).delete()
                                return render(request, 'hound-eng/alert.html',{'msn': alert, 'view': settings})
                                #return redirect('/settings/')
                            else:
                                messages.error(request,error)
                        else:
                            messages.error(request,error_match)
                    else:
                        SettingsView.atemps += 1
                        messages.error(request,error_passwords)

                else:
                    messages.error(request,formChangePassword.errors)
            return render(request,change_password,{'formChangePassword':formChangePassword,'hash':hash})
        else:
            Url.objects.get(url=hash).delete()
            return render(request,'hound-eng/not_found.html')

    def change(request,lenguage):

        hash = Hasher.encode(IdGenerator.generate_token_key(IdGenerator))

        email = '/email/0/'
        error_user = 'User does not exists'
        header = 'Hound change password request'
        msg =  "url: http://hound.ziiodek.com/url_settings/0/" + hash + '/'
        alert = 'An email with a link to change your password has been sent'
        settings = '/settings/0/'
        error_process = 'Error processing request'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_user = 'El usuario no existe'
            header = 'Hound solicitud de cambio de contraseña'
            msg = "url: http://hound.ziiodek.com//url_settings/1/" + hash + '/'
            alert = 'Un correo electronico para cambiar tu contraseña ha sido enviado'
            settings = '/settings/1/'
            error_process = 'Error procesando solicitud'

        if not Validator.validate_view(request):
            return redirect(email)

        if User.objects.filter(user_id=request.session['id']).exists():
            user = User.objects.get(user_id= request.session['id'])
        else:
            return render(request,'hound-eng/error.html',{'error':error_user})


        status = send_mail(
            header,
            msg,
            'settings.EMAIL_HOST_USER',
            [user.email],
            #['reyes.yahaira.a@gmail.com'],
            fail_silently=False,
        )
        if status > 0:
            url = Url.create(hash)
            url.save()
            return render(request,'hound-eng/alert.html',{'msn': alert, 'view': settings})
            #return redirect('/settings/')
        else:
            return render(request, 'hound-eng/error.html', {'error': error_process})



