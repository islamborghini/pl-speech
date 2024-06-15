import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
from PyQt5 import QtWidgets, QtCore

class TranslatorApp(QtWidgets.QWidget):
    def __init__(self, model, record_timeout, phrase_timeout, max_display_time):
        super().__init__()
        self.initUI()
        
        self.phrase_time = None
        self.data_queue = Queue()
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = 1000
        self.recorder.dynamic_energy_threshold = False
        
        self.source = sr.Microphone(sample_rate=16000)
        self.audio_model = whisper.load_model(model)
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.max_display_time = max_display_time
        self.transcription = []
        self.timestamps = []
        self.translator = GoogleTranslator(source='en', target='pl')

        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        
        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_text_widget)
        self.timer.start(100)

    def initUI(self):
        self.setWindowTitle('English to Polish Translator')
        self.showFullScreen()
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("QTextEdit { background-color : black; color : white; font-size: 64px; }")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def record_callback(self, _, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        self.data_queue.put(data)

    def update_text_widget(self):
        now = datetime.utcnow()
        
        # Remove old lines
        while self.timestamps and now - self.timestamps[0] > timedelta(seconds=self.max_display_time):
            self.timestamps.pop(0)
            self.transcription.pop(0)
        
        if not self.data_queue.empty():
            phrase_complete = False
            if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                phrase_complete = True
            self.phrase_time = now

            audio_data = b''.join(self.data_queue.queue)
            self.data_queue.queue.clear()

            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            result = self.audio_model.transcribe(audio_np, fp16=torch.cuda.is_available(), language='en')
            text = result['text'].strip()
            translated_text = self.translator.translate(text)

            if phrase_complete:
                self.transcription.append(translated_text)
                self.timestamps.append(now)
            else:
                if self.transcription:
                    self.transcription[-1] += " " + translated_text
                else:
                    self.transcription.append(translated_text)
                    self.timestamps.append(now)

            self.text_edit.setText("\n".join(self.transcription))
            self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--record_timeout", default=2, help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3, help="How much empty space between recordings before we consider it a new line in the transcription.", type=float)
    parser.add_argument("--max_display_time", default=30, help="Maximum time (in seconds) to display text before removing it.", type=int)
    args = parser.parse_args()

    app = QtWidgets.QApplication([])
    ex = TranslatorApp(args.model, args.record_timeout, args.phrase_timeout, args.max_display_time)
    app.exec_()

if __name__ == "__main__":
    main()
