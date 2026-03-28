from datetime import date


# Local file file
USER_DATA_FILENAME: str = "pixel_data.json"


# Default data
DEFAULT_DATA: dict[str, dict[str, str]] = {
    "palette": {"Happy": "#50fa7b", "Tired": "#f1fa8c", "Sad": "#ff5555"},
    "entries": {}}


# Days of week
DAYS_OF_WEEK: dict[int, str] = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}


# Month of year
MONTHS_OF_YEAR: dict[int, str] = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
                                  5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
                                  9: "Sep", 10: "Oct", 11: "Nov",12: "Dec"}


# Default colors
DEFAULT_BOX_COLOR: str = "#cccccc"
DEFAULT_BACKGROUND_DARK = "#23272a"
DEFAULT_MONTH_LABEL_FONT_COLOR = "#7289da"
DEFAULT_DAY_LABEL_FONT_COLOR = "#99aab5"
DEFAULT_HOVER_PIXEL_COLOR = "#999999"


# Application's visual configuration
APP_WINDOW_SIZE: str = "1600x280"
APP_TITLE: str = "Year in Pixels"
APP_FONT: str = "Source Serif 4"


# MISC
DATE_FORMAT: str = "%Y-%m-%d"
TOTAL_DAYS_IN_WEEK = 7


def string_the_date(given_date: date) -> str:
    return given_date.strftime(DATE_FORMAT)


