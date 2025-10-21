import pytest
import datetime
from PyQt6 import QtWidgets
from jdatetime import date as jdate

from jalali_datepicker import JalaliDatePicker  # adjust import path


@pytest.fixture(scope="module")
def app():
    """Provide a QApplication instance for Qt widgets."""
    app = QtWidgets.QApplication([])
    yield app
    app.quit()


@pytest.fixture
def picker(app):
    """Create a JalaliDatePicker with 3 comboboxes."""
    year_box = QtWidgets.QComboBox()
    month_box = QtWidgets.QComboBox()
    day_box = QtWidgets.QComboBox()
    picker = JalaliDatePicker(year_box, month_box, day_box)
    return picker


def test_initial_state(picker):
    """Test that the picker initializes with proper disabled states."""
    assert picker.year_combobox.isEnabled()
    assert not picker.month_combobox.isEnabled()
    assert not picker.day_combobox.isEnabled()

    # Check placeholders
    assert picker.year_combobox.itemText(0) == "سال"
    assert picker.month_combobox.itemText(0) == "ماه"
    assert picker.day_combobox.itemText(0) == "روز"


def test_year_change_enables_month(picker):
    """Selecting a year should enable the month combobox."""
    picker.year_combobox.setCurrentIndex(1)
    assert picker.month_combobox.isEnabled()


def test_month_change_populates_days(picker):
    """Changing month should populate the day combobox correctly."""
    # Force valid year/month values
    picker.year_combobox.setCurrentIndex(1)
    picker.month_combobox.setCurrentText("1")

    assert picker.day_combobox.isEnabled()
    assert picker.day_combobox.count() > 1  # "روز" + actual days


def test_get_jdate_and_get_date(picker):
    """Test jdate and Gregorian date conversion."""
    # Set specific known values
    picker.year_combobox.setCurrentText("1403")
    picker.month_combobox.setCurrentText("1")
    picker.day_combobox.setCurrentText("15")

    jd = picker.get_jdate()
    assert isinstance(jd, jdate)
    assert jd.year == 1403
    assert jd.month == 1
    assert jd.day == 15

    gd = picker.get_date()
    assert isinstance(gd, datetime.date)


def test_set_date_converts_back(picker):
    """Test setting a Gregorian date populates correct Jalali fields."""
    g_date = datetime.date(2024, 3, 20)  # ~ Nowruz 1403-01-01
    picker.set_date(g_date)

    assert picker.year_combobox.currentText() == "1403"
    assert picker.month_combobox.currentText() == "1"
    assert picker.day_combobox.currentText() == "1"


def test_reset_restores_initial_state(picker):
    """Test reset() returns comboboxes to their defaults."""
    picker.year_combobox.setCurrentIndex(2)
    picker.month_combobox.setCurrentIndex(3)
    picker.day_combobox.setCurrentIndex(5)

    picker.reset()

    assert picker.year_combobox.currentIndex() == 0
    assert picker.month_combobox.currentIndex() == 0
    assert picker.day_combobox.currentIndex() == 0
    assert not picker.month_combobox.isEnabled()
    assert not picker.day_combobox.isEnabled()
