FROM registry.access.redhat.com/ubi8/python-39:1-48
COPY --chmod=0755 s3_httpd.py /usr/bin/s3_httpd.py
RUN pip3 install boto3
