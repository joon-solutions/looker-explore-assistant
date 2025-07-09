# Prompt Engineering for Looker Explore Assistant

This directory contains all the scripts and resources related to the prompt engineering and context distillation pipeline for the Looker Explore Assistant.

## 1. Overview

The primary goal of this pipeline is to address performance issues caused by a large business context file. By using a Gemini model to "distill" the raw context into a smaller, more potent version, we can significantly improve the assistant's response time and reduce token consumption.

## 2. Pipeline Scripts

The pipeline consists of the following scripts, which should be run in order:

1.  **`create_distillation_log_table.py`**: This script creates the BigQuery table (`llm_distillation_experiments`) used to log metadata for each distillation experiment. This only needs to be run once to set up the table.

2.  **`update_context.py`**: This script ingests raw business context from the Google Docs and Sheets defined in `sources.csv` and creates the `business_context_full.md` file.

3.  **`distill_context.py`**: This script takes the `business_context_full.md` file, sends it to the Gemini API with a specialized "trainer" prompt, and saves the slimmed-down version as `business_context_distilled.md`. It also logs the metadata for the experiment to the BigQuery table.

## 3. How to Use



1.  **Authenticate with Google Cloud:**
    ```bash
    gcloud auth application-default login
    ```

2.  **Set up the logging table:** (only need to create if not existed)
    ```bash
    python create_distillation_log_table.py
    ```

3.  **Generate the full context:**
3.1. Prepare the necessary sources at `sources.csv`. **these docs should be gdoc / gspread** and shared to the adc google account you authenticated at step 1.
3.2. Run the prep script. Some notes
- The collibra doc is **hardcoded** to filter and extract only 3 columns. Check out the code content and update appropriately before running.
- For google sheets, the script will iterate and union all tables each under a <sheetname> </sheetname> block.

    ```bash
    python update_context.py
    ```

4.  **Generate the distilled context:**
- **Make sure the constants input files are set correctly in the script below.** (is hardcoded)
  - `full_context_file` : input 
  - `distilled_context_file` : output
  - `evaluation_notes` : note for the current run to distinct with previous runs (will be logged to the BQ log table.)
  - `prompt_version` : the target distill prompt outline to be used in `distillation_prompt.py`
    ```bash
    python distill_context.py
    ```

1.  **Integrate into the build process:** Once the `business_context.md` is created from step 4, use it to replace the old version in `explore-assistant-cloud-run` and run `bash cloudrun_build.sh` to push the image with new distilled business context docs.

## 4. Future Iterations

To add new data sources or update the context, simply add the new source to `sources.csv` and re-run the pipeline. For more advanced changes, such as modifying the distillation prompt or the BigQuery schema, you will need to update the relevant scripts (`distillation_prompt.py`, `create_distillation_log_table.py`).
