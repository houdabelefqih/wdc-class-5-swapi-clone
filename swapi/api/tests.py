import json
from copy import deepcopy
from freezegun import freeze_time

from django.test import TestCase

from api.models import People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS


class PeopleEndpointTestCase(TestCase):

    @freeze_time('2018-04-14T10:15:30+00:00')
    def setUp(self):
        self.people1 = People.objects.create(
            name='Luke Skywalker',
            height=172,
            mass=77,
            hair_color='blond')
        self.people2 = People.objects.create(
            name='C-3PO',
            height=167,
            mass=75,
            hair_color=None)
        self.people3 = People.objects.create(
            name='R2-D2',
            height=96,
            mass=32,
            hair_color=None)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_detail(self):
        response = self.client.get('/api/people/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected = {
            'name': 'Luke Skywalker',
            'height': 172,
            'mass': 77,
            'hair_color': 'blond',
            'created': '2018-04-14T10:15:30+00:00',
        }
        self.assertEqual(response.json(), expected)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_list(self):
        response = self.client.get('/api/people/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(len(response.json()), 3)
        expected = [
            {'created': '2018-04-14T10:15:30+00:00',
             'hair_color': 'blond',
             'height': 172,
             'mass': 77,
             'name': 'Luke Skywalker'},
            {'created': '2018-04-14T10:15:30+00:00',
             'hair_color': None,
             'height': 167,
             'mass': 75,
             'name': 'C-3PO'},
            {'created': '2018-04-14T10:15:30+00:00',
             'hair_color': None,
             'height': 96,
             'mass': 32,
             'name': 'R2-D2'}
        ]
        self.assertEqual(response.json(), expected)

    @freeze_time('2018-04-14T10:15:30+00:00')
    def test_create(self):
        self.assertEqual(People.objects.count(), 3)
        payload = {
            'name': 'New people',
            'height': 96,
            'mass': 32,
            'hair_color': 'black',
        }
        json_payload = json.dumps(payload)

        response = self.client.post(
            '/api/people/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected = {
            'name': 'New people',
            'height': 96,
            'mass': 32,
            'hair_color': 'black',
            'created': '2018-04-14T10:15:30+00:00',
        }
        self.assertEqual(response.json(), expected)
        self.assertEqual(People.objects.count(), 4)

    def test_create_invalid_payload(self):
        self.assertEqual(People.objects.count(), 3)
        payload = {
            'name': 'New people',
            'height': 'this-is-invalid',  # invalid type
            'mass': 32,
            'hair_color': 'black',
        }
        json_payload = json.dumps(payload)

        response = self.client.post(
            '/api/people/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected = {
            "success": False,
            "msg": "Provided payload is not valid"
        }
        self.assertEqual(response.json(), expected)

    def test_partial_update(self):
        payload = {"name": "New name"}
        json_payload = json.dumps(payload)

        response = self.client.patch(
            '/api/people/1/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['name'], 'New name')
        self.assertEqual(People.objects.get(id=1).name, 'New name')

    def test_full_update(self):
        payload = {
            'name': 'New name',
            'height': self.people1.height,
            'mass': self.people1.mass,
            'hair_color': self.people1.hair_color,
        }
        json_payload = json.dumps(payload)

        response = self.client.put(
            '/api/people/1/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json()['name'], 'New name')
        self.assertEqual(People.objects.get(id=1).name, 'New name')

    def test_full_update_missing_fields(self):
        payload = {
            'name': 'New name',
            'height': self.people1.height,
        }
        json_payload = json.dumps(payload)

        response = self.client.put(
            '/api/people/1/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(
            response.json(),
            {'msg': 'Missing field in full update', 'success': False})

    def test_full_update_invalid_field_value(self):
        payload = {
            'name': 'New name',
            'height': 'must-be-an-integer',  # will fail
            'mass': self.people1.mass,
            'hair_color': self.people1.hair_color,
        }
        json_payload = json.dumps(payload)

        response = self.client.put(
            '/api/people/1/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(
            response.json(),
            {'msg': 'Provided payload is not valid', 'success': False})

    def test_delete(self):
        self.assertEqual(People.objects.count(), 3)
        response = self.client.delete('/api/people/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(People.objects.count(), 2)

    def test_invalid_json(self):
        json_payload = '{"not a valid JSON"}'
        response = self.client.post(
            '/api/people/', data=json_payload, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(),
                         {'msg': 'Provide a valid JSON payload', 'success': False})

    def test_detail_invalid_method(self):
        response = self.client.post(
            '/api/people/1/', data='{}', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(),
                         {'msg': 'Invalid HTTP method', 'success': False})

    def test_list_invalid_method(self):
        response = self.client.delete('/api/people/', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(),
                         {'msg': 'Invalid HTTP method', 'success': False})