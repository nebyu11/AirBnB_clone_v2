#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers,
using the function do_deploy.
"""
from fabric.api import env, put, run
import os

env.hosts = ['52.55.249.213', '54.157.32.137']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        archive_path (str): The path to the archive to deploy.
    Returns:
        True if all operations succeeded, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        folder_name = filename.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, release_path))
        run("rm /tmp/{}".format(filename))
        run("mv {0}web_static/* {0}".format(release_path))
        run("rm -rf {0}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except Exception:
        return False
