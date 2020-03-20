import docker
import os
import sys

import getpass

from noteworthy.notectl.plugins import NoteworthyPlugin

dir_path = os.path.dirname(os.path.realpath(__file__))


class WireGuardController(NoteworthyPlugin):

    PLUGIN_NAME = 'noteworthy-wireguard'

    def __init__(self):
        super().__init__()
        self.docker = docker.from_env()


    def build(self, no_cache=False, **kwargs):
        print('Building WireGuard container.')
        print('This may take a few minutes.')
        dockerfile_path=os.path.join(dir_path, 'deploy/')
        #TODO debug print(dockerfile_path)
        #TODO write image build to log directory to help with debugging
        image = self.docker.images.build(path=dockerfile_path, tag='noteworthy-wireguard:latest',
        nocache=no_cache)
        print('Done.')
        print()
    
    def start_hub(self, **kwargs):
        hub_pass = getpass.getpass('Set hub password: ')
        hub_pass_confirm = getpass.getpass('Confirm hub password: ')
        if hub_pass != hub_pass_confirm:
            print('Passwords did not match! Please try again.')
            sys.exit(1)
        # TODO make sure we meet default Linux password policy
        # TODO Allow user to select password or pubkey based auth
        self.docker.containers.run('noteworthy-wireguard:latest',
        tty=True,
        stdin_open=True,
        environment=[f'HUB_PASSWORD={hub_pass}'],
        name="wg-easy-hub",
        auto_remove=True,
        ports={'22/tcp':None},
        volumes=['/opt/noteworthy/noteworth-wireguard/hub:/opt/noteworthy/noteworthy-wireguard/hub'],
        detach=True)
        print('Hub started. It will run for 5 minutes then shutdown.')

    def stop_hub(self, **kwargs):
        self.docker.containers.get('wg-easy-hub').stop()


    def help(self, **kwargs):
        print('''Usage: notectl wireguard <command>
    Available commands:
        build     ::: Build the WireGuard container
        start_hub ::: Start the wg-easy hub (stops automatically after 5 minutes)
        stop_hub  ::: Stop the wg-easy hub
 ''')

    @classmethod
    def setup_argparse(cls, arg_parser):
        super().setup_argparse(arg_parser)
        arg_parser.add_argument('--no-cache', action="store_true", help="discard container\
 build cache when building WireGuard container.")


Controller = WireGuardController