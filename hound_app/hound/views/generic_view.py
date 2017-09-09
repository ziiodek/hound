from django.shortcuts import render

class GenericView:

    def notFound(request):
        return render(request,'hound-eng/not_found.html')


