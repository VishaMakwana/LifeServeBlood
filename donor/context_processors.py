from .models import Donor

def donor_data(request):

    donor = None

    if request.user.is_authenticated:

        try:
            donor = Donor.objects.get(user=request.user)
        except Donor.DoesNotExist:
            donor = None

    return {
        "donor": donor
    }