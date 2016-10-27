# Copyright (c) 2016 Dataman Cloud
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging


from borgclient.client import HTTPClient
from borgclient.app import AppMixin
from borgclient.user import UserMixin
from borgclient.group import GroupMixin
from borgclient.auth import AuthMixin
from borgclient.info import BaseInfoMixin

from borgclient.exceptions import BorgException
from requests.models import Response

_DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)8s [%(name)s] %(message)s"
_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


LOG = logging.getLogger(__name__)

_handler = logging.FileHandler("/var/log/borg-client.log")
_handler.setFormatter(
    logging.Formatter(fmt=_DEFAULT_LOG_FORMAT,
                      datefmt=_DEFAULT_LOG_DATE_FORMAT))

LOG.addHandler(_handler)
LOG.setLevel(logging.INFO)


class BorgClient(AppMixin, UserMixin, AuthMixin, BaseInfoMixin, GroupMixin):
    """
    Client for user to use Borgsphere.
    """

    def __init__(self, server_url, token=None):

        self.server_url = server_url

        self.http = HTTPClient(server_url, token=token)

        super(BorgClient, self).__init__()

    @staticmethod
    def process_data(resp):
        """Processing data response from Borgsphere API."""
        if isinstance(resp, Response):
            try:
                LOG.info(resp.json)
                return resp.json()
            except ValueError:
                LOG.info(resp.json)
                return resp.status_code
        elif isinstance(resp, dict):
            LOG.info(resp)
            return resp
