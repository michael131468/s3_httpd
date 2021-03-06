# s3_httpd

Small Python server to make S3 buckets accessible via HTTP requests

## About

There are many http servers that make S3 buckets browseable. This is yet another
one. It's very minimal, it is a single Python script, simply run it and it works.

The main use case is to make private buckets browseable via http. My main use case
is to do so in small CI jobs that need to fetch files with a private bucket without
using the s3 apis (or temporary session urls).

The server binds to port 8082.

## Dependencies

Requires python3 and the boto3 python module installed.

## AWS Credentials

Configure per boto3 instructions: 

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

- https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

## Example Usage

Assuming you have boto3 credentials configured in the environment variables or in the
home directory, you can just wget the script and run it:

```
wget 'https://raw.githubusercontent.com/michael131468/s3_httpd/main/s3_httpd.py'
python3 s3_httpd.py &
```

You can fetch files using the url format:

```
http://127.0.0.1:8082/<bucket_name>/<prefix>/<filename>
```
