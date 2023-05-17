from django.http import JsonResponse


def error_400(request, exception):
    message = "could not connect to db"
    return JsonResponse(data={'code': 400, 'errors': message}, status=400)


def error_404(request, exception):
    message = "could not connect to db"
    return JsonResponse(data={'code': 400, 'errors': message}, status=400)


def error_500(exception):
    message = "Server Internal Error"
    return JsonResponse(data={'code': 500, 'errors': message}, status=500)
