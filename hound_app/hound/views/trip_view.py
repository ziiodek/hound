import pymysql
import xlwt
from xlwt import XFStyle
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.trip import *
from ..models.user import User
from ..models.driver import Driver
from ..models.driver_status import DriverStatus
from ..models.address import Address
from ..models.vehicle import Vehicle
from ..models.trailer import Trailer
from ..src.validator import Validator
from django.contrib import messages
from ..src.xls_generator import XlsGenerator
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.utils import timezone

class TripView:

    def get_today_trips(request, lenguage):

        email_template = '/email/0/'
        trip_template = 'hound-eng/trip_status.html'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            trip_template = 'hound-esp/trip_status.html'
            error_option = 'Opción invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        formSearchTrip = SearchTripForm()

        if int(lenguage) == 0:
            table = TripView.generate_today_table(None, request.session['id'])

        elif int(lenguage) == 1:
            table = TripView.generate_today_table_esp(None, request.session['id'])

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request,trip_template,{'table':table,
                                                            'formSearchTrip':formSearchTrip,
                                                            'status':False,
                                                            'action': 0,
                                                            })


    def get_all_trips(request,lenguage):

        email_template = '/email/0/'
        bitacora_template = 'hound-eng/bitacora.html'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            bitacora_template = 'hound-esp/bitacora.html'
            error_option = 'Opción invalida'


        if not Validator.validate_view(request):
            return redirect(email_template)

        formSearchTrip = SearchBitacoraForm()

        if int(lenguage) == 0:
            table = TripView.generate_bitacora_table(None, request.session['id'])
        elif int(lenguage) == 1:
            table = TripView.generate_bitacora_table_esp(None, request.session['id'])

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, bitacora_template, {'table': table,
                                                            'formSearchTrip': formSearchTrip,
                                                            'status':False,
                                                            'action':0,
                                                              })


    def get_trip(request,lenguage,trip_id):

        email_template = '/email/0/'
        trip_error = 'Trip does not exists'
        trip_template = 'hound-eng/trip_status.html'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            trip_error = 'El viaje no existe'
            trip_template = 'hound-esp/trip_status.html'

        if not Validator.validate_view(request):
            return redirect(email_template)

        formSearchTrip = SearchTripForm()
        if Trip.objects.filter(user_id=request.session['id']).filter(trip_id = trip_id).exists():
            trip = Trip.objects.get(user_id=request.session['id'],trip_id = trip_id)
        else:
            return render(request,'hound-eng/error.html',{'error':trip_error})

        driver = TripView.get_driver(trip.assigned_id,request.session['id'])
        address = Address.objects.get(user_id=request.session['id'],assigned_id=driver.assigned_id)
        vehicle = TripView.get_vehicle(trip.vehicle_no,request.session['id'])
        if trip.trailer_no != None:
            trailer = TripView.get_trailer(trip.trailer_no,request.session['id'])
        else:
            trailer = None
        table = TripTable(Trip.objects.filter(user_id=request.session['id'],trip_id=trip_id))
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, trip_template, {'table': table,
                                                              'formSearchTrip': formSearchTrip,
                                                              'driver':driver,
                                                              'phone':address.phone_number,
                                                              'vehicle':vehicle,
                                                              'trailer':trailer,
                                                              'status':True,
                                                              'trip_id':trip_id,
                                                              'action': 0,
                                                              })

    def cancel_trip(request,lenguage,trip_id):

        email_template = '/email/0/'
        error_trip = '/Trip does not exists/'
        trip_template = '/trip_status/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trip = 'El viaje no existe'
            trip_template = '/trip_status/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if Trip.objects.filter(user_id=request.session['id']).filter(trip_id=trip_id).exists():
            trip = Trip.objects.get(user_id=request.session['id'],trip_id=trip_id)
            trip.status='CANCELED'
            trip.save()
        else:
            return render(request,'hound-eng/error.html',error_trip)

        return redirect(trip_template)


    def edit_trip(request,lenguage,trip_id,assigned_id,economic_no):

        email_template = '/email/0/'
        error_trip = 'Trip does not exists'
        error_driver = 'Driver does not exists'
        error_active_driver = 'Driver has expired'
        error_trailer = 'Trailer does not exists'
        error_active_trailer = 'Trailer is not active'
        error_vehicle = 'Vehicle does not exists'
        trip_template = '/trip_status/0/'
        edit_template = 'hound-eng/edit_trip.html'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_trip = 'El viaje no existe'
            error_driver = 'El conductor no existe'
            error_trailer = 'La caja no existe'
            error_vehicle = 'El vehiculo no existe'
            error_active_vehicle = 'Vehicle is not active'
            trip_template = '/trip_status/1/'
            edit_template = 'hound-esp/edit_trip.html'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if Trip.objects.filter(user_id=request.session['id']).filter(trip_id=trip_id).exists():
            trip = Trip.objects.get(user_id=request.session['id'],trip_id=trip_id)
        else:
            return render(request,'hound-eng/error.html',{'error':error_trip})
        trip_id = trip.trip_id
        print(trip.trailer_no)
        formTrip = TripForm(request.POST or None, instance=trip)
        if trip.trailer_no == None:
            trip.trailer_no = ""
            formTrip = TripForm(request.POST or None,instance=trip,initial={'trailer_no': ""} )

        vehicle = 'hound/images/default.jpg'
        driver = 'hound/images/default.jpg'

        if int(economic_no) > 0:
            vehicle = TripView.load_vehicle(request.session['id'], int(economic_no))

        if int(assigned_id) > 0:
            if int(assigned_id) > 999999 and int(assigned_id) < 9999999:
                driver = TripView.load_driver(request.session['id'], int(assigned_id))

        if request.method == 'POST':
            formTrip = TripForm(request.POST)
            if formTrip.is_valid():

                status = True
                trip = formTrip.save(commit=False)
                tmp_trailer_no = None
                if formTrip.cleaned_data['vehicle_no'] != None:
                    tmp_trailer_no = int(formTrip.cleaned_data['vehicle_no'])

                if int(lenguage) == 1:
                    error = TripView.validate_fields_esp(int(formTrip.cleaned_data['assigned_id']), int(formTrip.cleaned_data['vehicle_no']), tmp_trailer_no)
                else:
                    error = TripView.validate_fields(int(formTrip.cleaned_data['assigned_id']),int(formTrip.cleaned_data['vehicle_no']),tmp_trailer_no)

                if error== '':
                    trip.user_id = User.objects.get(user_id = request.session['id'])
                    if Driver.objects.filter(user_id = request.session['id']).filter(assigned_id=formTrip.cleaned_data['assigned_id']).exists():
                        if DriverStatus.objects.filter(user_id = request.session['id']).filter(assigned_id=formTrip.cleaned_data['assigned_id']).exists():
                            driver_status = DriverStatus.objects.get(user_id = request.session['id'],assigned_id=formTrip.cleaned_data['assigned_id'])
                            if driver_status.expired == False:
                                trip.assigned_id = Driver.objects.get(user_id = request.session['id'],assigned_id=formTrip.cleaned_data['assigned_id']).assigned_id
                            else:
                                messages.error(request, error_active_driver)
                                status = False
                    else:
                        messages.error(request,error_driver)
                        status = False

                    if Vehicle.objects.filter(user_id = request.session['id']).filter(economic_no=formTrip.cleaned_data['vehicle_no']).exists():
                        vehicle_obj = Vehicle.objects.get(user_id=request.session['id'],
                                                          economic_no=formTrip.cleaned_data['vehicle_no'])
                        if vehicle_obj.active == False:
                            trip.vehicle_no = Vehicle.objects.get(user_id=request.session['id'],economic_no=formTrip.cleaned_data['vehicle_no']).economic_no
                        else:
                            messages.error(request, error_active_vehicle)
                            status = False
                    else:
                        messages.error(request, error_vehicle)
                        status = False

                    if formTrip.cleaned_data['trailer_no'] != None:
                        if Trailer.objects.filter(user_id = request.session['id']).filter(economic_no=formTrip.cleaned_data['trailer_no']).exists():
                            trailer = Trailer.objects.get(user_id=request.session['id'],
                                                          economic_no=formTrip.cleaned_data['trailer_no'])
                            if trailer.active == False:
                                trip.trailer_no = Trailer.objects.get(user_id=request.session['id'],economic_no=formTrip.cleaned_data['trailer_no']).economic_no
                            else:
                                messages.error(request, error_active_trailer)
                                status = False
                        else:
                            messages.error(request, error_trailer)
                            status = False



                    if status == True:
                        trip.trip_id = trip_id
                        trip.save()
                        return redirect(trip_template)
                else:
                    messages.error(request,error)
            else:
                messages.error(request,formTrip.errors)

        return render(request,edit_template,{'formTrip':formTrip,
                                                            'vehicle':vehicle,
                                                            'driver':driver,
                                                            'assigned_id':assigned_id,
                                                            'economic_no':economic_no,
                                                            'trailer_no':trip.trailer_no,
                                                            'trip_id':trip_id,
                                                            'lenguage':lenguage
                                                            })


    def assign_trip(request,lenguage,assigned_id,economic_no):

        email_template = '/email/0/'
        error_driver = 'Driver does not exists'
        error_active_driver='Driver has expired'
        error_trailer = 'Trailer does not exists'
        error_active_trailer = 'Trailer is not active'
        error_vehicle = 'Vehicle does not exists'
        error_active_vehicle = 'Vehicle is not active'
        trip_template = '/trip_status/0/'
        assign_template = 'hound-eng/assign_trip.html'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_driver = 'El conductor no existe'
            error_active_driver = 'El conductor ha expirado'
            error_trailer = 'La caja no existe'
            error_active_trailer = 'La caja no esta activa'
            error_vehicle = 'El vehiculo no existe'
            error_active_vehicle = 'El vehiculo no esta activo'
            trip_template = '/trip_status/1/'
            assign_template = 'hound-esp/assign_trip.html'


        if not Validator.validate_view(request):
            return redirect(email_template)

        formTrip = TripForm()

        vehicle = 'hound/images/default.jpg'
        driver = 'hound/images/default.jpg'

        if int(economic_no) > 0:
            vehicle = TripView.load_vehicle(request.session['id'], int(economic_no))

        if int(assigned_id) > 0:
            if int(assigned_id) > 999999 and int(assigned_id) < 9999999:
                driver = TripView.load_driver(request.session['id'], int(assigned_id))

        if request.method == 'POST':
            formTrip = TripForm(request.POST)
            if formTrip.is_valid():
                status = True
                trip = formTrip.save(commit=False)
                tmp_trailer_no = None
                if formTrip.cleaned_data['vehicle_no'] != None:
                    tmp_trailer_no = int(formTrip.cleaned_data['vehicle_no'])

                if int(lenguage) == 1:
                    error = TripView.validate_fields_esp(int(formTrip.cleaned_data['assigned_id']), int(formTrip.cleaned_data['vehicle_no']),  tmp_trailer_no)
                else:
                    error = TripView.validate_fields(int(formTrip.cleaned_data['assigned_id']), int(formTrip.cleaned_data['vehicle_no']), tmp_trailer_no)

                if error== '':
                    trip.user_id = User.objects.get(user_id = request.session['id'])
                    if Driver.objects.filter(user_id = request.session['id']).filter(assigned_id=formTrip.cleaned_data['assigned_id']).exists():
                        if DriverStatus.objects.filter(user_id = request.session['id']).filter(assigned_id=formTrip.cleaned_data['assigned_id']).exists():
                            driver_status = DriverStatus.objects.get(user_id = request.session['id'],assigned_id=formTrip.cleaned_data['assigned_id'])
                            if driver_status.expired == False:
                                trip.assigned_id = Driver.objects.get(user_id = request.session['id'],assigned_id=formTrip.cleaned_data['assigned_id']).assigned_id
                            else:
                                messages.error(request, error_active_driver)
                                status = False
                    else:
                        messages.error(request,error_driver)
                        status = False

                    if Vehicle.objects.filter(user_id = request.session['id']).filter(economic_no=formTrip.cleaned_data['vehicle_no']).exists():
                        vehicle_obj = Vehicle.objects.get(user_id = request.session['id'],economic_no=formTrip.cleaned_data['vehicle_no'])
                        if vehicle_obj.active == False:
                            trip.vehicle_no = Vehicle.objects.get(user_id=request.session['id'],economic_no=formTrip.cleaned_data['vehicle_no']).economic_no
                        else:
                            messages.error(request, error_active_vehicle)
                            status = False
                    else:
                        messages.error(request, error_vehicle)
                        status = False

                    if formTrip.cleaned_data['trailer_no'] != None:
                        if Trailer.objects.filter(user_id = request.session['id']).filter(economic_no=formTrip.cleaned_data['trailer_no']).exists():
                            trailer = Trailer.objects.get(user_id = request.session['id'],economic_no=formTrip.cleaned_data['trailer_no'])
                            if trailer.active == False:
                                trip.trailer_no = Trailer.objects.get(user_id=request.session['id'],economic_no=formTrip.cleaned_data['trailer_no']).economic_no
                            else:
                                messages.error(request, error_active_trailer)
                                status = False
                        else:
                            messages.error(request, error_trailer)
                            status = False



                    if status == True:

                        trip.save()
                        return redirect(trip_template)
                else:
                    messages.error(request,error)
            else:
                messages.error(request, formTrip.errors)

        return render(request,assign_template,{'formTrip':formTrip,
                                                            'vehicle':vehicle,
                                                            'driver':driver,
                                                            'assigned_id':assigned_id,
                                                            'economic_no':economic_no,
                                                            'lenguage':lenguage
                                                            })

    def get_driver(assigned_id,user_id):
        if Driver.objects.filter(user_id=user_id).filter(assigned_id=assigned_id):
            driver = Driver.objects.get(user_id=user_id,assigned_id=assigned_id)
            return driver
        return None

    def get_vehicle(economic_no,user_id):
        if Vehicle.objects.filter(user_id=user_id).filter(economic_no=economic_no):
            vehicle = Vehicle.objects.get(user_id=user_id,economic_no=economic_no)
            return vehicle
        return None

    def get_trailer(economic_no, user_id):
        if Trailer.objects.filter(user_id=user_id).filter(economic_no=economic_no):
            trailer = Trailer.objects.get(user_id=user_id, economic_no=economic_no)
            return trailer
        return None

    def validate_fields(assigned_id,economic_no,trailer_no):
        error = ''

        if assigned_id != None:
            if assigned_id < 1000000 or assigned_id > 9999999:
                error += 'Assigned Id must have 7 digits '

        if economic_no != None:
            if economic_no < 0:
                error += 'Vehicle Economic number must be positive '

        if trailer_no != None:
            if trailer_no < 0:
                error += 'Trailer Economic number must be positive '

        return error

    def validate_fields_esp(assigned_id,economic_no,trailer_no):
        error = ''

        if assigned_id != None:
            if assigned_id < 1000000 or assigned_id > 9999999:
                error += 'Id Asignado debe tener 7 digitos '

        if economic_no != None:
            if economic_no < 0:
                error += 'El No. Económico del Vehiculo debe de ser positivo '

        if trailer_no != None:
            if trailer_no < 0:
                error += 'El No. Económico de la Caja debe de ser positivo '

        return error

    def load_vehicle(user_id, economic_no):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select profile_img from hound_vehicle where user_id_id='%s' and economic_no='%d' and active=0;" % (user_id, economic_no))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            src = data[0]

        database.close()
        return src

    def load_driver(user_id, assigned_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select expired from hound_driverstatus where user_id_id='%s' and assigned_id='%d';" % (user_id, assigned_id))
        data = cursor.fetchone()
        if data[0] == False:
            cursor.execute("select profile_img from hound_driver where user_id_id='%s' and assigned_id='%d';" % (user_id, assigned_id))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                src = data[0]

        database.close()
        return src

    def search_today_trip(request,lenguage):

        email_template = '/email/0/'
        trip_template = '/trip_status/0/'

        if int(lenguage) == 1:
            email_template= '/email/1/'
            trip_template = '/trip_status/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':
            user_id = request.session['id']

            formSearchTrip = SearchTripForm(request.POST)
            if formSearchTrip.is_valid():
                trip = formSearchTrip.save(commit=False)
                fields = {'assigned_id':formSearchTrip.cleaned_data['assigned_id'],'vehicle_no':formSearchTrip.cleaned_data['vehicle_no'],'trailer_no':formSearchTrip.cleaned_data['trailer_no'],
                            'origin':trip.origin.lower(),'destiny':trip.destiny.lower(),'trip_type':trip.trip_type.lower(),

                            }
                error = TripView.validate_search_fields(request, fields, user_id)

                if int(lenguage) == 1:
                    error = TripView.validate_search_fields_esp(request, fields, user_id)



                if error != '':
                    return render(request, 'hound-eng/error.html',{'error':error})


            else:
                return render(request,'hound-eng/error.html',{'error':formSearchTrip.errors})
            return TripView.search_today_view(request,lenguage, fields)

        else:
            return redirect(trip_template)

    def search_bitacora_trip(request,lenguage):

        email_template = '/email/0/'
        bitacora_template = '/bitacora/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            bitacora_template = '/bitacora/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':
            user_id = request.session['id']

            formSearchTrip = SearchBitacoraForm(request.POST)
            if formSearchTrip.is_valid():
                trip = formSearchTrip.save(commit=False)
                fields = {'assigned_id':formSearchTrip.cleaned_data['assigned_id'],'vehicle_no':formSearchTrip.cleaned_data['vehicle_no'],'trailer_no':formSearchTrip.cleaned_data['trailer_no'],
                            'origin':trip.origin.lower(),'destiny':trip.destiny.lower(),'trip_type':trip.trip_type.lower(),
                            'date':formSearchTrip.cleaned_data['date']
                            }

                error = TripView.validate_search_fields(request, fields, user_id)

                if int(lenguage) == 1:
                    error = TripView.validate_search_fields_esp(request, fields, user_id)

                if error != '':
                    return render(request, 'hound-eng/error.html',{'error': error})


            else:
                return render(request, 'hound-eng/error.html',{'error': formSearchTrip.errors})
            return TripView.search_bitacora_view(request,lenguage, fields)

        else:
            return redirect(bitacora_template)

    def search_today_view(request,lenguage,fields):

        email_template = '/email/0/'
        trip_template = 'hound-eng/trip_status.html'
        error_record = 'No records found'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            trip_template = 'hound-esp/trip_status.html'
            error_record = 'No se encontraron resultados'
            error_option = 'Opción invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        formSearchTrip = SearchTripForm()

        if int(lenguage) == 0:
            table = TripView.generate_today_table(fields, request.session['id'])
        elif int(lenguage) == 1:
            table = TripView.generate_today_table_esp(fields, request.session['id'])
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})
        if table == None:
            return render(request,'hound-eng/error.html',{'error':error_record})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, trip_template, {
            'table': table, 'formSearchTrip':formSearchTrip
        })

    def search_bitacora_view(request,lenguage,fields):

        email_template = '/email/0/'
        bitacora_template = 'hound-eng/bitacora.html'
        error_record = 'No records found'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            bitacora_template = 'hound-esp/bitacora.html'
            error_record = 'No se encontraron resultados'
            error_option = 'Opción invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        formSearchTrip = SearchBitacoraForm()
        if int(lenguage) == 0:
            table = TripView.generate_bitacora_table(fields, request.session['id'])
        elif int(lenguage) == 1:
            table = TripView.generate_bitacora_table_esp(fields, request.session['id'])
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})
        if table == None:
            return render(request,'hound-eng/error.html',{'error':error_record})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, bitacora_template, {
            'table': table,'status':True, 'action':0,'formSearchTrip':formSearchTrip
        })

    def export_bitacora(request,lenguage,trip_list):

        email_template = '/email/0/'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_list = 'Lista vacía'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if len(trip_list) > 0:
            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="bitacora.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Trailers')

            row_num = 0

            rows_trip = Trip.objects.filter(trip_id__in = trip_list).filter(user_id=user_id).values_list('assigned_id','vehicle_no','trailer_no',
                                                                                               'date','start_time','end_time',
                                                                                               'origin','destiny','trip_type')

            date_format = XFStyle()
            date_format.num_format_str =  'M/D/YY'

            for row_trip in rows_trip:
                row_num += 1

                columns_trip = [
                'Assigned Id', 'Vehicle No', 'Trailer No',
                'Date', 'Start Time', 'End Time',
                'Origin', 'Destiny', 'Trip Type'
                ]

                columns_driver = ['Name', 'Lastname']

                if int(lenguage) == 1:
                    columns_trip = [
                        'Id Asignado', 'No. de Vehiculo', 'No. de Caja',
                        'Fecha', 'Tiempo de salida', 'Tiempo de llegada',
                        'Origen', 'Destino', 'Tipo de Viaje'
                    ]

                    columns_driver = ['Nombre', 'Apellido']

                row_num = XlsGenerator.create_headers(columns_trip, ws, row_num)

                row_num = XlsGenerator.create_content(ws,row_num,row_trip,xlwt.XFStyle())


                row_num = XlsGenerator.create_headers(columns_driver, ws, row_num)
                rows_driver = Driver.objects.filter(assigned_id=row_trip[0]).filter(user_id=user_id).values_list('name','last_name')

                for row_driver in rows_driver:
                    row_num = XlsGenerator.create_content(ws, row_num, row_driver, xlwt.XFStyle())

            wb.save(response)
            return response
        return render(request,'hound-eng/error.html',{'error':error_list})

    @require_POST
    def manager_bitacora(request,lenguage):
        email_template = '/email/0/'
        error_action = 'Invalid Action'
        bitacora_template = '/bitacora/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_action = 'Acción invalida'
            bitacora_template = '/bitacora/1/'


        if request.method == 'POST':
            if not Validator.validate_view(request):
                return redirect(email_template)

            pk = request.POST.getlist('select')
            action = request.POST.get('action')

            if action == "1":
                return TripView.export_bitacora(request,lenguage, pk)
            elif action == "2":
                return TripView.delete_trips(request,lenguage,pk,0)
            else:
                return render(request, 'hound-eng/error.html', {'error': error_action})

            return redirect(bitacora_template)

    @require_POST
    def manager_trip_status(request,lenguage):

        email_template = '/email/0/'
        error_action = 'Invalid Action'
        trip_template = '/trip_status/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_action = 'Acción invalida'
            trip_template = '/trip_status/1/'

        if request.method == 'POST':

            if not Validator.validate_view(request):
                return redirect(email_template)

            pk = request.POST.getlist('select')
            action = request.POST.get('action')

            if action == "2":
                return TripView.delete_trips(request,lenguage, pk,1)
            else:
                return render(request, 'hound-eng/error.html', {'error': error_action})

            return redirect(trip_template)

    @require_POST
    def delete_trips(request,lenguage,trip_list,status):

        error_list = 'Empty list'
        bitacora_template = '/bitacora/0/'
        trip_template = '/trip_status/0/'

        if int(lenguage) == 1:
            error_list = 'Lista vacía'
            bitacora_template = '/bitacora/1/'
            trip_template = '/trip_status/1/'



        if len(trip_list) > 0:
            trips = Trip.objects.filter(user_id=request.session['id'], pk__in=trip_list)
            for trip in trips:
                trip.delete()
            if status == 0:
                return redirect(bitacora_template)
            else:
                return redirect(trip_template)
        return render(request, 'hound-eng/error.html', {'error': error_list})

    def delete_bitacora(request,lenguage):

        bitacora_template = '/bitacora/0/'

        if int(lenguage) == 1:
            bitacora_template = '/bitacora/1/'

        Trip.objects.filter(user_id=request.session['id']).delete()
        return redirect(bitacora_template)


    def validate_search_fields(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['assigned_id'] != None:
                if int(fields['assigned_id']) < 1000000 or int(fields['assigned_id'] > 9999999):
                    error = 'Assigned Id must have 7 digits '

            if fields['vehicle_no'] != None:
                if int(fields['vehicle_no'] < 0):
                    error = 'Vehicle Economic number must be positive '

            if fields['trailer_no'] != None:
                if int(fields['trailer_no'] < 0):
                    error = 'Trailer Economic number must be positive '

        return error

    def validate_search_fields_esp(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['assigned_id'] != None:
                if int(fields['assigned_id']) < 1000000 or int(fields['assigned_id'] > 9999999):
                    error = 'Id Asignado debe tener 7 digitos '

            if fields['vehicle_no'] != None:
                if int(fields['vehicle_no'] < 0):
                    error = 'No. Económico del Vehiculo debe de ser positivo '

            if fields['trailer_no'] != None:
                if int(fields['trailer_no'] < 0):
                    error = 'No. Económico de la Caja debe de ser positivo '

        return error


    def generate_today_table(fields,user_id):
        table = TripTable(Trip.objects.filter(user_id=user_id).filter(date = str(timezone.now().strftime('%Y-%m-%d'))))
        if fields != None:
            if fields['assigned_id'] != None:
                if Trip.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None
            if fields['vehicle_no']!= None:
                print(fields['vehicle_no'])
                if Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['trailer_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['origin']!= '':
                if Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['destiny']!= '':
                if Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['trip_type']!= '':
                if Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

        return table

    def generate_today_table_esp(fields,user_id):
        table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(date = str(timezone.now().strftime('%Y-%m-%d'))))
        if fields != None:
            if fields['assigned_id'] != None:
                if Trip.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None
            if fields['vehicle_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['trailer_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['origin']!= '':
                if Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['destiny']!= '':
                if Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable(Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

            if fields['trip_type']!= '':
                if Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))).exists():
                    table = TripTable_esp(Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).filter(date=str(timezone.now().strftime('%Y-%m-%d'))))
                else:
                    table = None

        return table


    def generate_bitacora_table(fields,user_id):
        table = BitacoraTable(Trip.objects.filter(user_id=user_id))
        if fields != None:
            if fields['assigned_id'] != None:
                if Trip.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']))
                else:
                    table = None
            if fields['vehicle_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']))
                else:
                    table = None

            if fields['trailer_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']))
                else:
                    table = None

            if fields['origin']!= '':
                if Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']))
                else:
                    table = None

            if fields['destiny']!= '':
                if Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']))
                else:
                    table = None

            if fields['trip_type']!= '':
                if Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']))
                else:
                    table = None

            if fields['date']!= '':
                if Trip.objects.filter(user_id=user_id).filter(date=fields['date']).exists():
                    table = BitacoraTable(Trip.objects.filter(user_id=user_id).filter(date=fields['date']))
                else:
                    table = None

        return table


    def generate_bitacora_table_esp(fields,user_id):
        table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id))
        if fields != None:
            if fields['assigned_id'] != None:
                if Trip.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']))
                else:
                    table = None
            if fields['vehicle_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(vehicle_no=fields['vehicle_no']))
                else:
                    table = None

            if fields['trailer_no']!= None:
                if Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(trailer_no=fields['trailer_no']))
                else:
                    table = None

            if fields['origin']!= '':
                if Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(origin=fields['origin']))
                else:
                    table = None

            if fields['destiny']!= '':
                if Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(destiny=fields['destiny']))
                else:
                    table = None

            if fields['trip_type']!= '':
                if Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(trip_type=fields['trip_type']))
                else:
                    table = None

            if fields['date']!= '':
                if Trip.objects.filter(user_id=user_id).filter(date=fields['date']).exists():
                    table = BitacoraTable_esp(Trip.objects.filter(user_id=user_id).filter(date=fields['date']))
                else:
                    table = None

        return table


