from ..models.user import User

class Validator:

    def check_pattern(string):
        pattern = set('~`@#$%^&*()_-=+[]{}\/,."<>?|')
        if any((c in pattern) for c in string):
            return True

        for c in string:
            if c == "'":
                return True

        return False

    def check_pattern_phone_number(phone_number):
        pattern = set('~`@#$%^&*()_=[]{}\/,."<>?|')
        if any((c in pattern) for c in phone_number):
            return True

        for c in phone_number:
            if c == "'":
                return True

        return False

    def check_patter_street(street):
        pattern = set('~`@$%^&*()_=+[]{}\/"<>?|')
        if any((c in pattern) for c in street):
            return True

        for c in street:
            if c == "'":
                return True

        return False

    def check_pattern_ext(ext):
        pattern = set('~`@#$%^&*()_-=[]{}\/,."<>?|')
        if any((c in pattern) for c in ext):
            return True

        for c in ext:
            if c == "'":
                return True

        return False



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