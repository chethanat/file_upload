# File Uploader

This upload.py is module which uploads files from specific directory to AWS S3 and Google Cloud Storage 

## Prerequisites
- Python 3.8 or higher


## Usage
1. Clone the repository  https://github.com/chethanat/file_upload.git

2. Create Virtual environment and activate it
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install required dependencies from requirements.txt
```
pip3 install -r requirements.txt
```

4. Then set AWS and GCS credentials in the terminal 
```
set AWS_ACCESS_KEY = your-access-key
set AWS_SECRET_KEY = your-secret-key
set GOOGLE_APPLICATION_CREDENTIAL = path-to-json-file
```

5. Then import upload.py module and run your script. Refer main.py for reference
```
NOTE: It is not recomended to push credentials to git to set AWS and GCS credential using 4th step then run script
python3 main.py
```
