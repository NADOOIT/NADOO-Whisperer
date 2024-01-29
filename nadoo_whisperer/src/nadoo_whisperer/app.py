import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import json
import struct
import sys
import threading
from screeninfo import get_monitors


class NADOOWhisperer(toga.App):
    def __init__(self, title, id):
        super().__init__(title, id)
        self.latest_error = ""  # Attribute to hold the latest error message

    def send_message(self, message):
        """Send a message to the browser extension."""
        original_stdout = sys.stdout  # Keep the original stdout
        sys.stdout = sys.__stdout__  # Reassign to the original stdout to access buffer
        try:
            encoded_message = json.dumps(message).encode("utf-8")
            sys.stdout.buffer.write(struct.pack("I", len(encoded_message)))
            sys.stdout.buffer.write(encoded_message)
            sys.stdout.flush()
        finally:
            sys.stdout = original_stdout  # Reassign back to the original stdout

    def receive_message_loop(self):
        """Continuously listen for messages from the browser extension."""
        while True:
            self.receive_message()

    def receive_message(self):
        """Receive a message from the browser extension."""
        try:
            raw_length = sys.stdin.buffer.read(4)
            if not raw_length:
                sys.exit(0)
            message_length = struct.unpack("I", raw_length)[0]
            message = json.loads(sys.stdin.buffer.read(message_length).decode("utf-8"))
            print("Received:", message)

            # Handle the incoming message
            if message.get("command") == "start_recording":
                # Ensure GUI updates happen on the main thread
                toga.App.app._impl.loop.call_soon_threadsafe(
                    self.update_transcription_area, message.get("text", "")
                )

        except Exception as e:
            error_message = f"Failed to receive message: {e}"
            print(error_message)
            self.latest_error = error_message
            # Ensure GUI updates happen on the main thread
            toga.App.app._impl.loop.call_soon_threadsafe(
                self.update_error_area, error_message
            )

    def update_transcription_area(self, text):
        """Update the transcription_area with the received text."""
        self.transcription_area.value = text
        # Clear the error area if the text update is successful
        self.error_area.value = ""

    def update_error_area(self, error_message):
        """Update the error_area with the received error message or logs."""
        self.error_area.value += error_message + "\n"

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Text area for displaying transcribed text
        self.transcription_area = toga.MultilineTextInput(style=Pack(flex=1))
        main_box.add(self.transcription_area)

        # Text area for displaying errors and logs
        self.error_area = toga.MultilineTextInput(style=Pack(flex=1), readonly=True)
        self.error_area.style.bg_color = "lightgrey"  # Optional: Style for error/log area
        main_box.add(self.error_area)

        # Record button
        record_btn = toga.Button("Start Recording", on_press=self.start_recording, style=Pack(padding=5))
        main_box.add(record_btn)

        # Send button
        send_btn = toga.Button("Send Text", on_press=self.send_text, style=Pack(padding=5))
        main_box.add(send_btn)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        # Get the size of the primary monitor
        monitor = get_monitors()[0]
        screen_width, screen_height = monitor.width, monitor.height

        # Calculate half screen width and use full screen height
        half_screen_width = screen_width // 2

        # Set the window size to half of the screen width and full screen height
        self.main_window.size = (half_screen_width, screen_height)

        # Set the window position to the right side of the screen
        self.main_window.position = (half_screen_width, 0)

        self.main_window.show()

    def start_recording(self, widget):
        print("Start recording...")
        # TODO: Integrate with your recording functionality
        self.transcription_area.value = "Transcribed text appears here..."

    def send_text(self, widget):
        print("Sending text...")
        text = self.transcription_area.value
        self.send_message({"command": "send_text", "text": text})

def main():
    # Create an instance of the app
    app = NADOOWhisperer("NADOO Whisperer", "com.nadooit.nadoowhisperer")

    # Start the receive_message_loop in a separate thread
    threading.Thread(target=app.receive_message_loop, daemon=True).start()

    return app

if __name__ == "__main__":
    app = main()
    app.main_loop()  # Enter the Toga application main loop
