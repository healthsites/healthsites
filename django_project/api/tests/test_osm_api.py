from __future__ import unicode_literals
import datetime
import mock
import os
import sys

from osmapi import ElementDeletedApiError

from api.osm_api_client import OsmApiWrapper
from core.settings.base import DEV_OSM_API_URL
from core.settings.secret import (
    SOCIAL_AUTH_OPENSTREETMAP_KEY, SOCIAL_AUTH_OPENSTREETMAP_SECRET)

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)

OAUTH_TOKEN = ''  # use authorised oauth token
OAUTH_TOKEN_SECRET = ''  # use authorised oauth token secret


class TestOsmApi(unittest.TestCase):
    def setUp(self):
        self.oauth_token = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        self.api_base = DEV_OSM_API_URL
        self.app_id = 'healthsites.testcase'
        self.api = OsmApiWrapper(
            client_key=SOCIAL_AUTH_OPENSTREETMAP_KEY,
            client_secret=SOCIAL_AUTH_OPENSTREETMAP_SECRET,
            oauth_token=self.oauth_token,
            oauth_token_secret=self.oauth_token_secret,
            api=self.api_base,
            appid=self.app_id
        )
        self.maxDiff = None
        print(self._testMethodName)
        print(self.api)

    def _session_mock(self, auth=False, filenames=None, status=200,
                      reason=None):
        if auth:
            self.api._oauth_token = self.oauth_token
            self.api._oauth_token_secret = self.oauth_token_secret

        response_mock = mock.Mock()
        response_mock.status_code = status
        return_values = self._return_values(filenames)
        print(filenames)
        print(return_values)
        assert len(return_values) < 2
        if return_values:
            response_mock.content = return_values[0]

        session_mock = mock.Mock()
        session_mock.request = mock.Mock(return_value=response_mock)

        self.api._get_http_session = mock.Mock(return_value=session_mock)
        self.api._session = session_mock

        self.api._sleep = mock.Mock()

    def _return_values(self, filenames):
        if filenames is None:
            filenames = [self._testMethodName + '.xml']

        return_values = []
        for filename in filenames:
            path = os.path.join(
                __location__,
                'fixtures',
                filename
            )
            try:
                with open(path) as file:
                    return_values.append(file.read())
            except Exception:
                pass
        return return_values

    def teardown(self):
        pass

    def test_constructor(self):
        self.assertTrue(isinstance(self.api, OsmApiWrapper))

    def test_NodeGet(self):
        self._session_mock()

        result = self.api.NodeGet(123)

        args, kwargs = self.api._session.request.call_args
        self.assertEquals(args[0], 'GET')
        self.assertEquals(args[1], self.api_base + '/api/0.6/node/123')

        self.assertEquals(result, {
            'id': 123,
            'changeset': 15293,
            'uid': 605,
            'timestamp': datetime.datetime(2012, 4, 18, 11, 14, 26),
            'lat': 51.8753146,
            'lon': -1.4857118,
            'visible': True,
            'version': 8,
            'user': 'freundchen',
            'tag': {
                'amenity': 'school',
                'foo': 'bar',
                'name': 'Berolina & Schule'
            },
        })

    def test_NodeCreate(self):
        self._session_mock(auth=True)

        # setup mock
        self.api.ChangesetCreate = mock.Mock(
            return_value=1111
        )
        self.api._CurrentChangesetId = 1111

        test_node = {
            'lat': 47.287,
            'lon': 8.765,
            'tag': {
                'amenity': 'place_of_worship',
                'religion': 'pastafarian'
            }
        }

        cs = self.api.ChangesetCreate({
            'comment': 'This is a test dataset'
        })
        self.assertEquals(cs, 1111)
        result = self.api.NodeCreate(test_node)

        args, kwargs = self.api._session.request.call_args
        self.assertEquals(args[0], 'PUT')
        self.assertEquals(args[1], self.api_base + '/api/0.6/node/create')

        self.assertEquals(result['id'], 9876)
        self.assertEquals(result['lat'], test_node['lat'])
        self.assertEquals(result['lon'], test_node['lon'])
        self.assertEquals(result['tag'], test_node['tag'])

    @unittest.skipIf(
        condition=not (OAUTH_TOKEN and OAUTH_TOKEN_SECRET),
        reason='requires valid oauth token')
    def test_crud_osm_node(self):
        test_node = {
            'lat': 47.287,
            'lon': 8.765,
            'tag': {
                'amenity': 'place_of_worship',
                'religion': 'pastafarian'
            }
        }

        # Creating osm node using osm api client.
        result = self.api.create_node(test_node)
        node_id = result.get('id')
        node_version = result.get('version')
        self.assertIsNotNone(node_id)
        self.assertEqual(1, node_version)

        # Read osm node using osm api client and check whether newly created
        # osm node is exist in the osm instance.
        result = self.api.NodeGet(node_id)
        self.assertEqual(node_id, result.get('id'))

        # Update/modify an osm node data using osm api client.
        test_node['id'] = node_id
        test_node['tag']['name'] = 'pastafarian church'
        result = self.api.update_node(test_node)
        node_name = result.get('tag', {}).get('name')
        self.assertEqual(node_id, result.get('id'))
        self.assertEqual(node_name, 'pastafarian church')

        # Read osm node using osm api client and check whether newly updated
        # osm node is exist. Latest version number should be increased.
        result = self.api.NodeGet(node_id)
        node_version = result.get('version')
        self.assertEqual(node_id, result.get('id'))
        self.assertEqual(2, node_version)

        # Delete the latest version of an osm node using osm api client.
        test_node['version'] = 2
        _ = self.api.delete_node(test_node)

        # Read osm node using osm api client and check if it raises
        # ElementDeletedApiError since the osm node has been deleted.
        self.assertRaises(
            ElementDeletedApiError, self.api.delete_node, test_node)
