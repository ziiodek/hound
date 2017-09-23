import xlwt
import pymysql
from xlwt import XFStyle
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.vehicle import *
from ..models.profile import *
from ..src.id_generator import IdGenerator
from ..src.xls_generator import XlsGenerator
from ..src.validator import Validator
from ..src.database import Database
from ..static.hound.data.uploader import Uploader
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse



class VehicleView:

    def get_all_vehicles(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == "1":
            status = True
            template = 'hound-eng/archiver_vehicles.html'
            if int(lenguage) == 1:
                template = 'hound-esp/archiver_vehicles.html'
        elif status == "0":
            status = False
            template = 'hound-eng/assets_vehicles.html'
            if int(lenguage) == 1:
                template = 'hound-esp/assets_vehicles.html'


        else:
            return render(request,'hound-eng/error.html',{'error':error_option})


        Database.clear_profile(request.session['id'],'vehicle')
        formSearchVehicle = SearchVehicleForm()

        if int(lenguage) == 0:
            table = VehicleView.generate_table(None, request.session['id'], status)

        elif int(lenguage) == 1:
            table = VehicleView.generate_table_esp(None, request.session['id'], status)

        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request,template, {'table': table,'formSearchVehicle':formSearchVehicle,'status':status})


    def view_vehicle(request,lenguage,economic_no):

        email_template = '/email/0/'
        view_template = 'hound-eng/view_vehicle.html'
        error_trailer = 'Trailer does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = 'hound-esp/view_vehicle.html'
            error_trailer = 'La caja no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        if Vehicle.objects.filter(user_id=user_id).filter(economic_no=economic_no).exists():
            vehicle = Vehicle.objects.get(user_id=user_id, economic_no=economic_no)
            formVehicle = VehicleForm(instance=vehicle,initial={'country':vehicle.country} )
            profile = VehicleView.load_tmp_profile(user_id, economic_no)
            active = vehicle.active

            return render(request, view_template, {
                'formVehicle': formVehicle,
                'profile': profile,
                'economic_no': economic_no,
                'active':active
            })
        else:
            return render(request, 'hound-eng/error.html', {'error': error_trailer})


    def add_vehicle(request,lenguage):

        email_template = '/email/0/'
        view_template = '/view_vehicle/0/'
        error_user = 'Username does not exists'
        add_template = 'hound-eng/add_vehicle.html'
        error_version = 'For the free version you can only register 100 vehicles, upgrade to Big Company to register up to 10 vehicles'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = '/view_vehicle/1/'
            error_user = 'El nombre de usuario no existe'
            add_template = 'hound-esp/add_vehicle.html'
            error_version = 'Solo puedes registrar 100 vehiculos en la versión gratis, actualiza a Big Company para registrar mas de 100 vehiculos'


        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        economic_no = IdGenerator.generate_economic_no(user_id,'vehicles')
        country = None
        if request.method == 'POST':

            if Vehicle.objects.filter(user_id=user_id).count() >= 100:
                return render(request, 'hound-eng/error.html', {'error': error_version})

            formVehicle = VehicleForm( request.POST )


            if formVehicle.is_valid():
                vehicle = formVehicle.save(commit=False)
                error = ''

                if vehicle.vin != '':
                    if len(vehicle.vin) < 17 or len(vehicle.vin) > 17:
                        error = 'Vin number must be 17 characters length'

                        if int(lenguage) == 1:
                            error = 'Vin debe de tener 17 caracteres'

                    if Validator.check_pattern(vehicle.vin) == True:
                        error = 'Vin number must not have symbols'

                        if int(lenguage == 1):
                            error = 'Vin no debe de contener simbolos'

                if Validator.check_pattern(vehicle.brand) == True:
                    error = 'Brand must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Marca no debe de contener simbolos'

                if Validator.check_pattern(vehicle.model) == True:
                    error = 'Model must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Modelo no debe de contener simbolos'

                if Validator.check_pattern(vehicle.type) == True:
                    error = 'Type must not contain symbols'

                    if int(lenguage) == 1:
                        error = 'Tipo no debe de contener simbolos'

                if Validator.check_pattern(vehicle.status) == True:
                    error = 'Status must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Condición no debe de tener simbolos'


                if vehicle.plate_no != '':
                    if len(vehicle.plate_no) < 5 or len(vehicle.plate_no) > 10:
                        error = 'Plate number must have 5 to 10 character length'
                        if int(lenguage) == 1:
                            error = 'Número de placas debe de tener de 5 a 10 caracteres'

                    if Validator.check_pattern(vehicle.plate_no) == True:
                        error = 'Plate number must not have symbols'

                        if int(lenguage == 1):
                            error = 'Número de placas no debe de contener simbolos'

                if error == '':
                    if User.objects.filter(user_id=user_id).exists():
                        country = request.POST.get("country_select")
                        print(country)
                        if country == "USA":
                            state = request.POST.get("states_usa")
                            print (state)
                        elif vehicle.country == "MX":
                            state = request.POST.get("states_mx")
                            print (state)
                        else:
                            state = ""
                            country = ""


                        vehicle.user_id = User.objects.get(user_id=user_id)
                        vehicle.economic_no = int(economic_no)
                        vehicle.country = country
                        vehicle.state = state
                        vehicle.save()
                        VehicleView.save_profile(user_id,economic_no)
                        Database.clear_profile(user_id,'vehicle')
                        economic_no = IdGenerator.store_economic_no(user_id, 'vehicles')
                        return redirect(view_template+str(economic_no)+'/')
                    else:
                        return render( request, 'hound-eng/error.html', {'error': error_user} )
                else:
                    messages.error( request, error )

            else:
                messages.error(request,formVehicle.errors)


        formVehicle = VehicleForm( initial={'economic_no': economic_no,'country':country} )
        formProfile = ProfileForm()
        profile = VehicleView.load_tmp_profile(user_id,economic_no)
        return render(request,add_template,
                      {'formVehicle':formVehicle,
                       'profile': profile,
                       'formProfile':formProfile,
                       'economic_no':economic_no,
                       })


    def edit_vehicle(request,lenguage,economic_no):

        email_template = '/email/0/'
        view_template = '/view_vehicle/0/'
        edit_template = 'hound-eng/edit_vehicle.html/'
        error_trailer = 'Trailer does not exists'
        error_fields = 'Fill all the required fields'
        error_trailer = 'Trailer does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = '/view_vehicle/1/'
            edit_template = 'hound-esp/edit_vehicle.html/'
            error_trailer = 'La caja no existe'
            error_fields = 'Por favor llena los campos que se te piden'
            error_trailer = 'La caja no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        user = User.objects.get( user_id=user_id )

        if not Vehicle.objects.filter(user_id=user, economic_no=economic_no ).exists():
            return render(request,'hound-eng/error.html',{'error':error_trailer})

        vehicle = Vehicle.objects.get( user_id=user, economic_no=economic_no )
        formVehicle = VehicleForm(request.POST or None,instance=vehicle)
        formProfile = ProfileForm()
        profile = VehicleView.load_tmp_profile(user_id, economic_no)
        active = vehicle.active


        if request.method == 'POST':
            if formVehicle.is_valid():
                tmp = formVehicle.save(commit=False)
                error = ''
                if tmp.vin != '':
                    if len(tmp.vin) < 17 or len(tmp.vin) > 17:
                        error = 'Vin number must be 17 characters length'

                        if int(lenguage) == 1:
                            error = 'Vin debe de tener 17 caracteres'

                    if Validator.check_pattern(tmp.vin) == True:
                        error = 'Vin must not have symbols'

                        if int(lenguage == 1):
                            error = 'Vin no debe de contener simbolos'

                if Validator.check_pattern(vehicle.brand) == True:
                    error = 'Brand must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Marca no debe de contener simbolos'

                if Validator.check_pattern(vehicle.model) == True:
                    error = 'Model must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Modelo no debe de contener simbolos'

                if Validator.check_pattern(vehicle.type) == True:
                    error = 'Type must not contain symbols'

                    if int(lenguage) == 1:
                        error = 'Tipo no debe de contener simbolos'

                if Validator.check_pattern(vehicle.status) == True:
                    error = 'Status must not have symbols'

                    if int(lenguage) == 1:
                        error = 'Condición no debe de tener simbolos'

                if tmp.plate_no != '':
                    if len(tmp.plate_no) < 5 or len(tmp.plate_no) > 10:
                        error = 'Plate number must have 5 to 10 character length'
                        if int(lenguage) == 1:
                            error = 'Número de Placas debe de tener de 5 a 10 caracteres'

                    if Validator.check_pattern(tmp.plate_no) == True:
                        error = 'Plate number must not have symbols'

                        if int(lenguage == 1):
                            error = 'Número de placas no debe de contener simbolos'

                if error == '':
                    country = request.POST.get("country_select")
                    if country == "USA":
                        state = request.POST.get("states_usa")
                    elif country == "MX":
                        state = request.POST.get("states_mx")
                    else:
                        country = vehicle.country
                        state = vehicle.state

                    if state == "":
                        state = vehicle.state

                    tmp.country =country
                    tmp.state = state
                    tmp.economic_no = vehicle.economic_no
                    tmp.active = active
                    tmp.save()
                    VehicleView.save_profile(user_id, economic_no)
                    Database.clear_profile(user_id,'vehicle')

                    return redirect(view_template+economic_no+'/' )
                else:
                    messages.error(request, error)
            else:
                messages.error(request,error_fields)

        return render(request,edit_template,
                      {'formVehicle':formVehicle,
                       'formProfile':formProfile,
                       'profile':profile,
                       'economic_no': economic_no,
                       'active':active
                      })

    def export_vehicles(request,lenguage,vehicle_list):

        email_template = '/email/0/'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_list = 'Lista vacía'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if len(vehicle_list) > 0:
            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="vehicles.xls"'

            if int(lenguage) == 1:
                response['Content-Disposition'] = 'attachment; filename="vehiculos.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Trailers')

            row_num = 0

            rows_vehicle = Vehicle.objects.filter(economic_no__in = vehicle_list).filter(user_id=user_id).values_list('economic_no','vin','plate_no',
                                                                                               'country','state','year',
                                                                                               'model','brand','type','status',
                                                                                               )

            date_format = XFStyle()
            date_format.num_format_str =  'M/D/YY'

            for row_vehicle in rows_vehicle:
                row_num += 1
                columns = [
                'Economic No', 'Vin','Plate No',
                'Country', 'State', 'Year',
                'Model', 'Brand','type','status'
                ]

                if int(lenguage) == 1:
                    columns = [
                        'No. Económico', 'Vin', 'No. de Placas',
                        'País', 'Estado', 'Año',
                        'Modelo', 'Marca', 'Tipo','Condición'
                    ]

                row_num = XlsGenerator.create_headers(columns, ws, row_num)

                row_num = XlsGenerator.create_content(ws,row_num,row_vehicle,xlwt.XFStyle())

            wb.save(response)
            return response
        return render(request,'hound-eng/error.html',{'error':error_list})

    @require_POST
    def manager_vehicles(request,lenguage):

        email_template = '/email/0/'
        error_action = 'Invalid Action'
        vehicles_template = '/vehicles/0/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_action = 'Acción invalida'
            vehicles_template = '/vehicles/1/0/'

        if request.method == 'POST':

            if not Validator.validate_view(request):
                return redirect(email_template)

            pk = request.POST.getlist('select')
            action = request.POST.get('action')

            if action == "1":
                return VehicleView.export_vehicles(request,lenguage,pk)
            elif action == "2":
                return VehicleView.delete_vehicles(request,lenguage,pk)
            elif action == "3":
                return VehicleView.restore_vehicles(request,lenguage,pk)
            else:
                return render(request,'hound-eng/error.html',{'error':error_action})

            return redirect(vehicles_template)


    def restore_vehicles(request,lenguage,vehicle_list):

        vehicles_template = '/archiver_vehicles/0/1/'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            vehicles_template = '/archiver_vehicles/1/1/'
            error_list = 'Lista vacía'

        if len(vehicle_list) > 0:
                vehicles = Vehicle.objects.filter(user_id=request.session['id'],economic_no__in=vehicle_list)
                for vehicle in vehicles:
                    if vehicle.active == True:
                        vehicle.active = False
                        vehicle.save()
                return redirect(vehicles_template)

        return render(request, 'hound-eng/error.html', {'error': error_list})

    def restore_vehicle(request,lenguage,economic_no):

        email_template = '/email/0/'
        vehicles_template = '/archiver_vehicles/0/1/'
        error_vehicle = 'Vehicle does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            vehicles_template = '/archiver_vehicles/1/1/'
            error_vehicle = 'El vehiculo no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)


        if Vehicle.objects.filter(user_id = request.session['id']).filter(economic_no = economic_no).exists():
            vehicle = Vehicle.objects.get(user_id=request.session['id'],economic_no = economic_no)
            if vehicle.active == True:
                vehicle.active = False
                vehicle.save()
                return redirect(vehicles_template)
        else:
            return render(request,'hound-eng/error.html',{'error':error_vehicle})

    @require_POST
    def delete_vehicles(request,lenguage,vehicle_list):

        error_list = 'Empty List'

        if int(lenguage) == 1:
            error_list = 'Lista vacía'

        if len(vehicle_list) > 0:
            vehicles = Vehicle.objects.filter(user_id=request.session['id'],economic_no__in=vehicle_list)
            template = '/vehicles/0/0/'
            if int(lenguage) == 1:
                template = '/vehicles/1/0/'
            for vehicle in vehicles:
                if vehicle.active == False:
                    vehicle.active = True
                    vehicle.save()

                else:
                    vehicle.delete()
                    template = '/archiver_vehicles/0/1/'
                    if int(lenguage) == 1:
                        template = '/archiver_vehicles/1/1/'
            return redirect(template)
        return render(request, 'hound-eng/error.html', {'error': error_list})


    def delete_vehicle(request,lenguage,economic_no):

        email_template = '/email/0/'
        error_trailer = 'Trailer does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trailer = 'La caja no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if Vehicle.objects.filter(user_id = request.session['id']).filter(economic_no = economic_no).exists():
            template = '/vehicles/0/0/'

            if int(lenguage) == 1:
                template = '/vehicles/1/0/'

            vehicle = Vehicle.objects.get(user_id=request.session['id'],economic_no = economic_no)
            if vehicle.active == False:
                vehicle.active = True
                vehicle.save()
            else:
                vehicle.delete()
                template = '/archiver_vehicles/0/1/'
                if int(lenguage) == 1:
                    template = '/archiver_vehicles/1/1/'
            return redirect(template)

        else:
            return render(request,'hound-eng/error.html',{'error':error_trailer})



    def search_vehicle(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'
        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'


        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == "1":
            template = '/archiver_vehicles/0/1/'

            if int(lenguage) == 1:
                template = '/archiver_vehicles/1/1/'

        elif status == "0":
            template = '/vehicles/0/0/'
            if int(lenguage) == 1:
                template = '/vehicles/1/0/'
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        if request.method == 'POST':

            if status == "1":
                status = True

            elif status == "0":
                status = False

            else:
                return render(request, 'hound-eng/error.html', {'error': error_option})

            user_id = request.session['id']

            formSearchVehicle = SearchVehicleForm(request.POST)

            if formSearchVehicle.is_valid():
                print(formSearchVehicle.cleaned_data['country_select'])
                country = formSearchVehicle.cleaned_data['country_select']


                vehicle = formSearchVehicle.save(commit=False)
                fields = {'economic_no':formSearchVehicle.cleaned_data['economic_no'],'plate_no':vehicle.plate_no.upper(),'year':vehicle.year,
                            'state':vehicle.state.lower(),'country':country,'type':vehicle.type.lower(),
                            'vin':vehicle.vin.upper(),'model':vehicle.model.upper(),'brand':vehicle.brand.upper(),'type':vehicle.type
                            }

                error = VehicleView.validate_search_fields(request,fields,user_id)

                if int(lenguage) == 1:
                    error = VehicleView.validate_search_fields_esp(request, fields, user_id)

                if error != '':
                    return render(request, 'hound-eng/error.html', {'error': error})

                return VehicleView.search_view(request,lenguage,fields,status)
            else:
                return render(request, 'hound-eng/error.html', {'error': formSearchVehicle.errors})

        else:
            return redirect(template)

    def search_view(request,lenguage,fields,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'
        error_records = 'No records found'

        if int(lenguage) == 1:
            email_template = '/email/0/'
            error_option = 'Opción invalida'
            error_records = 'No se encontraron resultados'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if status == False:
            template = 'hound-eng/assets_vehicles.html'

            if int(lenguage) == 1:
                template = 'hound-esp/assets_vehicles.html'

        elif status == True:
            template = 'hound-eng/archiver_vehicles.html'

            if int(lenguage) == 1:
                template = 'hound-esp/archiver_vehicles.html'

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        formSearchVehicle = SearchVehicleForm()

        if int(lenguage) == 0:
            table = VehicleView.generate_table(fields, request.session['id'], status)
        elif int(lenguage) == 1:
            table = VehicleView.generate_table_esp(fields, request.session['id'], status)
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        if table == None:
            return render(request,'hound-eng/error.html',{'error':error_records})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, template, {
            'table': table, 'action': 0, 'formSearchVehicle':formSearchVehicle
        })


    def validate_search_fields(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['economic_no'] != None:
                if int(fields['economic_no']) < 0:
                    error = 'Economic number must be positive '

            if fields['plate_no'] != '':
                if len(fields['plate_no']) < 5 or len(fields['plate_no']) > 10 :
                    error = 'Plate number must be 5 to 10 character length '

            if fields['vin'] != '':
                if len(fields['vin']) < 17 or len(fields['vin']) > 17:
                    error = 'Vin number must be 17 character length '
        return error

    def validate_search_fields_esp(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['economic_no'] != None:
                if int(fields['economic_no']) < 0:
                    error = 'No. Económico debe ser positivo '

            if fields['plate_no'] != '':
                if len(fields['plate_no']) < 5 or len(fields['plate_no']) > 10 :
                    error = 'Número de placas debe de tener de 5 a 10 caracteres '

            if fields['vin'] != '':
                if len(fields['vin']) < 17 or len(fields['vin']) > 17:
                    error = 'Vin debe de tener 17 caracteres '
        return error

    def generate_table(fields,user_id,status):
        table = VehicleTable(Vehicle.objects.filter(user_id=user_id).filter(active=status))
        if fields != None:
            if fields['economic_no'] != None:
                if Vehicle.objects.filter(user_id = user_id).filter(economic_no=fields['economic_no']).filter(active=status).exists():
                    table = VehicleTable(Vehicle.objects.filter(user_id=user_id).filter(economic_no=fields['economic_no']).filter(active=status))
                else:
                    table = None
            if fields['plate_no']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status))
                else:
                    table = None

            if fields['vin']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(vin=fields['vin']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(vin=fields['vin']).filter(active=status))
                else:
                    table = None

            if fields['brand']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(brand=fields['brand']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(brand=fields['brand']).filter(active=status))
                else:
                    table = None

            if fields['year'] != None:
                if Vehicle.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status))
                else:
                    table = None

            if fields['type'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status))
                else:
                    table = None

            if fields['state'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status))
                else:
                    table = None

            if fields['country'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status).exists():
                    table = VehicleTable(
                        Vehicle.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status))
                else:
                    table = None

            if fields['model'] != '' :
                if Vehicle.objects.filter(user_id=user_id).filter(model=fields['model']).filter(active=status).exists():
                    table = VehicleTable(Vehicle.objects.filter(user_id=user_id).filter(model=fields['model']).filter(active=status))
                else:
                    table = None

        return table

    def generate_table_esp(fields,user_id,status):
        table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(active=status))
        if fields != None:
            if fields['economic_no'] != None:
                if Vehicle.objects.filter(user_id = user_id).filter(economic_no=fields['economic_no']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(economic_no=fields['economic_no']).filter(active=status))
                else:
                    table = None
            if fields['plate_no']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(plate_no=fields['plate_no']).filter(active=status))
                else:
                    table = None

            if fields['vin']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(vin=fields['vin']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(vin=fields['vin']).filter(active=status))
                else:
                    table = None

            if fields['brand']!= '':
                if Vehicle.objects.filter(user_id=user_id).filter(brand=fields['brand']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(brand=fields['brand']).filter(active=status))
                else:
                    table = None

            if fields['year'] != None:
                if Vehicle.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(year=fields['year']).filter(active=status))
                else:
                    table = None

            if fields['type'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(type=fields['type']).filter(active=status))
                else:
                    table = None

            if fields['state'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(state=fields['state']).filter(active=status))
                else:
                    table = None

            if fields['country'] != '':
                if Vehicle.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(country=fields['country']).filter(active=status))
                else:
                    table = None

            if fields['model'] != '' :
                if Vehicle.objects.filter(user_id=user_id).filter(model=fields['model']).filter(active=status).exists():
                    table = VehicleTable_esp(Vehicle.objects.filter(user_id=user_id).filter(model=fields['model']).filter(active=status))
                else:
                    table = None

        return table


    def load_tmp_profile(user_id, economic_no):
        database = pymysql.connect('localhost', 'root', '', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (user_id,'vehicle', int(economic_no)))
        if cursor.rowcount <= 0:
            cursor.execute("select profile_img from hound_vehicle where user_id_id='%s' and economic_no='%d';" % (user_id, int(economic_no)))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                try:
                    cursor.execute("insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (user_id,'vehicle', int(economic_no), data[0]))
                    database.commit()
                except:
                    database.rollback()
                src = data[0]
            else:
                try:
                    cursor.execute("insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (user_id,'vehicle',int(economic_no), 'hound/images/default.jpg'))
                    database.commit()
                except:
                    database.rollback()
        else:
            data = cursor.fetchone()
            src = data[0]
        database.close()
        return src

    @require_POST
    def upload_vehicle_profile(request,lenguage,economic_no,state):

        email_template = '/email/0/'


        if int(lenguage) == 1:
            email_template = '/email/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':

            if Profile.objects.filter(user_id=request.session['id']).filter(type='vehicle').filter(gen_id=economic_no):
                profile = Profile.objects.get(user_id=request.session['id'], type='vehicle', gen_id=economic_no)
                formProfile = ProfileForm(request.POST or None, request.FILES, instance=profile)
            else:
                formProfile = ProfileForm(request.POST, request.FILES)

            if formProfile.is_valid():
                file = request.FILES['profile']
                profile = formProfile.save(commit=False)
                fs = FileSystemStorage()
                url = request.session['id']+'/vehicles/'+str(economic_no)+'/'+file.name
                if not fs.exists(request.session['id']+'/vehicles/'+str(economic_no)+'/'+file.name):
                    filename = fs.save(request.session['id']+'/vehicles/'+str(economic_no)+'/'+file.name,file)
                    url = fs.url(filename)

                Uploader.create_directory('/'+request.session['id']+'/vehicles/'+str(economic_no)+'/')
                Uploader.clear_directory('/'+request.session['id']+'/vehicles/'+str(economic_no))
                Uploader.move_file('/system/hound/images/'+url,'/'+request.session['id']+'/vehicles/'+str(economic_no)+'/'+file.name)
                profile.type='vehicle'
                profile.gen_id = int(economic_no)
                profile.path = 'hound/data/'+request.session['id']+'/vehicles/'+str(economic_no)+'/'+file.name
                profile.user_id = request.session['id']
                profile.save()
                Uploader.clear_tmp_dir('/system/hound/images/')
            if state == "0":

                if int(lenguage) == 0:
                    return redirect('/add_vehicle/0/')
                elif int(lenguage) == 1:
                    return redirect('/add_vehicle/1/')
            elif state == "1":

                if int(lenguage) == 0:
                    return redirect('/edit_vehicle/0/'+str(economic_no)+'/')
                elif int(lenguage) == 1:
                    return redirect('/edit_vehicle/1/' + str(economic_no) + '/')
            else:
                return render(request,'hound-eng/error.html',{'error':'Internal error, Invalid state'})

    def save_profile(user_id,economic_no):
        database = pymysql.connect('localhost', 'root', '', 'hound_db')
        cursor = database.cursor()
        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (user_id,'vehicle',int(economic_no)))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            try:
                cursor.execute("select profile_img from hound_vehicle where user_id_id='%s' and economic_no='%d';" % (user_id,int(economic_no)))
                if cursor.rowcount > 0:
                    cursor.execute("update hound_vehicle set profile_img='%s' where user_id_id='%s' and economic_no='%d';" % (data[0],user_id,int(economic_no)))
                    database.commit()
                else:
                    cursor.execute("insert into hound_vehicle (user_id_id,economic_no,profile_img) values('%s','%d','%s');" % (user_id,int(economic_no),data[0]))
                    database.commit()
            except:
                database.rollback()
        database.close()



