"""
===========================================================
 File Name   : llmlib.py
 Author      : Adriana
 Created On  : 2026-06-14
 Last Update : 2026-06-14
 Version     : 1.0.0
===========================================================
 Purpose:
   - Libary of functions to interact with local LLMs via Ollama
   - Extract text from PDFs and chunk for LLM processing
   - Generate insights from report sections using LLM
   - Example function to start/stop Ollama server and call API
   - Designed for modular use in data analysis pipelines.

 Key Information for AI Systems:
   - Dependencies  : os, requests, PDFReader, subprocess, socket
   - Environment   : Python 3.10+, Windows 10.0
   - LLM Access    : Local Ollama server (http://localhost:11434)
   - Encoding      : UTF-8 

 Notes:
   - Ensure is up and running on port 11434
   - Model can be configured via OLLAMA_MODEL env var or passed to functions
 
===========================================================
"""

import os
import shutil
import socket
import subprocess
import sys
import time
from typing import Optional, List, Tuple
import requests
import json


# Global timeout (seconds) for LLM requests; configurable via env var LLM_TIMEOUT
try:
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "3000"))
except Exception:
    LLM_TIMEOUT = 3000
from PyPDF2 import PdfReader


# How to start ollama server 
"""
set OLLAMA_NUM_THREADS=8
set OLLAMA_MAX_LOADED_MODELS=1
set OLLAMA_KEEP_ALIVE=10m
ollama run gemma2:2b
"""


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, max_tokens=1500):
    """Split text into chunks suitable for LLM processing."""
    words = text.split()
    chunks, current_chunk = [], []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += 1
        if current_length >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def generate_insights(chunks, model=None, timeout=LLM_TIMEOUT):
    """Use local Ollama (CLI) to generate insights for each chunk.

    Requires the `ollama` CLI to be installed and the requested model available locally.
    The model can be set via the `OLLAMA_MODEL` environment variable or passed in.
    """
    if model is None:
        model = os.getenv("OLLAMA_MODEL", "llama2")
    # Use the local Ollama HTTP API by default. Allow overriding via OLLAMA_API_URL.
    api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

    insights = []
    system_prefix = "You are a helpful assistant for analyzing reports."

    print(f"[llm-analysis] Using model='{model}' and api_url='{api_url}' for {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        prompt = f"{system_prefix}\n\nExtract key insights, trends, and recommendations from the following report section:\n\n{chunk}"

        print(f"[llm-analysis] Processing chunk {i+1}/{len(chunks)} (chars: {len(chunk)})")
        preview = prompt.replace('\n', ' ')[:200]
        print(f"[llm-analysis] Prompt preview: {preview}...")

        try:
            import requests

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
            }

            resp = requests.post(api_url, json=payload, timeout=LLM_TIMEOUT)
        except Exception as e:
            msg = f"[Error] request failed for chunk {i}: {e}"
            print(msg)
            insights.append(msg)
            continue

        if resp.status_code != 200:
            msg = f"[Error] API returned {resp.status_code}: {resp.text}"
            print(msg)
            insights.append(msg)
            continue

        try:
            data = resp.json()
        except Exception as e:
            msg = f"[Error] failed to decode JSON for chunk {i}: {e}"
            print(msg)
            insights.append(msg)
            continue

        # Ollama's HTTP API may return different shapes; prefer `response` key
        output = data.get("response") or data.get("text") or data.get("output") or str(data)
        if not output:
            msg = f"[Error] empty response for chunk {i}"
            print(msg)
            insights.append(msg)
            continue

        print(f"[llm-analysis] Received output (chars): {len(output)}")
        text_preview = output.replace('\n', ' ')[:500]
        print(f"[llm-analysis] Output preview: {text_preview}...")
        insights.append(output)

    return insights


def _is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, int(port)), timeout=1):
            return True
    except Exception:
        return False


def start_ollama_server(port: int = 11434, model: Optional[str] = None, extra_args: Optional[List[str]] = None, timeout: int = 10):
    """Start a local Ollama server process bound to `port`.

    This tries common Ollama server commands and waits until the server answers the health check
    or the timeout is reached. Returns a tuple `(proc, message)` where `proc` is the subprocess
    object (or None on failure) and `message` describes the result.
    """
    if shutil.which("ollama") is None:
        return None, "'ollama' CLI not found on PATH"

    host = "127.0.0.1"
    if _is_port_open(host, port):
        return None, f"port {port} already in use"

    base_cmds = [
        ["ollama", "serve", "--port", str(port)],
        ["ollama", "daemon", "--port", str(port)],
    ]
    if extra_args:
        base_cmds = [cmd + extra_args for cmd in base_cmds]

    # If a specific model is requested and Ollama supports passing it at serve time,
    # append a model flag (best-effort; user can override with extra_args).
    if model:
        base_cmds = [cmd + ["--model", model] for cmd in base_cmds]

    for cmd in base_cmds:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            last_err = str(e)
            proc = None
        else:
            # give it a moment to start
            start = time.time()
            while time.time() - start < timeout:
                if proc.poll() is not None:
                    # process exited early; capture stderr and try next cmd
                    try:
                        _, err = proc.communicate(timeout=1)
                    except Exception:
                        err = "(failed to capture stderr)"
                    last_err = err.strip()
                    break

                # check if port is open or health-check succeeds
                if _is_port_open(host, port):
                    ok, msg = check_ollama_health(model=model, timeout=3)
                    if ok:
                        return proc, f"started and healthy (cmd: {' '.join(cmd)})"
                time.sleep(0.25)

            # if we reach here and proc still running but not healthy, terminate and try next
            if proc and proc.poll() is None:
                try:
                    proc.terminate()
                except Exception:
                    pass

    return None, f"failed to start ollama server: {last_err if 'last_err' in locals() else 'unknown error' }"


def stop_ollama_server(proc, timeout: int = 5):
    """Terminate the server subprocess started by `start_ollama_server`.

    Returns True if the process exited cleanly, False otherwise.
    """
    if not proc:
        return False
    try:
        proc.terminate()
        proc.wait(timeout=timeout)
        return True
    except Exception:
        try:
            proc.kill()
            proc.wait(timeout=timeout)
            return True
        except Exception:
            return False


def call_ollama(prompt, model="llama2"):
    """
    Call an Ollama server running locally to generate text.
    Args:
        prompt (str): The input text you want the model to process.
        model (str): The model name available in Ollama (e.g., 'llama2', 'mistral').
    Returns:
        str: The generated response from the model.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False   # set to True if you want streaming responses
    }

    response = requests.post(url, json=payload, timeout=LLM_TIMEOUT)
    print(f"[call_ollama] HTTP {response}")
    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def calling_ollama_example():
    # Example usage
    prompt = "Summarize the key insights from this financial report."
    print(f"=== Sending prompt to Ollama ===\n{prompt}\n")
    output = call_ollama(prompt, model="llama2")
    print("=== LLM Output ===")
    print(output)