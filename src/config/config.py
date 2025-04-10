import os
from dotenv import load_dotenv
load_dotenv()

configuration = {
    "AWS_ACCESS_KEY": os.getenv('AWS_ACCESS_KEY_ID'),
    "AWS_SECRET_KEY": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "OPENROUTE_KEY" : os.getenv('OPENROUTE_KEY')
}
