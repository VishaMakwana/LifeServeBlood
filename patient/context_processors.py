from .models import Patient

def patient_data(request):

    if request.user.is_authenticated:

        patient = Patient.objects.filter(user=request.user).first()

        return {

            "patient": patient

        }

    return {}