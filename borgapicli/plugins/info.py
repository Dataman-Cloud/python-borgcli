import argparse, getpass
from borgapicli.plugin_helpers import BORGClientPlugin
import borgclient


class BaseInfoPlugin(BORGClientPlugin):

    def register(self):

        # command: health-check
        parser_ping = self.parser.add_parser('health_check', help="check if service is healthy, host is required")
        parser_ping.add_argument("--host", dest="host", type=str, required=True)
        parser_ping.set_defaults(func=self._health_check)

        # command: get-borg-version
        parser_borg_version = self.parser.add_parser('get_borg_version', help="get borgsphere version info, host is required")
        parser_borg_version.add_argument("--host", dest="host", type=str, required=True)
        parser_borg_version.set_defaults(func=self._get_borg_version)

    def _health_check(self, args):
        host = args.host
        borg_client = borgclient.BorgClient(host)
        return borg_client.health_check()

    def _get_borg_version(self, args):
        host = args.host
        borg_client = borgclient.BorgClient(host)
        return borg_client.get_borg_version()

