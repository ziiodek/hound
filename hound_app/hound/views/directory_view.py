import xlwt
import pymysql
from xlwt import XFStyle
from xlwt import Font
from django.shortcuts import render
from django.contrib import messages
from ..models.directory import *
from ..src.validator import Validator
from ..models.directory import *
from ..src.xls_generator import *
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.http import HttpResponse

class DirectoryView:

    def add_directory(request,lenguage,assigned_id):

        email = '/email/0/'
        directory_template = 'hound-eng/directory.html/'
        error_driver = 'Driver does not exists'
        directory_url = '/add_directory/0/'
        if int(lenguage) == 1:
            email = '/email/1/'
            directory_template = 'hound-esp/directory.html/'
            error_driver = 'El conductor no existe'
            directory_url = '/add_directory/1/'


        if not Validator.validate_view(request):
            return redirect(email)

        driver = DirectoryView.get_driver(request, assigned_id)
        formDirectory = DirectoryForm
        driver_profile = DirectoryView.load_driver(request.session['id'],int(assigned_id))

        table_directory = DirectoryView.get_directory_table(request, lenguage, driver.assigned_id)
        if table_directory == None:
            empty = True
        else:
            empty = False
            table_directory.paginate(page=request.GET.get('page', 1), per_page=5)

        if request.method == 'POST':
            formDirectory = DirectoryForm(request.POST)
            print(formDirectory.errors)
            if formDirectory.is_valid():
                if Driver.objects.filter(user_id =request.session['id']).filter(assigned_id = assigned_id).exists():
                    user = User.objects.get(user_id = request.session['id'])
                    directory = formDirectory.save(commit = False)

                    if Validator.check_pattern_phone_number(directory.phone_number) == True:
                        error = 'Phone Number must not contain symbols'

                        if int(lenguage) == 1:
                            error = 'Número de teléfono no debe de contener simbolos'

                        messages.error(request, error)

                        values = {'table': table_directory,
                                  'assigned_id': assigned_id,
                                  'lenguage': lenguage,
                                  'empty': empty,
                                  'formDirectory': formDirectory,
                                  'driver': driver_profile,
                                  'state': False
                                  }
                        return render(request, directory_template, values)



                    directory.user_id = user
                    directory.assigned_id = assigned_id
                    directory.save()
                    return redirect(directory_url+assigned_id+'/')
                else:
                    return render(request,'hound-eng/error.html',{'error':error_driver})
            else:
                messages.error(request,formDirectory.errors)

        values = {'table': table_directory,
                  'assigned_id': assigned_id,
                  'lenguage': lenguage,
                  'empty':empty,
                  'formDirectory':formDirectory,
                  'driver':driver_profile,
                  'state':False
                  }
        return render(request, directory_template, values)

    def edit_directory(request, lenguage, assigned_id, phone_id):
        email = '/email/0/'
        directory_template = 'hound-eng/directory.html/'
        directory_url = '/edit_directory/0/'
        error_driver = 'Driver does not exists'
        error_directory = 'Phone number does not exists'
        if int(lenguage) == 1:
            email = '/email/1/'
            directory_template = 'hound-esp/directory.html/'
            error_driver = 'El conductor no existe'
            error_directory = 'Número de teléfono no existe'
            directory_url = '/edit_directory/1/'

        if not Validator.validate_view(request):
            return redirect(email)

        if Directory.objects.filter(id = phone_id).exists():
            directory = Directory.objects.get(id = phone_id)
            editDirectory = DirectoryForm(request.POST or None,instance = directory)
            formDirectory = DirectoryForm()
            driver = DirectoryView.get_driver(request, assigned_id)
            driver_profile = DirectoryView.load_driver(request.session['id'], int(assigned_id))

            table_directory = DirectoryView.get_directory_table(request, lenguage, driver.assigned_id)
            if table_directory == None:
                empty = True
            else:
                empty = False
                table_directory.paginate(page=request.GET.get('page', 1), per_page=5)

            if request.method == 'POST':
                editDirectory = DirectoryForm(request.POST)
                if editDirectory.is_valid():
                    if Driver.objects.filter(user_id=request.session['id']).filter(assigned_id=assigned_id).exists():
                        tmp_directory = editDirectory.save(commit = False)
                        directory.phone_number = tmp_directory.phone_number
                        directory.save()
                        return redirect(directory_url + assigned_id + '/'+phone_id+'/')
                    else:
                        return render(request, 'hound-eng/error.html', {'error': error_driver})
                else:
                    messages.error(request, editDirectory.errors)

            values = {'table': table_directory,
                    'assigned_id': assigned_id,
                    'empty': empty,
                    'phone_id':phone_id,
                    'lenguage': lenguage,
                    'formDirectory': formDirectory,
                    'editDirectory':editDirectory,
                    'phone_number':directory.phone_number,
                    'driver':driver_profile,
                    'state':True
                    }
            return render(request, directory_template, values)
        else:
            return render(request,'hound-eng/error.html',{'error':error_directory})

    def get_directory_table(request,lenguage,assigned_id):
        if Directory.objects.filter( assigned_id=assigned_id ).filter(user_id = request.session['id']).exists():
            directory = Directory.objects.filter( assigned_id=assigned_id ).filter(user_id = request.session['id'])

            if int(lenguage) == 0:
                table = DirectoryTable( directory)
            elif int(lenguage) == 1:
                table = DirectoryTableEsp(directory)
            else:
                return render(request,'hound-eng/error.html',{'error':'Internal error'})
            return table
        else:
            return None

    def get_driver(request,assigned_id):
        user = User.objects.get( user_id=request.session['id'] )
        driver = Driver.objects.get( user_id=user, assigned_id=assigned_id )
        return driver


    @require_GET
    def empty_directory(request,lenguage,assigned_id):

        directory_url = '/add_directory/0/'

        if int(lenguage) == 1:
            directory_url = '/add_directory/1/'

        directory = Directory.objects.filter(assigned_id = int(assigned_id)).filter(user_id = request.session['id'])
        directory.delete()
        return redirect(directory_url+str(assigned_id)+'/')

    @require_POST
    def delete_number(request, lenguage, assigned_id):

        directory_url = '/add_directory/0/'
        list_error = 'Empty list'

        if int(lenguage) == 1:
            directory_url = '/add_directory/1/'
            list_error = 'Lista vacía'

        if request.method == 'POST':
            pk = request.POST.getlist('select_numbers')
            if len(pk) > 0:
                directory = Directory.objects.filter(id__in = pk)
                for number in directory:
                    number.delete()
            else:
                return render(request,'hound-eng/error.html',{'error':list_error})

        return redirect(directory_url + str(assigned_id) + '/')

    def export_directory(request, lenguage, assigned_id):

        email = '/email/0/'

        if int(lenguage) == 1:
            email = '/email/1/'

        if not Validator.validate_view(request):
            return redirect(email)

        user_id = request.session['id']
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="directory.xls"'

        if int(lenguage) == 1:
            response['Content-Disposition'] = 'attachment; filename="directorio.xls"'

        rows_directory = Directory.objects.filter(user_id=user_id).filter(assigned_id=assigned_id).order_by(
            'id').values_list('phone_number')

        rows_driver = Driver.objects.filter(assigned_id=assigned_id).filter(user_id=user_id).values_list(
            'assigned_id',
            'name',
            'middle_name',
            'last_name',
        )

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Directory')

        if int(lenguage) == 1:
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Directorio')

        row_num = 0

        columns = ['Assigned Id', 'Name', 'Middle Name',
                   'Lastname'
                   ]

        if int(lenguage) == 1:
            columns = ['Id asignado', 'Nombre', 'Segundo nombre',
                       'Apellido'
                       ]

        row_num = XlsGenerator.create_headers(columns, ws, row_num)
        for row in rows_driver:
            row_num = XlsGenerator.create_content(ws, row_num, row, xlwt.XFStyle())

        columns_directory = [
            'Phone Number'
        ]

        if int(lenguage) == 1:
            columns_directory = [
                'Número de Teléfono'
            ]

        for row in rows_directory:
            row_num += 2
            row_num = XlsGenerator.create_headers(columns_directory, ws, row_num)
            row_num = XlsGenerator.create_content(ws, row_num, row, xlwt.XFStyle())

        wb.save(response)
        return response




    def load_driver(user_id, assigned_id):
        database = pymysql.connect('localhost', 'root', '', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'
        cursor.execute("select profile_img from hound_driver where user_id_id='%s' and assigned_id='%d';" % (
        user_id, assigned_id))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            src = data[0]

        database.close()
        return src

