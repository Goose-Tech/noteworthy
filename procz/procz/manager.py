import os
import re
import time
import daemon
import traceback
from lockfile.pidlockfile import PIDLockFile

class ProcManager():

    PID_REGEX = re.compile('^procz_([a-zA-Z0-9]*).pid$')

    def __init__(self, lock_dir = '/var/run'):
        self.lock_dir = lock_dir

    def start_proc(self, proc_name, proc_factory, chroot_dir=None,
                   kill_old=False):
        if not proc_name.isalnum():
            raise Exception('Invalid name: Only Alpha-Numeric Characters Allowed.')
        procs = self._get_procs()
        if proc_name in procs:
            if not kill_old:
                raise Exception('Process is already running!')
            self.kill_proc(proc_name)
        pidfilename = os.path.join(
            self.lock_dir, f'procz_{proc_name}.pid')
        pid = os.fork()
        if pid:
            return 'starting proc'
        else:
            try:
                with daemon.DaemonContext(pidfile=PIDLockFile(pidfilename),
                                          detach_process=True):
                    procd = proc_factory()
                    procd.run()
            except Exception as e:
                with open(f'{proc_name}.error.log', 'w') as f:
                    f.write(traceback.format_exc()+'\n')
                raise e

    def list_procs(self):
        return list(self._get_procs().values())

    def kill_proc(self, proc_name, safe=False):
        procs = self._get_procs()
        proc = procs.get(proc_name)
        if not proc and not safe:
            raise Exception('proc Does Not Exist!')
        pid = proc['pid']
        os.system(f'kill {pid}')
        time.sleep(1)


    def _get_procs(self):
        file_names = os.listdir(self.lock_dir)
        matches = [self.PID_REGEX.search(f) for f in file_names]
        procs = {}
        for match in matches:
            if match:
                name = match.group(1)
                file_name = match.group(0)
                file_path = os.path.join(self.lock_dir, file_name)
                with open(file_path, 'r') as f:
                    pid = int(f.read())
                procs[name] = {'pid': pid, 'name': name}
        return procs