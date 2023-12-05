from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import tests


def homepage(request):
    return render(request, 'homepage.html')


# decorator used for removing csrf protection from POST method for server end only
@csrf_exempt
def upload_file(request):
    """handle file from user"""
    if request.method == "POST":
        filename = request.headers.get("File-Name")
        file_size = int(request.headers.get("File-Size"))
        path = tests.save_text_file(filename, file_size, request.body)
        if path == "exist":
            return JsonResponse(data={"message": "already uploaded"}, status=200)
        elif path:
            data = tests.process_csv_file(path)
            if data:
                return JsonResponse(data={"message": "uploaded and processed", "filedata": data}, status=200)
            return JsonResponse(data={"message": "error while processing"}, status=200)
        return JsonResponse(data={"message": "not uploaded"}, status=201)
