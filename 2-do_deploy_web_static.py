#!/usr/bin/python3
"""
A Fabric script to deploy an archive to web servers.
Usage: fab -f 2-do_deploy_web_static.py
        do_deploy:archive_path=<path_to_archive>
"""
from fabric.api import env, run, put, local
from os.path import exists, splitext

# Define the remote user and hosts
env.user = 'ubuntu'
env.hosts = ['100.26.241.219', '100.26.122.241']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if all operations are done correctly, False otherwise.
    """
    # Check if the archive exists locally
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Extract the archive to the /data/web_static/releases/ directory
        archive_filename = splitext(archive_path.split("/")[-1])[0]
        release_path = "/data/web_static/releases/{}".format(archive_filename)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename + ".tgz",
                                            release_path))

        # Delete the uploaded archive from the server
        run("rm /tmp/{}".format(archive_filename + ".tgz"))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Error: {}".format(str(e)))
        return False
