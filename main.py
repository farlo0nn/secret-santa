import sys 


from bot.application import run_application
from db.models import update_models
from loguru import logger

def main():
    if "--update-db" in sys.argv:
        update_models()
        print("called")

    logger.add("log.log", format="{level}|{message}")
    run_application()

if __name__ == '__main__':
    main()