from ajaxutils.decorators import ajax
from school.models import School, Department, Speciality

@ajax(login_required=True, require_GET=True)
def get_all_schools(request):
    return {
        'schools': [school.getDataDict() for school in School.objects.all()]
    }

@ajax(login_required=True, require_GET=True)
def get_all_departments(request):
    return {
        'departments': [depart.getDataDict() for depart in
            Department.objects.filter(school__name__exact=request.GET['school'])]
    }

@ajax(login_required=True, require_GET=True)
def get_all_specialities(request):
    return {
        'specialities': [spec.getDataDict() for spec in
            Speciality.objects.filter(department__name__exact=request.GET['department'])]
    }
