import os
import json
import customtkinter as ctk
from datetime import date, timedelta
from typing import Any

# ===============================================================================================================
#                                        Global Data and Constants
# ===============================================================================================================
# Local file file
USER_DATA_FILENAME: str = "pixel_data.json"


# Default data
DEFAULT_DATA: dict[str, dict[str, str]] = {
    "palette": {"Happy": "#50fa7b", "Tired": "#f1fa8c", "Sad": "#ff5555"},
    "entries": {},
}

# Days of week
DAYS_OF_WEEK: dict[int, str] = {
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat",
    7: "Sun",
}

# Days of month
MONTHS_OF_YEAR: dict[int, str] = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

# Colors
DEFAULT_COLOR: str = "#aba09f"

# Application's visual configuration
APP_WINDOW_SIZE = "1700x400"
APP_TITLE = "Year in Pixels"
APP_FONT = "Helvetica"

# MISC
TOTAL_DAYS_IN_WEEK: int = 7
DATE_FORMAT = "%Y-%m-%d"


# ===============================================================================================================
#                                               Helper Function
# ===============================================================================================================
def load_users_data() -> dict[str, dict[str, str]]:
    if os.path.exists(USER_DATA_FILENAME):
        print(f"Loading user's data file ({USER_DATA_FILENAME}).")
        with open(USER_DATA_FILENAME, "r") as file:
            user_data = json.load(file)
    else:
        print(
            f"File: {USER_DATA_FILENAME} was not found in your directory. Creating a new one..."
        )
        with open(USER_DATA_FILENAME, "w") as file:
            file.write(json.dumps(DEFAULT_DATA))
            user_data = DEFAULT_DATA

    return user_data


def update_users_data(user_data: dict[str, dict[str, str]]) -> None:
    if os.path.exists(USER_DATA_FILENAME):
        with open(USER_DATA_FILENAME, "w") as file:
            file.write(json.dumps(user_data))

    else:
        print(f"File: {USER_DATA_FILENAME} was not found in your directory.")


# ===============================================================================================================
#                                                 Event Handlers
# ===============================================================================================================
def on_mood_select(
    color: str,
    clicked_date: date,
    calender_frame,
    pixel_detail_frame,
    pixel_buttons: dict[date, Any],
) -> None:
    user_data = load_users_data()
    entries = user_data["entries"]

    stringed_date = clicked_date.strftime(DATE_FORMAT)
    entries[stringed_date] = color
    update_users_data(user_data)

    pixel_detail_frame.destroy()
    calender_frame.pack()

    current_button = pixel_buttons[clicked_date]
    current_button.configure(
        fg_color=entries[stringed_date], hover_color=entries[stringed_date]
    )


def on_pixel_click(
    clicked_date: date,
    color_palette: dict[str, str],
    app,
    calender_frame,
    pixel_buttons: dict[date, Any],
) -> None:
    print(f"You cliked on: [{clicked_date}]")

    calender_frame.pack_forget()

    pixel_detail_frame = ctk.CTkFrame(master=app)
    pixel_detail_frame.pack(pady=20, padx=20)

    stringed_date = clicked_date.strftime("%Y-%m-%d")
    title = ctk.CTkLabel(master=pixel_detail_frame, text=stringed_date)
    title.pack()

    for mood, color in color_palette.items():
        mood_button = ctk.CTkButton(
            master=pixel_detail_frame,
            width=15,
            height=15,
            fg_color=color,
            hover_color=color,
            border_width=0,
            text=mood,
            command=lambda d=color: on_mood_select(
                d, clicked_date, calender_frame, pixel_detail_frame, pixel_buttons
            ),
        )
        mood_button.pack()


# ===============================================================================================================
#                                              Main Function
# ===============================================================================================================
def main():
    user_data = load_users_data()
    user_entries = user_data["entries"]
    color_palette = user_data["palette"]

    pixel_buttons = {}

    # Create main window
    app = ctk.CTk()

    # Set window size
    app.geometry(APP_WINDOW_SIZE)

    # Set title
    app.title(APP_TITLE)

    # Create the grid
    calender_frame = ctk.CTkFrame(app)
    calender_frame.pack(pady=20, padx=20)

    # Create Day Labels in the first column
    for i in range(TOTAL_DAYS_IN_WEEK):
        day_label = ctk.CTkLabel(
            master=calender_frame,
            text=DAYS_OF_WEEK[i + 1],
            font=(APP_FONT, 12),
            text_color="gray",
            padx=5,
        )
        day_label.grid(row=i + 1, column=0)

    # Start of the year (Year, 1 , 1)
    start_of_year = date(date.today().year, 1, 1)
    days_passed = 0

    month_gap_offset = 0

    for day in range(365):
        delta = timedelta(days=day)
        current_date = start_of_year + delta
        row = current_date.weekday() + 1

        # Finding number of week
        week = int(current_date.strftime("%V"))

        if current_date.year == start_of_year.year:
            # Check if it start of a month
            if current_date.day == 1:
                month_gap_offset += 3
                calender_frame.grid_columnconfigure(
                    week + month_gap_offset - 1, minsize=20
                )

                # Month Lables (In the first row)
                month_label = ctk.CTkLabel(
                    master=calender_frame,
                    text=MONTHS_OF_YEAR[current_date.month],
                    font=(APP_FONT, 14),
                    text_color="gray",
                    pady=-15,
                )
                month_label.grid(
                    row=0, column=week + month_gap_offset, columnspan=4, sticky="w"
                )

            # Change to date type to string
            stringed_date = current_date.strftime(DATE_FORMAT)

            color = user_entries.get(stringed_date, DEFAULT_COLOR)

            # Squares (days in a year)
            button = ctk.CTkButton(
                master=calender_frame,
                width=18,
                height=18,
                fg_color=color,
                hover_color=color,
                border_width=0,
                text="",
                corner_radius=4,
                command=lambda d=current_date: on_pixel_click(
                    d, color_palette, app, calender_frame, pixel_buttons
                ),
            )
            pixel_buttons[current_date] = button
            button.grid(row=row, column=week + month_gap_offset, padx=2, pady=2)

        days_passed += 1

    app.mainloop()


# ===============================================================================================================
#                                              Main Entry
# ===============================================================================================================
if __name__ == "__main__":
    main()
