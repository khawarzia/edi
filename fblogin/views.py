from django.shortcuts import render_to_response

def server_error(request, *args, **kwargs):
    response = render_to_response(
        '500.html'
        )
    response.status_code = 500
    return response