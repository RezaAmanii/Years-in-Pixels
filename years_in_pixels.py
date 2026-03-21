import os
import json
import customtkinter as ctk
from datetime import date, timedelta
from typing import Any

# ===============================================================================================================
#                                        Global Data and Constants
# ===============================================================================================================
DEFAULT_DATA = {
    "palette": {"Happy": "#50fa7b", "Tired": "#f1fa8c", "Sad": "#ff5555"},
    "entries": {},
}

# Dark grey
DEFAULT_COLOR = "#aba09f"

USER_DATA_FILENAME = "pixel_data.json"


# ===============================================================================================================
#                                              Helper Function
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


def on_mood_select(
    color: str,
    clicked_date: date,
    calender_frame,
    pixel_detail_frame,
    pixel_buttons: dict[date, Any],
) -> None:
    user_data = load_users_data()
    entries = user_data["entries"]

    stringed_date = clicked_date.strftime("%Y-%m-%d")
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
    pixel_buttons = {}

    # Create main window
    app = ctk.CTk()

    # Set window size
    app.geometry("1000x400")

    # Set title
    app.title("Year in Pixels")

    # Create the grid
    calender_frame = ctk.CTkFrame(app)
    calender_frame.pack(pady=20, padx=20)

    start_of_year = date(date.today().year, 1, 1)
    days_passed = 0

    for week in range(53):
        for day in range(7):
            delta = timedelta(days=days_passed)
            current_date = start_of_year + delta

            if current_date.year == start_of_year.year:
                # Change to date type to string
                stringed_date = current_date.strftime("%Y-%m-%d")

                user_entries = user_data["entries"]
                color = user_entries.get(stringed_date, DEFAULT_COLOR)

                # Color palette
                color_palette = user_data["palette"]

                button = ctk.CTkButton(
                    master=calender_frame,
                    width=15,
                    height=15,
                    fg_color=color,
                    hover_color=color,
                    border_width=0,
                    text="",
                    command=lambda d=current_date: on_pixel_click(
                        d, color_palette, app, calender_frame, pixel_buttons
                    ),
                )
                pixel_buttons[current_date] = button
                button.grid(row=day, column=week)

            days_passed += 1

    app.mainloop()


# ===============================================================================================================
#                                              Main Entry
# ===============================================================================================================
if __name__ == "__main__":
    main()
