#!/usr/bin/env python3

import http.server

import boto3
from botocore.errorfactory import ClientError

class S3RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Break up requested url into bucket, prefix, filename
        print(f"GET: {self.path}")
        path_parts = self.path.split("/")
        if len(path_parts) < 2:
            print(f"Invalid path: {path_parts}")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')
            return

        bucket = path_parts[1]
        prefix = "/".join(path_parts[2:-1])
        filename = path_parts[-1]
        print(f"bucket={bucket}, prefix={prefix}, filename={filename}")

        # Get connection to s3
        s3 = boto3.client('s3')

        # Check file exists, if not return 404
        try:
            s3.head_object(Bucket=bucket, Key=f"{prefix}/{filename}")
        except ClientError:
            print(f"Not found: {bucket}/{prefix}/{filename}")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')
            return

        # Try to serve s3 file
        self.send_response(200)
        self.end_headers()
        try:
            s3.download_fileobj(bucket, f"{prefix}/{filename}", self.wfile)
        except:
            # Write to socket
            self.send_response(500)

def main():
    print("Starting...")
    httpd = http.server.HTTPServer(('0.0.0.0', 8082), S3RequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
