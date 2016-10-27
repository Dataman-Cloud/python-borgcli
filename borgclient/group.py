from borgclient.utils import url_maker

class GroupMixin(object):
    """Group related apis"""

    def get_all_groups(self):
        """List all groups"""

        resp = self.http.get("/groups")
        return self.process_data(resp)

    def get_group(self, group_id):
        """Get specified group"""

        resp = self.http.get(url_maker("/groups", group_id))
        return self.process_data(resp)
