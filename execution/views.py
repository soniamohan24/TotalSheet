from django.shortcuts import render
from .models import ExecutionGroup, ExecutionSubGroup
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def fetch_subgroups(request):
    group_id = request.GET.get("group_id")
    group = get_object_or_404(ExecutionGroup, id=group_id)
    # Use distinct() if needed to avoid duplicates in query results
    subgroups = group.sub_groups.all().distinct()

    subgroups_data = [{"id": sg.id, "name": sg.name} for sg in subgroups]
    print(subgroups_data)
    return JsonResponse(subgroups_data, safe=False)
