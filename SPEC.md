# DpForge - Display Picture Forge

**Creative name**: DpForge (Display Picture Forge)

**Tagline**: "Forge your perfect avatar in seconds"

## Concept & Vision

DpForge is a sleek, local-first web application that generates unique display pictures (DPs) for online accounts, messengers, and social profiles. It leverages local AI models via Ollama to create artistic avatars without sending data to external servers. The experience feels like using a magical forge - enter a simple description, watch the creation unfold, and download your perfect avatar.

## Design Language

- **Aesthetic**: Dark forge theme with ember/fire accents - industrial yet magical
- **Color Palette**:
  - Background: `#0d0d0d` (deep black)
  - Surface: `#1a1a1a` (dark gray)
  - Primary: `#ff6b35` (ember orange)
  - Secondary: `#f7c59f` (warm cream)
  - Accent: `#2ec4b6` (teal glow)
  - Text: `#e8e8e8` (soft white)
- **Typography**: 
  - Headings: Orbitron (futuristic, forge-like)
  - Body: Inter (clean, readable)
- **Motion**: Glowing pulse animations, smooth fade-ins, ember particle effects on generation
- **Icons**: Lucide icons for consistency

## Layout & Structure

- **Single-page app** with centered card layout
- Hero section with animated logo and tagline
- Main generation card with:
  - Text prompt input with example suggestions
  - Style preset buttons (Cartoon, Realistic, Abstract, Anime)
  - Generate button with loading animation
  - Image preview with download option
- Footer with Ollama status indicator

## Features & Interactions

1. **Prompt Input**: Text field with placeholder suggestions like "a cat", "space explorer", "forest spirit"
2. **Style Presets**: Quick-select buttons to enhance prompts with style keywords
3. **Generation**: Calls Ollama's image generation endpoint, shows progress animation
4. **Preview**: Displays generated image with smooth fade-in
5. **Download**: One-click download as PNG
6. **Ollama Status**: Shows connection status with visual indicator

## Technical Approach

- **Backend**: Python FastAPI server
- **Frontend**: Vanilla HTML/CSS/JS (no framework needed)
- **AI Integration**: Ollama with image generation models (stable-diffusion, llama-image)
- **API**: REST endpoints for generation and status check
- **File output**: Generated images saved locally and served via API

## API Endpoints

- `GET /api/status` - Check Ollama connection status
- `POST /api/generate` - Generate image from prompt
- `GET /api/image/{filename}` - Serve generated image
