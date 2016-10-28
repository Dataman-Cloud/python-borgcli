# python-borgcli

## build image:
```
$sudo docker build -t IMAGE_NAME .
```

## setup container and use cli:
```
$sudo docker run -it IMAGE_NAME bash
```

## check service
```
$python3 borgapi_cli.py health_check --host http://192.168.1.155:9999
$python3 borgapi_cli.py get_borg_version --host http://192.168.1.155:9999
```

## Usage

1. To use this client tool, please login first with following command:
```
$python3 borgapi_cli.py login --host --username --password
```
arguments host, username and password must be specified.
password is prompted for credential when command is entered.

example:
```
$python3 borgapi_cli.py login --host="http://192.168.1.155:9999" --username admin@dataman-inc.com --password
```

2. After login, user can get user info through command:
```
$python3 borgapi_cli.py user info
```

3. Meanwhile, user can logout through command:
```
$python3 borgapi_cli.py logout
```

## Commands
Following are all commands borgapi_cli supports currently:

### basic
```
$python3 borgapi_cli.py -h
```
```
usage: borgapi_cli [-h] [--version] COMMAND ...

borgsphere api client tool

positional arguments:
  COMMAND
    health_check    check if service is healthy, host is required
    get_borg_version
                    get borgsphere version info, host is required
    login           login with username and password, api server is required
    logout          delete login user's token, return code 0 if success
    app             borgsphere app api command list
    user            get user information
    group           get group information
    registry        registry related commands

optional arguments:
  -h, --help        show this help message and exit
  --version, -v     show program's version number and exit
```

### login

```
$python3 borgapi_cli.py login
```
```
usage: borgapi_cli login [-h] --host HOST --username USERNAME --password

optional arguments:
  -h, --help     show this help message and exit

authentication:
  --host HOST
  --username USERNAME
  --password
```
### user

```
$python3 borgapi_cli.py user -h
```
```
usage: borgapi_cli user [-h] ACTION ...

positional arguments:
  ACTION
    info        show current login user information
    switch_group
                change user's current group

optional arguments:
  -h, --help    show this help message and exit
```
### group
```
$python3 borgapi_cli.py group -h
```
```
usage: borgapi_cli group [-h] ACTION ...

positional arguments:
  ACTION
    all       get all group information
    get       get specified group

optional arguments:
  -h, --help  show this help message and exit
```

### app

```
$python3 borgapi_cli.py app -h
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
$python3 borgapi_cli.py app all
$python3 borgapi_cli.py app create -f json_examples/app_create_templ.json
$python3 borgapi_cli.py app create_multi_apps -d json_examples/
$python3 borgapi_cli.py app get --app_id wordpress
$python3 borgapi_cli.py app update --app_id wordpress -f json_examples/app_update_templ.json
$python3 borgapi_cli.py app restart --app_id wordpress
$python3 borgapi_cli.py app get_app_versions --app_id wordpress
$python3 borgapi_cli.py app get_app_version --app_id wordpress --version_id "2016-09-19T05:54:53.981Z"
$python3 borgapi_cli.py app get_queue
$python3 borgapi_cli.py app get_app_tasks --app_id wordpress
$python3 borgapi_cli.py app delete_tasks --task_ids simple-template.05c3a9cc-7edd-11e6-aafb-26097dc1dffd
$python3 borgapi_cli.py app delete_multi_apps --app_ids 123 123 haha
```

### registry
```
$python3 borgapi_cli.py registry -h
```
```
usage: borgapi_cli registry [-h] ACTION ...

positional arguments:
  ACTION
    create    create third party registry
    get       get specific third party registry
    all       get all third party registries
    update    update specific registry
    delete    delete specific registry
    get_uri   get specific registry's certification file uri

optional arguments:
  -h, --help  show this help message and exit
```
#### Examples:
```
$python3 borgapi_cli.py registry create --username admin --password dataman1234 --address calalog.shurenyun.com
$python3 borgapi_cli.py registry all
$python3 borgapi_cli.py registry get --registry_id 37
$python3 borgapi_cli.py registry update --registry_id 37 --name test --username admin@dataman-inc.com --address index.shurenyun.com
$python3 borgapi_cli.py registry get_uri --registry_id 36
$python3 borgapi_cli.py registry delete --registry_id 36
```
