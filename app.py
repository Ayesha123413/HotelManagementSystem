from fastapi import FastAPI, status;
from decouple import config;
from supabase import create_client,Client;
import random

url=config("SUPABASE_URL")
key=config("SUPABASE_KEY")
jwt=config("SUPABASE_JWT_SECRET")

app=FastAPI()
supabase : Client =create_client(url,key)
id=random.randint(0,100)