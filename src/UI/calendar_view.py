import customtkinter as ctk
from datetime import date, timedelta
from src import config


class CalendarView(ctk.CTkFrame):
    def __init__(self, master, user_entries, color_palette, on_pixel_click_callback, **kwargs):
        super().__init__(master, fg_color=config.DEFAULT_BACKGROUND_DARK, **kwargs)
        self.user_entries = user_entries
        self.color_palette = color_palette
        self.on_pixel_click_callback = on_pixel_click_callback
        self.pixel_buttons = {}

        self.create_day_labels()
        self.create_pixel_grid()

        self.create_stats_section()
        self.update_stats()


    def create_day_labels(self):
        for i in range(config.TOTAL_DAYS_IN_WEEK):
            day_label = ctk.CTkLabel(
                master=self,
                text=config.DAYS_OF_WEEK[i + 1],
                font=(config.APP_FONT, 13, "bold"),
                text_color=config.DEFAULT_DAY_LABEL_FONT_COLOR,
                padx=10
            )
            day_label.grid(row=i + 1, column=0)


    def create_month_labels(self, current_date: date, week, month_gap_offset):
        month_label = ctk.CTkLabel(
            master=self,
            text=config.MONTHS_OF_YEAR[current_date.month],
            font=(config.APP_FONT, 15, "bold"),
            text_color=config.DEFAULT_MONTH_LABEL_FONT_COLOR,
            pady=5
        )
        month_label.grid(row=0, column=week + month_gap_offset, columnspan=4, sticky="w")



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
            stringed_date = config.string_the_date(current_date)

            # Finding number of week
            week = int(current_date.strftime("%V"))

            # Check if we are in the same year as current year
            if current_date.year == start_of_year.year:
                # Check if it is start of month
                if current_date.day == 1:
                    month_gap_offset += 3
                    self.grid_columnconfigure(week + month_gap_offset - 1, minsize=20)

                    # Month Lables (In the first row)
                    self.create_month_labels(current_date, week, month_gap_offset)

                color = self.user_entries.get(stringed_date, config.DEFAULT_BOX_COLOR)

                if color == config.DEFAULT_BOX_COLOR:
                    hover = config.DEFAULT_HOVER_PIXEL_COLOR
                else:
                    hover = config.lighten_color(color, amount=config.DEFAULT_BRITHNESS_AMOUNT)

                # Squares (days in a year)
                button = ctk.CTkButton(
                    master=self,
                    width=16,
                    height=16,
                    fg_color=color,
                    hover_color=hover,
                    border_width=0,
                    text="",
                    corner_radius=config.DEFAULT_CORNER_RADIUS - 3,
                    command=lambda d=current_date: self.on_pixel_click_callback(d),
                )
                self.pixel_buttons[current_date] = button
                button.grid(row=row, column=week + month_gap_offset, padx=2, pady=2)

            days_passed += 1

    def update_pixel_color(self, clicked_date: date, color: str):
        if clicked_date in self.pixel_buttons:
            button = self.pixel_buttons[clicked_date]

            if color == config.DEFAULT_BOX_COLOR:
                hover = config.DEFAULT_HOVER_PIXEL_COLOR
            else:
                hover = config.lighten_color(color, amount=config.DEFAULT_BRITHNESS_AMOUNT)
            button.configure(fg_color=color, hover_color=hover)


    def create_stats_section(self):
        # Separator
        separator = ctk.CTkFrame(
            master=self,
            height=2,
            fg_color="#333333"
        )
        separator.grid(row=8, column=0, columnspan=90, sticky="ew", pady=(15, 5), padx=10)

        # Statistics Label
        stats_title = ctk.CTkLabel(
            master=self,
            text="Statistics:",
            font=(config.APP_FONT, 13, "bold"),
            text_color=config.DEFAULT_DAY_LABEL_FONT_COLOR
        )
        stats_title.grid(row=9, column=0, columnspan=2, sticky="w", padx=10)

        # Container for the dynamic numbers
        self.stats_container = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.stats_container.grid(row=9, column=2, columnspan=88, sticky="w", padx=10)

    def update_stats(self):
        for child in self.stats_container.winfo_children():
            child.destroy()

        mood_counts = {}
        for entry in self.user_entries.values():
            if entry in self.color_palette:
                mood_counts[entry] = mood_counts.get(entry, 0) + 1

            else:
                for m, c in self.color_palette.items():
                    if c == entry:
                        mood_counts[m] = mood_counts.get(m, 0) + 1
                        break

        col_index = 0
        for mood, color in self.color_palette.items():
            count = mood_counts.get(mood, 0)

            if count > 0:

                color_box = ctk.CTkFrame(
                    master=self.stats_container,
                    width=16, height=16,
                    fg_color=color,
                    corner_radius=config.DEFAULT_CORNER_RADIUS
                )
                color_box.grid(row=0, column=col_index, padx=(0, 6), pady=2)

                stat_label = ctk.CTkLabel(
                    master=self.stats_container,
                    text=f"{mood}: {count}",
                    font=(config.APP_FONT, 14, "bold"),
                    text_color="white"
                )
                stat_label.grid(row=0, column=col_index + 1, padx=(0, 25), pady=2)
                col_index += 2
