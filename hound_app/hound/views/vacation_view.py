import xlwt
from xlwt import XFStyle
from xlwt import Font
from django.shortcuts import render
from django.contrib import messages
from ..models.vacations import *
from ..src.validator import Validator
from ..models.date import *
from ..src.xls_generator import *
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.http import HttpResponse

class VacationView:

    def get_vacations(request,lenguage,assigned_id):

        email = '/email/0/'
        vacations = 'hound-eng/vacations.html/'
        if int(lenguage) == 1:
            email = '/email/1/'
            vacations = 'hound-esp/vacations.html/'


        if not Validator.validate_view(request):
            return redirect(email)

        state = False
        driver = VacationView.get_driver(request,assigned_id)
        name = driver.name
        last_name = driver.last_name
        searchVacation = SearchVacationForm()
        table_vacations = VacationView.get_vacations_table(request,lenguage,driver.assigned_id)
        if table_vacations == None:
            empty = True
        else:
            empty = False
            table_vacations.paginate(page=request.GET.get('page', 1), per_page=10)
        values = {'table_vacations':table_vacations,
                  'assigned_id':assigned_id,
                  'name': name,
                  'last_name': last_name,
                  'state':state,
                  'empty':empty,
                  'lenguage':lenguage,
                  'has_dates':False,
                  'searchVacation':searchVacation,
                  'has_id':False
                  }
        return render(request, vacations, values)

    def get_vacations_dates(request,lenguage,assigned_id,vacation_id):

        email = '/email/0/'
        error_cycle = 'The requested vacation cycle does not exists'
        vacations_template = 'hound-eng/vacations.html/'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_cycle = 'El ciclo de vacaciones solicitado no existe'
            vacations_template = 'hound-esp/vacations.html/'

        if not Validator.validate_view(request):
            return redirect(email)

        state = False
        if vacation_id != '0':
            if Vacations.objects.filter(vacation_id = vacation_id).filter(user_id = request.session['id']).exists():
                vacations = Vacations.objects.get(vacation_id=vacation_id)
                no_days = vacations.no_days
                taken_days = vacations.taken_days
                if taken_days < no_days:
                    state = True
            else:
                return render(request, "hound-eng/error.html",{'error': error_cycle})

        driver = VacationView.get_driver(request,assigned_id)
        name = driver.name
        last_name = driver.last_name
        table_vacations = VacationView.get_vacations_table(request,lenguage,driver.assigned_id)
        table_dates = VacationView.get_dates( vacation_id,lenguage)
        if table_dates == None:
            has_dates = False
        else:
            has_dates = True
        formDate = DateForm
        searchVacation = SearchVacationForm()
        table_vacations.paginate(page=request.GET.get('page', 1), per_page=10)
        values = {'table_vacations':table_vacations,
                  'assigned_id':assigned_id,
                  'name': name,
                  'last_name': last_name,
                  'table_dates':table_dates,
                  'state':state,
                  'vacation_id':vacation_id,
                  'formDate':formDate,
                  'lenguage': lenguage,
                  'has_dates':has_dates,
                  'searchVacation': searchVacation,
                  'has_id':True
                  }

        return render(request,vacations_template,values)

    def get_vacations_table(request,lenguage,assigned_id):
        if Vacations.objects.filter( assigned_id=assigned_id ).filter(user_id=request.session['id']).exists():
            vacations = Vacations.objects.filter( assigned_id=assigned_id ).filter(user_id=request.session['id'])

            if int(lenguage) == 0:
                table = VacationsTable( vacations )
            elif int(lenguage) == 1:
                table = VacationsTable_esp(vacations)
            else:
                return render(request,'hound-eng/error.html',{'error':'Internal error'})
            table.paginate(page=request.GET.get('page', 1), per_page=5)
            return table
        else:
            return None

    def get_driver(request,assigned_id):
        user = User.objects.get( user_id=request.session['id'] )
        driver = Driver.objects.get( user_id=user, assigned_id=assigned_id )
        return driver

    def get_dates(vacation_id,lenguge):
        table = None
        if Vacations.objects.filter(vacation_id = vacation_id).exists():
            vacation = Vacations.objects.get(vacation_id = vacation_id)
            dates = Date.objects.filter(vacation_id = vacation)
            if dates.count() > 0:

                if int(lenguge) == 0:
                    table = DateTable(dates)
                elif int(lenguge) == 1:
                    table = DateTable_esp(dates)
        return table


    def add_vacations(request,lenguage,assigned_id):

        email = '/email/0/'
        error_fields = 'Fill al the required fields'
        vacations_template = 'hound-eng/add_vacations.html/'
        vacations_url = '/vacations/0/'
        error_request = 'Driver does not exists'
        if int(lenguage) == 1:
            email = '/email/1/'
            error_fields = 'Completa los campos que se requieren'
            vacations_template = 'hound-esp/add_vacations.html/'
            vacations_url = '/vacations/1/'
            error_request = 'El conductor no existe'


        if not Validator.validate_view(request):
            return redirect(email)

        user_id = request.session['id']
        user = User.objects.get( user_id=user_id )
        if Driver.objects.filter(user_id = user).filter(assigned_id=assigned_id).exists():
            driver = Driver.objects.get( user_id=user_id, assigned_id=assigned_id )
            formVacations = VacationsForm()

            if request.method == 'POST':
                formVacations = VacationsForm(request.POST)
                if formVacations.is_valid( ):
                    vacations = formVacations.save( commit=False )
                    vacations.id_driver = driver
                    vacations.assigned_id = driver.assigned_id
                    vacations.user_id = user
                    if vacations.amount_payed == vacations.payment_rate:
                        vacations.payed = True
                    vacations.save()

                    return redirect(vacations_url+str(assigned_id)+'/')
                else:
                    messages.error(request,error_fields)

            return render(request,vacations_template,{
                                    'formVacations':formVacations,
                                    'assigned_id':assigned_id
                                    })
        else:
            return render(request,"hound-eng/error.html",{'error':error_request})

    def add_date(request,lenguage,assigned_id,vacation_id):
        email = '/email/0/'
        error_days = 'Taken days exceeded the number of total vacation days'
        vacations_url = '/vacations_dates/0/'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_days = 'El número de dias exceden el total de dias de vacaciones'
            vacations_url = '/vacations_dates/1/'

        if not Validator.validate_view(request):
            return redirect(email)

        if request.method == 'POST':
            vacation = Vacations.objects.get(vacation_id=vacation_id)
            no_days = vacation.no_days
            formDate = DateForm(request.POST)
            date = formDate.save(commit=False)
            vacation.taken_days += 1
            if vacation.taken_days <= no_days:
                vacation.save()
                date.vacation_id = vacation
                date.save()
            else:
                return render(request, "hound-eng/error.html", {'error': error_days})
        return redirect(vacations_url+str(assigned_id)+'/'+str(vacation_id)+'/')

    def delete_dates(request,lenguage,assigned_id,vacation_id):
        email = '/email/0/'
        error_list ='Empty list'
        vacations_url = '/vacations_dates/0/'
        if int(lenguage) == 1:
            error_list = 'Lista vacia'
            vacations_url = '/vacations_dates/1/'
            email = '/email/1/'

        if not Validator.validate_view(request):
            return redirect(email)

        if request.method == 'POST':
            pk = request.POST.getlist('select_dates')
            if len(pk) > 0:
                Date.objects.filter(pk__in=pk).delete()
                vacations = Vacations.objects.get(vacation_id = vacation_id)
                vacations.taken_days -= len(pk)
                vacations.save()
            else:
                return render(request,'hound-eng/error.html',{'error':error_list})
        return redirect(vacations_url+str(assigned_id)+'/'+str(vacation_id)+'/')

    def edit_vacations(request,lenguage,assigned_id,vacation_id):
        email = '/email/0/'
        vacations_url = '/vacations_dates/0/'
        vacations_template = 'hound-esp/edit_vacations.html/'
        error_fields = 'Fill all the required fields'
        error_cycle = 'The requested vacation cycle does not exists'
        error_driver = 'The requested driver does not exists'

        if int(lenguage) == 1:
            email = '/email/1/'
            vacations_url = '/vacations_dates/1/'
            vacations_template = 'hound-esp/edit_vacations.html/'
            error_fields = 'Por favor llena los campos que se te piden'
            error_cycle = 'El ciclo de vacaciones solicitado no existe'
            error_driver = 'El conductor no existe'

        if not Validator.validate_view(request):
            return redirect(email)

        user_id = request.session['id']
        user = User.objects.get( user_id=user_id )
        if Driver.objects.filter( user_id=user ).filter( assigned_id=assigned_id ).exists( ):
            if Vacations.objects.filter(user_id=user).filter(assigned_id=Driver.objects.filter(assigned_id=assigned_id).values_list('assigned_id')).exists():
                vacations = Vacations.objects.get(vacation_id = vacation_id)
                formVacations = VacationsForm(request.POST or None,instance=vacations)

                if request.method == 'POST':
                    if formVacations.is_valid():
                        if vacations.amount_payed == vacations.payment_rate:
                            vacations.payed = True
                        else:
                            vacations.payed = False
                        formVacations.save()
                        return redirect(vacations_url+assigned_id+'/'+vacation_id+'/')
                    else:
                        messages.error(request,error_fields)

                return render(request, vacations_template,{'formVacations':formVacations,
                                                                     'assigned_id':assigned_id,
                                                                     'vacation_id':vacation_id
                                                                     })
            else:
                return render( request, "hound-eng/error.html", {'error': error_cycle} )

        else:
            return render( request, "hound-eng/error.html", {'error': error_driver} )

    @require_GET
    def delete_vacations(request,lenguage,assigned_id,vacation_id):

        email = '/email/0/'
        error_cycle = 'The vacation cycle does not exists'
        vacations_url = '/vacations/0/'

        if int(lenguage) == 1:
            email = '/email/1/'
            error_cycle = 'El ciclo de vacaciones no existe'
            vacations_url = '/vacations/1/'

        if not Validator.validate_view(request):
            return redirect(email)

        if Vacations.objects.filter(vacation_id = vacation_id).exists():
            vacations = Vacations.objects.get(vacation_id = vacation_id)
            if Date.objects.filter(vacation_id=vacations).exists():
                dates = Date.objects.filter(vacation_id = vacations)
                for date in dates:
                    date.delete()
            vacations.delete()
        else:
            return render(request, "hound-eng/error.html", {'error': error_cycle})
        return redirect(vacations_url+str(assigned_id)+'/')

    @require_GET
    def delete_all(request,lenguage,assigned_id):

        vacations_url = '/vacations/0/'

        if int(lenguage) == 1:
            vacations_url = '/vacations/1/'


        driver = Driver.objects.get(assigned_id = assigned_id,user_id = request.session['id'])
        vacations = Vacations.objects.filter(assigned_id = driver.assigned_id)
        if Date.objects.filter(vacation_id__in = vacations).exists():
            Date.objects.filter(vacation_id__in = vacations).delete()
        vacations.delete()

        return redirect(vacations_url+str(assigned_id)+'/')

    def search_vacation(request,lenguage,assigned_id):
        email = '/email/0/'
        vacations_template = 'hound-eng/vacations.html/'
        error = 'No records found'
        error_option = 'Invalid option'
        if int(lenguage) == 1:
            email = '/email/1/'
            vacations_template = 'hound-esp/vacations.html/'
            error= 'No se encontraron resultados'
            error_option = 'Opcion invalida'

        if not Validator.validate_view(request):
            return redirect(email)

        if request.method == 'POST':
            searchVacation = SearchVacationForm(request.POST)
            vacation = searchVacation.save(commit=False)
            if searchVacation.is_valid():
                if Vacations.objects.filter( assigned_id=assigned_id ).filter(user_id = request.session['id']).filter(year=vacation.year).exists():
                    vacations = Vacations.objects.filter( assigned_id=assigned_id).filter(user_id = request.seesion['id']).filter(year=vacation.year)
                    if int(lenguage) == 0:
                        table = VacationsTable(vacations)
                    elif int(lenguage) == 1:
                        table = VacationsTable_esp(vacations)
                    else:
                        return render(request, 'hound-eng/error.html', {'error': error_option})
                else:
                    return render(request,'hound-eng/error.html',{'error':error})

        state = False
        driver = VacationView.get_driver(request, assigned_id)
        name = driver.name
        last_name = driver.last_name
        searchVacation = SearchVacationForm()
        empty = False
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        values = {'table_vacations': table,
                  'assigned_id': assigned_id,
                  'name': name,
                  'last_name': last_name,
                  'state': state,
                  'empty': empty,
                  'lenguage': lenguage,
                  'has_dates': False,
                  'searchVacation': searchVacation
                  }
        return render(request, vacations_template, values)


    def export_vacations(request,lenguage,assigned_id):

            email = '/email/0/'

            if int(lenguage) == 1:
                email = '/email/1/'

            if not Validator.validate_view(request):
                return redirect(email)

            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="vacations.xls"'

            if int(lenguage) == 1:
                response['Content-Disposition'] = 'attachment; filename="vacaciones.xls"'

            rows_vacations = Vacations.objects.filter(user_id=user_id).filter(assigned_id=assigned_id).order_by(
                'vacation_id').values_list('vacation_id','year', 'no_days', 'payment_rate',
                                           'taken_days', 'amount_payed', 'payed', 'exchange_rate')

            rows_driver = Driver.objects.filter(assigned_id=assigned_id).filter(user_id=user_id).values_list(
                'assigned_id',
                'name',
                'middle_name',
                'last_name',
                )

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Drivers')

            if int(lenguage) == 1:
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Conductores')

            row_num = 0

            columns = [ 'Assigned Id','Name','Middle Name',
                        'Lastname'
                        ]

            if int(lenguage) == 1:
                columns = ['Id asignado', 'Nombre', 'Segundo nombre',
                           'Apellido'
                           ]

            row_num = XlsGenerator.create_headers(columns, ws, row_num)
            for row in rows_driver:
                row_num = XlsGenerator.create_content(ws,row_num,row,xlwt.XFStyle())

            columns_vacations = [
                                'Vacation Id','Year','No Days',
                                'Payment Rate','Taken Days','Amount Payed',
                                'Exchange Rate'
                                ]

            columns = ['Date']

            if int(lenguage) == 1:
                columns_vacations = [
                    'Id vacaciones', 'Año', 'No de dias',
                    'Tarifa', 'Dias tomados', 'Cantidad pagada',
                    'Tipo de cambio'
                ]

                columns = ['Fecha']

            date_format = XFStyle()
            date_format.num_format_str = 'M/D/YY'


            for row in rows_vacations:
                row_num += 2
                row_num = XlsGenerator.create_headers(columns_vacations, ws, row_num)
                row_num = XlsGenerator.create_content(ws,row_num,row,xlwt.XFStyle())
                row_num = XlsGenerator.create_headers(columns,ws,row_num)
                rows_dates = Date.objects.filter(vacation_id = row[0]).values_list('date')
                for row_date in rows_dates:
                    row_num = XlsGenerator.create_content(ws,row_num,row_date,date_format)

            wb.save(response)
            return response



