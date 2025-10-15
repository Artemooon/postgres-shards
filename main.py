import uvicorn
from fastapi import FastAPI

from routes.url_routes import urls_router

app = FastAPI()


app.include_router(urls_router, prefix="/urls")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
