from django.shortcuts import render

def server_error(request, *args, **kwargs):
    response = render(
        None,
        '500.html'
        )
    response.status_code = 500
    return response
