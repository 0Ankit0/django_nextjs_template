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
        """Start the frontend dev server in a separate terminal window."""
        self.stdout.write(self.style.SUCCESS("Starting frontend in new terminal..."))

        # Get the project root (parent of backend directory)
        frontend_dir = os.path.join(os.path.dirname(settings.BASE_DIR), "frontend")

        # Open frontend in a new macOS Terminal tab
        # This prevents the reload events from interfering with Django
        applescript = f"""
        tell application "Terminal"
            do script "cd {frontend_dir} && npm run dev"
            activate
        end tell
        """

        self.frontend_process = subprocess.Popen(
            ["osascript", "-e", applescript],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
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

        try:
            # More reliable way to kill the process on port 3000 (Next.js)
            # This handles cases where the terminal window closes but the process remains
            cmd = "lsof -ti:3000 | xargs kill -9"
            subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except Exception:
            pass  # Ignore errors during cleanup, e.g. if nothing is running

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C and kill signals."""
        self.stop_frontend()
        # Re-raise KeyboardInterrupt so Django's runserver exits cleanly
        raise KeyboardInterrupt
