import argparse
import os
import shutil
import sys
from pathlib import Path
from clicz import cli_method

import docker
import dockerpty
from jinja2 import Template

from noteworthy.notectl.plugins import NoteworthyPlugin


class LauncherController(NoteworthyPlugin):
    '''lightweight service orchestration
    '''

    PLUGIN_NAME = 'launcher'
    USER_CLI = True

    PACKAGE_CACHE = '/var/noteworthy/cache/packages'

    def __init__(self):
        super().__init__(__file__)
        self.args = None
        self.docker = docker.from_env()
        self.hub_hostname = os.environ.get('NOTEWORTHY_HUB', 'noteworthy.im:8000')

    # TODO move this code to a lib; its duplicated here and in riot-web plugin
    def _generate_file_from_template(self, tmpl_path, target, configs):
        with open(tmpl_path, 'r') as f:
            tmpl = Template(f.read())
        rendered = tmpl.render(configs)
        with open(target, 'w') as f:
            f.write(rendered)

    def old_install(self, archive_path: str = None, **kwargs):
        # we use env here to figure out which Dockerfile we should use
        # when building an apps' container; in PROD we want to use the base
        # decentralabs/noteworthy:latest container that the user has already downloaded
        # in dev we want to use decentralabs/noteworthy:DEV that we build locally
        # with make .docker
        # TODO figure out if version pinning is needed here
        profile = kwargs.get('profile') or os.environ['NOTEWORTHY_PROFILE']
        app_env = {
            'NOTEWORTHY_DOMAIN': os.environ['NOTEWORTHY_DOMAIN'],
            'NOTEWORTHY_PROFILE': profile}
        dashed_domain = os.environ['NOTEWORTHY_DOMAIN'].replace('.', '-')
        volumes = []
        if archive_path or self.args.archive:
            if not archive_path:
                archive_path = self.args.archive
            app, version = os.path.basename(archive_path).split('-')
            version = version.replace('.tar.gz', '')
            app_dir = os.path.join(self.PACKAGE_CACHE, f'{app}/{version}')
            Path(self.PACKAGE_CACHE).mkdir(parents=True, exist_ok=True)
            shutil.unpack_archive(archive_path, self.PACKAGE_CACHE)
            shutil.copyfile(os.path.join(self.deploy_dir, 'install.sh'), os.path.join(app_dir, 'install.sh'))
            shutil.copyfile(os.path.join(self.deploy_dir, f'Dockerfile'), os.path.join(app_dir, 'Dockerfile'))
            self._build_container(app_dir, app, version)
            app_name = f'{dashed_domain}-{app}'
            app_container_name = f"noteworthy-{app_name}-{profile}"
            profile_volume = self._create_profile_volume(app_name, profile)
            volumes.append(f'{profile_volume.name}:/opt/noteworthy/profiles')
            self.docker.containers.run(f'noteworthy-{app}:{version}',
            tty=True,
            cap_add=['NET_ADMIN'],
            network='noteworthy',
            stdin_open=True,
            name=app_container_name,
            #auto_remove=True,
            volumes=volumes,
            detach=True,
            environment=app_env,
            restart_policy={"Name": "always"})
            # setup app's nginx config
            from noteworthy.nginx import NginxController
            nc = NginxController()
            try:
                nc.set_http_proxy_pass(app, os.environ['NOTEWORTHY_DOMAIN'], app_container_name,
                    os.path.join(self.PACKAGE_CACHE,
                        f'{app}/{version}/{app}/noteworthy/{app}/deploy/nginx.conf'))
            except:
                print(f'No nginx config found for app {app}')

        else:
            raise NotImplementedError(
                'Installing from repository not supported yet.')
        print('Done.')

    @cli_method
    def launch_hub(self, hub_host: str, profile: str = 'default'):
        '''deploy a Noteworthy hub
        ---
        Args:
            hub_host: fqdn or ip to return to hub clients
            profile: profile to associate with hub
        '''
        volumes = []
        ports = {}
        app_env = {
                'NOTEWORTHY_HUB': hub_host,
                'NOTEWORTHY_PROFILE': profile
        }
        volumes.append('/var/run/docker.sock:/var/run/docker.sock')
        volumes.append('/usr/local/bin/docker:/usr/local/bin/docker')
        app = 'launcher'
        app_name = app + '-hub'
        ports={
                '80/tcp' : 80,
                '443/tcp': 443,
                '8000/tcp': 8000,
                }
        app_env['NOTEWORTHY_ROLE'] = 'hub'

        # create and add profiles volume
        profile_volume = self._create_profile_volume(app_name, profile)
        volumes.append(f'{profile_volume.name}:/opt/noteworthy/profiles')

        release_tag = self._load_release_tag()
        # deploy launcher / launcher-hub
        self.docker.containers.run(f"decentralabs/noteworthy:{app_env['NOTEWORTHY_ROLE']}-{release_tag}",
        entrypoint='notectl launcher start',
        tty=True,
        cap_add=['NET_ADMIN'],
        network='noteworthy',
        stdin_open=True,
        name=f"noteworthy-{app_name}-{profile}",
        volumes=volumes,
        ports=ports,
        detach=True,
        environment=app_env,
        restart_policy={"Name": "always"})

    def launch_launcher_taproot(self, domain: str, hub_host: str,
                                    auth_code: str, profile: str):
        volumes = []
        ports = {}
        app_env = {
                'NOTEWORTHY_HUB': hub_host,
                'NOTEWORTHY_PROFILE': profile
        }
        volumes.append('/var/run/docker.sock:/var/run/docker.sock')
        volumes.append('/usr/local/bin/docker:/usr/local/bin/docker')
        app = 'launcher'
        dash_domain = domain.replace('.', '-')
        app_name = f'{dash_domain}-{app}'
        app_env['NOTEWORTHY_DOMAIN'] = domain
        app_env['NOTEWORTHY_ROLE'] = 'taproot'
        app_env['NOTEWORTHY_AUTH_CODE'] = auth_code

        # create and add profiles volume
        profile_volume = self._create_profile_volume(app_name, profile)
        volumes.append(f'{profile_volume.name}:/opt/noteworthy/profiles')

        release_tag = self._load_release_tag()
        # deploy launcher / launcher-hub
        self.docker.containers.run(f"decentralabs/noteworthy:{app_env['NOTEWORTHY_ROLE']}-{release_tag}",
        entrypoint='notectl launcher start',
        tty=True,
        cap_add=['NET_ADMIN'],
        network='noteworthy',
        stdin_open=True,
        name=f"noteworthy-{app_name}-{profile}",
        volumes=volumes,
        ports=ports,
        detach=True,
        environment=app_env,
        restart_policy={"Name": "always"})

    def _build_container(self, app_dir, app, version):
        # read release tag from /opt/noteworthy/release
        with open('/opt/noteworthy/release', 'r') as tag_file:
            release_tag = tag_file.read().strip()
        self.docker.images.build(
            path=app_dir, tag=f'noteworthy-{app}:{version}', nocache=True, buildargs={'RELEASE_TAG': release_tag})

    def _create_profile_volume(self, app, profile_name):
        profile_volume_name = f'noteworthy-{app}-{profile_name}-vol'
        volume = self.docker.volumes.create(name=profile_volume_name)
        return volume

    def _load_release_tag(self):
        with open('/opt/noteworthy/release', 'r') as tag_file:
            return tag_file.read().strip()

    @cli_method
    def start(self):
        '''start launcher, Noteworthy's service orchestration layer
        '''
        self.start_dependencies()

        if os.environ['NOTEWORTHY_ROLE'] == 'taproot':
            if self.is_first_run:
                self.create_config_dir()
                # write out .well-known/matrix/server so matrix federation works
                well_know_target = '/var/www/html/.well-known/matrix/'
                Path(well_know_target).mkdir(parents=True, exist_ok=True)
                self._generate_file_from_template(os.path.join(self.deploy_dir, 'server'),
                    os.path.join(well_know_target, 'server'),
                    {'domain': os.environ['NOTEWORTHY_DOMAIN']})

        print('noteworthy finished booting!')
        # TODO tail log file
        os.system('tail -f /dev/null')

    @cli_method
    def create_user(self, profile):
        '''create a matrix user
        ---
        Args:
            profile: profile to create matrix account
        '''
        # use docker proxy for invoking shell commands
        # via the docker exec
        dashed_domain = os.environ['NOTEWORTHY_DOMAIN'].replace('.', '-')
        c = self.docker.containers.list(filters={'name':f'noteworthy-{dashed_domain}-messenger-{profile}'})[0]
        dockerpty.exec_command(self.docker.api, c.id, 'register_new_matrix_user -c /opt/noteworthy/.messenger/homeserver.yaml http://localhost:8008')

    @cli_method
    def install(self, app: str, domain: str = None, invite_code: str = None, hub: str = 'noteworthy.im',
                    profile: str = 'default', accept_tos: bool = False):
        '''install a Noteworthy application
        ---
        Args:
            app: name of app to install
            domain: fqdn to deploy app to
            invite_code: beta invitation code
            hub: fqdn of a Noteworthy hub
            profile: profile to deploy app to
            accept_tos: accept terms of service, useful for non-interactive installation
        '''
        if 'launcher' not in self.plugins:
            raise Exception('Launcher plugin unavailable; something\'s broken.')
        print(f'Installing {app}...')
        if app == 'launcher':
            return self.install_launcher_cli(self.args)

    install.clicz_aliases = ['install']
    install.clicz_defaults = {'app':'launcher'}

    def install_launcher_cli(self, args):

        if not args.accept_tos:
            print('''\
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT
HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER
LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n''')
            agree = input('Do you accept the terms of service? [y/n]: ')
            if agree not in ['y', 'Y', 'yes']:
                print('You must accept the terms of service to continue.')
                sys.exit(2)


        if not args.domain or not args.invite_code:
            args = self._install_launcher_interactive(args.hub, args.profile, domain=args.domain, invite_code=args.invite_code)

        if not args.invite_code:
            print('invite-code is required to provision Noteworthy Launcher.')
            sys.exit(2)
        elif not args.domain:
            print('domain is required to provision Noteworthy Launcher')
            sys.exit(2)

        # TODO each profile should get a dedicated network
        try:
            self.docker.networks.create('noteworthy', check_duplicate=True)
        except:
            pass
        self.plugins['launcher'].Controller().launch_launcher_taproot(
            args.domain, args.hub, args.invite_code, args.profile)

    def _install_launcher_interactive(self, hub, profile, domain=None, invite_code=None):
        domain = input(f'Enter your domain [{domain}]: ') or domain
        # TODO make sure domain is available
        invite_code = input(f'Enter your invite code [{invite_code}]: ') or invite_code
        return argparse.Namespace(domain=domain, invite_code=invite_code, hub=hub, profile=profile)

Controller = LauncherController
