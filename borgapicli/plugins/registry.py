import argparse
from borgapicli.plugin_helpers import BORGClientPlugin
import borgclient

class RegistryPlugin(BORGClientPlugin):

    def register(self):

        # command: registry
        self.set_command('registry', help='registry related commands')

        # sub-command: create
        create_registry_parser = self.add_action('create', help='create third party registry')
        create_registry_parser.add_argument("--username", dest="username", type=str, required=True)
        create_registry_parser.add_argument("--password", dest="password", type=str, required=True)
        create_registry_parser.add_argument("--address", dest="addr", type=str, required=True)
        create_registry_parser.add_argument("--name", dest="name", type=str)
        create_registry_parser.set_defaults(func=self._create_registry)

        # sub-command: get
        get_registry_parser = self.add_action('get', help='get specific third party registry')
        get_registry_parser.add_argument("--registry_id", dest="registry_id", type=str, required=True)
        get_registry_parser.set_defaults(func=self._get_registry)


        # sub-command: all
        all_registry_parser = self.add_action('all', help='get all third party registries')
        all_registry_parser.set_defaults(func=self._get_registries)

        # sub-command: update
        update_registry_parser = self.add_action('update', help='update specific registry')
        update_registry_parser.add_argument("--registry_id", dest="registry_id", type=str, required=True)
        update_registry_parser.add_argument("--username", dest="username", type=str, required=True)
        update_registry_parser.add_argument("--address", dest="addr", type=str, required=True)
        update_registry_parser.add_argument("--password", dest="password", type=str)
        update_registry_parser.add_argument("--name", dest="name", type=str)
        update_registry_parser.set_defaults(func=self._update_registry)

        # sub-command: delete
        delete_registry_parser = self.add_action('delete', help='delete specific registry')
        delete_registry_parser.add_argument("--registry_id", dest="registry_id", type=str, required=True)
        delete_registry_parser.set_defaults(func=self._delete_registry)

        # sub-command: get_uri
        get_uri_parser = self.add_action('get_uri', help="get specific registry's certification file uri")
        get_uri_parser.add_argument("--registry_id", dest="registry_id", type=str, required=True)
        get_uri_parser.set_defaults(func=self._get_uri)

    def _create_registry(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        data = {
                "userName": args.username,
                "password": args.password,
                "addr": args.addr,
        }
        if args.name:
            data.update({"name": args.name})
        return borg_client.create_registry(**data)

    def _get_registry(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        registry_id = args.registry_id
        return borg_client.get_registry(registry_id)

    def _get_registries(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        return borg_client.get_registries()

    def _update_registry(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        registry_id = args.registry_id
        data = {
                "userName": args.username,
                "addr": args.addr
        }
        if args.name:
            data.update({"name": args.name})
        if args.password:
            data.update({"password": args.password})
        return borg_client.update_registry(registry_id, **data)

    def _delete_registry(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        registry_id = args.registry_id
        return borg_client.delete_registry(registry_id)

    def _get_uri(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], token=configs['token'])
        registry_id = args.registry_id
        return borg_client.get_uri(registry_id)
