from PyQt6 import QtCore

from jdatetime import date as jdate


class JalaliDatePicker(QtCore.QObject):
    years = {}
    months = {}
    days = {}

    def __init__(
        self, year_combobox, month_combobox, day_combobox, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.year_combobox = year_combobox
        self.month_combobox = month_combobox
        self.day_combobox = day_combobox

        self.year_combobox.setEnabled(True)
        self.month_combobox.setEnabled(False)
        self.day_combobox.setEnabled(False)

        self.__load_dates()

        self.year_combobox.currentTextChanged.connect(self.__on_year_changed)
        self.month_combobox.currentTextChanged.connect(self.__on_month_changed)

    def __load_dates(self):
        year_range = self.__get_years_range()
        month_range = [str(month) for month in range(1, 13)]

        self.month_combobox.addItem("ماه")
        self.year_combobox.addItem("سال")
        self.day_combobox.addItem("روز")

        self.month_combobox.addItems(month_range)
        self.year_combobox.addItems(year_range)

        self.year_combobox.setCurrentIndex(0)
        self.month_combobox.setCurrentIndex(0)
        self.day_combobox.setCurrentIndex(0)

    def __on_year_changed(self, selected_year):
        self.month_combobox.setEnabled(True)

    def __on_month_changed(self, selected_month):
        try:
            self.__clear(self.day_combobox)
            days_range = self.__get_days_range(
                self.year_combobox.currentText(), selected_month
            )
            self.day_combobox.addItems(days_range)
            self.day_combobox.setEnabled(True)
        except Exception as ex:
            self.day_combobox.setEnabled(False)
            print(ex)

    def get_date(self):
        try:
            year = int(self.year_combobox.currentText())
            month = int(self.month_combobox.currentText())
            day = int(self.day_combobox.currentText())
            return jdate(year, month, day).togregorian()
        except Exception as ex:
            print(f"ERROR (get_date): {ex}")

    def set_date(self, gregorian_date_object) -> None:
        try:
            self.year_combobox.blockSignals(True)
            self.month_combobox.blockSignals(True)
            self.day_combobox.blockSignals(True)

            jalali_date = jdate.fromgregorian(
                day=gregorian_date_object.day,
                month=gregorian_date_object.month,
                year=gregorian_date_object.year,
            )

            jalali_year = jalali_date.year
            jalali_month = jalali_date.month
            jalali_day = jalali_date.day

            jalali_year_index = self.year_combobox.findText(
                str(jalali_year)
            )
            self.year_combobox.setCurrentIndex(jalali_year_index)

            jalali_month_index = self.month_combobox.findText(
                str(jalali_month)
            )
            self.month_combobox.setCurrentIndex(jalali_month_index)

            days_range = self.__get_days_range(jalali_year, jalali_month)
            self.__clear(self.day_combobox)
            self.day_combobox.addItems(days_range)

            jalali_day_index = self.day_combobox.findText(
                str(jalali_day)
            )
            self.day_combobox.setCurrentIndex(jalali_day_index)
        except Exception as ex:
            print(ex)
        finally:
            self.year_combobox.blockSignals(False)
            self.month_combobox.blockSignals(False)
            self.day_combobox.blockSignals(False)

    def __clear(self, combobox):
        header = combobox.itemText(0)
        combobox.clear()
        combobox.addItem(header)
        combobox.setCurrentIndex(0)

    def __get_days_range(self, year, month):
        first_day_of_this_month = jdate(int(year), int(month), 1)
        first_day_of_the_next_month = self.__get_next_month_date(int(year), int(month), 1)
        days_count = (first_day_of_the_next_month - first_day_of_this_month).days
        return [str(day) for day in range(1, days_count + 1)]

    def __get_years_range(self) -> list:
        current_year = jdate.today().year
        return [str(year) for year in range(current_year - 10, current_year + 10)]

    def __get_next_month(self, month):
        if month == 12:
            return 1
        return month + 1

    def __get_next_month_date(self, year, month, day):
        next_month = self.__get_next_month(month)
        next_year = year + 1 if next_month == 1 else year

        return jdate(next_year, next_month, day)

    def reset(self):
        """Reset the date picker to its initial empty state."""
        # Temporarily block signals to avoid unnecessary callbacks
        self.year_combobox.blockSignals(True)
        self.month_combobox.blockSignals(True)
        self.day_combobox.blockSignals(True)

        # Reset values and states
        self.year_combobox.setCurrentIndex(0)
        self.month_combobox.setCurrentIndex(0)
        self.day_combobox.setCurrentIndex(0)

        self.month_combobox.setEnabled(False)
        self.day_combobox.setEnabled(False)

        # Clear day combobox items but keep header
        self.__clear(self.day_combobox)

        # Re-enable signals
        self.year_combobox.blockSignals(False)
        self.month_combobox.blockSignals(False)
        self.day_combobox.blockSignals(False)

    def get_jdate(self) -> jdate:
        try:
            year = int(self.year_combobox.currentText())
            month = int(self.month_combobox.currentText())
            day = int(self.day_combobox.currentText())
            return jdate(year, month, day)
        except Exception as ex:
            print(f"ERROR (get_jdate): {ex}")
