# helper_functions.py

import os
import hmac
import logging
import mysql.connector
import requests
import vertexai
from requests.auth import HTTPBasicAuth
from google.cloud import bigquery
import uuid
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

# Configuration (Best practice: use a dedicated config management library)
PROJECT = os.environ.get("PROJECT_NAME")
REGION = os.environ.get("REGION_NAME")
VERTEX_CF_AUTH_TOKEN = os.environ.get("VERTEX_CF_AUTH_TOKEN")
VERTEX_CF_SECRET = os.getenv("VERTEX_CF_SECRET")
LOOKER_API_URL = os.getenv("LOOKER_API_URL", "https://looker.example.com/api/4.0")
LOOKER_CLIENT_ID = os.getenv("LOOKER_CLIENT_ID")
LOOKER_CLIENT_SECRET = os.getenv("LOOKER_CLIENT_SECRET")
CLOUD_SQL_HOST = os.getenv("CLOUD_SQL_HOST")
CLOUD_SQL_USER = os.getenv("CLOUD_SQL_USER")
CLOUD_SQL_PASSWORD = os.getenv("CLOUD_SQL_PASSWORD")
CLOUD_SQL_DATABASE = os.getenv("CLOUD_SQL_DATABASE")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET", "beck_explore_assistant")
BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE", "_prompts")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.0-pro-001") # Get the model name

logging.basicConfig(level=logging.INFO)

# Initialize the Vertex AI model globally
vertexai.init(project=PROJECT, location=REGION)
model = GenerativeModel(MODEL_NAME)

def get_response_headers():
    return {
        "Access-Control-Allow-Origin": "*",  # Be cautious in production!
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Signature, Authorization",
    }


def has_valid_signature(request):
    signature = request.headers.get("X-Signature")
    if not signature:
        logging.warning("Missing signature")
        return False

    if not VERTEX_CF_SECRET:
        raise ValueError("VERTEX_CF_SECRET environment variable not set")

    secret = VERTEX_CF_SECRET.encode("utf-8")
    request_data = request.get_data()
    hmac_obj = hmac.new(secret, request_data, "sha256")
    expected_signature = hmac_obj.hexdigest()

    return hmac.compare_digest(signature.encode('utf-8'), expected_signature.encode('utf-8'))


def verify_looker_user(user_id):
    looker_api_url = f"{LOOKER_API_URL}/user/{user_id}"
    auth = HTTPBasicAuth(LOOKER_CLIENT_ID, LOOKER_CLIENT_SECRET)
    response = requests.get(looker_api_url, auth=auth)

    if response.status_code == 200:
        return True

    logging.warning(
        f"Looker user verification failed for user {user_id}: {response.status_code} {response.text}"
    )
    return False
def get_user_from_db(user_id):
    try:
        connection = mysql.connector.connect(
            host=CLOUD_SQL_HOST, user=CLOUD_SQL_USER, password=CLOUD_SQL_PASSWORD, database=CLOUD_SQL_DATABASE
        )
        cursor = connection.cursor(dictionary=True) # Use dictionary cursor
        query = "SELECT user_id, name, email FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        return user_data
    except mysql.connector.Error as e:
        logging.error(f"Database error in get_user_from_db: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def create_new_user(user_id, name, email):
    try:
        connection = mysql.connector.connect(
            host=CLOUD_SQL_HOST, user=CLOUD_SQL_USER, password=CLOUD_SQL_PASSWORD, database=CLOUD_SQL_DATABASE
        )
        cursor = connection.cursor()
        query = "INSERT INTO users (user_id, name, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, name, email))
        connection.commit()
        return {"user_id": user_id, "status": "created"}  # Consider returning more data
    except mysql.connector.Error as e:
        logging.error(f"Database error in create_new_user: {e}")
        connection.rollback() # Rollback on error
        return {"error": "Failed to create user", "details": str(e)}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def create_chat_thread(user_id, explore_key):
    try:
        connection = mysql.connector.connect(
            host=CLOUD_SQL_HOST, user=CLOUD_SQL_USER, password=CLOUD_SQL_PASSWORD, database=CLOUD_SQL_DATABASE
        )
        cursor = connection.cursor()
        query = "INSERT INTO chats (explore_key, user_id) VALUES (%s, %s)"
        cursor.execute(query, (explore_key, user_id))
        connection.commit()
        chat_id = cursor.lastrowid
        return chat_id
    except mysql.connector.Error as e:
        logging.error(f"Database error in create_chat_thread: {e}")
        connection.rollback()
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def add_message(chat_id, user_id, content, is_user_message=1):
    try:
        connection = mysql.connector.connect(
            host=CLOUD_SQL_HOST, user=CLOUD_SQL_USER, password=CLOUD_SQL_PASSWORD, database=CLOUD_SQL_DATABASE
        )
        cursor = connection.cursor()
        query = "INSERT INTO messages (chat_id, user_id, content, is_user_message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (chat_id, user_id, content, is_user_message))
        connection.commit()
        message_id = cursor.lastrowid
        return message_id
    except mysql.connector.Error as e:
        logging.error(f"Database error in add_message: {e}")
        connection.rollback()
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def add_feedback(user_id, message_id, feedback_text, is_positive):
    try:
        connection = mysql.connector.connect(
            host=CLOUD_SQL_HOST, user=CLOUD_SQL_USER, password=CLOUD_SQL_PASSWORD, database=CLOUD_SQL_DATABASE
        )
        cursor = connection.cursor()
        query = "INSERT INTO feedback (user_id, message_id, feedback_text, is_positive) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, message_id, feedback_text, is_positive))
        connection.commit()
        feedback_id = cursor.lastrowid
        update_query = "UPDATE messages SET feedback_id = %s WHERE message_id = %s"
        cursor.execute(update_query, (feedback_id, message_id))
        connection.commit()
        return True  # Or return feedback_id
    except mysql.connector.Error as e:
        logging.error(f"Database error in add_feedback: {e}")
        connection.rollback()
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def generate_looker_query(contents, parameters=None):
    default_parameters = {"temperature": 0.2, "max_output_tokens": 500, "top_p": 0.8, "top_k": 40}
    if parameters:
        default_parameters.update(parameters)

    response = model.generate_content(
        contents=contents,
        generation_config=GenerationConfig(**default_parameters),
    )

    metadata = response._raw_response.usage_metadata
    log_entry = {
        "severity": "INFO",
        "message": {
            "request": contents,
            "response": response.text,
            "input_characters": metadata.prompt_token_count,
            "output_characters": metadata.candidates_token_count,
        },
        "component": "explore-assistant-metadata",
    }
    logging.info(log_entry)
    return response.text

def generate_response(contents, parameters=None):
    default_parameters = {"temperature": 0.3, "max_output_tokens": 600, "top_p": 0.9, "top_k": 50}
    if parameters:
        default_parameters.update(parameters)

    response = model.generate_content(
        contents=contents,
        generation_config=GenerationConfig(**default_parameters)
    )

    metadata = response._raw_response.usage_metadata

    entry = {
        "severity": "INFO",
        "message": {"request": contents, "response": response.text,
                    "input_characters": metadata.prompt_token_count, "output_characters": metadata.candidates_token_count},
        "component": "prompt-response-metadata",
    }
    logging.info(entry)
    return response.text

def record_prompt(data):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
    table_ref = f"{PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    try:
      load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
      load_job.result()  # Wait for the job to complete
      logging.info(f"Loaded {load_job.output_rows} prompts into {table_ref}")
    except Exception as e:
      logging.error(f"BigQuery load job failed: {e}")
