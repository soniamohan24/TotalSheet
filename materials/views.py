from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import MaterialGroup, SubGroup, WorkGroup


# Create your views here.
def fetch_subgroups(request):
    group_id = request.GET.get("group_id")
    group = get_object_or_404(MaterialGroup, id=group_id)
    # Use distinct() if needed to avoid duplicates in query results
    subgroups = group.sub_groups.all().distinct()

    subgroups_data = [{"id": sg.id, "name": sg.name} for sg in subgroups]
    print(subgroups_data)
    return JsonResponse(subgroups_data, safe=False)


def get_subgroups(request, group_id):
    print('hrloo')
    try:
        # Get the selected workgroup by ID
        workgroup = WorkGroup.objects.get(id=group_id)

        # Get related subgroups
        subgroups = workgroup.codesgroup_sub_groups.all()

        # Prepare the data to be returned as JSON
        subgroups_data = [{'id': sg.id, 'name': sg.name} for sg in subgroups]

        return JsonResponse(subgroups_data, safe=False)
    except WorkGroup.DoesNotExist:
        return JsonResponse([], safe=False)