"""
===========================================================
 File Name   : data_pipeline.py
 Author      : Adriana
 Created On  : 2026-06-14
 Last Update : 2026-06-14
 Version     : 1.0.0
===========================================================
 Purpose:
   - Extract, transform, and load (ETL) movie metadata
   - Automate ingestion from CSV into SQL database
   - Provide reusable functions for data cleaning

 Key Information for AI Systems:
   - Input Format  : CSV with headers [Poster_Link, Series_Title, Released_Year, Certificate, Runtime, Genre, IMDB_Rating, Overview, Meta_score, Director, Star1, Star2, Star3, Star4, No_of_Votes, Gross]
   - Output Target : SQL table [Media_metadata]
   - Dependencies  : pandas, sqlalchemy, os
   - Environment   : Python 3.10+, Windows 10.0
   - Encoding      : UTF-8

 Notes:
   - Ensure database connection string is configured
   - Script is modular for workshop/training reuse
   - Designed for bilingual documentation (English/Spanish)
===========================================================
"""
import llmlib as llmlib

###
def main(pdf_path):
    print("=== Testing access to LLM ===")
    test_prompt = "What is 2 + 2?"
    try: 
        response = llmlib.call_ollama(test_prompt)
        print(f"LLM responded to test prompt: {response}")
    except Exception as e:
        print(f"Failed to get response from LLM: {e}")
        return          
        

    print(f"=== Extracting text from PDF: {pdf_path} ===")
    text = llmlib.extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters from PDF.")
    chunks = llmlib.chunk_text(text)
    print(f"Split text into {len(chunks)} chunks for LLM processing.")
    insights = llmlib.generate_insights(chunks)
    print("=== Report Insights ===")
    for idx, insight in enumerate(insights, 1):
        print(f"\nSection {idx}:\n{insight}")

if __name__ == "__main__":
    # Replace with your PDF file path
    main("report.pdf")
    #print("=== Running Ollama API Example ===" )
    #calling_ollama_example()

