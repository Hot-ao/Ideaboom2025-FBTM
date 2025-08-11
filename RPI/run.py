from threading import Thread
from network.sender import run_all_senders
from app import create_app

app = create_app()

if __name__ == "__main__":
    t = Thread(target=run_all_senders, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000)