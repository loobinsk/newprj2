from django.views.generic import View
from django.shortcuts import get_object_or_404
from ..models import Region, User
from django.shortcuts import redirect


class ChooseRegionView(View):
    # Set region to user and redirect user to the same page but with new region

    def post(self, *args, **kwargs):
        # get region from modal
        region = self.request.POST.get('region')
        # find such region in DB
        # assign this region to user
        origin_url = self.request.POST.get('origin_url', '/')
        region_obj = get_object_or_404(Region, region_name=region)
        self.request.session['region'] = region_obj.id
        if self.request.user.id:
            user_obj = User.objects.get(id=self.request.user.id)
            user_obj.region = region_obj
            user_obj.save()

        return redirect(to=origin_url)
