from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_take_courses(request):
    pass
