import logging
from urllib.parse import urlparse

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "postgres://postgres:postgres@db:5432/db"
parsed_db_url = urlparse(DATABASE_URL)

# S3 configuration
S3_CONFIG = {
    'endpoint_url': 'http://s3mock:9090',
    'region_name': 'us-east-1',
    'aws_access_key_id': 'dummy_access_key',
    'aws_secret_access_key': 'dummy_secret_key'
}

# Bucket configuration
BUCKET_NAME = 'cocrafter-dev'