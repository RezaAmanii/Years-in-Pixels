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


# Default metrics
DEFAULT_CORNER_RADIUS = 5
DEFAULT_BRITHNESS_AMOUNT = 0.4


# Application's visual configuration
APP_WINDOW_SIZE: str = "1600x300"
APP_TITLE: str = "Year in Pixels"
APP_FONT: str = "Source Serif 4"


# MISC
DATE_FORMAT: str = "%Y-%m-%d"
TOTAL_DAYS_IN_WEEK = 7


# --- Methods ---
def string_the_date(given_date: date) -> str:
    return given_date.strftime(DATE_FORMAT)


def lighten_color(hex_color: str, amount: float = 0.2) -> str:
    """
    Take a hex color and lightens it.
    """
    hex_color = hex_color.lstrip('#')

    if len(hex_color) != 6:
        return f"#{hex_color}"

    # Convert hex to integer RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Blend the color toward white
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)

    # return hex
    return f"#{r:02x}{g:02x}{b:02x}"







