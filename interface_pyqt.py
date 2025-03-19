import sys
import json
import os
import translators as ts
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, \
    QRadioButton, QTextEdit, QFormLayout, QMessageBox


class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up window properties
        self.setWindowTitle("Text Translator")
        self.setGeometry(100, 100, 500, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Input text field
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text to translate...")
        main_layout.addWidget(self.text_input)

        # Language selection dropdown
        self.language_dropdown = QComboBox(self)
        self.language_dropdown.addItems(['en', 'fr', 'es', 'de', 'zh', 'ja'])
        main_layout.addWidget(self.language_dropdown)

        # Translate button
        translate_button = QPushButton("Translate", self)
        translate_button.clicked.connect(self.translate_text)
        main_layout.addWidget(translate_button)

        # Batch translation button
        batch_button = QPushButton("Batch Translate", self)
        batch_button.clicked.connect(self.batch_translate)
        main_layout.addWidget(batch_button)

        # Result display
        self.result_label = QLabel("Translated text will appear here.", self)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.result_label)

        # Feedback button
        feedback_button = QPushButton("Provide Feedback", self)
        feedback_button.clicked.connect(self.show_feedback_form)
        main_layout.addWidget(feedback_button)

        # Feedback form (hidden initially)
        self.feedback_form = QWidget(self)
        feedback_form_layout = QFormLayout()

        # Feedback radio buttons
        self.feedback_radio_group = {}
        issues = [
            "Translation is too complex.",
            "The translation lacks cultural adaptation and makes me confused.",
            "The translation has grammatical errors.",
            "The translation is overly literal and I can not understand.",
            "The translation misinterprets context-specific terms.",
            "Other (please specify below)"
        ]

        for issue in issues:
            radio_button = QRadioButton(issue, self)
            feedback_form_layout.addRow(radio_button)
            self.feedback_radio_group[issue] = radio_button

        # Additional comments box
        self.comments_box = QTextEdit(self)
        self.comments_box.setPlaceholderText("Additional comments...")
        feedback_form_layout.addRow("Additional Comments:", self.comments_box)

        # Submit button
        submit_button = QPushButton("Submit Feedback", self)
        submit_button.clicked.connect(self.submit_feedback)
        feedback_form_layout.addRow(submit_button)

        self.feedback_form.setLayout(feedback_form_layout)

        # Hide feedback form by default
        self.feedback_form.setVisible(False)

        # Add feedback form to layout
        main_layout.addWidget(self.feedback_form)

        # Set main layout
        self.setLayout(main_layout)

    def translate_text(self):
        input_text = self.text_input.text()
        target_language = self.language_dropdown.currentText()
        if not input_text:
            self.show_message("Warning", "Please enter text to translate.")
            return

        try:
            translation = ts.translate_text(input_text, to_language=target_language)
            self.result_label.setText(f"Translated Text: {translation}")
        except Exception as e:
            self.show_message("Error", f"Translation failed: {e}")

    def batch_translate(self):
        target_language = self.language_dropdown.currentText()
        try:
            phrases = self.load_phrases()
            result = [ts.translate_text(phrase, to_language=target_language, sleep_seconds=5)
                      for phrase in phrases.values()]
            self.result_label.setText(f"Batch Translations: {result}")
        except Exception as e:
            self.show_message("Error", f"Batch translation failed: {e}")

    def show_feedback_form(self):
        self.feedback_form.setVisible(True)

    def submit_feedback(self):
        selected_issue = None
        for issue, radio_button in self.feedback_radio_group.items():
            if radio_button.isChecked():
                selected_issue = issue
                break

        additional_comments = self.comments_box.toPlainText()

        if not selected_issue:
            self.show_message("Warning", "Please select an issue.")
            return

        print(f"Feedback Submitted: {selected_issue}, Comments: {additional_comments}")
        self.show_message("Thank You", "Feedback received, thank you for your help!")

        # Hide feedback form after submission
        self.feedback_form.setVisible(False)

    def load_phrases(self):
        filepath = os.path.join(os.path.dirname(__file__), "i18n/en.json")
        if not os.path.exists(filepath):
            raise FileNotFoundError("Translation file not found.")
        with open(filepath, "r") as i18n_file:
            return json.load(i18n_file)

    # display a popup message box showing the user the specified title and message content
    def show_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())