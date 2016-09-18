import argparse, json
import borgclient
from borgapicli.plugin_helpers import BORGClientPlugin
ACTIONS = ['stop', 'start']


class AppPlugin(BORGClientPlugin):

    def register(self):
        self.set_command('app', help='borgsphere app api command list')

        # sub-command: get_apps
        get_apps_parser = self.add_action('get_apps', help='list all apps' )
        get_apps_parser.set_defaults(func=self._get_apps)

        # sub-command: create_apps
        create_apps_parser = self.add_action('create', help='create app from specified file')
        create_apps_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        create_apps_parser.set_defaults(func=self._create_apps)

        # sub-command: get_app
        get_app_parser = self.add_action('get', help='list specified app information when given the app id')
        get_app_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_app_parser.set_defaults(func=self._get_cluster_app)

        # sub-command: get_app_stats
        get_app_stats_parser = self.add_action('get_app_stats', help="list a specific app's status")
        get_app_stats_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_app_stats_parser.set_defaults(func=self._get_app_stats)

        # sub-command: update_app
        update_app_parser = self.add_action('update_app', help='update app configuration')
        update_app_parser.add_argument('--app_id', dest='app_id', type=int, required=True)
        update_app_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        update_app_parser.set_defaults(func=self._update_app)

        # sub-command: delete_app
        delete_app_parser = self.add_action('delete', help='Delete specified app')
        delete_app_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        delete_app_parser.set_defaults(func=self._delete_app)

        # sub-command: restart_app
        restart_app_parser = self.add_action('restart', help='Restart specified app')
        restart_app_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        restart_app_parser.set_defaults(func=self._restart_app)

        # sub-command: get_app_versions
        get_app_versions_parser = self.add_action('get_app_version', help='list all history versions for a specific app')
        get_app_versions_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_app_versions_parser.set_defaults(func=self._get_app_versions)

        # sub-command: get_app_version
        get_app_version_parser = self.add_action('get_app_version', help='list all history versions for a specific app')
        get_app_version_parser.add_argument('--app_id', dest="app_id", type=int, required=True)
        get_app_version_parser.add_argument('--version_id', dest="version_id", type=int, required=True)
        get_app_version_parser.set_defaults(func=self._get_app_version)

        # sub-command: scale
        scale_parser = self.add_action('scale', help='scale tasks for apps')
        scale_parser.add_argument('--scale', dest="if_scale", type=bool, required=True)
        scale_parser.set_defaults(func=self._scale_app)

        # sub-command: get_queue
        get_queue_parser = self.add_action('get_queue', help='list all queues')
        get_queue_parser.set_defaults(func=self._get_queue)

        # sub-command: get_app_tasks
        get_app_tasks_parser = self.add_action('get_app_tasks', help='list all tasks for a specific app')
        get_app_tasks_parser.add_argument('--app_id', dest='app_id', type=str, required=True)
        get_app_tasks_parser.set_defaults(func=self._get_app_tasks)

    def _get_apps(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_apps()

    def _create_apps(self, args):
        configs = self._get_config()
        data = json.loads(args.file.read())
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.create_apps(**data)

    def _get_app(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_app(app_id)

    def _delete_app(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.delete_app(app_id)

    def _restart_app(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.restart_app(app_id)

    def _get_app_stats(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_app_stats()

    def _update_app(self, args):
        configs = self._get_config()
        app_id = args.app_id
        data = json.loads(args.file.read())
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.update_app(app_id, **data)

    def _get_app_tasks(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_app_tasks(app_id)

    def _get_app_versions(self, args):
        configs = self._get_config()
        app_id = args.app_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_app_versions(app_id)

    def _get_app_version(self, args):
        configs = self._get_config()
        app_id = args.app_id
        version_id = args.version_id
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_app_versions(app_id, version_id)

    #def _scale_app(self, args):
    #    configs = self._get_config()
    #    if_scale = args.if_scale
    #    borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
    #    return borg_client.scale_app(if_scale, **data)

    def _get_quque(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_queue()
