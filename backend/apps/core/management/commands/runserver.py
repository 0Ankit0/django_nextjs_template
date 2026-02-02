import atexit
import os
import signal
import subprocess

from django.conf import settings
from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    frontend_process = None

    def handle(self, *args, **options):
        # CRITICAL: Only start in the parent process, NOT in the reloader child
        # When RUN_MAIN is "true", we're in the reloader child process
        is_reloader_child = os.environ.get("RUN_MAIN") == "true"

        if not is_reloader_child:
            self.start_frontend()
            # Ensure cleanup happens even on crash/exit
            atexit.register(self.stop_frontend)
            # Handle Ctrl+C properly
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            super().handle(*args, **options)
        finally:
            # Cleanup when server stops
            if not is_reloader_child:
                self.stop_frontend()

    def start_frontend(self):
        """Start the frontend dev server."""
        self.stdout.write(self.style.SUCCESS("Starting frontend (npm run dev)..."))

        # Get the project root (parent of backend directory)
        frontend_dir = os.path.join(os.path.dirname(settings.BASE_DIR), "frontend")

        # Use shell=True on Windows if needed, but list args are safer on Unix
        # npm start or npm run dev depending on your package.json scripts
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdin=subprocess.DEVNULL,
            # Optional: pipe output to avoid mixing with Django logs in the same terminal
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL,
        )

    def stop_frontend(self):
        """Stop the frontend dev server."""
        if self.frontend_process and self.frontend_process.poll() is None:
            self.stdout.write(self.style.WARNING("Stopping frontend..."))

            # Terminate gracefully first
            self.frontend_process.terminate()

            try:
                # Wait up to 5 seconds for graceful shutdown
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't stop
                self.frontend_process.kill()
                self.frontend_process.wait()

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C and kill signals."""
        self.stop_frontend()
        # Re-raise KeyboardInterrupt so Django's runserver exits cleanly
        raise KeyboardInterrupt
