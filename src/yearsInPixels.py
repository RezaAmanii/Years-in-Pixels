from src.dataManager import DataManager
from PIL import Image
import customtkinter as ctk
from tkinter.colorchooser import askcolor
from datetime import date, timedelta

# ===============================================================================================================
#                                        Global Data and Constants
# ===============================================================================================================
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
TOTAL_DAYS_IN_WEEK: int = 7
DATE_FORMAT: str = "%Y-%m-%d"


# ===============================================================================================================
#                                               Helper Function
# ===============================================================================================================
def string_the_date(given_date: date) -> str:
    return given_date.strftime(DATE_FORMAT)


# ===============================================================================================================
#                                              Main Classes
# ===============================================================================================================
class YearInPixelApp:
    def __init__(self):
        self.dataManager = DataManager(USER_DATA_FILENAME, DEFAULT_DATA)

        self.app = ctk.CTk()
        self.app.geometry(APP_WINDOW_SIZE)
        self.app.title(APP_TITLE)
        self.app.resizable(False, False)
        self.user_data = self.dataManager.load_users_data()
        self.user_entries = self.user_data["entries"]
        self.color_palette = self.user_data["palette"]
        self.pixel_buttons = {}


        # Loading icons for the buttons
        self.icon_back = ctk.CTkImage(
            light_image=Image.open("Icons/back_button_light.png"),
            dark_image=Image.open("Icons/back_button_dark.png"),
            size=(20, 20)
        )

        self.icon_clear = ctk.CTkImage(
            light_image=Image.open("Icons/clear.png"),
            dark_image=Image.open("Icons/clear.png"),
            size=(30,30)

        )

        self.pixel_detail_frame = ctk.CTkFrame(master=self.app)


    def create_calender(self):
        self.calender_frame = ctk.CTkFrame(self.app, fg_color=DEFAULT_BACKGROUND_DARK)
        self.calender_frame.pack(fill="both", expand=True)

        # Create Day Labels in the first column
        self.create_day_labels()

        # Create the grid pixel
        self.create_pixel_grid()


    def create_pixel_grid(self):
        start_of_year = date(date.today().year, 1, 1)
        start_of_next_year = date(date.today().year + 1, 1, 1)
        delta = start_of_next_year - start_of_year
        days = (start_of_next_year - start_of_year).days

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
                    self.calender_frame.grid_columnconfigure(week + month_gap_offset - 1, minsize=20)

                    # Month Lables (In the first row)
                    self.create_month_labels(current_date, week, month_gap_offset)

                color = self.user_entries.get(stringed_date, DEFAULT_BOX_COLOR)

                # Squares (days in a year)
                button = ctk.CTkButton(
                    master=self.calender_frame,
                    width=16,
                    height=16,
                    fg_color=color,
                    hover_color=DEFAULT_HOVER_PIXEL_COLOR,
                    border_width=0,
                    text="",
                    corner_radius=2,
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
                font=(APP_FONT, 13, "bold"),
                text_color=DEFAULT_DAY_LABEL_FONT_COLOR,
                padx=10
            )
            day_label.grid(row=i + 1, column=0)


    def create_month_labels(self, current_date: date, week, month_gap_offset):
        month_label = ctk.CTkLabel(
            master=self.calender_frame,
            text=MONTHS_OF_YEAR[current_date.month],
            font=(APP_FONT, 15, "bold"),
            text_color=DEFAULT_MONTH_LABEL_FONT_COLOR,
            pady=5
        )
        month_label.grid(row=0, column=week + month_gap_offset, columnspan=4, sticky="w")


    def on_pixel_click(self, clicked_date: date):
        """
        Renders the detailed view Card for a specific date.

        Args:
            clicked_date (date): The specific date the user clicked on the calendar.
        """
        for child in self.pixel_detail_frame.winfo_children():
            child.destroy()

        stringed_date = string_the_date(clicked_date)

        # Card" frame to hold everything
        card_frame = ctk.CTkFrame(
            master=self.pixel_detail_frame,
            fg_color=DEFAULT_BACKGROUND_DARK
        )
 
        card_frame.pack(expand=True, fill="both")

        # Back Button & Title
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 10))

        back_button = ctk.CTkButton(
            master=header_frame,
            text="",
            image=self.icon_back,
            fg_color="transparent",
            hover_color="#444444",
            command=self.go_back,
            width=20,
            height=20
        )
        back_button.pack(side="left")

        title = ctk.CTkLabel(
            master=header_frame,
            text=stringed_date,
            font=(APP_FONT, 20, "bold"),
            text_color="white"
        )
        title.pack(side="left", padx=20)

        clear_button = ctk.CTkButton(
            master=header_frame,
            text="",
            image=self.icon_clear,
            fg_color="transparent",
            hover_color="#ff4c4c",
            command=lambda: self.clear_mood(clicked_date),
            width=30,
        )
        clear_button.pack(side="right")

        content_frame = ctk.CTkFrame(
            master=card_frame,
            fg_color="transparent"
        )
        content_frame.pack(expand=True)

        # The Pixel Preview
        current_color = self.user_entries.get(stringed_date, DEFAULT_BOX_COLOR)
        self.pixel_preview = ctk.CTkFrame(
            master=content_frame,
            width=120,
            height=120,
            fg_color=current_color,
            corner_radius=15,
        )
        self.pixel_preview.pack(side="left", padx=(0, 50))

        # Mood Buttons
        mood_grid_frame = ctk.CTkFrame(master=content_frame, fg_color="transparent")
        mood_grid_frame.pack(side="left")

        for i, (mood, color) in enumerate(self.color_palette.items()):
            row = i // 5
            col = i % 5

            mood_button = ctk.CTkButton(
                master=mood_grid_frame,
                width=80,
                height=30,
                fg_color=color,
                hover_color=color,
                text=mood,
                text_color="black",
                font=(APP_FONT, 12, "bold"),
                corner_radius=20,
                command=lambda d=color: self.on_mood_select(d, clicked_date),
            )
            mood_button.grid(row=row, column=col, padx=5, pady=5)

        total_moods = len(self.color_palette)
        add_row = total_moods // 5
        add_col = total_moods % 5

        add_mood_btn = ctk.CTkButton(
            master=mood_grid_frame,
            width=18,
            height=18,
            fg_color="#555555",
            hover_color="#777777",
            text="+",
            font=(APP_FONT, 18, "bold"),
            corner_radius=50,
            command=lambda: self.add_new_mood(clicked_date)
        )

        add_mood_btn.grid(row=add_row, column=add_col, padx=5, pady=5)

        self.calender_frame.pack_forget()
        self.pixel_detail_frame.pack(expand=True, fill="both")

    def go_back(self):
        self.pixel_detail_frame.pack_forget()
        self.calender_frame.pack(fill="both", expand=True)


    def clear_mood(self, clicked_date: date):
        stringed_date = string_the_date(clicked_date)
        self.user_entries.pop(stringed_date, None)
        self.dataManager.update_users_data(self.user_data)
        self.reset_buttons_color(clicked_date)
        self.on_pixel_click(clicked_date)


    def on_mood_select(self, color: str, clicked_date: date):
        stringed_date = string_the_date(clicked_date)
        self.user_entries[stringed_date] = color
        self.dataManager.update_users_data(self.user_data)

        current_button = self.pixel_buttons[clicked_date]
        current_button.configure(
            fg_color=color,
            hover_color=color,
        )

        if hasattr(self, 'pixel_preview'):
            self.pixel_preview.configure(fg_color=color)


    def reset_buttons_color(self, clicked_date: date):
        button = self.pixel_buttons[clicked_date]
        button.configure(fg_color=DEFAULT_BOX_COLOR, hover_color=DEFAULT_BOX_COLOR)


    def add_new_mood(self, clicked_date: date):
        """
        Prompts the user to create a new custom mood and color.

        Args:
            clicked_date (date): The current date being viewed, used to reload the current card.
        """
        dialog = ctk.CTkInputDialog(
            text="Enter the name of your new mood:",
            title="Add Custom Mood"
        )
        mood_name = dialog.get_input()

        if mood_name and mood_name.strip() != "":
            chosen_color = askcolor(title=f"Choose a color for '{mood_name}'")
            hex_color = chosen_color[1]

            if hex_color:
                self.color_palette[mood_name] = hex_color
                self.dataManager.update_users_data(self.user_data)

                self.on_pixel_click(clicked_date)


    def run(self):
        self.create_calender()
        self.app.mainloop()

