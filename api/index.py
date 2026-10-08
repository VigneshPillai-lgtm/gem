import io
import os

from flask import Flask, jsonify, request
from google import genai
from PIL import Image

app = Flask(__name__)

STACKS = {
    "fastapi": "FastAPI (Python) + Docker",
    "express": "Express.js (Node.js) + Docker",
    "go": "Go (Gin) + Docker",
}


def build_prompt(stack: str) -> str:
    return f"""
You are CodeSketch-AI, an expert Principal Software Architect.
Analyze the hand-drawn system design or architectural diagram in the provided image.
The user wants to scaffold this using: {stack}.

Provide a production-ready breakdown with the following exact sections:

### 1. Detected Architecture & Components
- List every client, service, database, cache, or message broker identified in the sketch.
- Explain the data flow between them.

### 2. Mermaid.js Flowchart
Provide clean `mermaid` diagram code showing the architecture.

### 3. Repository Directory Structure
Generate an intuitive ASCII tree structure for the project.

### 4. Starter docker-compose.yml
Provide a working `docker-compose.yml` file wiring up the identified services and databases.

### 5. Core API Server Stub
Provide a clean starter server file implementing the primary entry-point service.
"""


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/generate")
def generate():
    uploaded = request.files.get("image")
    stack_key = request.form.get("stack", "fastapi")
    stack = STACKS.get(stack_key)

    if uploaded is None or not uploaded.filename:
        return jsonify({"error": "Please upload a PNG, JPG, or JPEG architecture sketch."}), 400
    if stack is None:
        return jsonify({"error": "Unsupported backend framework selection."}), 400

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return jsonify({"error": "GOOGLE_API_KEY is not configured on the Vercel project."}), 500

    try:
        image = Image.open(io.BytesIO(uploaded.read()))
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemma-4-26b-a4b-it"),
            contents=[build_prompt(stack), image],
        )
        return jsonify({"text": response.text})
    except Exception as exc:
        app.logger.exception("Architecture generation failed")
        return jsonify({"error": f"Unable to generate a scaffold: {exc}"}), 502
