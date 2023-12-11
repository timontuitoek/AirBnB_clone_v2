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
        local("mkdir -p versions")

        # Get the current date and time
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")

        # Set the archive path and name
        archive_path = "versions/web_static_{}.tgz".format(date_time)

        # Create the .tgz archive
        print("Packing web_static to {}".format(archive_path))
        local("tar -cvzf {} web_static".format(archive_path))

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
    if os.path.exists(archive_path):
        # Extracting necessary information from the archive_path
        archived_file = archive_path.split("/")[-1]
        filename_no_ext = os.path.splitext(archived_file)[0]

        # Remote paths on the server
        newest_version = "/data/web_static/releases/" + filename_no_ext
        archived_file_remote = "/tmp/" + archived_file

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file_remote,
                                             newest_version))

        # Delete the archive from the web server
        run("sudo rm {}".format(archived_file_remote))

        # Move content to the correct location
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))

        # Remove unnecessary directory
        run("sudo rm -rf {}/web_static".format(newest_version))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False


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
