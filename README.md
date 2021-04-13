# s3-playground
S3 Playground with MinIO

## spin up a s3 server via docker

https://docs.min.io/docs/minio-docker-quickstart-guide.html

docker command

```
docker run -p 9000:9000 \
  -e "MINIO_ROOT_USER=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_ROOT_PASSWORD=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  minio/minio server /data
```

web access: http://127.0.0.1:9000/minio/

## access s3 via python client

tutorial: https://docs.min.io/docs/python-client-quickstart-guide

`pip3 install minio`

## use file_uploader.py

run the command below

```
python file_uploader.py my-first-bucket test.txt helloworld.txt
```

this will:
1. create a bucket 'my-first-bucket' 
2. create the object 'test.txt' (with the identical content of file helloworld.txt)

the output of the command should look like this

```
creating minio client connecting to host 127.0.0.1:9000
creating bucket my-first-bucket
new bucket created -> name: my-first-bucket
new object created -> name: test.txt, last_modified: None, etag: 8247fe786a6173b2ad5bb1f099d21ac1, version_id: None
all objects with prefix '/':
name: test.txt, is_dir: False, size: 13, last_modified: 2021-04-13 12:04:37.909000+00:00, etag: 8247fe786a6173b2ad5bb1f099d21ac1, version_id: None
```

the [etag](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Object.html) is the content md5 hash in many (but not all) cases.

```
md5 helloworld.txt 
MD5 (helloworld.txt) = 8247fe786a6173b2ad5bb1f099d21ac1
```

