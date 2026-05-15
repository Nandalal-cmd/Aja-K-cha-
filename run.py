"""Run both the backend server and the Streamlit frontend simultaneously."""
import subprocess
import sys
import signal
import os

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("=" * 60)
    print("🔥 Aaj K Garne? - Starting the app...")
    print("=" * 60)
    print()
    print("  Backend API : http://localhost:8000")
    print("  Frontend    : http://localhost:8501")
    print("  API Docs    : http://localhost:8000/docs")
    print()

    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=BACKEND_DIR,
    )

    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"],
        cwd=BACKEND_DIR,
    )

    def shutdown(sig, frame):
        print("\nShutting down...")
        backend.terminate()
        frontend.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
