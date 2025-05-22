from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()


mongo_uri = "mongodb+srv://saqib:saqib1234@cluster0.rppmgkb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client['user_database']
users_collection = db['users']

class RegisterRequest(BaseModel):
    identifier: str
    password: str

@app.get("/")
async def root():
    return {"message": "API is working"}
    
@app.post("/register")
async def register(data: RegisterRequest):
    identifier = data.identifier
    password = data.password

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Missing identifier or password")

    user_data = {
        'identifier': identifier,
        'password': password
    }

    try:
        users_collection.insert_one(user_data)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # --- Deployment block ---
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
