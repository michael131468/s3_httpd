#!/usr/bin/env python3

import http.server
import os

import boto3
from botocore.errorfactory import ClientError


class S3RequestHandler(http.server.BaseHTTPRequestHandler):
    def split_path(self, path):
        path_parts = self.path.split("/")
        if len(path_parts) < 2:
            raise Exception("Insufficient path parts")
        bucket = path_parts[1]
        prefix = "/".join(path_parts[2:-1])
        filename = path_parts[-1]
        return bucket, prefix, filename

    def serve_s3_object(self, headers_only=False):
        # Break up requested url into bucket, prefix, filename
        try:
            bucket, prefix, filename = self.split_path(self.path)
            print(f"bucket={bucket}, prefix={prefix}, filename={filename}")
        except:
            print(f"Invalid path: {path_parts}")
            self.send_response(404)
            self.end_headers()
            if not headers_only:
                self.wfile.write(b"File not found")
            return

        # Get connection to s3
        s3 = boto3.client("s3")

        # If filename is empty (url ends with /), return a listing of the prefix
        if not filename:
            try:
                response = s3.list_objects_v2(
                                              Bucket=bucket,
                                              Delimiter='/',
                                              Prefix=prefix,
                                             )
                print(response)
                self.send_response(200)
                self.end_headers()
            except ClientError:
                print(f"Not found: {bucket}/{prefix}/{filename}")
                self.send_response(404)
                self.end_headers()
                if not headers_only:
                    self.wfile.write(b"File not found")

            return

        # Try to get the s3 metadata of the requested file, if not possible return 404
        try:
            metadata = s3.head_object(Bucket=bucket, Key=os.path.join(prefix, filename))
        except ClientError:
            print(f"Not found: {bucket}/{prefix}/{filename}")
            self.send_response(404)
            self.end_headers()
            if not headers_only:
                self.wfile.write(b"File not found")
            return

        # Return 200 headers
        self.send_response(200)

        # Set content-type
        if filename.endswith((".htm", ".html")):
            self.send_header("Content-type", "text/html; charset=utf-8")
        elif filename.endswith(".txt"):
            self.send_header("Content-type", "text/plain; charset=utf-8")
        else:
            self.send_header("Content-type", "application/octet-stream; charset=utf-8")

        # Set content-length
        self.send_header(
            "Content-length",
            metadata["ResponseMetadata"]["HTTPHeaders"]["content-length"],
        )

        self.end_headers()

        # Send file
        if not headers_only:
            try:
                s3.download_fileobj(bucket, os.path.join(prefix, filename), self.wfile)
            except:
                self.send_response(500)

    def do_HEAD(self):
        print(f"HEAD: {self.path}")
        self.serve_s3_object(headers_only=True)

    def do_GET(self):
        print(f"GET: {self.path}")
        self.serve_s3_object()


def main():
    print("Starting...")
    httpd = http.server.HTTPServer(("0.0.0.0", 8082), S3RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
