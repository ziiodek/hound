import xlwt
import pymysql
from xlwt import XFStyle
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.trailer import *
from ..models.profile import *
from ..src.id_generator import IdGenerator
from ..src.xls_generator import XlsGenerator
from ..src.database import Database
from ..static.hound.data.uploader import Uploader
from ..src.validator import Validator
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.http import HttpResponse



class TrailerView:

    def get_all_trailers(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción Invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == "1":
            status = True
            template = 'hound-eng/archiver_trailers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/archiver_trailers.html'

        elif status == "0":
            status = False
            template = 'hound-eng/assets_trailers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/assets_trailers.html'

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        Database.clear_profile(request.session['id'], 'trailer')
        formSearchTrailer = SearchTrailerForm()

        if int(lenguage) == 0:
            table = TrailerView.generate_table(None, request.session['id'], status)
            table.paginate(page=request.GET.get('page', 1), per_page=5)
        elif int(lenguage) == 1:
            table = TrailerView.generate_table_esp(None, request.session['id'], status)
            table.paginate(page=request.GET.get('page', 1), per_page=5)
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        return render(request,template, {'table': table,'formSearchTrailer':formSearchTrailer,'status':status})

    def view_trailer(request,lenguage,economic_no):

        email_template = '/email/0/'
        error_trailer = 'Trailer does not exists'
        view_template = 'hound-eng/view_trailer.html'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trailer = 'La caja no existe'
            view_template = 'hound-esp/view_trailer.html'

        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        if Trailer.objects.filter(user_id=user_id).filter(economic_no=economic_no).exists():
            trailer = Trailer.objects.get(user_id=user_id, economic_no=economic_no)
            formTrailer = TrailerForm(instance=trailer)
            profile = TrailerView.load_tmp_profile(user_id, economic_no)
            active = trailer.active

            return render(request, view_template, {
                'formTrailer': formTrailer,
                'profile': profile,
                'economic_no': economic_no,
                'active':active
            })
        else:
            return render(request, 'hound-eng/error.html', {'error': error_trailer})


    def add_trailer(request,lenguage):

        email_template = '/email/0/'
        view_template = '/view_trailer/0/'
        error_user = 'Username does not exists'
        add_template = 'hound-eng/add_trailer.html'
        error_version = 'For the free version you can only register 100 trailers, upgrade to Big Company to register up to 10 trailers'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = '/view_trailer/1/'
            error_user = 'El nombre de usuario no existe'
            add_template = 'hound-esp/add_trailer.html'
            error_version = 'Solo puedes registrar 100 cajas en la versión gratis, actualiza a Big Company para registrar mas de 100 cajas'



        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        economic_no = IdGenerator.generate_economic_no(user_id,'trailers')
        country = None
        if request.method == 'POST':

            if Trailer.objects.filter(user_id=user_id).count() >= 100:
                return render(request, 'hound-eng/error.html', {'error': error_version})

            formTrailer = TrailerForm( request.POST )

            if formTrailer.is_valid():
                trailer = formTrailer.save(commit=False)
                error = ''
                if trailer.plate_no != '':
                    if len(trailer.plate_no) < 5 or len(trailer.plate_no) > 10:
                        error = 'Plate number must have 5 to 10 character length'

                        if int(lenguage) == 1:
                            error = 'Número de placas debe de tener de 5 a 10 caracteres'

                    if Validator.check_pattern(trailer.plate_no) == True:
                        error = 'Plate number must not have symbols'

                        if int(lenguage == 1):
                            error = 'Número de placas no debe de contener simbolos'

                if Validator.check_pattern(trailer.client_name) == True:
                    error = 'Client Name must not have symbols'
                    if int(lenguage == 1):
                        error = 'Nombre de cliente no debe de contener simbolos'

                if Validator.check_pattern(trailer.client_last_name) == True:
                    error = 'Client Lastname must not have symbols'
                    if int(lenguage == 1):
                        error = 'Apellido de cliente no debe de contener simbolos'

                if trailer.capacity != None and trailer.capacity < 0:
                    error = 'Capacity must be a positive number'

                    if int(lenguage) == 1:
                        error = 'Capacidad debe de ser un número'

                if error == '':
                    if User.objects.filter(user_id=user_id).exists():
                        country = request.POST.get("country_select")
                        if country == "USA":
                            state = request.POST.get("states_usa")
                        elif country == "MX":
                            state = request.POST.get("states_mx")
                        else:
                            state = ""
                            country = ""

                        type = formTrailer.cleaned_data['type_select']
                        if formTrailer.cleaned_data['type_select'] == None:
                            type = ""
                        trailer.user_id = User.objects.get(user_id=user_id)
                        trailer.economic_no = int(economic_no)
                        trailer.state = state
                        trailer.country = country
                        trailer.type = type
                        trailer.save()
                        TrailerView.save_profile(user_id, economic_no)
                        Database.clear_profile(user_id, 'trailer')
                        economic_no = IdGenerator.store_economic_no(user_id, 'trailers')
                        return redirect(view_template+str(economic_no)+'/')
                    else:
                        return render( request, 'hound-eng/error.html', {'error': error_user} )
                else:
                    messages.error( request, error )

            else:
                messages.error(request,formTrailer.errors)


        formTrailer = TrailerForm( initial={'economic_no': economic_no,'country':country} )
        formProfile = ProfileForm()
        profile = TrailerView.load_tmp_profile(user_id, economic_no)
        return render(request,add_template,
                      {'formTrailer':formTrailer,
                       'formProfile':formProfile,
                       'profile': profile,
                       'economic_no':economic_no,
                       })


    def edit_trailer(request,lenguage,economic_no):

        email_template = '/email/0/'
        error_trailer = 'Trailer does not exists'
        view_template = '/view_trailer/0/'
        error_fields = 'Fill all the required fields'
        edit_template = 'hound-eng/edit_trailer.html/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trailer = 'La caja no existe'
            view_template = '/view_trailer/0/'
            error_fields = 'Por favor llena los campos que se te piden'
            edit_template = 'hound-esp/edit_trailer.html/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        user = User.objects.get( user_id=user_id )

        if not Trailer.objects.filter(user_id=user, economic_no=economic_no ).exists():
            return render(request,'hound-eng/error.html',{'error':error_trailer})

        trailer = Trailer.objects.get( user_id=user, economic_no=economic_no )
        formTrailer = TrailerForm(request.POST or None,instance=trailer )
        formProfile = ProfileForm()
        profile = TrailerView.load_tmp_profile(user_id, economic_no)
        active = trailer.active


        if request.method == 'POST':
            if formTrailer.is_valid():
                tmp = formTrailer.save(commit=False)

                error = ''

                if tmp.plate_no != '':
                    if len(tmp.plate_no) < 5 or len(tmp.plate_no) > 10:
                        error = 'Plate number must have 5 to 10 character length'

                        if int(lenguage) == 1:
                            error = 'Número de placas debe de tener de 5 a 10 caracteres'

                    if Validator.check_pattern(tmp.plate_no) == True:
                        error = 'Plate number must not have symbols'

                        if int(lenguage == 1):
                            error = 'Número de placas no debe de contener simbolos'

                if Validator.check_pattern(tmp.client_name) == True:
                    error = 'Client Name must not have symbols'
                    if int(lenguage == 1):
                        error = 'Nombre de cliente no debe de contener simbolos'

                if Validator.check_pattern(tmp.client_last_name) == True:
                    error = 'Client Lastname must not have symbols'
                    if int(lenguage == 1):
                        error = 'Apellido de cliente no debe de contener simbolos'

                if tmp.capacity < 0:
                    error = 'Capacity must be a positive number'

                    if int(lenguage) == 1:
                        error = 'Capacidad debe de ser un número'

                if error == '':
                    country = request.POST.get("country_select")
                    if country == "USA":
                        state = request.POST.get("states_usa")
                    elif country == "MX":
                        state = request.POST.get("states_mx")
                    else:
                        country = trailer.country
                        state = trailer.state

                    if state == "":
                        state = trailer.state

                    type = formTrailer.cleaned_data['type_select']
                    if type == "":
                        type = trailer.type

                    trailer.type = type
                    tmp.country = country
                    tmp.state = state
                    tmp.economic_no = trailer.economic_no
                    tmp.active = active
                    tmp.save()
                    TrailerView.save_profile(user_id, economic_no)
                    Database.clear_profile(user_id, 'trailer')
                    return redirect(view_template+economic_no+'/')
                else:
                    messages.error(request, error)

            else:
                messages.error(request,error_fields)


        return render(request,edit_template,
                      {'formTrailer':formTrailer,
                       'formProfile': formProfile,
                       'profile':profile,
                       'economic_no': economic_no,
                       'active':active
                      })

    def export_trailers(request,lenguage,trailers_list):

        email_template = '/email/0/'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_list = 'Lista vacía'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if len(trailers_list) > 0:
            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="trailers.xls"'

            if int(lenguage) == 1:
                response['Content-Disposition'] = 'attachment; filename="cajas.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Trailers')

            row_num = 0

            rows_trailer = Trailer.objects.filter(economic_no__in = trailers_list).filter(user_id=user_id).values_list('economic_no','plate_no','country',
                                                                                               'state','year','capacity',
                                                                                               'client_name','client_last_name','use','type',
                                                                                               'start_service_date','end_service_date','status',
                                                                                               'rent_date','deliver_date')

            date_format = XFStyle()
            date_format.num_format_str =  'M/D/YY'

            for row_trailer in rows_trailer:
                row_num += 1
                columns = [
                'Economic No', 'Plate No', 'Country',
                'State', 'Year', 'Capacity',
                'Client Name', 'Client Lastname', 'Use','type',
                'Service Start Date', 'Service End Date', 'Status',
                'Rent Date', 'Deliver Date',
                ]

                if int(lenguage) == 1:
                    columns = [
                        'No. Económico', 'No. de Placas', 'País',
                        'Estado', 'Año', 'Capacidad',
                        'Nombre del Cliente', 'Apellido del Cliente', 'Uso', 'Tipo',
                        'Fecha de Inicio de Servicio', 'Fecha de Termino de Servicio', 'Condición',
                        'Fecha de Renta', 'Fecha de Entrega',
                    ]

                row_num = XlsGenerator.create_headers(columns, ws, row_num)

                row_num = XlsGenerator.create_content(ws,row_num,row_trailer,xlwt.XFStyle())

            wb.save(response)
            return response
        return render(request,'hound-eng/error.html',{'error':error_list})

    @require_POST
    def manager_trailers(request,lenguage):

        email_template = '/email/0/'
        error_option = 'Invalid Action'
        trailers_template = '/trailers/0/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Acción invalida'
            trailers_template = '/trailers/1/0/'

        if request.method == 'POST':

            if not Validator.validate_view(request):
                return redirect(email_template)

            pk = request.POST.getlist('select')
            action = request.POST.get('action')

            if action == "1":
                return TrailerView.export_trailers(request,lenguage,pk)
            elif action == "2":
                return TrailerView.delete_trailers(request,lenguage,pk)
            elif action == "3":
                return TrailerView.restore_trailers(request,lenguage,pk)
            else:
                return render(request,'hound-eng/error.html',{'error':error_option})

            return redirect(trailers_template)


    def restore_trailers(request,lenguage,trailer_list):

        trailers_template = '/archiver_trailers/0/1/'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            trailers_template = '/archiver_trailers/1/1/'
            error_list = 'Lista vacía'

        if len(trailer_list) > 0:
                trailers = Trailer.objects.filter(user_id=request.session['id'],economic_no__in=trailer_list)
                for trailer in trailers:
                    if trailer.active == True:
                        trailer.active = False
                        trailer.save()
                return redirect(trailers_template)

        return render(request, 'hound-eng/error.html', {'error': error_list})

    def restore_trailer(request,lenguage,economic_no):

        email_template = '/email/0/'
        trailers_template = '/archiver_trailers/0/1/'
        error_trailer = 'Trailer does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            trailers_template = '/archiver_trailers/1/1/'
            error_trailer = 'La caja no existe'


        if not Validator.validate_view(request):
            return redirect(email_template)


        if Trailer.objects.filter(user_id = request.session['id']).filter(economic_no = economic_no):
            trailer = Trailer.objects.get(user_id=request.session['id'],economic_no = economic_no)
            if trailer.active == True:
                trailer.active = False
                trailer.save()
                return redirect(trailers_template)
        else:
            return render(request,'hound-eng/error.html',{'error':error_trailer})

    @require_POST
    def delete_trailers(request,lenguage,trailer_list):

        error_list = 'Empty List'

        if int(lenguage) == 1:
            error_list = 'Lista vacía'

        if len(trailer_list) > 0:
            trailers = Trailer.objects.filter(user_id=request.session['id'],economic_no__in=trailer_list)
            for trailer in trailers:
                if trailer.active == False:
                    trailer.active = True
                    template='/trailers/0/0/'

                    if int(lenguage) == 1:
                        template = '/trailers/1/0/'

                    trailer.save()
                else:
                    template='/archiver_trailers/0/1/'
                    if int(lenguage) == 1:
                        template = '/archiver_trailers/1/1/'


                    trailer.delete()
            return redirect(template)
        return render(request, 'hound-eng/error.html', {'error': error_list})


    def delete_trailer(request,lenguage,economic_no):

        email_template = '/email/0/'
        error_trailer = 'Trailer does not exists'
        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trailer = 'La caja no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if Trailer.objects.filter(user_id = request.session['id']).filter(economic_no = economic_no):
            trailer = Trailer.objects.get(user_id=request.session['id'],economic_no = economic_no)
            if trailer.active == False:
                trailer.active = True
                template = '/trailers/0/0/'
                if int(lenguage) == 1:
                    template = '/trailers/1/0/'

                trailer.save()
            else:
                template = '/archiver_trailers/0/1/'
                if int(lenguage) == 1:
                    template = '/archiver_trailers/1/1/'
                trailer.delete()
            return redirect(template)

        else:
            return render(request,'hound-eng/error.html',{'error':error_trailer})



    def search_trailer(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'


        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == "1":
            template = '/archiver_trailers/0/1/'

            if int(lenguage) == 1:
                template = '/archiver_trailers/1/1/'

        elif status == "0":
            template = '/trailers/0/0/'
            if int(lenguage) == 1:
                template = '/trailers/1/0/'
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        if request.method == 'POST':
            user_id = request.session['id']

            formSearchTrailer = SearchTrailerForm(request.POST)

            if formSearchTrailer.is_valid():
                trailer = formSearchTrailer.save(commit=False)
                print(trailer.status)
                fields = {'economic_no':formSearchTrailer.cleaned_data['economic_no'],'plate_no':trailer.plate_no.upper(),'year':trailer.year,
                            'state':trailer.state.lower(),'use':trailer.use.lower(),'status':trailer.status.lower(),
                            'type':trailer.type.lower(),'capacity':trailer.capacity,'client_name':trailer.client_name.lower(),
                            'client_last_name':trailer.client_last_name.lower(),'country':formSearchTrailer.cleaned_data['country_select'].upper()}

                error = TrailerView.validate_search_fields(request,fields,user_id)

                if int(lenguage) == 1:
                    error = TrailerView.validate_search_fields_esp(request, fields, user_id)

                if error != '':
                    return render(request, 'hound-eng/error.html', {'error': error})

                return TrailerView.search_view(request,lenguage,fields,status)
            else:
                return render(request, 'hound-eng/error.html', {'error': formSearchTrailer.errors})

        else:
            return redirect(template)

    def search_view(request,lenguage,fields,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'
        error_records = 'No records found'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'
            error_records = 'No se encontraron resultados'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == "1":
            status = True
            template = 'hound-eng/archiver_trailers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/archiver_trailers.html'

        elif status == "0":
            status = False
            template = 'hound-eng/assets_trailers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/assets_trailers.html'

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        formSearchTrailer = SearchTrailerForm()

        if int(lenguage) == 0:
            table = TrailerView.generate_table(fields, request.session['id'], status)

        elif int(lenguage) == 1:
            table = TrailerView.generate_table_esp(fields, request.session['id'], status)

        if table == None:
            return render(request,'hound-eng/error.html',{'error':error_records})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, template, {
            'table': table, 'action': 0, 'formSearchTrailer':formSearchTrailer,'status':status
        })


    def validate_search_fields(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['economic_no'] != None:
                if int(fields['economic_no']) < 0:
                    error = 'Economic number must be positive '

            if fields['plate_no'] != '':
                if len(fields['plate_no']) < 5 or len(fields['plate_no']) > 10 :
                    error = 'Plate number must have 5 to 10 character length '
        return error

    def validate_search_fields_esp(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['economic_no'] != None:
                if int(fields['economic_no']) < 0:
                    error = 'Número económico debe ser un número positivo '

            if fields['plate_no'] != '':
                if len(fields['plate_no']) < 5 or len(fields['plate_no']) > 10 :
                    error = 'El número de placas debe de tener de 5 a 10 caracteres '
        return error


    def generate_table(fields,user_id,status):
        table = TrailerTable(Trailer.objects.filter(user_id=user_id).filter(active=status))
        if fields != None:
            if fields['economic_no'] != None:
                if Trailer.objects.filter(user_id = user_id).filter(economic_no=fields['economic_no']).filter(active=status).exists():
                    table = TrailerTable(Trailer.objects.filter(user_id=user_id).filter(economic_no=fields['economic_no']).filter(active=status))
                else:
                    table = None
            if fields['plate_no']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status))
                else:
                    table = None

            if fields['use']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(use=fields['use']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(use=fields['use']).filter(active=status))
                else:
                    table = None

            if fields['status']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(status=fields['status']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(status=fields['status']).filter(active=status))
                else:
                    table = None

            if fields['year'] != None:
                if Trailer.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status))
                else:
                    table = None

            if fields['type'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status))
                else:
                    table = None

            if fields['state'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status))
                else:
                    table = None

            if fields['country'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status))
                else:
                    table = None

            if fields['capacity'] != None:
                if Trailer.objects.filter(user_id=user_id).filter(capacity=fields['capacity']).filter(active=status).exists():
                    table = TrailerTable(
                        Trailer.objects.filter(user_id=user_id).filter(capacity=fields['capacity']).filter(active=status))
                else:
                    table = None

            if fields['client_name'] != '' and fields['client_last_name'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(client_last_name=fields['client_last_name']).filter(active=status).exists():
                    table = TrailerTable(Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(client_last_name=fields['client_last_name']).filter(active=status))
                else:
                    table = None

            if fields['client_name'] != '' :
                if Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(active=status).exists():
                    table = TrailerTable(Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(active=status))
                else:
                    table = None

            if fields['client_last_name'] != '' :
                if Trailer.objects.filter(user_id=user_id).filter(client_last_name=fields['client_last_name']).filter(active=status).exists():
                    table = TrailerTable(Trailer.objects.filter(user_id=user_id).filter(client_last_name=fields['client_last_name']).filter(active=status))
                else:
                    table = None

        return table


    def generate_table_esp(fields,user_id,status):
        table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(active=status))
        if fields != None:
            if fields['economic_no'] != None:
                if Trailer.objects.filter(user_id = user_id).filter(economic_no=fields['economic_no']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(economic_no=fields['economic_no']).filter(active=status))
                else:
                    table = None
            if fields['plate_no']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status))
                else:
                    table = None

            if fields['use']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(use=fields['use']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(use=fields['use']).filter(active=status))
                else:
                    table = None

            if fields['status']!= '':
                if Trailer.objects.filter(user_id=user_id).filter(status=fields['status']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(status=fields['status']).filter(active=status))
                else:
                    table = None

            if fields['year'] != None:
                if Trailer.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status))
                else:
                    table = None

            if fields['type'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status))
                else:
                    table = None

            if fields['state'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status))
                else:
                    table = None

            if fields['country'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status))
                else:
                    table = None

            if fields['capacity'] != None:
                if Trailer.objects.filter(user_id=user_id).filter(capacity=fields['capacity']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(capacity=fields['capacity']).filter(active=status))
                else:
                    table = None

            if fields['client_name'] != '' and fields['client_last_name'] != '':
                if Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(client_last_name=fields['client_last_name']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(client_last_name=fields['client_last_name']).filter(active=status))
                else:
                    table = None

            if fields['client_name'] != '' :
                if Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(client_name=fields['client_name']).filter(active=status))
                else:
                    table = None

            if fields['client_last_name'] != '' :
                if Trailer.objects.filter(user_id=user_id).filter(client_last_name=fields['client_last_name']).filter(active=status).exists():
                    table = TrailerTable_esp(Trailer.objects.filter(user_id=user_id).filter(client_last_name=fields['client_last_name']).filter(active=status))
                else:
                    table = None

        return table

    def load_tmp_profile(user_id, economic_no):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (
        user_id, 'trailer', int(economic_no)))
        if cursor.rowcount <= 0:
            cursor.execute("select profile_img from hound_trailer where user_id_id='%s' and economic_no='%d';" % (
                user_id, int(economic_no)))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                try:
                    cursor.execute(
                        "insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (
                        user_id, 'trailer', int(economic_no), data[0]))
                    database.commit()
                except:
                    database.rollback()
                src = data[0]
            else:
                try:
                    cursor.execute(
                        "insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (
                        user_id, 'trailer', int(economic_no), 'hound/images/default.jpg'))
                    database.commit()
                except:
                    database.rollback()
        else:
            data = cursor.fetchone()
            src = data[0]
        database.close()
        return src

    @require_POST
    def upload_trailer_profile(request,lenguage, economic_no, state):
        email_template = '/email/0/'
        add_template = '/add_trailer/0/'
        edit_template = '/edit_trailer/0/'
        error_state = 'Internal error, Invalid state'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            add_template = '/add_trailer/1/'
            edit_template = '/edit_trailer/1/'
            error_state = 'Error interno, Estado invalido'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':

            if Profile.objects.filter(user_id=request.session['id']).filter(type='trailer').filter(gen_id=economic_no):
                profile = Profile.objects.get(user_id=request.session['id'], type='trailer', gen_id=economic_no)
                formProfile = ProfileForm(request.POST or None, request.FILES, instance=profile)
            else:
                formProfile = ProfileForm(request.POST, request.FILES)

            if formProfile.is_valid():
                file = request.FILES['profile']
                profile = formProfile.save(commit=False)
                fs = FileSystemStorage()
                url = request.session['id'] + '/trailers/' + str(economic_no) + '/' + file.name
                if not fs.exists(request.session['id'] + '/trailers/' + str(economic_no) + '/' + file.name):
                    filename = fs.save(request.session['id'] + '/trailers/' + str(economic_no) + '/' + file.name, file)
                    url = fs.url(filename)

                Uploader.create_directory('/' + request.session['id'] + '/trailers/' + str(economic_no) + '/')
                Uploader.clear_directory('/' + request.session['id'] + '/trailers/' + str(economic_no))
                Uploader.move_file('/system/hound/images/' + url,
                                   '/' + request.session['id'] + '/trailers/' + str(economic_no) + '/' + file.name)
                profile.type = 'trailer'
                profile.gen_id = int(economic_no)
                profile.path = 'hound/data/' + request.session['id'] + '/trailers/' + str(economic_no) + '/' + file.name
                profile.user_id = request.session['id']
                profile.save()
                Uploader.clear_tmp_dir('/system/hound/images/')
            if state == "0":
                return redirect(add_template)
            elif state == "1":
                return redirect(edit_template + str(economic_no) + '/')
            else:
                return render(request, 'hound-eng/error.html', {'error': error_state})

    def save_profile(user_id, economic_no):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (
        user_id, 'trailer', int(economic_no)))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            try:
                cursor.execute("select profile_img from hound_trailer where user_id_id='%s' and economic_no='%d';" % (
                    user_id, int(economic_no)))
                if cursor.rowcount > 0:
                    cursor.execute(
                        "update hound_trailer set profile_img='%s' where user_id_id='%s' and economic_no='%d';" % (
                        data[0], user_id, int(economic_no)))
                    database.commit()
                else:
                    cursor.execute(
                        "insert into hound_trailer (user_id_id,economic_no,profile_img) values('%s','%d','%s');" % (
                        user_id, int(economic_no), data[0]))
                    database.commit()
            except:
                database.rollback()
        database.close()



