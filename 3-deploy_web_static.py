#!/usr/bin/python3
"""
Creates and distributes an archive to web servers
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ["100.26.241.219", "100.26.122.241"]
env.user = "ubuntu"


@task
def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if generated successfully, None otherwise.
    """
    try:
        # Create the 'versions' folder if it doesn't exist
        if local("mkdir -p versions").failed is True:
            return None

        # Get the current date and time
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")

        # Set the archive path and name
        archive_path = "versions/web_static_{}.tgz".format(date_time)

        # Create the .tgz archive
        print("Packing web_static to {}".format(archive_path))
        if local("tar -cvzf {} web_static".format(
                archive_path)).failed is True:
            return None

        # Check if the archive was created successfully
        if os.path.exists(archive_path):
            return archive_path
        else:
            return None

    except Exception as e:
        print("Error: {}".format(str(e)))
        return None


@task
def do_deploy(archive_path):
    """
    Distribute archive.
    """
    if os.path.exists(archive_path) is False:
        return False

    # Extract file name and remove extension
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to the temporary directory on the server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False

    # Remove existing deployment directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    # Create necessary deployment directories
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False

    # Extract the contents of the archive to the deployment directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False

    # Remove the temporary archive file
    if run("rm /tmp/{}".format(file)).failed is True:
        return False

    # Move contents to the proper deployment directory
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False

    # Remove unnecessary subdirectory from deployment directory
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False

    # Remove the old symbolic link to the current release
    if run("rm -rf /data/web_static/current").failed is True:
        return False

    # Create a new symbolic link to the current release
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False

    # Deployment successful
    return True


@task
def deploy():
    """
    Deploy the web static to both web servers
    """

    archive_path = do_pack()
    if archive_path is None:
        return False

    # Deploy the archive to the web servers
    return do_deploy(archive_path)
