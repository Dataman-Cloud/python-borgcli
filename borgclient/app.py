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

import copy
import os, json

from jsonschema import SchemaError, ValidationError, validate
from borgclient.utils import url_maker

class AppMixin(object):
    """App associated APIs"""

    def get_apps(self, **kwargs):
        """List all apps for speicified cluster"""

        resp = self.http.get("/apps")

        return self.process_data(resp)

    def create_app(self, **kwargs):
        """Create app

        :param data: Dictionary to send in the body of the request.

        """
        resp = self.http.post("/apps", data=kwargs)

        return self.process_data(resp)

    def get_app(self, app_id):
        """List specified app information under specified cluster"""

        resp = self.http.get(url_maker("/apps", app_id))

        return self.process_data(resp)

    def get_app_stats(self, app_id):
        """List a specific app's stats"""

        resp = self.http.get(url_maker("/apps", app_id, "stats" ))

        return self.process_data(resp)

    def update_app(self, app_id, **kwargs):
        """Updated app configuration"""

        resp = self.http.put(url_maker("/apps", app_id), data=kwargs)

        return self.process_data(resp)

    def delete_app(self, app_id):
        """Delete specified app"""

        resp = self.http.delete(url_maker("/apps", app_id))
        return self.process_data(resp)

    def restart_app(self, app_id):
        """Delete specified app"""

        resp = self.http.post(url_maker("/apps", app_id, "restart"))
        return self.process_data(resp)

    def get_app_tasks(self, app_id):
        """List a specific app's tasks"""

        resp = self.http.get(url_maker("/apps", app_id, "tasks"))

        return self.process_data(resp)

    def get_app_versions(self, app_id):
        """List all history versions for app"""

        resp = self.http.get(url_maker("/apps", app_id, "versions"))

        return self.process_data(resp)

    def get_app_version(self, app_id, version_id):
        """List all history versions for app"""

        resp = self.http.get(url_maker("/apps", app_id, "versions", version_id))

        return self.process_data(resp)

    def delete_tasks(self, if_scale, **kwargs):
        resp = self.http.post("/tasks/delete?scale=" + str(if_scale).lower(), data=kwargs)
        return self.process_data(resp)

    def get_queue(self):
        resp = self.http.get("/queue")
        return self.process_data(resp)
