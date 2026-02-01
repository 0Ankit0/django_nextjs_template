import os
import platform
import subprocess

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    help = "Starts the Django development server and the Next.js frontend in a separate terminal."

    # Track the macOS terminal window/tab to close it on exit
    frontend_process_info = None

    def handle(self, *args, **options):
        # Only start frontend in the main process (not reloader)
        if os.environ.get("RUN_MAIN") != "true":
            self.start_frontend()

        try:
            super().handle(*args, **options)
        finally:
            # This block runs when Ctrl+C is pressed (KeyboardInterrupt)
            # But ONLY in the process catching it.
            # Note: handle() is called in both main and reloader processes.
            # We only want to clean up if we are the one who started it?
            # Actually, typically prompt returns, and variables are lost.
            # But the main process stays alive waiting for the reloader thread/process?
            # No, 'runserver' runs indefinitely.

            if os.environ.get("RUN_MAIN") != "true" and self.frontend_process_info:
                self.stop_frontend()

    def start_frontend(self):
        self.stdout.write(self.style.SUCCESS("Starting Next.js frontend in a new terminal..."))

        frontend_dir = settings.BASE_DIR.parent / "frontend"
        command = f"cd {frontend_dir} && npm run dev"
        system = platform.system()

        try:
            if system == "Darwin":
                # Simplified AppleScript to just get the window ID of the new script
                # 'do script' creates a new window by default if no target is specified
                script = f"""
                tell application "Terminal"
                    do script "{command}"
                    set winId to id of front window
                    return winId
                end tell
                """
                process = subprocess.Popen(
                    ["osascript", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    window_id = stdout.strip()
                    self.frontend_process_info = {"type": "macos_window", "id": window_id}
                    self.stdout.write(f"Frontend started in Terminal Window ID: {window_id}")
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to capture frontend terminal: {stderr}"))

            # Linux/Windows implementations remain similar but hard to track cleanup without PIDs
            elif system == "Linux":
                # Simplified for Linux
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"])

            elif system == "Windows":
                subprocess.Popen(f'start cmd /k "{command}"', shell=True)

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to start frontend: {e}"))

    def stop_frontend(self):
        self.stdout.write(self.style.SUCCESS("Stopping frontend terminal..."))
        if not self.frontend_process_info:
            return

        try:
            if self.frontend_process_info["type"] == "macos_window":
                window_id = self.frontend_process_info["id"]
                # AppleScript to close the specific window
                close_script = f"""
                tell application "Terminal"
                    close window id {window_id}
                end tell
                """
                subprocess.run(["osascript", "-e", close_script], check=False)

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to stop frontend: {e}"))
