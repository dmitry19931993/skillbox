from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        "a" : a,
        "b": b,
        "result" : result,
    }
    return render(request, "requestdataapp/request-query-params.html", context= context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request, "requestdataapp/user-bio-form.html", context= context)

def handle_file_upload (request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        if myfile.size > 2 ** 20:
            print('Error, file is so big')
            return render(request, "requestdataapp/error_file.html")
        else:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('Saved file', filename)
    return render(request, "requestdataapp/file-upload.html")