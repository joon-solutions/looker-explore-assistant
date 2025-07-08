
### 1. setup runtime
-- if uv is used
uv init
uv add -r requirements.txt


-- otherwise standard venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

-- authenticate as tpv account - select tpv in the popup google login dialog


gcloud auth login


gcloud auth application-default login


### 2. load scripts
chmod +x load_examples.sh 
chmod +x load_samples.sh
chmod +x load_refinements.sh
chmod +x load_feedback_categories.sh


