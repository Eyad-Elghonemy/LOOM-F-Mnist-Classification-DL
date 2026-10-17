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

    Note: the frontend's own check_api_key() already treats a 503 here
    as "key accepted, logging just isn't available" -- it does NOT
    lock the user out of /classify over this, by design. So unlike the
    other two backends, this one doesn't need a static fallback
    dataset: a bounded 503 (via the timeout in config.py) is enough to
    keep /classify fully usable while Supabase is asleep.
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
        raise HTTPException(
            status_code=503,
            detail=f"Logs are temporarily unavailable (database unreachable): {str(e)}"
        )
