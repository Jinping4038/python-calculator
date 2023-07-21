import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QLabel
from PyQt6.QtGui import QPalette, QColor, QFont
import math

class BetterCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Best Calculator")

        # Set the color scheme for QLineEdit
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # white
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))  # black text

        self.display = QLineEdit()
        self.display.setFont(QFont('Arial', 16))  # Changed the font size here
        self.display.setPalette(palette)
        self.display.setReadOnly(False)  # Make the display editable

        # Create grid layout
        self.grid = QGridLayout()

        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'BS',
            '1', '2', '3', '-', '(',
            '0', '.', '=', '+', ')',
            'sin', 'cos', 'tan', '%', 'pow'
        ]

        row = 0
        col = 0

        # Add buttons to the grid layout
        for button in buttons:
            btn = QPushButton(button)
            btn.setFixedSize(64, 64)
            btn.setFont(QFont('Arial', 16))
            btn.setStyleSheet("QPushButton{border-radius: 32px; background-color: white;}")

            if button in {'sin', 'cos', 'tan'}:
                btn.clicked.connect(self.append_trig_function)
            elif button == '=':
                btn.clicked.connect(self.evaluate)
            elif button == 'C':
                btn.clicked.connect(self.clear_display)
            elif button == 'BS':
                btn.clicked.connect(self.backspace)
            elif button == 'pow':
                btn.clicked.connect(self.append_power)
            elif button == '%':
                btn.clicked.connect(self.calculate_percent)
            else:
                btn.clicked.connect(self.append_value)

            self.grid.addWidget(btn, row, col, 1, 1)

            col += 1
            if col > 4:  # Change the number here to fit a 5x5 grid
                col = 0
                row += 1

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.display)
        vbox_layout.addLayout(self.grid)
        self.setLayout(vbox_layout)

        # Status Bar
        self.statusBar = QLabel()
        vbox_layout.addWidget(self.statusBar)

    def append_value(self):
        self.statusBar.clear()

        button_text = self.sender().text()
        current_value = self.display.text()
        new_value = current_value + button_text
        self.display.setText(new_value)

    def append_trig_function(self):
        self.statusBar.clear()

        button_text = self.sender().text()
        current_value = self.display.text()
        new_value = current_value + button_text + '('
        self.display.setText(new_value)

    def backspace(self):
        self.statusBar.clear()

        current_value = self.display.text()
        new_value = current_value[:-1]
        self.display.setText(new_value)

    def clear_display(self):
        self.statusBar.clear()
        self.display.clear()

    def evaluate(self):
        try:
            expression = self.display.text()
            # Replace '^' operator with Python's built-in '**' operator
            expression = expression.replace('^', '**')
            result = eval(expression, {'__builtins__': None}, {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'pow': math.pow
            })
            self.display.setText(str(result))
        except Exception as e:
            self.statusBar.setText("Error: " + str(e))

    def append_power(self):
        self.statusBar.clear()

        current_value = self.display.text()
        new_value = current_value + '^'
        self.display.setText(new_value)

    def calculate_percent(self):
        self.statusBar.clear()

        current_value = self.display.text()
        new_value = current_value + '/100'
        self.display.setText(new_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = BetterCalculator()
    window.show()

    sys.exit(app.exec())
