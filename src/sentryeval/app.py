from fastapi import FastAPI

app = FastAPI(title="SentryEval")

@app.get("/")
def root():
    return {"status": "ok", "service": "SentryEval"}

@app.get("/health")
def health():
    return {"healthy": True}