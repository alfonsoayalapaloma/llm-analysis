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
