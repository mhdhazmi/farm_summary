# scripts/run_pipeline.py

import sys
import os

# Add src/ to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
print("Python Path:", sys.path)

# Debugging: List contents of zenml_pipelines
zenml_pipelines_path = os.path.join(src_path, 'zenml_pipelines')
if os.path.isdir(zenml_pipelines_path):
    print("Contents of zenml_pipelines:", os.listdir(zenml_pipelines_path))
else:
    print("zenml_pipelines directory not found in src/")

try:
    from zenml_pipelines.pipeline import farms_load_estimation_pipeline
    print("Import successful!")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")

def run_pipeline():
    farms_load_estimation_pipeline.run()

if __name__ == "__main__":
    run_pipeline()
