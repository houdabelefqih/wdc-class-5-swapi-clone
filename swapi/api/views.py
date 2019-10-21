import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS
from api.serializers import serialize_people_as_json


def single_people(request):
    return JsonResponse(SINGLE_PEOPLE_OBJECT)


def list_people(request):
    return JsonResponse(PEOPLE_OBJECTS, safe=False)


@csrf_exempt
def people_list_view(request):
    """
    People `list` actions:

    Based on the request method, perform the following actions:

        * GET: Return the list of all `People` objects in the database.

        * POST: Create a new `People` object using the submitted JSON payload.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        people_data = [serialize_people_as_json(people) for people in People.objects.all()]

        return JsonResponse(people_data, safe= False, status=200)

    elif request.method == 'POST':
        if not request.body:
            return JsonResponse({"success": False, "msg": "Empty payload"}, status=400)

        else:
            try:
                payload = json.loads(request.body)

            except ValueError:
                return JsonResponse({"success": False, "msg": "Provide a valid JSON payload"}, status=400)

            try:
                newly_created_people = People.objects.create(
                    name=payload['name'],
                    height=payload['height'],
                    mass=payload['mass'],
                    hair_color=payload['hair_color']
                )

            except (ValueError, KeyError):
                return JsonResponse({"success": False, "msg": "Provided payload is not valid"}, status=400)

            return JsonResponse(serialize_people_as_json(newly_created_people), status=201)



    else:
        return JsonResponse({"success": False, "msg": "Invalid HTTP method"}, status=400)


@csrf_exempt
def people_detail_view(request, people_id):
    """
    People `detail` actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `People` object with given `people_id`.

        * PUT/PATCH: Updates the `People` object either partially (PATCH)
          or completely (PUT) using the submitted JSON payload.

        * DELETE: Deletes `People` object with given `people_id`.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    pass
