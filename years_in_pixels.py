import os
import json
import customtkinter as ctk
from datetime import date, timedelta

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

# Default box colors
DEFAULT_COLOR: str = "#aba09f"

# Application's visual configuration
APP_WINDOW_SIZE: str = "1700x400"
APP_TITLE: str = "Year in Pixels"
APP_FONT: str = "Helvetica"

# MISC
TOTAL_DAYS_IN_WEEK: int = 7
DATE_FORMAT: str = "%Y-%m-%d"


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


def string_the_date(given_date: date) -> str:
    return given_date.strftime(DATE_FORMAT)


# ===============================================================================================================
#                                              Main Classes
# ===============================================================================================================
class YearInPixelApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry(APP_WINDOW_SIZE)
        self.app.title(APP_TITLE)

        self.user_data = load_users_data()
        self.user_entries = self.user_data["entries"]
        self.color_palette = self.user_data["palette"]
        self.pixel_buttons = {}

        self.pixel_detail_frame = ctk.CTkFrame(master=self.app)

    def create_calender(self):
        self.calender_frame = ctk.CTkFrame(self.app)
        self.calender_frame.pack(pady=20, padx=20)

        # Create Day Labels in the first column
        self.create_day_labels()

        # Create the grid pixel
        self.create_pixel_grid()

    def create_pixel_grid(self):
        start_of_year = date(date.today().year, 1, 1)
        start_of_next_year = date(date.today().year + 1, 1, 1)
        delta = start_of_next_year - start_of_year
        days = delta.days

        month_gap_offset = 0
        days_passed = 0

        for day in range(days):
            delta = timedelta(days=day)
            current_date = start_of_year + delta
            row = current_date.weekday() + 1
            stringed_date = string_the_date(current_date)

            # Finding number of week
            week = int(current_date.strftime("%V"))

            # Check if we are in the same year as current year
            if current_date.year == start_of_year.year:
                # Check if it is start of month
                if current_date.day == 1:
                    month_gap_offset += 3
                    self.calender_frame.grid_columnconfigure(
                        week + month_gap_offset - 1, minsize=20
                    )

                    # Month Lables (In the first row)
                    self.create_month_labels(current_date, week, month_gap_offset)

                color = self.user_entries.get(stringed_date, DEFAULT_COLOR)

                # Squares (days in a year)
                button = ctk.CTkButton(
                    master=self.calender_frame,
                    width=18,
                    height=18,
                    fg_color=color,
                    hover_color=color,
                    border_width=0,
                    text="",
                    corner_radius=4,
                    command=lambda d=current_date: self.on_pixel_click(d),
                )
                self.pixel_buttons[current_date] = button
                button.grid(row=row, column=week + month_gap_offset, padx=2, pady=2)

            days_passed += 1

    def create_day_labels(self):
        for i in range(TOTAL_DAYS_IN_WEEK):
            day_label = ctk.CTkLabel(
                master=self.calender_frame,
                text=DAYS_OF_WEEK[i + 1],
                font=(APP_FONT, 12),
                text_color="gray",
                padx=5,
            )
            day_label.grid(row=i + 1, column=0)

    def create_month_labels(self, current_date: date, week, month_gap_offset):
        month_label = ctk.CTkLabel(
            master=self.calender_frame,
            text=MONTHS_OF_YEAR[current_date.month],
            font=(APP_FONT, 14),
            text_color="gray",
            pady=-15,
        )
        month_label.grid(
            row=0, column=week + month_gap_offset, columnspan=4, sticky="w"
        )

    def on_pixel_click(self, clicked_date: date):
        for child in self.pixel_detail_frame.winfo_children():
            child.destroy()

        self.calender_frame.pack_forget()
        self.pixel_detail_frame.pack(pady=20, padx=20)

        stringed_date = string_the_date(clicked_date)
        title = ctk.CTkLabel(master=self.pixel_detail_frame, text=stringed_date)
        title.pack()

        for mood, color in self.color_palette.items():
            mood_button = ctk.CTkButton(
                master=self.pixel_detail_frame,
                width=15,
                height=15,
                fg_color=color,
                hover_color=color,
                border_width=0,
                text=mood,
                command=lambda d=color: self.on_mood_select(d, clicked_date),
            )
            mood_button.pack()

        # Back button
        back_button = ctk.CTkButton(
            master=self.pixel_detail_frame, text="Back", command=lambda: self.go_back()
        )
        back_button.pack()

        # Clear button
        clear_button = ctk.CTkButton(
            master=self.pixel_detail_frame,
            text="Clear",
            command=lambda: self.clear_mood(clicked_date),
        )
        clear_button.pack()

    def go_back(self):
        self.pixel_detail_frame.pack_forget()
        self.calender_frame.pack(padx=20, pady=20)

    def clear_mood(self, clicked_date: date):
        stringed_date = string_the_date(clicked_date)
        self.user_entries.pop(stringed_date, None)
        update_users_data(self.user_data)
        self.reset_buttons_color(clicked_date)

    def on_mood_select(self, color: str, clicked_date: date):
        stringed_date = string_the_date(clicked_date)
        self.user_entries[stringed_date] = color
        update_users_data(self.user_data)

        current_button = self.pixel_buttons[clicked_date]
        current_button.configure(
            fg_color=self.user_entries[stringed_date],
            hover_color=self.user_entries[stringed_date],
        )

        self.go_back()

    def reset_buttons_color(self, clicked_date: date):
        button = self.pixel_buttons[clicked_date]
        button.configure(fg_color=DEFAULT_COLOR, hover_color=DEFAULT_COLOR)

    def run(self):
        self.create_calender()
        self.app.mainloop()


# ===============================================================================================================
#                                              Main Function
# ===============================================================================================================
def main():
    app = YearInPixelApp()
    app.run()


# ===============================================================================================================
#                                              Main Entry
# ===============================================================================================================
if __name__ == "__main__":
    main()
