from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

# the "bind" param will pretty much point to the engine that has all the required info of the database in database.py
models.Base.metadata.create_all(bind=engine)

