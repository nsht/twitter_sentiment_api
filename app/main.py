from fastapi import FastAPI
from twitter_sentiment import main
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": True}


@app.get("/items/{item_id}")
def get_items(item_id, q):
    return {"item_id": item_id, "q": q}


@app.get("/twitter_sentiment")
def get_twitter_sentiment(location=None, search_term=None):
    print(search_term)
    return main(location, search_term)
