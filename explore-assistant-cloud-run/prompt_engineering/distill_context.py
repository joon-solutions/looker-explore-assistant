import os
import time
import logging
import hashlib
import json
from datetime import datetime
from google.cloud import bigquery
from distillation_prompt import return_prompt
import vertexai
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig


# BigQuery table for logging experiments
TABLE_ID = "llm_distillation_experiments"
BIGQUERY_DATASET = "explore_assistant_poc"
PROJECT = "one-global-looker-dev"
MODEL_NAME = "gemini-2.5-pro"
REGION='global'


# Initialize the Vertex AI model globally
vertexai.init(project=PROJECT, location=REGION)
model = GenerativeModel(MODEL_NAME)
logging.basicConfig(level=logging.INFO)

def generate_response(contents) -> tuple[str, int, int]:
    start_time = time.time()
    logging.info(f"Sending prompt to gemini at {start_time}")

    response = model.generate_content(
        contents=contents,
    )
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"LLM request ran for {duration:.4f}")

    metadata = response._raw_response.usage_metadata
    input_token_count = metadata.prompt_token_count
    output_token_count = metadata.candidates_token_count

    return response.text, input_token_count, output_token_count


def calculate_checksum(file_path: str) -> str:
    """Calculates the SHA256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def log_distillation_experiment(
    experiment_id: str,
    timestamp: datetime,
    input_prompt: str,
    distilled_output: str,
    model_used: str,
    input_context_path: str,
    input_token_count: int,
    input_context_checksum: str,
    output_context_path: str,
    output_token_count: int,
    output_context_checksum: str,
    runtime_seconds: float,
    evaluation_notes: str,
    status: str,
    error_details: dict,
    generation_parameters: dict
):
    """Logs distillation experiment metadata to BigQuery."""
    client = bigquery.Client(project=PROJECT)
    table_ref = client.dataset(BIGQUERY_DATASET).table(TABLE_ID) # Use BIGQUERY_DATASET here

    row = {
        "experiment_id": experiment_id,
        "timestamp": timestamp.isoformat(),
        "input_prompt": input_prompt,
        "distilled_output": distilled_output,
        "model_used": model_used,
        "input_context_path": input_context_path,
        "input_token_count": input_token_count,
        "input_context_checksum": input_context_checksum,
        "output_context_path": output_context_path,
        "output_token_count": output_token_count,
        "output_context_checksum": output_context_checksum,
        "runtime_seconds": runtime_seconds,
        "evaluation_notes": evaluation_notes,
        "status": status,
        "error_details": json.dumps(error_details),
        "generation_parameters": json.dumps(generation_parameters),
    }

    errors = client.insert_rows_json(table_ref, [row])
    if errors:
        print(f"Error inserting row into BigQuery: {errors}")
    else:
        print(f"Successfully logged experiment {experiment_id} to BigQuery.")

def distill_context(full_context_path: str, distilled_context_path: str, evaluation_notes: str = "", prompt_version: str = "v1"):
    """
    Reads the full business context, sends it to the Gemini model via the
    shared generate_response function, and saves the distilled content.
    Logs experiment metadata to BigQuery.
    """
    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    start_time = datetime.now()
    status = "FAILURE"
    error_details = {} # Initialize as empty dict
    input_token_count = 0
    output_token_count = 0
    runtime_seconds = 0.0
    input_checksum = ""
    output_checksum = ""
    generation_params = {} # Example parameters
    distilled_output = "" # Initialize distillation_prompt here to ensure it's always bound
    distillation_prompt= ""

    try:
        # Read the full business context
        with open(full_context_path, 'r', encoding='utf-8') as f:
            full_context = f.read()
        
        input_checksum = calculate_checksum(full_context_path)

        if not full_context:
            print(f"Warning: {full_context_path} is empty. Skipping distillation.")
            with open(distilled_context_path, 'w', encoding='utf-8') as f:
                f.write("") # Create an empty distilled file
            status = "SUCCESS" # Consider empty distillation a success if input is empty
            return

        # Get the distillation prompt from the new function
        distillation_prompt = return_prompt(version=prompt_version) + "\n\n" + \
                              "<Business Documentation>\n" + \
                              f"{full_context}\n\n" + \
                              "</Business Documentation>\n"

        print("Sending full context to Gemini for distillation...")
        # Use the shared generate_response function
        distilled_output, input_token_count, output_token_count = generate_response(distillation_prompt)
        
        print("Distillation complete. Saving distilled content.")

        # Save the distilled content
        with open(distilled_context_path, 'w', encoding='utf-8') as f:
            f.write(distilled_output)
        
        output_checksum = calculate_checksum(distilled_context_path)
        

        status = "SUCCESS"
        print(f"Distilled context saved to {distilled_context_path}")

    except FileNotFoundError as e:
        error_details = {"type": "FileNotFoundError", "message": str(e)}
        print(f"Error: One of the context files not found. Ensure '{full_context_path}' exists.")
    except Exception as e:
        error_details = {"type": type(e).__name__, "message": str(e)}
        print(f"An error occurred during context distillation: {e}")
    finally:
        end_time = datetime.now()
        runtime_seconds = (end_time - start_time).total_seconds()
        log_distillation_experiment(
            experiment_id=experiment_id,
            timestamp=start_time,
            input_prompt=distillation_prompt,
            distilled_output=distilled_output,
            model_used=MODEL_NAME,
            input_context_path=full_context_path,
            input_token_count=input_token_count,
            input_context_checksum=input_checksum,
            output_context_path=distilled_context_path,
            output_token_count=output_token_count,
            output_context_checksum=output_checksum,
            runtime_seconds=runtime_seconds,
            evaluation_notes=evaluation_notes,
            status=status,
            error_details=error_details,
            generation_parameters=generation_params # Use the defined generation parameters
        )

if __name__ == "__main__":
    full_context_file = "business_context_full.md"
    distilled_context_file = "business_context_distilled_v1_1.md"
    evaluation_notes="v1.1 prompt with updated spreadsheets business context."
    prompt_version="v1"

    distill_context(
        full_context_file,
        distilled_context_file,
        # evaluation_notes="v1 prompt with simple instructions and raw business contexts",
        evaluation_notes=evaluation_notes,
        prompt_version=prompt_version
    )
