class BaseInfoMixin(object):
    """base check apis"""

    def health_check(self):

        resp = self.http.get("/health")

        return self.process_data(resp)

    def get_borg_version(self):
        """get borgsphere version info"""

        resp = self.http.get("/version")

        return self.process_data(resp)
