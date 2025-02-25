#📂 cloud/ (AWS, GCP, Azure Storage & Compute)
 #│   ├── 📜 aws_s3_storage.py
 #│   ├── 📜 azure_blob.py
 #│   ├── 📜 gcp_storage.py
 #│   ├── 📜 serverless_functions.py
### Cloud Storage (cloud/aws_s3_storage.py)
```python
import boto3
s3 = boto3.client('s3')
def upload_to_s3(file_name, bucket_name):
    s3.upload_file(file_name, bucket_name, file_name)
```
