from fastapi import FastAPI, BackgroundTasks
from typing import Dict
import dataProcessing

app = FastAPI()

@app.post("/data/")
async def receive_json(data: Dict, background_tasks: BackgroundTasks):
    print(f"Received data: {data}")
    # Schedule the data processing task to run in the background
    background_tasks.add_task(dataProcessing.insert_data, dict(data))
    return {"message": "Data received", "data": data}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.0.34", port=8000)