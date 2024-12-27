from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.post("/data/")
async def receive_json(data: Dict):
    print(f"Received data: {data}")
    # Make dictionary with data
    dict_data = dict(data)
    return {"message": "Data received", "data": data}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.0.34", port=8000)