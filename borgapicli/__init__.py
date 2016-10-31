import argparse, getpass, json

from borgapicli.plugins.app import AppPlugin
from borgapicli.plugins.auth import AuthPlugin
from borgapicli.plugins.user import UserPlugin
from borgapicli.plugins.info import BaseInfoPlugin
from borgapicli.plugins.group import GroupPlugin
from borgapicli.plugins.registry import RegistryPlugin


class ClientRunner(object):
    """
    This class is for registering all plugin commands
    """

    def setup(self):
        self.parser = argparse.ArgumentParser(prog='borgapi_cli', description='borgsphere api client tool')
        self.parser.add_argument('--version', '-v', action='version', version='borgsphere api client 1.0')

        subparsers = self.parser.add_subparsers(metavar='COMMAND')

        # ping and version
        self.base_plugin = BaseInfoPlugin(self)
        self.base_plugin._before_register(subparsers)
        self.base_plugin.register()

        # authenticate first
        self.auth_plugin = AuthPlugin(self)
        self.auth_plugin._before_register(subparsers)
        self.auth_plugin.register()

        # load omega app api command line
        app_plugin = AppPlugin(self)
        app_plugin._before_register(subparsers)
        app_plugin.register()

        # load user api command line
        user_plugin = UserPlugin(self)
        user_plugin._before_register(subparsers)
        user_plugin.register()

        # load group api command line
        group_plugin = GroupPlugin(self)
        group_plugin._before_register(subparsers)
        group_plugin.register()

        # load registry api command line
        registry_plugin = RegistryPlugin(self)
        registry_plugin._before_register(subparsers)
        registry_plugin.register()

    def run(self, args=None):
        self.args = self.parser.parse_args(args=args)
        if len(vars(self.args)) > 0:
            data = self.args.func(self.args)
            print(json.dumps(data))
        else:
            print(json.dumps({"cliErr":"please specify one argument, or add -h to check help"}))
