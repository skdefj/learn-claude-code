import logging
import os
import sys

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        #logging.StreamHandler(sys.stdout), 
        logging.FileHandler(os.path.join('.', 'lcc.log'), encoding='utf-8') 
    ]
)
logging.getLogger("anthropic").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)