import pyperclip
import PySide6

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

def spreadsheet_to_sql_list(raw_lines):
    lines = [line for line in raw_lines.strip().splitlines() if line.strip()]
    
    formatted_lines = ""
    for line in lines:
        formatted_lines += f'"{line}",\n'
    if formatted_lines:
        formatted_lines = formatted_lines[:-2]

    return len(lines), formatted_lines

class TextInputApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 200, 280, 400)
        
        # Layout & Populate
        layout = QVBoxLayout()
    
        self.title = QLabel("Reformat List", self)
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        title_font = QFont()
        title_font.setFamily("Helvetica")
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Normal)

        self.title.setFont(title_font)
        
        self.label = QLabel("Newline delimited \u2192 SQL-friendly", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        
        label_font = QFont()
        label_font.setFamily("Helvetica")
        label_font.setWeight(QFont.Light)

        self.label.setFont(label_font)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Enter or paste newline delimited list...")

        layout.addWidget(self.text_edit)
        
        self.submit_button = QPushButton("Submit", self)
        layout.addWidget(self.submit_button)
        
        self.submit_button.clicked.connect(self.show_output_window)

        self.setLayout(layout)

    def show_output_window(self):
        # Get the content from the text edit
        text_content = self.text_edit.toPlainText()

        line_count, processed_text = spreadsheet_to_sql_list(text_content)

        self.output_window = OutputWindow(line_count, processed_text)
        self.output_window.show()

    def keyPressEvent(self, event):
        # Check for Cmd+Enter on macOS or Ctrl+Enter on other platforms
        if event.key() == Qt.Key_Return and (event.modifiers() & Qt.MetaModifier):  # Cmd+Enter on macOS
            self.show_output_window()
        elif event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):  # Ctrl+Enter on Windows/Linux
            self.show_output_window()

class OutputWindow(QDialog):
    def __init__(self, line_count, processed_text):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Output")
        self.setGeometry(200, 250, 280, 400)

        # Create layout
        layout = QVBoxLayout()

        # Create a label to display the line count
        self.line_count_label = QLabel(f"{line_count} lines detected", self)
        layout.addWidget(self.line_count_label)

        # Create a text edit to display the processed text (non-editable)
        self.text_display = QTextEdit(self)
        self.text_display.setText(processed_text)
        self.text_display.setReadOnly(True)  # Make the text non-editable
        layout.addWidget(self.text_display)
        
        # Add a copy button
        self.copy_button = QPushButton("Copy", self)
        layout.addWidget(self.copy_button)
        
        # Connect the copy button to an action
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Set the layout
        self.setLayout(layout)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_display.toPlainText())

        self.accept() # Close the window after copying

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the application window
    window = TextInputApp()
    window.show()

    # Start the application loop
    sys.exit(app.exec())