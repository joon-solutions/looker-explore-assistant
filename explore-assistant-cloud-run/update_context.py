import csv
import os.path
import re
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/documents.readonly"]

def get_creds():
    creds, project = google.auth.default(scopes=SCOPES)
    return creds

def get_sheet_data(service, spreadsheet_id, doc_description):
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        all_sheet_data = ""
        for sheet in sheets:
            sheet_title = sheet.get("properties", {}).get("title", "Sheet")
            all_sheet_data += f"### {sheet_title}\n\n"
            range_name = f"'{sheet_title}'"
            if doc_description == "Collibra Business Glossary":
                range_name = f"'{sheet_title}'!A:I"
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])
            if not values:
                all_sheet_data += "No data found.\n\n"
            else:
                df = pd.DataFrame(values[1:], columns=values[0])
                all_sheet_data += df.to_markdown(index=False) + "\n\n"
        return all_sheet_data
    except HttpError as err:
        print(err)
        return ""

def get_doc_content(service, document_id):
    try:
        document = service.documents().get(documentId=document_id).execute()
        content = document.get('body').get('content')
        return read_strucutural_elements(content)
    except HttpError as err:
        print(err)
        return ""

def read_strucutural_elements(elements):
    text = ""
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += elem.get('textRun', {}).get('content', '')
    return text

def main():
    creds = get_creds()
    docs_service = build('docs', 'v1', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)

    with open('business_context.md', 'w') as md_file:
        with open('sources.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                doc_description = row['doc_description']
                url = row['url']
                md_file.write(f"<{doc_description}>\n\n")

                if "spreadsheets" in url:
                    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
                    if match:
                        spreadsheet_id = match.group(1)
                        sheet_data = get_sheet_data(sheets_service, spreadsheet_id, doc_description)
                        md_file.write(sheet_data)
                elif "document" in url:
                    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
                    if match:
                        document_id = match.group(1)
                        doc_content = get_doc_content(docs_service, document_id)
                        md_file.write(doc_content)
                
                md_file.write(f"</{doc_description}>\n\n")

if __name__ == '__main__':
    main()
