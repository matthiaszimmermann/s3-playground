import os
import re
import sys

from minio import Minio
from minio.error import S3Error

CMD_LINE_ARGS = "s3-bucket path-prefix [hostname access-key secret-key]"

host_ip = '127.0.0.1'
if os.environ['HOST_IP']:
    host_ip = os.environ['HOST_IP']

MINIO_PORT = "9000"
MINIO_HOSTNAME = "{}:9000".format(host_ip)
MINIO_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
MINIO_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def _parse_command_line():
    print(sys.argv)
    if len(sys.argv) != 3 and len(sys.argv) != 6:
        print("usage: {cmd} {args}".format(cmd=sys.argv[0], args=CMD_LINE_ARGS))
        sys.exit(1)
    else:
        (bucket_name, path_prefix) = tuple(sys.argv[1:3])

        if len(sys.argv) == 6:
            (host_name, access_key, secret_key) = tuple(sys.argv[3:])
        else:
            (host_name, access_key, secret_key) = (MINIO_HOSTNAME, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

        return (bucket_name, path_prefix, host_name, access_key, secret_key)

def _wo2string(obj):
    return "name: {name}, last_modified: {modified}, etag: {etag}, version_id: {version_id}".format(
            name=obj.object_name, 
            etag=obj.etag, 
            modified=obj.last_modified,
            version_id=obj.version_id)

def _obj2string(obj):
    return "name: {name}, is_dir: {dir}, size: {size}, last_modified: {modified}, etag: {etag}, version_id: {version_id}".format(
            name=obj.object_name, 
            dir=obj.is_dir,
            size=obj.size,
            etag=obj.etag, 
            modified=obj.last_modified,
            version_id=obj.version_id)

def main():
    # parse command line args
    (bucket_name, path_prefix, host_name, username, secret) = _parse_command_line()

    # create minio client
    print("creating minio client connecting to host {host}".format(host = host_name))
    client = Minio(host_name, access_key=username, secret_key=secret, secure=False)
    print("minio client created: {}".format(client))

    print("all objects with prefix '{0}':".format(path_prefix))
    for s3o in client.list_objects(bucket_name, prefix=path_prefix):
        print(_obj2string(s3o))

if __name__ == "__main__":
    main()