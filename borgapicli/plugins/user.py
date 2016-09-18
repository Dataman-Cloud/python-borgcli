import argparse
from borgapicli.plugin_helpers import BORGClientPlugin
import borgclient


class UserPlugin(BORGClientPlugin):

    def register(self):

        # command: me
        self.set_command('user', help='get user information')
        user_info_parser = self.add_action('info', help='show current login user information')
        user_info_parser.set_defaults(func=self._get_my_info)

    def _get_my_info(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_user()
