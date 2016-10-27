import argparse
from borgapicli.plugin_helpers import BORGClientPlugin
import borgclient


class UserPlugin(BORGClientPlugin):

    def register(self):

        # command: user
        self.set_command('user', help='get user information')

        # sub-command: info
        user_info_parser = self.add_action('info', help='show current login user information')
        user_info_parser.set_defaults(func=self._get_my_info)

        # sub-command: switch_group
        switch_group_parser = self.add_action('switch_group', help="change user's current group")
        switch_group_parser.add_argument("--group_id", dest="group_id", type=int, required=True)
        switch_group_parser.set_defaults(func=self._switch_group)

    def _get_my_info(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        return borg_client.get_user()

    def _switch_group(self, args):
        configs = self._get_config()
        data = {"groupId": args.group_id}
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        return borg_client.switch_group(**data)
