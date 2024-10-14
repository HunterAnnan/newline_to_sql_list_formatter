from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QDialog, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

def spreadsheet_to_sql_list(raw_lines, use_single_quotes=False):
    lines = [line for line in raw_lines.strip().splitlines() if line.strip()]
    
    formatted_lines = ""
    quote_char = "'" if use_single_quotes else '"'
    for line in lines:
        formatted_lines += f'{quote_char}{line}{quote_char},\n'
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

        button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Submit", self)
        button_layout.addWidget(self.submit_button)

        # Add toggle button for quotes, default to double quotes
        self.toggle_button = QPushButton('"', self)
        self.toggle_button.setStyleSheet("background-color: #4d8a58; color: white;")  # Green color for double quotes
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.setFont(QFont('Helvetica', 16, QFont.Bold))
        button_layout.addWidget(self.toggle_button)

        self.toggle_button.setToolTip("Currently using double quotes")

        self.toggle_button.clicked.connect(self.toggle_quotes)

        layout.addLayout(button_layout)

        self.submit_button.clicked.connect(self.show_output_window)

        self.use_single_quotes = False  # Default to double quotes

        self.setLayout(layout)

    def toggle_quotes(self):
        self.use_single_quotes = not self.use_single_quotes
        
        # Change the button text, color, and tooltip based on the current state
        if self.use_single_quotes:
            self.toggle_button.setText("'")
            self.toggle_button.setStyleSheet("background-color: #4092a8; color: white;")  # Blue color for single quotes
            self.toggle_button.setToolTip("Currently using single quotes")
        else:
            self.toggle_button.setText('"')
            self.toggle_button.setStyleSheet("background-color: #4d8a58; color: white;")  # Green color for double quotes
            self.toggle_button.setToolTip("Currently using double quotes")
            

    def show_output_window(self):
        # Get the content from the text edit
        text_content = self.text_edit.toPlainText()

        line_count, processed_text = spreadsheet_to_sql_list(text_content, use_single_quotes=self.use_single_quotes)

        self.output_window = OutputWindow(line_count, processed_text, self.use_single_quotes)
        self.output_window.show()

    def keyPressEvent(self, event):
        # Check for Cmd+Enter on macOS or Ctrl+Enter on other platforms
        if event.key() == Qt.Key_Return and (event.modifiers() & Qt.MetaModifier):  # Cmd+Enter on macOS
            self.show_output_window()
        elif event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):  # Ctrl+Enter on Windows/Linux
            self.show_output_window()

class OutputWindow(QDialog):
    def __init__(self, line_count, processed_text, use_single_quotes):
        super().__init__()

        self.setWindowTitle("Output")
        self.setGeometry(200, 250, 280, 400)

        layout = QVBoxLayout()

        self.line_count_label = QLabel(f"{line_count} lines detected", self)
        layout.addWidget(self.line_count_label)

        self.text_display = QTextEdit(self)
        self.text_display.setText(processed_text)
        self.text_display.setReadOnly(True)  # Make the text non-editable
        layout.addWidget(self.text_display)
        
        self.copy_button = QPushButton("Copy", self)
        layout.addWidget(self.copy_button)

        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.setLayout(layout)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_display.toPlainText())
        self.accept()  # Close the window after copying

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the application window
    window = TextInputApp()
    window.show()

    # Start the application loop
    sys.exit(app.exec())
