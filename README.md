# python-borgcli

## check service
```
$python borgapi_cli.py health_check --host http://192.168.1.155:9999
$python borgapi_cli.py get_borg_version --host http://192.168.1.155:9999
```

## Usage

1. To use this client tool, please login first with following command:
```
$python borgapi_cli.py login --host --email --password
```
arguments host, email and password must be specified.
password is prompted for credential when command is entered.

example:
```
$python borgapi_cli.py login --host="http://192.168.1.155:9999" --email admin@dataman-inc.com --password
```

2. After login, user can get user info through command:
```
$python borgapi_cli.py user info
```

3. Meanwhile, user can logout through command:
```
$python borgapi_cli.py logout
```

## Commands
Following are all commands borgapi_cli supports currently:

### basic
```
$python borgapi_cli.py -h
```
```
usage: borgapi_cli [-h] [--version] COMMAND ...

borgsphere api client tool

positional arguments:
  COMMAND
    health_check    check if service is healthy, host is required
    get_borg_version
                    get borgsphere version info, host is required
    login           login with user email and password, api server is required
    logout          delete login user's token, return code 0 if success
    app             borgsphere app api command list
    user            get user information

optional arguments:
  -h, --help        show this help message and exit
  --version, -v     show program's version number and exit
```

### login

```
$python borgapi_cli.py login
```
```
usage: borgapi_cli login [-h] --host HOST --email EMAIL --password

optional arguments:
  -h, --help     show this help message and exit

authentication:
  --host HOST
  --email EMAIL
  --password
```
### user

```
$python borgapi_cli.py user -h
```
```
usage: borgapi_cli user [-h] ACTION ...

positional arguments:
  ACTION
    info      show current login user information

optional arguments:
  -h, --help  show this help message and exit
```

### app

```
$python borgapi_cli.py app -h
```
```
usage: borgapi_cli app [-h] ACTION ...

positional arguments:
  ACTION
    all              list all apps
    create           create app from specified file
    create_multi_apps
                     create multiple apps from a directory containing app json
                     files
    get              list specified app information when given the app id
    update           update app configuration
    delete           delete specified app
    delete_multi_apps
                     delete multiple apps
    restart          restart specified app
    get_app_versions
                     list all history versions for a specific app
    get_app_version  get specific history version for a specific app
    delete_tasks     scale tasks for apps
    get_queue        list all queues
    get_app_tasks    list all tasks for a specific app

optional arguments:
  -h, --help         show this help message and exit
```
#### Examples:
```
$python borgapi_cli.py app all
$python borgapi_cli.py app create -f json_examples/app_create_templ.json
$python borgapi_cli.py app create_multi_apps -d json_examples/
$python borgapi_cli.py app get --app_id wordpress
$python borgapi_cli.py app update --app_id wordpress -f json_examples/app_update_templ.json
$python borgapi_cli.py app restart --app_id wordpress
$python borgapi_cli.py app get_app_versions --app_id wordpress
$python borgapi_cli.py app get_app_version --app_id wordpress --version_id "2016-09-19T05:54:53.981Z"
$python borgapi_cli.py app get_queue
$python borgapi_cli.py app get_app_tasks --app_id wordpress
$python borgapi_cli.py app delete_tasks --task_ids simple-template.05c3a9cc-7edd-11e6-aafb-26097dc1dffd
$python borgapi_cli.py app delete_multi_apps --app_ids 123 123 haha
```

