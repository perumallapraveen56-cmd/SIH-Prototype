from fastapi import FastAPI

app = FastAPI(title="SIH Prototype API")

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}