from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from src.utils.config import APP_NAME, VERSION, API_SECRET_KEY, SUPABASE
from src.utils.models import PredictionRespond
from src.utils.inference import classify_fmnist

app = FastAPI(title=APP_NAME, version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    
)

@app.get('/', tags=['check'])
async def home():
    
    return {
        'message': "Up & Running"
    }
    

api_key_header = APIKeyHeader(name="X-API-KEY")
async def verify_api_key(api_key: str=Depends(api_key_header)):
    if api_key != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="You are not authorized to use this API")
    return api_key

    
@app.post("/classify",tags=['NN'], response_model=PredictionRespond)
async def classify(file: UploadFile, api_key: str=Depends(verify_api_key)):
    
    
    # async function (called by await)
    try:
        contents = await file.read()
        response = classify_fmnist(contents)
        return PredictionRespond(**response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making predictions: {str(e)}")


@app.get("/logs", tags=['analytics'])
async def get_logs(api_key: str = Depends(verify_api_key)):
    """
    Returns every logged prediction (success + failure) from Supabase,
    newest first. Used by the frontend's Usage Analytics page.
    Protected by the same X-API-KEY as /classify.
    """
    if SUPABASE is None:
        raise HTTPException(
            status_code=503,
            detail="Logging is not configured on this server (missing Supabase credentials)."
        )

    try:
        result = (
            SUPABASE.table("predictions_log")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return {"count": len(result.data), "logs": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")