import re
import sys

from minio import Minio
from minio.error import S3Error

CMD_LINE_ARGS = "s3-bucket s3-object-name file-to-upload [hostname access-key secret-key]"

MINIO_HOSTNAME = "127.0.0.1:9000"
MINIO_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
MINIO_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def _validate_bucket_name(bucket_name):
    # https://stackoverflow.com/questions/50480924/regex-for-s3-bucket-name
    regexp = "(?=^.{3,63}$)(?!^(\d+\.)+\d+$)(^(([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)*([a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])$)"

    if not re.match(regexp, bucket_name):
        print("invalid bucket name. for bucket name rules see https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html")
        sys.exit(2)

def _parse_command_line():
    if len(sys.argv) != 4 & len(sys.argv) != 7:
        print("usage: {cmd} {args}".format(cmd=sys.argv[0], args=CMD_LINE_ARGS))
        sys.exit(1)
    else:
        (bucket_name, object_name, file_name) = tuple(sys.argv[1:4])

        _validate_bucket_name(bucket_name)

        if len(sys.argv) == 7:
            (host_name, access_key, secret_key) = tuple(sys.argv[4:])
        else:
            (host_name, access_key, secret_key) = (MINIO_HOSTNAME, MINIO_ACCESS_KEY, MINIO_SECRET_KEY)

        return (bucket_name, object_name, file_name, host_name, access_key, secret_key)

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

def _object_exists(client, bucket_name, object_name):
    # https://github.com/minio/minio-py/blob/master/minio/datatypes.py
    try:
        s3o = client.stat_object(bucket_name, object_name)
        print("object already exists -> {obj}".format(obj= _obj2string(s3o)))
        return True
    except S3Error as exc:
        return False

def main():
    # parse command line args
    (bucket_name, object_name, file_name, host_name, username, secret) = _parse_command_line()

    # create minio client
    print("creating minio client connecting to host {host}".format(host = host_name))
    client = Minio(host_name, access_key=username, secret_key=secret, secure=False)
    
    # create bucket if it does not yet exist
    print("creating bucket {bucket}".format(bucket=bucket_name))
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print("new bucket created -> name: {name}".format(name=bucket_name))
    else:
        print("bucket already exists -> name: {name}".format(name=bucket_name))

    # upload file if it is not already uploaded
    if not _object_exists(client, bucket_name, object_name):
        s3wo = client.fput_object(bucket_name, object_name, file_name)
        print("new object created -> {obj}".format(obj=_wo2string(s3wo)))

    # list other objects that share the same prefix
    if '/' in object_name:
        s3folder = "{0}/".format(object_name.rsplit('/', 1)[0])
    else:
        s3folder = "/"

    print("all objects with prefix '{0}':".format(s3folder))
    for s3o in client.list_objects(bucket_name, prefix=s3folder):
        print(_obj2string(s3o))

if __name__ == "__main__":
    main()