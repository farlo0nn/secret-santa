import sys 


from app.bot.application import run_application
from db.services import check_db_status, update_models

def app():
    if "--update-db" in sys.argv:
        update_models()
        print("Updated Database")
    if not (status := check_db_status()).valid():
        raise Exception(status)
    run_application()

if __name__ == '__main__':
    app()