# 🗓️ JalaliDatePicker (PyQt6)

A lightweight **Jalali (Persian) date picker** widget for PyQt6 applications, built using [`jdatetime`](https://pypi.org/project/jdatetime/).  
It connects three `QComboBox` widgets (Year, Month, Day) and handles all Jalali ↔ Gregorian date conversions automatically.

---

## 🚀 Features

- ✅ Simple integration with existing PyQt6 UI
- ✅ Dynamic day population (handles leap years and month lengths)
- ✅ Converts Jalali → Gregorian and back
- ✅ Disable/enable comboboxes logically
- ✅ Fully testable with `pytest` and `pytest-qt`

---

## 📦 Installation

Install dependencies:
```bash
pip install PyQt6 jdatetime pytest pytest-qt
```

---

## 🧱 Project Structure

```
jdatepicker/
├── jalali_datepicker.py
├── test.py
└── README.md
```

---

## 🧩 Usage Example

```python
from PyQt6 import QtWidgets
from jalali_datepicker import JalaliDatePicker

import sys
import datetime


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create combo boxes for year, month, day
        self.year_box = QtWidgets.QComboBox()
        self.month_box = QtWidgets.QComboBox()
        self.day_box = QtWidgets.QComboBox()

        # Initialize Jalali date picker
        self.date_picker = JalaliDatePicker(self.year_box, self.month_box, self.day_box)

        # Layout setup
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.year_box)
        layout.addWidget(self.month_box)
        layout.addWidget(self.day_box)
        self.setLayout(layout)

        # Example: set current date
        today = datetime.date.today()
        self.date_picker.set_date(today)

        # Example: get Jalali and Gregorian dates
        print("Gregorian:", self.date_picker.get_date())
        print("Jalali:", self.date_picker.get_jdate())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

---

## ⚙️ Public Methods

| Method | Description |
|--------|--------------|
| `get_date()` | Returns the selected date as a **Gregorian** `datetime.date` |
| `get_jdate()` | Returns the selected date as a **Jalali** `jdatetime.date` |
| `set_date(gregorian_date)` | Sets the picker to a given **Gregorian** date |
| `reset()` | Resets all combo boxes to their initial empty state |

---

## 🧠 Behavior Summary

| Action | Result |
|--------|--------|
| Select a year | Enables the month combo box |
| Select a month | Enables and fills the day combo box dynamically |
| Invalid date | Day combo box is disabled |
| `reset()` | Disables month/day, clears selection |

---

## 🧪 Running Tests

Unit tests are provided to verify that all logic works correctly.

Run tests with:
```bash
pytest test.py
```

### Test coverage includes:
- Initialization state  
- Enabling/disabling combo boxes  
- Day population logic  
- Jalali ↔ Gregorian conversion  
- Reset behavior  

---

## 🧩 Example Output

```
Gregorian: 2025-03-21
Jalali: 1404-01-01
```

---

## 🪪 License

MIT License © 2025  
You may freely use and modify this class in your own PyQt projects.

---
