import argparse, json, os
from os import listdir
from os.path import isfile, join

import borgclient
from borgapicli.plugin_helpers import BORGClientPlugin

class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("ReadableDir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("ReadableDir:{0} is not a readable dir".format(prospective_dir))


class AppPlugin(BORGClientPlugin):

    def register(self):
        self.set_command('app', help='borgsphere app api command list')

        # sub-command: get_apps
        get_apps_parser = self.add_action('all', help='list all apps' )
        get_apps_parser.set_defaults(func=self._get_apps)

        # sub-command: create_app
        create_apps_parser = self.add_action('create', help='create app from specified file')
        create_apps_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        create_apps_parser.set_defaults(func=self._create_app)

        # sub-command: create_multi_apps
        create_multi_apps_parser = self.add_action('create_multi_apps', help='create multiple apps from a directory containing app json files')
        create_multi_apps_parser.add_argument('-d', '--dir', help='directory containing app json files', action=ReadableDir, required=True)
        create_multi_apps_parser.set_defaults(func=self._create_multi_apps)

        # sub-command: get_app
        get_app_parser = self.add_action('get', help='list specified app information when given the app id')
        get_app_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        get_app_parser.set_defaults(func=self._get_app)

        # sub-command: get_app_stats
        #get_app_stats_parser = self.add_action('get_app_stats', help="list a specific app's status")
        #get_app_stats_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        #get_app_stats_parser.set_defaults(func=self._get_app_stats)

        # sub-command: update_app
        update_app_parser = self.add_action('update', help='update app configuration')
        update_app_parser.add_argument('--app_id', dest='app_id', type=str, required=True)
        update_app_parser.add_argument('-f', '--file', help='bundle json containing new app info', type=argparse.FileType('r'), required=True)
        update_app_parser.set_defaults(func=self._update_app)

        # sub-command: delete_app
        delete_app_parser = self.add_action('delete', help='delete specified app')
        delete_app_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        delete_app_parser.set_defaults(func=self._delete_app)

        # sub-command: restart_app
        restart_app_parser = self.add_action('restart', help='restart specified app')
        restart_app_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        restart_app_parser.set_defaults(func=self._restart_app)

        # sub-command: get_app_versions
        get_app_versions_parser = self.add_action('get_app_versions', help='list all history versions for a specific app')
        get_app_versions_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        get_app_versions_parser.set_defaults(func=self._get_app_versions)

        # sub-command: get_app_version
        get_app_version_parser = self.add_action('get_app_version', help='get specific history version for a specific app')
        get_app_version_parser.add_argument('--app_id', dest="app_id", type=str, required=True)
        get_app_version_parser.add_argument('--version_id', dest="version_id", type=str, required=True)
        get_app_version_parser.set_defaults(func=self._get_app_version)

        # sub-command: delete_tasks
        #scale_parser = self.add_action('delete_tasks', help='scale tasks for apps')
        #scale_parser.add_argument('--scale', dest="if_scale", type=bool, required=False)
        #scale_parser.add_argument('--app_ids', dest="app_ids", nargs='+', required=True)
        #scale_parser.set_defaults(func=self._delete_tasks)

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

    def _create_app(self, args):
        configs = self._get_config()
        try:
            data = json.loads(args.file.read())
        except ValueError as e:
            raise e

        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.create_app(**data)

    def _create_multi_apps(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        app_dir = args.dir
        files = [f for f in listdir(app_dir) if isfile(join(app_dir, f))]
        created_apps = []
        for file in files:
            app_file = join(app_dir, file)
            try:
                with open(app_file, 'r') as f:
                    data = json.loads(f.read())
                    result = borg_client.create_app(**data)
                    created_apps.append({
                        "source_file": file,
                        "result": result
                    })
            except ValueError as e:
                return "Fail to load file " + file + ", please ensure the data is in json format:\n" + str(e)
        return created_apps

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
        return borg_client.get_app_stats(app_id)

    def _update_app(self, args):
        configs = self._get_config()
        app_id = args.app_id
        try:
            data = json.loads(args.file.read())
        except ValueError as e:
            raise e

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
        return borg_client.get_app_version(app_id, version_id)

    def _delete_tasks(self, args):
        configs = self._get_config()
        if_scale = False
        if args.if_scale:
            if_scale = args.if_scale
        app_ids = args.app_ids
        #TODO(zliu): data is not valid json
        data = {"ids": app_ids}
        print("data:", data)
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.delete_tasks(if_scale, **data)

    def _get_queue(self, args):
        configs = self._get_config()
        borg_client = borgclient.BorgClient(configs['host'], None, None, token=configs['token'])
        return borg_client.get_queue()
