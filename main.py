import platform
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.voicehat
from google.assistant.library.event import EventType
import socket
import subprocess

# This file is based from the code at
# https://github.com/google/aiyprojects-raspbian/blob/aiyprojects/src/examples/voice/assistant_library_demo.py
# and is not entirely written by me. It is necessary to copy the code in order to use the Google Assistant API
# with the raspberry pi hardware.

def process_command(command: str):
    command = command.lower()
    if command == "Ip address":
        aiy.audio.say(str(socket.gethostbyname(socket.gethostname())))
    elif command == "shutdown":
        aiy.audio.say("You have no power over me")
    elif command == "sudo shutdown" :
        aiy.audio.say("Bye bye!")
        subprocess.call('sudo shutdown now', shell=True)

def process_event(assistant, event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args :
        command = event.args["text"].lower()
        process_command(command)

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

def main():
    credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, event)


if __name__ == '__main__':
    main()