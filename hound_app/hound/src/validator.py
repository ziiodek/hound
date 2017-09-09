from ..models.user import User

class Validator:

    def validate_integer(id,lower,upper):
        if id < lower or id > upper :
            return False
        return True

    def validate_string(string,lenght):
        if len(string) < lenght or len(string) > lenght:
            return False
        return True

    def validate_view(request):
        if request.session.get('id') == None:
            return False
        return True

    def validate_image(file):
        types = ['jpg','jpeg','png','bmp']
        file_type = file.content_type.split('/')[1]
        print (file_type)


        if len(file.name.split('.')) == 1:
            return 'Invalid imagen file'
        if file_type in types:
            if file._size > 2621440:
                return 'Image file too large'
        else:
            return 'Invalid imagen file'
        return ''

    def get_user_status(email):
        if User.objects.filter(email = email).exists():
            status = User.objects.get(email=email).active
            return status
        return None

    def get_confirmation(email):
        if User.objects.filter(email = email).exists():
            confirm = User.objects.get(email=email).confirmed
            return confirm
        return None