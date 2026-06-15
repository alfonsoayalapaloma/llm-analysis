# llm-analysis
 Purpose:
   - Automate inclusion of LLM insights into data analysis workflow
   - Process PDF reports, extract insights, and print summaries
   - Uses OLLAMA running in 'http://localhost:11434/api/generate'


## Run Example:

```bash
(.venv) C:\sf\src\llm-analysis>python data_pipeline.py
=== Testing access to LLM ===
[call_ollama] HTTP <Response [200]>
LLM responded to test prompt: The answer to 2 + 2 is 4.
=== Extracting text from PDF: report.pdf ===
Extracted 5015 characters from PDF.
Split text into 1 chunks for LLM processing.
[llm-analysis] Using model='llama2' and api_url='http://localhost:11434/api/generate' for 1 chunks
[llm-analysis] Processing chunk 1/1 (chars: 4946)
[llm-analysis] Prompt preview: You are a helpful assistant for analyzing reports.  Extract key insights, trends, and recommendations from the following report section:  UNITED STATES SECURITIES AND EXCHANGE COMMISSION Washington, D...
[llm-analysis] Received output (chars): 2420
[llm-analysis] Output preview: Based on the provided report section, I have extracted the following key insights, trends, and recommendations:  Key Insights:  1. Financial Performance: The company's revenue and net income increased by 8% and 9%, respectively, in the fiscal year ended June 30, 2024 compared to the previous year. This indicates a positive financial performance for the company. 2. Growth Opportunities: The report mentions that the company is investing in growth opportunities such as digital and e-commerce initia...
=== Report Insights ===

Section 1:
Based on the provided report section, I have extracted the following key insights, trends, and recommendations:

Key Insights:

1. Financial Performance: The company's revenue and net income increased by 8% and 9%, respectively, in the fiscal year ended June 30, 2024 compared to the previous year. This indicates a positive financial performance for the company.
2. Growth Opportunities: The report mentions that the company is investing in growth opportunities such as digital and e-commerce initiatives, which could potentially drive future revenue and profit growth.
3. Internal Controls: The report states that the company's internal controls over financial reporting are effective, which suggests a strong governance and risk management framework in place.
4. Shareholder Value: The aggregate market value of the voting stock held by non-affiliates amounted to $345 billion on December 31, 2023, indicating that shareholders have seen significant value creation in recent years.

Trends:

1. Increasing Focus on Digital Transformation: The company is investing in digital and e-commerce initiatives, which suggests a growing focus on leveraging technology to drive growth and efficiency.
2. Expansion into New Markets: The report mentions that the company has expanded its presence in new markets, which could potentially lead to increased revenue and profit growth in the future.
3. Emphasis on Sustainability: The report highlights the company's commitment to sustainability and reducing its environmental footprint, which could help to build brand loyalty and attract environmentally-conscious consumers.

Recommendations:

1. Continue to Invest in Digital Transformation: Given the growing importance of digital technologies, the company should continue to invest in digital and e-commerce initiatives to drive growth and efficiency.
2. Expand into New Markets: The company should explore opportunities to expand its presence in new markets, particularly those with high growth potential, to drive future revenue and profit growth.
3. Enhance Sustainability Efforts: The company should continue to prioritize sustainability and reduce its environmental footprint to build brand loyalty and attract environmentally-conscious consumers.

```
4. Foster a Strong Governance Culture: The company should maintain a strong governance culture to ensure that internal controls are effective and to protect shareholder value.
