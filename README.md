# Fashion Assistant

Fashion Assistant is an AI-powered Streamlit application that helps users discover and explore fashion items. It uses advanced machine learning models to provide personalized recommendations based on user inputs, including text queries and image uploads.

## Demo

[Project Demo Video](fashion_trend/assets/demo.mp4)
<!-- <video width="1820" height="720" controls>
  <source src="fashion_trend/assets/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video> -->


## Features

- Text-based search for fashion items
- Image-based similar item search
- Personalized recommendations based on purchase history
- Integration with CLIP model for efficient image and text embeddings
- Responsive UI with a chat-like interface

## Prerequisites

- Python 3.10
- Conda
- Poetry
- Google's Generative AI API
- CLIP model

## Setup Guide

1. Clone the repository:
   ```
   git clone https://github.com/your-username/fashion-assistant.git
   cd fashion-assistant
   ```

2. Create a Conda environment:
   ```
   conda create -n fashion-assistant python=3.10
   conda activate fashion-assistant
   ```

3. Install Poetry (if not already installed):
   ```
   pip install poetry
   ```

4. Install project dependencies using Poetry:
   ```
   poetry install
   ```

5. Set up the environment variables:
   - Rename `.envexample` to `.env`
   - Add your Google API key to the `.env` file:
     ```
     API_KEY=your_google_api_key_here
     ```

6. Download and set up the CLIP model:
   - Download the CLIP model from https://huggingface.co/openai/clip-vit-large-patch14 and place it in the `./CLIP` directory

7. Prepare the vector database:
   - Ensure the vector database file is present at `./data/app_data/vector_indices/vector_db.pkl`

8. Run the Streamlit app:
   ```
   poetry run streamlit run app.py
   ```

9. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`)

## Usage

1. Use the chat interface to ask questions about fashion items or request recommendations.
2. Upload images to find similar fashion items.
3. Explore the personalized recommendations based on your interactions.
