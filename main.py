from fastapi import FastAPI
from twitter_sentiment import main

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": True}


@app.get("/hello")
def hello_world(test):
    return {"message": "Hello World!!", "test": test}


@app.get("/items/{item_id}")
def get_items(item_id, q):
    return {"item_id": item_id, "q": q}


@app.get("/twitter_sentiment")
def get_twitter_sentiment(location=None, search_term=None):
    return main(location, search_term)
