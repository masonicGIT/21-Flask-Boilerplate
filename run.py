from app import app
import os

app.secret_key = os.urandom(24)
if __name__ == '__main__':
    app.run()
