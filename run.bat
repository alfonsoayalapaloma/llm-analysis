@echo off
REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the Python program and redirect output to results.txt
python data_pipeline.py > results.txt 2>&1

REM Deactivate the virtual environment
deactivate

echo Script execution complete. Results saved to results.txt
