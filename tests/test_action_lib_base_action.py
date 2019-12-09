#!/usr/bin/env python
# Copyright 2019 Encore Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from st2tests.base import BaseActionTestCase
from lib.base_action import SharepointBaseAction
from st2common.runners.base_action import Action
# Using this to run tests. Otherwise get an error for no run method.
from sites_list import SitesList


class SharePointBaseActionTestCase(BaseActionTestCase):
    __test__ = True
    action_cls = SitesList

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, SharepointBaseAction)
        self.assertIsInstance(action, Action)

    @mock.patch('lib.base_action.SharepointBaseAction.rest_request')
    def test_get_doc_libs(self, mock_request):
        action = self.get_action_instance({})

        test_base_url = 'https://test.com/api'
        test_auth = 'user'

        # This endpoint is hard coded in base_action.py
        endpoint_uri = '/_api/web/lists?$filter=BaseTemplate eq ' \
                       '101&$select=Title,Id,DocumentTemplateUrl'

        expected_result = 'doc_lib'

        rest_result = {
            'd': {
                'results': expected_result
            }
        }

        mock_request.return_value = mock.MagicMock()
        mock_request.return_value.json.return_value = rest_result

        result = action.get_doc_libs(test_base_url, test_auth)

        self.assertEqual(result, expected_result)
        mock_request.assert_called_with(test_base_url + endpoint_uri, test_auth)

    @mock.patch('lib.base_action.requests.request')
    def test_rest_request(self, mock_request):
        action = self.get_action_instance({})

        test_headers = {
            'accept': 'application/json;odata=verbose',
            'content-type': 'application/json;odata=verbose',
            'odata': 'verbose',
            'X-RequestForceAuthentication': 'true'
        }

        test_endpoint = 'https://test.com/api/endpoint'
        test_auth = 'user'
        test_payload = {'data': 'test'}
        test_method = 'POST'
        test_verify = False

        expected_result = 'response'

        mock_request.return_value = expected_result

        result = action.rest_request(test_endpoint, test_auth, test_method,
                                     test_payload, test_verify)

        self.assertEqual(result, expected_result)
        mock_request.assert_called_with(test_method, test_endpoint,
                                        auth=test_auth, data=test_payload,
                                        headers=test_headers, verify=test_verify)
