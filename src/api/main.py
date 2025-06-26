from fastapi import FastAPI

app = FastAPI(title="Realtime Fact Checker")

@app.get("/ping")
def ping():
    return {"status": "ok"}
