import boto3
import csv

from flask import jsonify
import hashlib

FILE_LOCAL = "./config/cesar_accessKeys_local.csv"
FILE_PROD = "./config/cesar_accessKeys.csv"
TABLE_PICTURE = "picture_saved"


def read_credentials(csv_file):
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        credentials = next(reader)
        access_key = credentials["Access key ID"]
        secret_key = credentials["Secret access key"]
        return access_key, secret_key
    
access_key, secret_key = read_credentials(FILE_LOCAL)

def hash(txt):
    full = (txt).lower().strip()
    hashed = hashlib.sha256(full.encode()).hexdigest()
    return hashed

def insert_picture(lastname, firstname, img):
    dynamodb = boto3.client("dynamodb", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name="eu-west-3")
    
    image_id = hash(lastname+firstname)
    dynamodb.put_item(TableName=TABLE_PICTURE,Item={"id": {"S": image_id},"image": {"S": img}})


    return jsonify({"message": "image ajoutée", "id": image_id}), 200
        
