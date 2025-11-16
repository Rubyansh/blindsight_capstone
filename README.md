# Blind Vision Assistant

I created this AI-powered image description service for my **AI Capstone Project 2025**. It's a web and CLI application that helps visually impaired users by describing images and converting those descriptions to speech.

## What This Does

This is my take on building an accessible AI assistant for the visually impaired. The application combines computer vision and text-to-speech to:

- **Image Analysis** — Uses the LLaVA model to generate objective, concise descriptions of images
- **Text-to-Speech** — Converts the descriptions into natural-sounding audio
- **Web Interface** — Provides a user-friendly web app with drag-and-drop image upload
- **CLI Tool** — Works as a command-line tool for developers
- **RESTful API** — JSON API for integration with other applications
- **Accessibility Focus** — Designed specifically for visually impaired users with clear, objective descriptions

## Tech Behind the Assistant

Built using:

- **Python 3.8+** with async/await for concurrent tasks
- **Flask** for the web framework and API
- **Ollama** with the LLaVA model for image analysis
- **Edge-TTS** for text-to-speech
- **Custom CSS** for accessibility and responsive UI

## How To Set It Up

The project uses a `config.py` file where you can configure:

- Ollama model and parameters
- TTS voice and speed
- File upload settings
- Description style and verbosity

## How to Use It

After starting the server:

- **Web Interface:** Upload an image to receive a description + audio
- **CLI Tool:** Process images from the terminal
- **REST API:** Integrate using JSON responses
- **Audio Download:** Save audio descriptions for offline use

## RESTful API

### `POST /api/describe`

Upload an image and receive a JSON response containing the description and audio URL.

**Request:**

```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/api/describe
```

**Response:**

```json
{
  "success": true,
  "description": "A red car parked in front of a modern building with glass windows...",
  "image_url": "/static/uploads/photo_20241201_143022.jpg",
  "audio_url": "/audio/description_20241201_143022.mp3"
}
```

**Features:**

- Supports `multipart/form-data` uploads
- Returns structured JSON
- Proper HTTP status codes for errors
- File validation and 16MB upload limit

## Current Status

This was my submission for the **AI Capstone Project 2025** and is currently in the **proof-of-concept stage**. It showcases how to build a full-stack AI application focused on accessibility.

## Why I Built It This Way

- **Accessible** — Designed specifically for visually impaired users
- **Modular** — Vision, TTS, and Web layers separated
- **User-Friendly** — Simple UI + CLI
- **Extensible** — Easy to add new features
- **API-First** — REST endpoints for integration

## License

Licensed under the **GNU AGPL 3.0**. Feel free to explore, modify, and improve — just share modifications under the same license.

---
