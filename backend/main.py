from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "TrustChain AI Backend Running"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "File uploaded successfully"
    }