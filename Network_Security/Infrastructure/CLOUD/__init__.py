import os
from Network_Security.Exception.NS_exception import NetworkSecurityException
from Network_Security.Constants.Training_Constant  import *
import subprocess
class S3Sync:

    def sync_folder_to_s3( folder, aws_bucket_url):
        subprocess.run(
            ["aws", "s3", "sync", folder, aws_bucket_url],
            check=True
        )

    def sync_folder_from_s3( folder, aws_bucket_url):
        
        subprocess.run(
            ["aws", "s3", "sync", aws_bucket_url, folder],
            check=True
        )
   