import io
import xlwt
from xlsxwriter.workbook import Workbook
import pymysql
from xlwt import XFStyle
from django.shortcuts import render
from django.shortcuts import redirect
from ..models.driver import *
from ..models.address import *
from ..models.documents import *
from ..models.driver_status import *
from ..models.profile import *
from ..models.prints import *
from ..src.id_generator import IdGenerator
from ..src.xls_generator import XlsGenerator
from ..src.validator import Validator
from ..src.database import Database
from ..static.hound.data.uploader import Uploader
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import datetime



class DriverView:

    def get_all_drivers(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'


        if not Validator.validate_view(request):
            return redirect(email_template)


        if status == "1":
            status = True
            template = 'hound-eng/archiver_drivers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/archiver_drivers.html'

        elif status == "0":
            status = False
            template = 'hound-eng/assets_drivers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/assets_drivers.html'

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        Database.clear_profile(request.session['id'], 'driver')
        Database.clear_prints(request.session['id'])
        nameField = Name()
        lastNameField = LastName()
        assignedIdField = AssignedId()
        country = Country()
        idField = Id()
        rfcField = RFC()
        startDateField = StartDate()

        if int(lenguage) == 0:
            table = DriverView.generate_table(None,request.session['id'],status)
        elif int(lenguage) == 1:
            table = DriverView.generate_table_esp(None, request.session['id'], status)
        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render( request, template,{
                                                                  'table':table,'action':0,'nameField':nameField,
                                                                  'lastNameField':lastNameField,'idField':idField,
                                                                  'startDateField':startDateField,'assignedIdField':assignedIdField,
                                                                  'rfcField':rfcField,'country':country,'status':status
                                                                })

    def view_driver(request,lenguage,assigned_id):

        email_template = '/email/0/'
        view_template = 'hound-eng/view_driver.html'
        error_driver = 'Driver does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = 'hound-esp/view_driver.html'
            error_driver = 'El conductor no existe'



        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        user = User.objects.get(user_id = user_id)
        if Driver.objects.filter(user_id = user).filter(assigned_id=assigned_id).exists():
            driver = Driver.objects.get(user_id = user,assigned_id = assigned_id)
            address = Address.objects.get(user_id=user,assigned_id=driver.assigned_id)
            documents = Documents.objects.get(user_id = user,assigned_id=driver.assigned_id)
            status = DriverStatus.objects.get(user_id = user, assigned_id=driver.assigned_id)
            expired = status.expired
            formDriver = DriverForm(instance=driver)
            formAddress = AddressForm(instance = address)
            formDocuments = DocumentsForm(instance=documents)
            formStatus = DriverStatusForm(instance=status)
            profile = DriverView.load_tmp_profile(user_id, assigned_id)
            prints = DriverView.load_tmp_prints(user_id,assigned_id)


            return render(request,view_template,{'formDriver':formDriver,
                                                                'formAddress':formAddress,
                                                                'formDocuments':formDocuments,
                                                                'formStatus':formStatus,
                                                                'profile':profile,
                                                                'prints':prints,
                                                                'assigned_id':assigned_id,
                                                                'expired':expired,
                                                                'phone_number':address.phone_number,
                                                                'email_address':driver.email_address
                                                                })
        else:
            return render(request,'hound-eng/error.html',{'error':error_driver})

    def add_driver(request,lenguage):

        email_template = '/email/0/'
        view_template = '/view_driver/0/'
        error_user = 'Username does not exists'
        error_driver = 'Driver exists'
        add_template = 'hound-eng/add_driver.html'
        error_version = 'For the free version you can only register 100 drivers, upgrade to Big Company to register up to 10 drivers'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            view_template = '/view_driver/1/'
            error_user = 'El nombre de usuario no existe'
            add_template = 'hound-esp/add_driver.html'
            error_driver = 'El conductor ya existe'
            error_version = 'Solo puedes registrar 100 conductores en la versión gratis, actualiza a Big Company para registrar mas de 100 conductores'

        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        assigned_id = IdGenerator.generate_assigned_id(user_id)
        formProfile = ProfileForm()
        formPrints = PrintsForm()
        profile = DriverView.load_tmp_profile(user_id, assigned_id)
        prints = DriverView.load_tmp_prints(user_id, assigned_id)
        if request.method == 'POST':
            if Driver.objects.filter(user_id = user_id).count() >= 100:
                return render(request,'hound-eng/error.html',{'error':error_version})

            formDriver = DriverForm( request.POST )
            formAddress = AddressForm( request.POST )
            formDocuments = DocumentsForm( request.POST )
            formStatus = DriverStatusForm( request.POST )

            if not formStatus.is_valid():
                messages.error(request, formStatus.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })

            if not formDocuments.is_valid():
                messages.error(request, formDocuments.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })

            if not formAddress.is_valid():
                messages.error(request, formAddress.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })


            if formDriver.is_valid():
                driver = formDriver.save(commit=False)



                address = formAddress.save(commit=False)
                documents = formDocuments.save(commit=False)
                status = formStatus.save(commit=False)
                error = DriverView.validate_documents(documents)

                if int(lenguage) == 1:
                    error = DriverView.validate_documents_esp(documents)



                if error == '':
                    if User.objects.filter(user_id=user_id).exists():
                        user =  User.objects.get(user_id=user_id)
                        if Driver.objects.filter(user_id = user_id).filter(assigned_id=assigned_id).exists():
                            return render(request, 'hound-eng/error.html', {'error': error_driver})
                        driver.assigned_id = assigned_id
                        driver.user_id = User.objects.get(user_id=user_id)
                        driver.save()

                        driver = Driver.objects.get(user_id = user, assigned_id=assigned_id)
                        address.id_driver = driver
                        address.user_id = user
                        address.assigned_id = driver.assigned_id
                        documents.id_driver = driver
                        documents.user_id = user
                        documents.license_type.upper()
                        documents.assigned_id = driver.assigned_id
                        status.id_driver = driver
                        status.user_id = user
                        status.assigned_id = driver.assigned_id

                        address.save()
                        documents.save()
                        status.save()
                        DriverView.save_profile(user_id, assigned_id)
                        DriverView.save_prints(user_id,assigned_id)
                        Database.clear_prints(user_id)
                        Database.clear_profile(user_id, 'driver')
                        assigned_id = IdGenerator.store_assigned_id(user_id)

                        return redirect(view_template+str(assigned_id)+'/')
                    else:
                        return render( request, 'hound-eng/error.html', {'error': error_user} )
                else:
                    messages.error( request, error )

            else:
                messages.error(request,formDriver.errors)


        formDriver = DriverForm( initial={'assigned_id': assigned_id} )
        formAddress = AddressForm()
        formDocuments = DocumentsForm()
        formStatus = DriverStatusForm()


        return render(request,add_template,
                      {'formDriver':formDriver,
                       'formAddress':formAddress,
                       'formDocuments':formDocuments,
                       'formStatus': formStatus,
                       'formProfile': formProfile,
                       'formPrints': formPrints,
                       'profile': profile,
                       'prints':prints,
                       'assigned_id':assigned_id
                       })

    def validate_documents(documents):
        error = ''

        if documents.id != '':
            if len(documents.id) < 8 or len(documents.id) > 20:
                error += 'Id must have 8 to 20 characters length '

        if  documents.rfc != '':
            if len( documents.rfc) < 10 or len(documents.rfc) > 10:
                error += 'RFC must have 10 characters length '

        if documents.curp != '':
            if len( documents.curp ) < 18 or len(documents.curp) > 18:
                error += 'CURP must have 18 characters length '

        if documents.license_no != '':
            if len( documents.license_no ) < 8 or len(documents.license_no) > 20:
                error += 'License number must have 8 to 20 characters length '

        if documents.passport_no != '':
            if len( documents.passport_no ) < 10 or len(documents.passport_no) > 30:
                error += 'Passport number must have 10 to 20 characters length '

        return error

    def validate_documents_esp(documents):
        error = ''

        if documents.id != '':
            if len(documents.id) < 8 or len(documents.id) > 20:
                error += 'Id debe tener de 8 a 20 caracteres '

        if  documents.rfc != '':
            if len( documents.rfc) < 10 or len(documents.rfc) > 10:
                error += 'RFC debe tener 10 caracteres '

        if documents.curp != '':
            if len( documents.curp ) < 18 or len(documents.curp) > 18:
                error += 'CURP debe tener 18 caracteres '

        if documents.license_no != '':
            if len( documents.license_no ) < 8 or len(documents.license_no) > 20:
                error += 'Número de licencia debe tener de 8 a 20 caracteres '

        if documents.passport_no != '':
            if len( documents.passport_no ) < 10 or len(documents.passport_no) > 30:
                error += 'Pasaporte debe tener 10 a 30 caracteres '

        return error

    def edit_driver(request,lenguage,assigned_id):

        email_template = '/email/0/'
        error_driver = 'Driver does not exists'
        view_template = '/view_driver/0/'
        edit_template = 'hound-eng/edit_driver.html/'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_driver = 'El conductor no existe'
            view_template = '/view_driver/1/'
            edit_template = 'hound-esp/edit_driver.html/'


        if not Validator.validate_view(request):
            return redirect(email_template)

        user_id = request.session['id']
        user = User.objects.get( user_id=user_id )

        if not Driver.objects.filter(user_id=user,assigned_id=assigned_id ).exists():
            return render(request,'hound-eng/error.html',{'error':error_driver})

        driver = Driver.objects.get( user_id=user, assigned_id=assigned_id )
        address = Address.objects.get( user_id=user, assigned_id=driver.assigned_id )
        documents = Documents.objects.get( user_id=user, assigned_id=driver.assigned_id )
        status = DriverStatus.objects.get( user_id=user, assigned_id=driver.assigned_id )
        expired = status.expired
        formDriver = DriverForm(request.POST or None,instance=driver )
        formAddress = AddressForm(request.POST or None,instance=address )
        formDocuments = DocumentsForm(request.POST or None,instance=documents )
        formStatus = DriverStatusForm(request.POST or None,instance=status )
        formProfile = ProfileForm()
        formPrints = PrintsForm()
        profile = DriverView.load_tmp_profile(user_id, assigned_id)
        prints = DriverView.load_tmp_prints(user_id,assigned_id)

        if request.method == 'POST':

            if not formStatus.is_valid():
                messages.error(request, formStatus.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })

            if not formDocuments.is_valid():
                messages.error(request, formDocuments.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })

            if not formAddress.is_valid():
                messages.error(request, formAddress.errors)
                return render(request, add_template,
                              {'formDriver': formDriver,
                               'formAddress': formAddress,
                               'formDocuments': formDocuments,
                               'formStatus': formStatus,
                               'formProfile': formProfile,
                               'formPrints': formPrints,
                               'profile': profile,
                               'prints': prints,
                               'assigned_id': assigned_id
                               })

            if formDriver.is_valid():
                tmp = formDriver.save(commit=False)
                print(tmp.country)
                documents = formDocuments.save(commit = False)

                error = DriverView.validate_documents(documents)

                if int(lenguage) == 1:
                    error = DriverView.validate_documents_esp(documents)

                if error == '':
                    tmp.assigned_id = driver.assigned_id
                    tmp.save()
                    documents.save()
                    formDocuments.save()
                    formAddress.save()
                    driver_status = formStatus.save(commit=False)
                    driver_status.expired = expired
                    driver_status.save()
                    DriverView.save_profile(user_id, assigned_id)
                    DriverView.save_prints(user_id,assigned_id)
                    Database.clear_profile(user_id, 'driver')
                    Database.clear_prints(user_id)
                    return redirect(view_template + assigned_id + '/')
                else:
                    messages.error(request, error)

            else:
                messages.error(request,formDriver.errors)

        return render(request,edit_template,
                      {'formDriver':formDriver,
                       'formAddress':formAddress,
                       'formDocuments':formDocuments,
                       'formStatus':formStatus,
                       'formProfile': formProfile,
                       'formPrints': formPrints,
                       'profile':profile,
                       'prints':prints,
                       'assigned_id': assigned_id,
                       'expired':expired
                      })


    def generate_case_file(request,assigned_id):



        if not Validator.validate_view(request):
            return redirect('/email/0/')

        output = io.BytesIO()

        user_id = request.session['id']
        user = User.objects.get(user_id=user_id)
        wb = Workbook(output, {'in_memory': True})
        ws = wb.add_worksheet()

        format = wb.add_format({'font_color': 'silver','font_name':'arial','align':'right', 'font_size': 11})
        ws.write('K3',datetime.datetime.now().strftime("%Y-%m-%d"),format)

        format = wb.add_format({'font_color': 'navy','font_name':'arial','font_size':28,'bottom':1,'bottom_color':'navy'})
        bold = wb.add_format({'bold': True})

        driver = Driver.objects.get(assigned_id = assigned_id,user_id=user_id)
        address = Address.objects.get(assigned_id = assigned_id,user_id=user_id)
        documents = Documents.objects.get(assigned_id = assigned_id,user_id=user_id)
        status = DriverStatus.objects.get(assigned_id = assigned_id,user_id=user_id)

        ws.write('C6', user.company,format)
        ws.write('D6','', format)
        ws.write('E6','', format)
        ws.write('F6', '',format)
        ws.write('G6', '', format)
        ws.write('H6', '', format)
        ws.write('I6', '', format)
        ws.write('J6', '', format)
        ws.write('K6', '', format)

        format = wb.add_format({'bottom': 1, 'bottom_color': 'navy'})
        ws.write('C7','', format)
        ws.write('D7', '', format)
        ws.write('E7', '', format)
        ws.write('F7', '', format)
        ws.write('G7', '', format)
        ws.write('H7', '', format)

        format = wb.add_format({'bottom': 1, 'bottom_color': 'navy'})
        ws.write('C8', '', format)
        ws.write('D8', '', format)
        ws.write('E8', '', format)

        format = wb.add_format({'font_color': 'gray','font_name':'arial', 'font_size': 24, 'bottom': 6, 'bottom_color': 'gray'})
        ws.write('C11',str(driver.assigned_id),format)
        ws.write('D11', '', format)
        ws.write('E11', '', format)
        ws.write('F11', '', format)
        ws.write('G11', '', format)
        ws.write('H11', '', format)
        ws.write('I11', '', format)

        ws.write('C12','', format)
        ws.write('D12', '', format)

        ws.set_column('C:C', 30)

        if user.profile_img != "hound/images/default.jpg":
            ws.insert_image('A1',Uploader.get_path(user.profile_img),{'positioning': 3,'x_scale': 0.1, 'y_scale': 0.1})

        if driver.profile_img != "hound/images/default.jpg":
            ws.insert_image('C15', Uploader.get_path(driver.profile_img),{'positioning': 3,'x_scale': 0.1, 'y_scale': 0.1})

        if documents.prints_img != "hound/images/default.jpg":
            ws.insert_image('C18', Uploader.get_path(documents.prints_img), {'x_scale': 0.1, 'y_scale': 0.1})

        format = wb.add_format({'align':'justify'})
        ws.set_column('E:E',8.75,format)
        ws.set_column('F:F',8.75, format)

        ws.set_column('H:H', 8.75, format)
        ws.set_column('I:I', 8.75, format)

        ws.write('E16','Assigned Id',bold)
        ws.write('F16', driver.assigned_id)
        ws.write('E17', 'Name', bold)
        ws.write('F17', driver.name)
        ws.write('E18', 'Middle Name', bold)
        ws.write('F18', driver.middle_name)
        ws.write('E19', 'Lastname', bold)
        ws.write('F19', driver.last_name)
        ws.write('E20', 'Date of Birth', bold)
        ws.write('F20', str(driver.date_of_birth))
        ws.write('E22', 'Place of Birth', bold)
        ws.write('E24', 'Country',bold)
        ws.write('F24', driver.country)
        ws.write('E25', 'State', bold)
        ws.write('F25', driver.state)
        ws.write('E26', 'City', bold)
        ws.write('F26', driver.city)
        ws.write('E27', 'Start Date', bold)
        ws.write('F27', str(status.start_date))

        ws.write('E29', 'Address', bold)

        ws.write('E31', 'Country', bold)
        ws.write('F31', address.country_addr)
        ws.write('E32', 'State', bold)
        ws.write('F32', address.state_addr)
        ws.write('E33', 'City', bold)
        ws.write('F33', address.city_addr)

        ws.write('E34', 'Zip Code', bold)
        ws.write('F34', address.zip_code)
        ws.write('E35', 'Ext', bold)
        ws.write('F35', address.ext)
        ws.write('E36', 'Phone Number', bold)
        ws.write('F36', address.phone_number)

        if status.expired == True:
            ws.write('E37', 'End Date', bold)
            ws.write('F37', str(status.end_date))
            ws.write('E38', 'Reason of Leaving', bold)
            ws.write('F38', status.leave_reason)

        ws.write('H16', 'License No', bold)
        ws.write('I16', documents.license_no)
        ws.write('H17', 'License Type', bold)
        ws.write('I17', documents.license_type)
        ws.write('H18', 'License Issue Date', bold)
        ws.write('I18', str(documents.license_issue_date))
        ws.write('H19', 'License Expiration Date', bold)
        ws.write('I19', str(documents.license_exp_date))
        ws.write('H20', 'Passport No', bold)
        ws.write('I20', documents.passport_no)
        ws.write('H21', 'Passport Issue Date', bold)
        ws.write('I21', str(documents.passport_issue_date))
        ws.write('H22', 'Passport Expiration Date', bold)
        ws.write('I22', str(documents.passport_exp_date))
        ws.write('H23', 'DOT', bold)
        ws.write_boolean('I23', documents.dot)
        ws.write('H24', 'Criminal Record', bold)
        ws.write_boolean('I24', documents.criminal_record)

        wb.close()
        output.seek(0)
        response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Case_File.xlsx"

        return response

    def generate_case_file_esp(request, assigned_id):

        if not Validator.validate_view(request):
            return redirect('/email/1/')

        output = io.BytesIO()

        user_id = request.session['id']
        user = User.objects.get(user_id=user_id)
        wb = Workbook(output, {'in_memory': True})
        ws = wb.add_worksheet()

        format = wb.add_format({'font_color': 'silver', 'font_name': 'arial', 'align': 'right', 'font_size': 11})
        ws.write('K3', datetime.datetime.now().strftime("%Y-%m-%d"), format)

        format = wb.add_format(
            {'font_color': 'navy', 'font_name': 'arial', 'font_size': 28, 'bottom': 1, 'bottom_color': 'navy'})
        bold = wb.add_format({'bold': True})

        driver = Driver.objects.get(assigned_id=assigned_id, user_id=user_id)
        address = Address.objects.get(assigned_id=assigned_id, user_id=user_id)
        documents = Documents.objects.get(assigned_id=assigned_id, user_id=user_id)
        status = DriverStatus.objects.get(assigned_id=assigned_id, user_id=user_id)

        ws.write('C6', user.company, format)
        ws.write('D6', '', format)
        ws.write('E6', '', format)
        ws.write('F6', '', format)
        ws.write('G6', '', format)
        ws.write('H6', '', format)
        ws.write('I6', '', format)
        ws.write('J6', '', format)
        ws.write('K6', '', format)

        format = wb.add_format({'bottom': 1, 'bottom_color': 'navy'})
        ws.write('C7', '', format)
        ws.write('D7', '', format)
        ws.write('E7', '', format)
        ws.write('F7', '', format)
        ws.write('G7', '', format)
        ws.write('H7', '', format)

        format = wb.add_format({'bottom': 1, 'bottom_color': 'navy'})
        ws.write('C8', '', format)
        ws.write('D8', '', format)
        ws.write('E8', '', format)

        format = wb.add_format(
            {'font_color': 'gray', 'font_name': 'arial', 'font_size': 24, 'bottom': 6, 'bottom_color': 'gray'})
        ws.write('C11', str(driver.assigned_id), format)
        ws.write('D11', '', format)
        ws.write('E11', '', format)
        ws.write('F11', '', format)
        ws.write('G11', '', format)
        ws.write('H11', '', format)
        ws.write('I11', '', format)

        ws.write('C12', '', format)
        ws.write('D12', '', format)

        ws.set_column('C:C', 30)

        if user.profile_img != "hound/images/default.jpg":
            ws.insert_image('A1', Uploader.get_path(user.profile_img),
                            {'positioning': 3, 'x_scale': 0.1, 'y_scale': 0.1})

        if driver.profile_img != "hound/images/default.jpg":
            ws.insert_image('C15', Uploader.get_path(driver.profile_img),
                            {'positioning': 3, 'x_scale': 0.1, 'y_scale': 0.1})

        if documents.prints_img != "hound/images/default.jpg":
            ws.insert_image('C18', Uploader.get_path(documents.prints_img), {'x_scale': 0.1, 'y_scale': 0.1})

        format = wb.add_format({'align': 'justify'})
        ws.set_column('E:E', 8.75, format)
        ws.set_column('F:F', 8.75, format)

        ws.set_column('H:H', 8.75, format)
        ws.set_column('I:I', 8.75, format)

        ws.write('E16', 'Id asignado', bold)
        ws.write('F16', driver.assigned_id)
        ws.write('E17', 'Nombre', bold)
        ws.write('F17', driver.name)
        ws.write('E18', 'Segundo nombre', bold)
        ws.write('F18', driver.middle_name)
        ws.write('E19', 'Apellido', bold)
        ws.write('F19', driver.last_name)
        ws.write('E20', 'Fecha de nacimiento', bold)
        ws.write('F20', str(driver.date_of_birth))
        ws.write('E22', 'Lugar de nacimiento', bold)
        ws.write('E24', 'País', bold)
        ws.write('F24', driver.country)
        ws.write('E25', 'Estado', bold)
        ws.write('F25', driver.state)
        ws.write('E26', 'Ciudad', bold)
        ws.write('F26', driver.city)
        ws.write('E27', 'Fecha de inicio', bold)
        ws.write('F27', str(status.start_date))

        ws.write('E29', 'Dirección', bold)

        ws.write('E31', 'País', bold)
        ws.write('F31', address.country_addr)
        ws.write('E32', 'Estado', bold)
        ws.write('F32', address.state_addr)
        ws.write('E33', 'Ciudad', bold)
        ws.write('F33', address.city_addr)

        ws.write('E34', 'Código postal', bold)
        ws.write('F34', address.zip_code)
        ws.write('E35', 'Ext', bold)
        ws.write('F35', address.ext)
        ws.write('E36', 'Número de telefono', bold)
        ws.write('F36', address.phone_number)

        if status.expired == True:
            ws.write('E37', 'Fecha de expiracion', bold)
            ws.write('F37', str(status.end_date))
            ws.write('E38', 'Porque expiro', bold)
            ws.write('F38', status.leave_reason)

        ws.write('H16', 'No. de licencia', bold)
        ws.write('I16', documents.license_no)
        ws.write('H17', 'Tipo de licencia', bold)
        ws.write('I17', documents.license_type)
        ws.write('H18', 'Desde', bold)
        ws.write('I18', str(documents.license_issue_date))
        ws.write('H19', 'Hasta', bold)
        ws.write('I19', str(documents.license_exp_date))
        ws.write('H20', 'No. de pasaporte', bold)
        ws.write('I20', documents.passport_no)
        ws.write('H21', 'Desde', bold)
        ws.write('I21', str(documents.passport_issue_date))
        ws.write('H22', 'Hasta', bold)
        ws.write('I22', str(documents.passport_exp_date))
        ws.write('H23', 'DOT', bold)
        ws.write_boolean('I23', documents.dot)
        ws.write('H24', 'Expediente criminal', bold)
        ws.write_boolean('I24', documents.criminal_record)

        wb.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=Expediente.xlsx"

        return response


    def export_drivers(request,driver_list,status):

        if not Validator.validate_view(request):
            return redirect('/email/0/')

        if len(driver_list) > 0:
            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="drivers.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Drivers')

            row_num = 0

            assigned_id = DriverStatus.objects.filter(assigned_id__in=driver_list,expired=status,user_id = user_id).values_list('assigned_id')

            rows_driver = Driver.objects.filter(assigned_id__in = assigned_id).values_list('assigned_id', 'name', 'middle_name','last_name', 'date_of_birth','country','state','city')



            for row_driver in rows_driver:
                row_num += 1
                columns = [
                'Assigned Id', 'Name', 'Middle Name',
                'Lastname', 'Date of birth', 'Country','State','City'
                ]

                row_num = XlsGenerator.create_headers(columns, ws, row_num)

                row_num = XlsGenerator.create_content(ws,row_num,row_driver,xlwt.XFStyle())

                columns = ['Start Date']
                row_num = XlsGenerator.create_headers(columns, ws, row_num)
                rows_status = DriverStatus.objects.filter(assigned_id=row_driver[0]).filter(user_id=user_id).values_list(
                    'start_date')

                for row_status in rows_status:
                    row_num = XlsGenerator.create_content(ws, row_num,row_status, xlwt.XFStyle())


                columns = [
                    'Country','State','City','Street', 'Zip Code',
                    'Ext', 'Phone Number',
                ]
                row_num = XlsGenerator.create_headers(columns,ws,row_num)
                rows_address = Address.objects.filter(assigned_id = row_driver[0]).filter(user_id=user_id).values_list(
                                                                                                                    'country_addr','state_addr','city_addr','street','zip_code',
                                                                                                                    'ext', 'phone_number')

                for row_address in rows_address:
                    row_num = XlsGenerator.create_content(ws,row_num,row_address,xlwt.XFStyle())

                columns = [
                    'Id', 'RFC', 'CURP', 'License No',
                    'License Issue Date', 'License Exp Date', 'License Type',
                    'Passport No', 'Passport Issue Date', 'Passport Exp Date',
                    'Dot', 'Criminal Record'
                ]

                row_num = XlsGenerator.create_headers(columns,ws,row_num)
                rows_documents = Documents.objects.filter(assigned_id = row_driver[0]).filter(user_id=user_id).values_list(
                                                                                                                        'id', 'rfc', 'curp', 'license_no', 'license_issue_date', 'license_exp_date',
                                                                                                                        'license_type', 'passport_no', 'passport_issue_date', 'passport_exp_date',
                                                                                                                        'dot', 'criminal_record')


                for row_documents in rows_documents:
                    row_num = XlsGenerator.create_content(ws,row_num,row_documents,xlwt.XFStyle())

                columns = ['End Date']
                row_num = XlsGenerator.create_headers(columns, ws, row_num)
                rows_status = DriverStatus.objects.filter(assigned_id=row_driver[0]).filter(
                    user_id=user_id).values_list(
                    'end_date')

                for row_status in rows_status:
                    row_num = XlsGenerator.create_content(ws, row_num, row_status, xlwt.XFStyle())

            wb.save(response)
            return response
        return render(request,'hound-eng/error.html',{'error':'Empty List'})


    def export_drivers_esp(request,driver_list,status):

        if not Validator.validate_view(request):
            return redirect('/email/1/')

        if len(driver_list) > 0:
            user_id = request.session['id']
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="conductores.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Drivers')

            row_num = 0

            assigned_id = DriverStatus.objects.filter(assigned_id__in=driver_list,expired=status,user_id = user_id).values_list('assigned_id')

            rows_driver = Driver.objects.filter(assigned_id__in = assigned_id).values_list('assigned_id', 'name', 'middle_name','last_name', 'date_of_birth','country','state','city')



            for row_driver in rows_driver:
                row_num += 1
                columns = [
                'Id Asignado', 'Nombre', 'Segundo nombre',
                'Apellido', 'Fecha de nacimiento', 'País','Estado','Ciudad'
                ]

                row_num = XlsGenerator.create_headers(columns, ws, row_num)

                row_num = XlsGenerator.create_content(ws,row_num,row_driver,xlwt.XFStyle())

                columns = ['Fecha de inicio']
                row_num = XlsGenerator.create_headers(columns, ws, row_num)
                rows_status = DriverStatus.objects.filter(assigned_id=row_driver[0]).filter(user_id=user_id).values_list(
                    'start_date')

                for row_status in rows_status:
                    row_num = XlsGenerator.create_content(ws, row_num,row_status, xlwt.XFStyle())


                columns = [
                    'País','Estado','Ciudad','Calle', 'Código postal',
                    'Ext', 'Número de teléfono',
                ]
                row_num = XlsGenerator.create_headers(columns,ws,row_num)
                rows_address = Address.objects.filter(assigned_id = row_driver[0]).filter(user_id=user_id).values_list(
                                                                                                                    'country_addr','state_addr','city_addr','street','zip_code',
                                                                                                                    'ext', 'phone_number')

                for row_address in rows_address:
                    row_num = XlsGenerator.create_content(ws,row_num,row_address,xlwt.XFStyle())

                columns = [
                    'Id', 'RFC', 'CURP', 'No. de licencia',
                    'Desde', 'Hasta', 'Tipo de licencia',
                    'No. de pasaporte', 'Desde', 'Hasta',
                    'DOT', 'Expediente criminal'
                ]

                row_num = XlsGenerator.create_headers(columns,ws,row_num)
                rows_documents = Documents.objects.filter(assigned_id = row_driver[0]).filter(user_id=user_id).values_list(
                                                                                                                        'id', 'rfc', 'curp', 'license_no', 'license_issue_date', 'license_exp_date',
                                                                                                                        'license_type', 'passport_no', 'passport_issue_date', 'passport_exp_date',
                                                                                                                        'dot', 'criminal_record')


                for row_documents in rows_documents:
                    row_num = XlsGenerator.create_content(ws,row_num,row_documents,xlwt.XFStyle())

                columns = ['Fecha de expiración']
                row_num = XlsGenerator.create_headers(columns, ws, row_num)
                rows_status = DriverStatus.objects.filter(assigned_id=row_driver[0]).filter(
                    user_id=user_id).values_list(
                    'end_date')

                for row_status in rows_status:
                    row_num = XlsGenerator.create_content(ws, row_num, row_status, xlwt.XFStyle())

            wb.save(response)
            return response
        return render(request,'hound-eng/error.html',{'error':'Lista vacía'})


    @require_POST
    def manager_drivers(request,lenguage):

        email_template = '/email/0/'
        error_option = 'Invalid Action'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Acción invalida'

        if request.method == 'POST':

            if not Validator.validate_view(request):
                return redirect(email_template)

            pk = request.POST.getlist('select')
            action = request.POST.get('action')
            status = request.POST.get('status')
            if action == "1":

                if int(lenguage) == 1:
                    return DriverView.export_drivers_esp(request, pk, status)
                return DriverView.export_drivers(request,pk,status)
            elif action == "2":
                return DriverView.delete_drivers(request,lenguage,pk)
            elif action == "3":
                return DriverView.restore_drivers(request,lenguage,pk)
            else:
                return render(request,'hound-eng/error.html',{'error':error_option})

            return redirect('/drivers/0/')


    @require_POST
    def delete_drivers(request,lenguage,driver_list):

        error_internal = 'Internal Error'
        error_list = 'Empty List'

        if int(lenguage) == 1:
            error_internal = 'Error interno'
            error_list = 'Lista vacía'

        if len(driver_list) > 0:
                drivers = DriverStatus.objects.filter(user_id=request.session['id'],assigned_id__in=driver_list)
                expired = 0
                for driver in drivers:
                    if driver.expired == False:
                        driver.expired = True
                        driver.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        driver.save()


                    elif driver.expired == True:
                        expired = 1
                        driver_obj = Driver.objects.get(user_id=request.session['id'], assigned_id=driver.assigned_id)
                        driver_obj.delete()

                        if Address.objects.filter(user_id=request.session['id']).filter(
                                assigned_id=driver.assigned_id).exists():
                            address = Address.objects.get(user_id=request.session['id'], assigned_id=driver.assigned_id)
                            address.delete()

                        if Documents.objects.filter(user_id=request.session['id']).filter(
                                assigned_id=driver.assigned_id).exists():
                            documents = Documents.objects.get(user_id=request.session['id'],
                                                              assigned_id=driver.assigned_id)
                            documents.delete()

                        if Directory.objects.filter(user_id=request.session['id']).filter(
                                assigned_id=driver.assigned_id).exists():
                            directory = Directory.objects.filter(user_id=request.session['id'],
                                                                 assigned_id=driver.assigned_id)
                            for phone_number in directory:
                                phone_number.delete()

                        if Vacations.objects.filter(user_id=request.session['id']).filter(
                                assigned_id=driver.assigned_id).exists():
                            vacations = Vacations.objects.filter(user_id=request.session['id'],
                                                                 assigned_id=driver.assigned_id)
                            for vacation in vacations:
                                if Date.objects.filter(vacation.vacation_id).exists():
                                    dates = Date.objects.filter(vacation.vacation_id)
                                    for date in dates:
                                        date.delete()
                                vacation.delete()
                        driver.delete()
                    else:
                        return render(request, 'hound-eng/error.html', {'error':error_internal})

                if expired == 0:
                    if int(lenguage) == 1:
                        return redirect('/drivers/1/0/')
                    return redirect('/drivers/0/0/')
                elif expired == 1:
                    if int(lenguage) == 1:
                        return redirect('/archiver_drivers/1/1/')
                    return redirect('/archiver_drivers/0/1/')


        return render(request, 'hound-eng/error.html', {'error': error_list})

    def restore_drivers(request,lenguage,driver_list):

        error_list = 'Empty List'

        if int(lenguage) == 1:
            error_list = 'Lista vacía'

        if len(driver_list) > 0:
                drivers = DriverStatus.objects.filter(user_id=request.session['id'],assigned_id__in=driver_list)
                for driver in drivers:
                    if driver.expired == True:
                        driver.expired = False
                        driver.start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        driver.save()

                if int(lenguage) == 1:
                    return redirect('/archiver_drivers/1/1/')

                return redirect('/archiver_drivers/0/1/')

        return render(request, 'hound-eng/error.html', {'error': error_list})

    def delete_driver(request,lenguage,assigned_id):

        email_template = '/email/0/'
        error_internal = 'Internal Error'
        error_driver = 'Driver does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_internal = 'Error interno'
            error_driver = 'El conductor no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)


        if DriverStatus.objects.filter(user_id = request.session['id']).filter(assigned_id = assigned_id).exists():
            driver = DriverStatus.objects.get(user_id=request.session['id'],assigned_id=assigned_id)
            if driver.expired == False:
                driver.expired = True
                driver.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                driver.save()
                if int(lenguage) == 1:
                    return redirect('/drivers/1/0/')
                return redirect('/drivers/0/0/')
            elif driver.expired == True:
                driver_obj = Driver.objects.get(user_id=request.session['id'], assigned_id=assigned_id)
                driver_obj.delete()

                if Address.objects.filter(user_id=request.session['id']).filter(assigned_id=assigned_id).exists():
                    address = Address.objects.get(user_id=request.session['id'], assigned_id=assigned_id)
                    address.delete()

                if Documents.objects.filter(user_id=request.session['id']).filter(assigned_id=assigned_id).exists():
                    documents = Documents.objects.get(user_id=request.session['id'], assigned_id=assigned_id)
                    documents.delete()

                if Directory.objects.filter(user_id=request.session['id']).filter(assigned_id=assigned_id).exists():
                    directory = Directory.objects.filter(user_id=request.session['id'], assigned_id=assigned_id)
                    for phone_number in directory:
                        phone_number.delete()

                if Vacations.objects.filter(user_id=request.session['id']).filter(assigned_id=assigned_id).exists():
                    vacations = Vacations.objects.filter(user_id=request.session['id'], assigned_id=assigned_id)
                    for vacation in vacations:
                        if Date.objects.filter(vacation.vacation_id).exists():
                            dates = Date.objects.filter(vacation.vacation_id)
                            for date in dates:
                                date.delete()
                        vacation.delete()
                driver.delete()
                if int(lenguage) == 1:
                    return redirect('/archiver_drivers/1/1/')
                return redirect('/archiver_drivers/0/1/')
            else:
                return render(request, 'hound-eng/error.html', {'error':error_internal})
        else:
            return render(request,'hound-eng/error.html',{'error':error_driver})

    def restore_driver(request,lenguage,assigned_id):

        email_template = '/email/0/'
        error_driver = 'Driver does not exists'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_driver = 'El conductor no existe'

        if not Validator.validate_view(request):
            return redirect(email_template)


        if DriverStatus.objects.filter(user_id = request.session['id']).filter(assigned_id = assigned_id).exists():
            driver = DriverStatus.objects.get(user_id=request.session['id'],assigned_id=assigned_id)
            if driver.expired == True:
                driver.expired = False
                driver.start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                driver.save()

                if int(lenguage) == 1:
                    return redirect('/archiver_drivers/1/1/')
                return redirect('/archiver_drivers/0/1/')
        else:
            return render(request,'hound-eng/error.html',{'error':error_driver})

    @require_POST
    def search_driver(request,lenguage,status):

        email_template = '/email/0/'
        error_option = 'Invalid option'

        if int(lenguage) == 1:
            email_template = '/email/1/'
            error_option = 'Opción invalida'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if int(status) == 1:
            template = '/archiver_drivers/0/1/'

            if int(lenguage) == 1:
                template = '/archiver_drivers/1/1/'

        elif int(status) == 0:
            template = '/drivers/0/0/'
            if int(lenguage) == 1:
                template = '/drivers/1/0/'

        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        if request.method == 'POST':

            if int(status) == 1:
                status = True

            elif int(status) == 0:
                status = False

            else:
                return render(request, 'hound-eng/error.html', {'error': error_option})

            user_id = request.session['id']

            assignedIdField = AssignedId(request.POST)
            if assignedIdField.is_valid():



                nameField = Name(request.POST)
                lastNameField = LastName(request.POST)
                idField = Id(request.POST)
                rfcField = RFC(request.POST)
                startDateField = StartDate(request.POST)
                country = Country(request.POST)

                if not idField.is_valid():
                    return render(request, 'hound-eng/error.html', {'error': idField.errors})

                if not startDateField.is_valid():
                    return render(request, 'hound-eng/error.html', {'error': startDateField.errors})

                if not rfcField.is_valid():
                    return render(request, 'hound-eng/error.html', {'error': rfcField.errors})

                assignedId = assignedIdField.cleaned_data['assigned_id']
                name = nameField.save(commit=False)
                lastName = lastNameField.save(commit=False)
                id = idField.save(commit=False)

                rfc = rfcField.save(commit=False)
                startDate = startDateField.save(commit=False)
                country = country.save(commit = False)

                if not startDateField.is_valid():
                    return render(request, 'hound-eng/error.html', {'error':startDateField.errors})


                fields = {'assigned_id':assignedId,'name':name.name.lower(),'last_name':lastName.last_name.lower(),'id':id.id.upper(),'rfc':rfc.rfc.lower(),'start_date':startDate.start_date,'country':country.country.upper()}

                error = DriverView.validate_search_fields(request,fields,user_id)

                if int(lenguage) == 1:
                    error = DriverView.validate_search_fields_esp(request, fields, user_id)


                if error != '':
                    return render(request, 'hound-eng/error.html', {'error': error})

                return DriverView.search_view(request,lenguage,fields,status)
            else:
                return render(request, 'hound-eng/error.html', {'error': assignedIdField.errors})

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

        if status == True:
            template = 'hound-eng/archiver_drivers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/archiver_drivers.html'

        elif status == False:
            template = 'hound-eng/assets_drivers.html'

            if int(lenguage) == 1:
                template = 'hound-esp/assets_drivers.html'

        else:
            return render(request,'hound-eng/error.html',{'error':error_option})

        nameField = Name()
        lastNameField = LastName()
        assignedIdField = AssignedId()
        idField = Id()
        rfcField = RFC()
        startDateField = StartDate()
        country = Country()
        if int(lenguage) == 0:
            table = DriverView.generate_table(fields, request.session['id'],status)

        elif int(lenguage) == 1:
            table = DriverView.generate_table_esp(fields, request.session['id'], status)

        else:
            return render(request, 'hound-eng/error.html', {'error': error_option})

        if table == None:
            return render(request,'hound-eng/error.html',{'error':error_records})
        table.paginate(page=request.GET.get('page', 1), per_page=5)
        return render(request, template, {
            'table': table, 'action': 0, 'nameField': nameField,
            'lastNameField': lastNameField, 'idField': idField,
            'startDateField': startDateField, 'assignedIdField': assignedIdField,
            'rfcField': rfcField,'country':country,'status':status
        })


    def validate_search_fields(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['assigned_id'] != None:

                if int(fields['assigned_id']) < 0:
                    error = 'Assigned Id must be positive'

                if not Validator.validate_integer(fields['assigned_id'],1000000,9999999):
                    error = 'Assigned Id must be 7 digits length'

            if fields['rfc'] != '':
                if len(fields['rfc']) < 10 or len(fields['rfc']) > 20:
                    error = 'RFC must be at least 18 characters length'
            if fields['id'] != '':
                if len(fields['id']) < 8 or len(fields['id']) > 20:
                    error = 'Id must be 8 to 20 digits length'
        return error

    def validate_search_fields_esp(request,fields,user_id):
        error = ''
        if fields != None:
            if fields['assigned_id'] != None:

                if int(fields['assigned_id']) < 0:
                    error = 'Id Asignado debe de ser un numero positivo'

                if not Validator.validate_integer(fields['assigned_id'],1000000,9999999):
                    error = 'Id Asignado debe de tener 7 digitos'

            if fields['rfc'] != '':
                if len(fields['rfc']) < 10 or len(fields['rfc']) > 20:
                    error = 'RFC debe tener de 10 a 20 caracteres'
            if fields['id'] != '':
                if len(fields['id']) < 8 or len(fields['id']) > 20:
                    error = 'Id debe de tener de 8 a 20 caracteres'
        return error

    def generate_table(fields,user_id,status):
        assigned_id = DriverStatus.objects.filter(user_id=user_id).filter(expired = status).values_list('assigned_id')
        table = DriverTable(Driver.objects.filter(assigned_id__in = assigned_id).filter(user_id=user_id))
        if fields != None:
            if fields['assigned_id'] != None:
                if Driver.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).filter(assigned_id__in=assigned_id).exists():
                    table = DriverTable(Driver.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']).filter(assigned_id__in=assigned_id))
                else:
                    table = None

            if fields['name'] != '':
                if Driver.objects.filter(user_id=user_id).filter(name=fields['name']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable(Driver.objects.filter(user_id=user_id).filter(name=fields['name']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['country'] != '':
                if Driver.objects.filter(user_id=user_id).filter(country=fields['country']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable(Driver.objects.filter(user_id=user_id).filter(country=fields['country']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['last_name'] != '':
                if Driver.objects.filter(user_id = user_id).filter(last_name=fields['last_name']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable(Driver.objects.filter(user_id=user_id).filter(last_name=fields['last_name']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['rfc'] != '':
                if Documents.objects.filter(user_id=user_id).filter(rfc=fields['rfc']).exists():
                    documents = Documents.objects.filter(user_id=user_id).filter(rfc=fields['rfc'])
                    if Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in = assigned_id).exists():
                        drivers = Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in = assigned_id)
                        table = DriverTable(drivers)
                    else:
                        table = None
                else:
                    table = None
            if fields['id'] != '':
                if Documents.objects.filter(user_id = user_id).filter(id=fields['id']).exists():
                    documents = Documents.objects.filter(user_id=user_id).filter(id=fields['id'])
                    if Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in=assigned_id).exists():
                        drivers = Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in=assigned_id)
                        table = DriverTable(drivers)
                    else:
                        table = None

                else:
                    table = None
            if fields['start_date'] != None:
                if DriverStatus.objects.filter(user_id = user_id).filter(start_date = fields['start_date']).filter(assigned_id__in = assigned_id).exists():
                    status = DriverStatus.objects.filter(user_id=user_id).filter(start_date=fields['start_date']).filter(assigned_id__in = assigned_id).values_list('assigned_id')
                    table = DriverTable(Driver.objects.filter(user_id=user_id).filter(assigned_id__in=status))
                else:
                    table = None
            return table
        return table


    def generate_table_esp(fields,user_id,status):
        assigned_id = DriverStatus.objects.filter(user_id=user_id).filter(expired = status).values_list('assigned_id')
        table = DriverTable_esp(Driver.objects.filter(assigned_id__in = assigned_id).filter(user_id=user_id))
        if fields != None:
            if fields['assigned_id'] != None:
                if Driver.objects.filter(user_id = user_id).filter(assigned_id=fields['assigned_id']).filter(assigned_id__in=assigned_id).exists():
                    table = DriverTable_esp(Driver.objects.filter(user_id=user_id).filter(assigned_id=fields['assigned_id']).filter(assigned_id__in=assigned_id))
                else:
                    table = None

            if fields['name'] != '':
                if Driver.objects.filter(user_id=user_id).filter(name=fields['name']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable_esp(Driver.objects.filter(user_id=user_id).filter(name=fields['name']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['country'] != '':
                if Driver.objects.filter(user_id=user_id).filter(country=fields['country']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable_esp(Driver.objects.filter(user_id=user_id).filter(country=fields['country']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['last_name'] != '':
                if Driver.objects.filter(user_id = user_id).filter(last_name=fields['last_name']).filter(assigned_id__in = assigned_id).exists():
                    table = DriverTable_esp(Driver.objects.filter(user_id=user_id).filter(last_name=fields['last_name']).filter(assigned_id__in = assigned_id))
                else:
                    table = None
            if fields['rfc'] != '':
                if Documents.objects.filter(user_id=user_id).filter(rfc=fields['rfc']).exists():
                    documents = Documents.objects.filter(user_id=user_id).filter(rfc=fields['rfc'])
                    if Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in = assigned_id).exists():
                        drivers = Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in = assigned_id)
                        table = DriverTable_esp(drivers)
                    else:
                        table = None
                else:
                    table = None
            if fields['id'] != '':
                if Documents.objects.filter(user_id = user_id).filter(id=fields['id']).exists():
                    documents = Documents.objects.filter(user_id=user_id).filter(id=fields['id'])
                    if Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in=assigned_id).exists():
                        drivers = Driver.objects.filter(assigned_id__in=documents).filter(assigned_id__in=assigned_id)
                        table = DriverTable_esp(drivers)
                    else:
                        table = None

                else:
                    table = None
            if fields['start_date'] != None:
                if DriverStatus.objects.filter(user_id = user_id).filter(start_date = fields['start_date']).filter(assigned_id__in = assigned_id).exists():
                    status = DriverStatus.objects.filter(user_id=user_id).filter(start_date=fields['start_date']).filter(assigned_id__in = assigned_id).values_list('assigned_id')
                    table = DriverTable_esp(Driver.objects.filter(user_id=user_id).filter(assigned_id__in=status))
                else:
                    table = None
            return table
        return table


    def load_tmp_profile(user_id, assigned_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (user_id, 'driver', int(assigned_id)))
        if cursor.rowcount <= 0:
            cursor.execute("select profile_img from hound_driver where user_id_id='%s' and assigned_id='%d';" % (user_id, int(assigned_id)))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                try:
                    cursor.execute("insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (user_id, 'driver', int(assigned_id), data[0]))
                    database.commit()
                except:
                    database.rollback()
                src = data[0]
            else:
                try:
                    cursor.execute("insert into hound_profile (user_id, type,gen_id,path) values('%s','%s','%d','%s');" % (user_id, 'driver', int(assigned_id), 'hound/images/default.jpg'))
                    database.commit()
                except:
                    database.rollback()
        else:
            data = cursor.fetchone()
            src = data[0]
        database.close()
        return src

    def load_tmp_prints(user_id, assigned_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        src = 'hound/images/default.jpg'

        cursor.execute("select path from hound_prints where user_id='%s' and gen_id='%d';" % (user_id, int(assigned_id)))
        if cursor.rowcount <= 0:
            cursor.execute("select prints_img from hound_documents where user_id_id='%s' and assigned_id='%d';" % (user_id, int(assigned_id)))
            if cursor.rowcount > 0:
                data = cursor.fetchone()
                try:
                    cursor.execute("insert into hound_prints (user_id,gen_id,path) values('%s','%d','%s');" % (user_id, int(assigned_id), data[0]))
                    database.commit()
                except:
                    database.rollback()
                src = data[0]
            else:
                try:
                    cursor.execute("insert into hound_prints (user_id,gen_id,path) values('%s','%d','%s');" % (user_id,  int(assigned_id), 'hound/images/default.jpg'))
                    database.commit()
                except:
                    database.rollback()
        else:
            data = cursor.fetchone()
            src = data[0]
        database.close()
        return src

    @require_POST
    def upload_driver_profile(request,lenguage,assigned_id, state):

        email_template = '/email/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':

            if Profile.objects.filter(user_id=request.session['id']).filter(type='driver').filter(gen_id=assigned_id):
                profile = Profile.objects.get(user_id=request.session['id'], type='driver', gen_id=assigned_id)
                formProfile = ProfileForm(request.POST or None, request.FILES, instance=profile)
            else:
                formProfile = ProfileForm(request.POST, request.FILES)

            if formProfile.is_valid():
                file = request.FILES['profile']
                error = Validator.validate_image(file)
                if error != '':
                    return render(request, 'hound-eng/error.html', {'error': error})

                if ' ' in file.name:
                    return render(request, 'hound-eng/error.html', {'error': 'Image file name must not have white spaces'})

                profile = formProfile.save(commit=False)
                fs = FileSystemStorage()
                url = request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/' + file.name
                if not fs.exists(request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/' + file.name):
                    filename = fs.save(request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/' + file.name, file)
                    url = fs.url(filename)

                Uploader.create_directory('/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/')
                Uploader.clear_directory('/' + request.session['id'] + '/drivers/' + str(assigned_id)+'/profile')
                Uploader.move_file('/system/hound/images/' + url,'/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/' + file.name)
                profile.type = 'driver'
                profile.gen_id = int(assigned_id)
                profile.path = 'hound/data/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/profile/' + file.name
                profile.user_id = request.session['id']
                profile.save()
                Uploader.clear_tmp_dir('/system/hound/images/')
            if state == "0":
                if int(lenguage) == 0:
                    return redirect('/add_driver/0/')
                elif int(lenguage) == 1:
                    return redirect('/add_driver/1/')
            elif state == "1":
                if int(lenguage) == 0:
                    return redirect('/edit_driver/0/' + str(assigned_id) + '/')
                elif int(lenguage) == 1:
                    return redirect('/edit_driver/1/' + str(assigned_id) + '/')
            else:
                return render(request, 'hound-eng/error.html', {'error': 'Internal error, Invalid state'})


    @require_POST
    def upload_driver_prints(request,lenguage,assigned_id, state):

        email_template = '/email/0/'

        if int(lenguage) == 1:
            email_template = '/email/1/'

        if not Validator.validate_view(request):
            return redirect(email_template)

        if request.method == 'POST':

            if Prints.objects.filter(user_id=request.session['id']).filter(gen_id=assigned_id):
                prints = Prints.objects.get(user_id=request.session['id'], gen_id=assigned_id)
                formPrints = PrintsForm(request.POST or None, request.FILES, instance=prints)
            else:
                formPrints = PrintsForm(request.POST, request.FILES)

            if formPrints.is_valid():
                file = request.FILES['prints']
                error = Validator.validate_image(file)
                if error != '':
                    return render(request, 'hound-eng/error.html', {'error': error})

                if ' ' in file.name:
                    return render(request, 'hound-eng/error.html', {'error': 'Image file name must not have white spaces'})

                prints = formPrints.save(commit=False)
                fs = FileSystemStorage()
                url = request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/' + file.name
                if not fs.exists(request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/' + file.name):
                    filename = fs.save(request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/' + file.name, file)
                    url = fs.url(filename)

                Uploader.create_directory('/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/')
                Uploader.clear_directory('/' + request.session['id'] + '/drivers/' + str(assigned_id)+'/prints')
                Uploader.move_file('/system/hound/images/' + url,'/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/' + file.name)
                prints.gen_id = int(assigned_id)
                prints.path = 'hound/data/' + request.session['id'] + '/drivers/' + str(assigned_id) + '/prints/' + file.name
                prints.user_id = request.session['id']
                prints.save()
                Uploader.clear_tmp_dir('/system/hound/images/')
            if state == "0":
                if int(lenguage) == 0:
                    return redirect('/add_driver/0/')
                elif int(lenguage) == 1:
                    return redirect('/add_driver/1/')
            elif state == "1":
                if int(lenguage) == 0:
                    return redirect('/edit_driver/0/' + str(assigned_id) + '/')
                if int(lenguage) == 1:
                    return redirect('/edit_driver/1/' + str(assigned_id) + '/')
            else:
                return render(request, 'hound-eng/error.html', {'error': 'Internal error, Invalid state'})


    def save_profile(user_id, assigned_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        cursor.execute("select path from hound_profile where user_id='%s' and type='%s' and gen_id='%d';" % (user_id, 'driver', int(assigned_id)))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            try:
                cursor.execute("select profile_img from hound_driver where user_id_id='%s' and assigned_id='%d';" % (user_id, int(assigned_id)))
                if cursor.rowcount > 0:
                    cursor.execute("update hound_driver set profile_img='%s' where user_id_id='%s' and assigned_id='%d';" % (data[0], user_id, int(assigned_id)))
                    database.commit()
                else:
                    cursor.execute("insert into hound_driver (user_id_id,assigned_id,profile_img) values('%s','%d','%s');" % (user_id, int(assigned_id), data[0]))
                    database.commit()
            except:
                database.rollback()
        database.close()

    def save_prints(user_id, assigned_id):
        database = pymysql.connect('localhost', 'hound_admin', 'N1nj@ k1tty', 'hound_db')
        cursor = database.cursor()
        cursor.execute("select path from hound_prints where user_id='%s' and gen_id='%d';" % (user_id, int(assigned_id)))
        if cursor.rowcount > 0:
            data = cursor.fetchone()
            try:
                cursor.execute("select prints_img from hound_documents where user_id_id='%s' and assigned_id='%d';" % (user_id, int(assigned_id)))
                if cursor.rowcount > 0:
                    cursor.execute("update hound_documents set prints_img='%s' where user_id_id='%s' and assigned_id='%d';" % (data[0], user_id, int(assigned_id)))
                    database.commit()
                else:
                    cursor.execute("insert into hound_documents (user_id_id,assigned_id,profile_img) values('%s','%d','%s');" % (user_id, int(assigned_id), data[0]))
                    database.commit()
            except:
                database.rollback()
        database.close()





