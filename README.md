# Realtime Fact Checker

This project provides a pipeline for detecting factual claims in YouTube videos,
searching for supporting or refuting evidence on the web and returning a score
for each claim. It can be used as a command line tool or through the provided
FastAPI service.

## Features

- Extract transcripts from YouTube videos
- Detect factual claims using the OpenAI API
- Retrieve search results via the Bing Search API
- Score each claim with large language model reasoning
- Export results as WebVTT captions or JSON

## Setup

1. **Install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API keys**

Copy `.env.example` to `.env` and fill in your API credentials.
These variables are used by the CLI and API server.

```bash
cp .env.example .env
# edit .env and set the keys
```

Required keys:

- `YOUTUBE_API_KEY` – YouTube Data API key for fetching transcripts
- `OPENAI_API_KEY` – OpenAI API key for claim detection and scoring
- `BING_API_KEY` – Bing Search API key for snippet retrieval

## Usage

### Command Line

Run a fact check on a YouTube URL and output a WebVTT file:

```bash
python cli/factcheck.py factcheck "https://www.youtube.com/watch?v=VIDEO_ID" --out result.vtt
```

API keys will be read from the environment, but you can also pass them
explicitly:

```bash
python cli/factcheck.py factcheck URL --out result.vtt \
  --youtube-key XXX --openai-key YYY --bing-key ZZZ
```

### API Server

Start the API using Uvicorn:

```bash
uvicorn src.api.main:app --reload
```

Send a POST request to `/factcheck` with a JSON body:

```json
{"youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"}
```

The response contains the detected claims with evidence and scores.

### Docker

A minimal `Dockerfile` is provided. Build and run the container:

```bash
docker build -t factchecker .
docker run -p 8000:8000 --env-file .env factchecker
```

## Development

Run the test suite with `pytest`:

```bash
pytest
```

Contributions are welcome!
