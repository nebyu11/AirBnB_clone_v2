#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers,
using the function deploy.
"""
from datetime import datetime
from fabric.api import env, local, put, run, runs_once
import os

env.hosts = ['52.55.249.213', '54.157.32.137']


@runs_once
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        The archive path if generated correctly, otherwise None.
    """
    try:
        if not os.path.isdir("versions"):
            local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        result = local("tar -cvzf {} web_static".format(archive_path))
        if result.failed:
            return None
        return archive_path
    except Exception:
        return None


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
        folder_name = filename.replace(".tgz", "")
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


def deploy():
    """
    Creates and distributes an archive to the web servers.
    Returns:
        The return value of do_deploy, or False if archive creation fails.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
