from borgclient.utils import url_maker

class RegistryMixin(object):
    """Registry related apis"""

    def create_registry(self, **kwargs):
        """Create third party registry"""

        resp = self.http.post("/external_registries", data=kwargs)
        return self.process_data(resp)

    def get_registry(self, registry_id):
        """Get specific third party registry"""

        resp = self.http.get(url_maker("/external_registries", registry_id))
        return self.process_data(resp)

    def get_registries(self):
        """Get all registries"""

        resp = self.http.get("/external_registries")
        return self.process_data(resp)

    def update_registry(self, registry_id, **kwargs):
        """Update specific registry"""

        resp = self.http.put(url_maker("/external_registries", registry_id), data=kwargs)
        return self.process_data(resp)

    def delete_registry(self, registry_id):
        """Delete specific registry"""

        resp = self.http.delete(url_maker("/external_registries", registry_id))
        return self.process_data(resp)

    def get_uri(self, registry_id):
        """Get sepcific registry's certification file uri"""

        resp = self.http.get(url_maker("/uri", registry_id))
        return self.process_data(resp)

