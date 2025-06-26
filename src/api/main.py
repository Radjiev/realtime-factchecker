from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.utils.youtube import get_transcript
from src.pipeline.claim_detector import ClaimDetector
from src.pipeline.retriever import search
from src.pipeline.scorer import FactCheckScorer

import os

app = FastAPI(title="Realtime Fact Checker")


class FactcheckRequest(BaseModel):
    youtube_url: str


class Evidence(BaseModel):
    url: str
    snippet: str


class FactcheckResult(BaseModel):
    claim: str
    label: str
    confidence: float
    evidence: List[Evidence]


class FactcheckResponse(BaseModel):
    results: List[FactcheckResult]

@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/factcheck", response_model=FactcheckResponse)
def factcheck(req: FactcheckRequest):
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    bing_key = os.getenv("BING_API_KEY")
    if not all([youtube_key, openai_key, bing_key]):
        raise HTTPException(status_code=500, detail="API keys not configured")

    video_id = req.youtube_url.split("v=")[-1]
    transcript = get_transcript(video_id, youtube_key) or ""
    detector = ClaimDetector(api_key=openai_key)
    claims = detector.detect(transcript)

    scorer = FactCheckScorer(api_key=openai_key)
    results: List[FactcheckResult] = []
    for claim in claims:
        retrieved = search(claim, api_key=bing_key)
        snippets = [r["snippet"] for r in retrieved]
        score = scorer.score(claim, snippets)
        evidence = [Evidence(**r) for r in retrieved]
        results.append(
            FactcheckResult(
                claim=claim,
                label=score.get("label", "unverified"),
                confidence=float(score.get("confidence", 0)),
                evidence=evidence,
            )
        )

    return FactcheckResponse(results=results)
