import sys
import logging
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler
import paramiko, os

class Sync:
    def __init__(self):

        self.ssh = paramiko.SSHClient()

        paramiko.util.load_host_keys(os.path.expanduser('C:/Users/Has/.ssh/known_hosts'))

        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('192.168.10.10', username="has", password='')
        self.r_path = '/home/has/haskell/'

    def get_files(self):
        sftp = self.ssh.open_sftp()
        localpath = './hello.hs'
        remotepath = '/home/has/haskell/hello.hs'

        _path = '/home/has/haskell/'
        files = sftp.listdir(self.r_path)
        files.remove('\\')

        print(files)
        for _file in files:
            sftp.get( os.path.join(self.r_path, _file), _file)

        sftp.close()

    def put_file(self,file_path):
        sftp = self.ssh.open_sftp()

        sftp.put( file_path, os.path.join( self.r_path, file_path.split('\\')[-1] ))

        sftp.close()

    def make_dir(self, dir_name):
        sftp = self.ssh.open_sftp()

        sftp.mkdir(os.path.join( self.r_path, dir_name.split('\\')[-1] ))

        sftp.close()

    def close(self):
        self.ssh.close()


class Interject(PatternMatchingEventHandler):
    def on_created(self, event):
        print(f"hey, {event.src_path} has been created!")

    def on_deleted(self, event):
        print(f"what the f**k! Someone deleted {event.src_path}!")

    def on_modified(self, event):
        print(f"hey buddy, {event.src_path} has been modified")

        if os.path.isdir(event.src_path):
            ssh_handle.make_dir(event.src_path)
        else:
            ssh_handle.put_file(event.src_path)

    def on_moved(self, event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

if __name__ == "__main__":
    ssh_handle = Sync()
    patterns = ["*"]
    ignore_patterns = [""]
    ignore_directories = False
    case_sensitive = True

    my_event_handler = Interject(patterns, ignore_patterns, ignore_directories, case_sensitive)

    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        ssh_handle.close()

    