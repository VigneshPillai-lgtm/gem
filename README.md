# CodeSketch-AI

CodeSketch-AI turns a hand-drawn software architecture diagram into a practical project scaffold. Upload a whiteboard or paper sketch, choose a target backend stack, and let Gemma 4 describe the detected components, data flow, project structure, Docker Compose setup, and starter API server.

The production web version is a Vercel-compatible Python API with a static browser UI. The original Streamlit implementation remains in [`app.py`](./app.py) for local experimentation.

## Features

- Upload PNG, JPG, or JPEG architecture sketches.
- Choose a target backend:
  - FastAPI (Python) + Docker
  - Express.js (Node.js) + Docker
  - Go (Gin) + Docker
- Generate:
  - Detected architecture components and data flows
  - Mermaid.js flowchart code
  - Repository directory structure
  - Starter `docker-compose.yml`
  - Core API server stub
- View the generated result directly in the Streamlit interface.

## Requirements

- Python 3.10 or later
- A Google GenAI API key with access to the configured Gemma model

## Local Vercel-compatible version

1. Clone the repository:

   ```bash
   git clone https://github.com/VigneshPillai-lgtm/gem.git
   cd gem
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, use:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your API key:

   ```bash
   export GOOGLE_API_KEY="your-api-key"
   ```

   On Windows PowerShell:

   ```powershell
   $env:GOOGLE_API_KEY = "your-api-key"
   ```

5. Start the API locally with your preferred WSGI server, or deploy it to Vercel:

   ```bash
   flask --app api.index run
   ```

The browser UI is in [`public/index.html`](./public/index.html). Vercel serves it at `/` and routes generation requests to [`api/index.py`](./api/index.py).

## Streamlit version

To run the original Streamlit interface:

```bash
streamlit run app.py
```

## Configuration

The application creates a Google GenAI client using the environment configured for the Google GenAI SDK. Keep API keys out of source control and do not commit `.env` files.

The model is currently configured in [`app.py`](./app.py) as:

```text
gemma-4-26b-a4b-it
```

If your account uses a different model identifier, update the `model` value in `app.py`.

## How it works

1. Streamlit receives the uploaded image.
2. The selected backend framework is included in an architecture-focused prompt.
3. The image and prompt are sent to the Google GenAI client.
4. The generated architecture analysis and starter code are rendered as Markdown.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Security notes

- Store credentials in environment variables or a local secret manager.
- Never commit API keys, tokens, or uploaded diagrams containing confidential information.
- Treat generated infrastructure and code as starter material: review it before using it in production.

## Troubleshooting

### The app cannot create a GenAI client

Verify that `GOOGLE_API_KEY` is set in the same shell used to start Streamlit and that the key has access to the configured model.

### Image upload fails

Use a supported PNG, JPG, or JPEG file and verify that the file is not corrupted.

### Generation returns an error

Check the Streamlit terminal output, confirm network access, and verify that the configured model name is available to your account.

## License

No license has been selected yet. Add a license before distributing this project.
