import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(
    page_title="CodeSketch-AI | Gemma 4",
    page_icon="📐",
    layout="wide"
)

client = genai.Client()

st.title("📐 CodeSketch-AI: Visual Architecture to Code Scaffolder")
st.caption("Powered by Google Gemma 4 (`gemma-4-26b-a4b-it`) for MLH Hacktoberfest Hack Day 2026")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Upload Hand-Drawn Architecture")
    uploaded_image = st.file_uploader(
        "Upload a photo of a whiteboard or paper diagram:", 
        type=["jpg", "jpeg", "png"]
    )
    
    stack_preference = st.selectbox(
        "Target Backend Framework:",
        ["FastAPI (Python) + Docker", "Express.js (Node.js) + Docker", "Go (Gin) + Docker"]
    )
    
    generate_btn = st.button("🚀 Scaffold Project with Gemma 4", type="primary", use_container_width=True)

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Architecture Sketch", use_container_width=True)

with col2:
    st.subheader("🛠️ Generated Architecture & Boilerplate")
    
    if generate_btn:
        if not uploaded_image:
            st.error("Please upload an image of a sketched system diagram.")
        else:
            with st.spinner("Gemma 4 is inspecting system diagram components and data flows..."):
                prompt = f"""
You are CodeSketch-AI, an expert Principal Software Architect.
Analyze the hand-drawn system design or architectural diagram in the provided image.
The user wants to scaffold this using: {stack_preference}.

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
                try:
                    contents = [prompt, image]
                    response = client.models.generate_content(
                        model="gemma-4-26b-a4b-it",
                        contents=contents
                    )
                    st.markdown(response.text)
                    st.success("Scaffold completed live using Gemma 4 Multimodal API!")
                except Exception as e:
                    st.error(f"Error calling Gemma 4: {e}")