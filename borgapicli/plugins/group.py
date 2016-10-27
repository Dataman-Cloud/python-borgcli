import argparse
from borgapicli.plugin_helpers import BORGClientPlugin
import borgclient

class GroupPlugin(BORGClientPlugin):
    def register(self):

        # command: group
        self.set_command('group', help='get group information')

        # sub-command: all
        group_all_parser = self.add_action('all', help='get all group information')
        group_all_parser.set_defaults(func=self._get_all_groups)

        # sub-command: get
        get_group_parser = self.add_action("get", help='get specified group')
        get_group_parser.add_argument('--group_id', dest="group_id", type=str, required=True)
        get_group_parser.set_defaults(func=self._get_group)

    def _get_all_groups(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        return borg_client.get_all_groups()

    def _get_group(self, args):
        configs = self._get_config()
        group_id = args.group_id
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        return borg_client.get_group(group_id)
