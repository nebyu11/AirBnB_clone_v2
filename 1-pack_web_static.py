#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of the AirBnB Clone repo, using the function do_pack.
"""
from datetime import datetime
from fabric.api import local
import os


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
