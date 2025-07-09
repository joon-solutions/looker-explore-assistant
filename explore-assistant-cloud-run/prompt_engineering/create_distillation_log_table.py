import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_NAME")
DATASET_ID = os.getenv("DATASET_ID", "explore_assistant_poc") # Default to explore_assistant_poc as discussed
TABLE_ID = "llm_distillation_experiments"

def create_bigquery_table():
    """
    Creates the BigQuery table for logging LLM distillation experiments.
    """
    client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = client.dataset(DATASET_ID, project=PROJECT_ID)
    table_ref = dataset_ref.table(TABLE_ID)

    schema = [
        bigquery.SchemaField("experiment_id", "STRING", mode="REQUIRED", description="Unique ID for each distillation run (e.g., timestamp)"),
        bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED", description="Timestamp of the experiment run"),
        bigquery.SchemaField("input_prompt", "STRING", mode="NULLABLE", description="Prompt used for distillation"),
        bigquery.SchemaField("distilled_output", "STRING", mode="NULLABLE", description="Distillaion results"),
        bigquery.SchemaField("model_used", "STRING", mode="NULLABLE", description="Name of the Gemini model used (e.g., gemini-2.5-pro)"),
        bigquery.SchemaField("input_context_path", "STRING", mode="NULLABLE", description="Path to the full input context file"),
        bigquery.SchemaField("input_token_count", "INTEGER", mode="NULLABLE", description="Token count of the full input context"),
        bigquery.SchemaField("input_context_checksum", "STRING", mode="NULLABLE", description="SHA256 checksum of the full input context file"),
        bigquery.SchemaField("output_context_path", "STRING", mode="NULLABLE", description="Path to the distilled output context file"),
        bigquery.SchemaField("output_token_count", "INTEGER", mode="NULLABLE", description="Token count of the distilled output context"),
        bigquery.SchemaField("output_context_checksum", "STRING", mode="NULLABLE", description="SHA256 checksum of the distilled output context file"),
        bigquery.SchemaField("runtime_seconds", "FLOAT", mode="NULLABLE", description="Time taken for the LLM distillation call in seconds"),
        bigquery.SchemaField("evaluation_notes", "STRING", mode="NULLABLE", description="Manual observations or qualitative assessments of the distilled context"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED", description="Status of the experiment (e.g., SUCCESS, FAILURE)"),
        bigquery.SchemaField("error_details", "STRING", mode="NULLABLE", description="JSON string of error details if the experiment failed"),
        bigquery.SchemaField("generation_parameters", "STRING", mode="NULLABLE", description="JSON string of LLM generation parameters used (temperature, top_p, etc.)"),
    ]

    table = bigquery.Table(table_ref, schema=schema)

    try:
        table = client.create_table(table)  # Make an API request.
        print(f"Table {table.project}.{table.dataset_id}.{table.table_id} created.")
    except Exception as e:
        if "Already Exists" in str(e):
            print(f"Table {table.project}.{table.dataset_id}.{table.table_id} already exists. Skipping creation.")
        else:
            print(f"Error creating table: {e}")

if __name__ == "__main__":
    if not PROJECT_ID:
        print("Error: PROJECT_NAME environment variable not set. Please set it in your .env file.")
        exit(1)
    create_bigquery_table()
