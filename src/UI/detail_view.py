import customtkinter as ctk
import tkinter.messagebox as messagebox
from datetime import date
from src import config


class DetailView(ctk.CTkFrame):
    def __init__(self, master, clicked_date: date, user_entries: dict, color_palette: dict,
                 icons: dict, on_back_callback, on_clear_callback, on_mood_select_callback,
                 on_add_mood_callback, on_delete_mood_callback, **kwargs):
        super().__init__(master, fg_color=config.DEFAULT_BACKGROUND_DARK, **kwargs)

        self.clicked_date = clicked_date
        self.stringed_date = config.string_the_date(clicked_date)
        self.user_entries = user_entries
        self.color_palette = color_palette
        self.icons = icons


        # Callbacks
        self.on_back_callback = on_back_callback
        self.on_clear_callback = on_clear_callback
        self.on_mood_select_callback = on_mood_select_callback
        self.on_add_mood_callback = on_add_mood_callback
        self.on_delete_mood_callback = on_delete_mood_callback

        self.build_ui()


    def build_ui(self):
        # --- Header Frame (Back button, Title, Clear button) ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 10))


        # Back button
        back_button = ctk.CTkButton(
            master=header_frame,
            text="",
            image=self.icons['back'],
            fg_color="transparent",
            hover_color="#444444",
            command=self.on_back_callback,
            width= 30, height=30
        )
        back_button.pack(side="left")


        # Title Label
        title = ctk.CTkLabel(
            master=header_frame,
            text=self.stringed_date,
            font=(config.APP_FONT, 30, "bold"),
            text_color="white"
        )
        title.pack(side="left", padx=30)


        # Clear button
        clear_button = ctk.CTkButton(
            master=header_frame,
            text="",
            image=self.icons['clear'],
            fg_color="transparent",
            hover_color="#ff4c4c",
            command=lambda: self.on_clear_callback(self.clicked_date),
            width=30, height=30
        )
        clear_button.pack(side="right")


        # --- Content Frame (Pixel Preview, Mood buttons Grid, ...)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True)


        # Pixel Preview
        current_color = self.user_entries.get(self.stringed_date, config.DEFAULT_BOX_COLOR)
        self.pixel_preview = ctk.CTkFrame(
            master=content_frame,
            width= 200, height=200,
            fg_color=current_color,
            corner_radius=config.DEFAULT_CORNER_RADIUS
        )
        self.pixel_preview.pack(side="left", padx=(0, 50))


        # Mood Button Grid
        mood_grid_frame = ctk.CTkFrame(master=content_frame, fg_color="transparent")
        mood_grid_frame.pack(side="left")

        for i, (mood, color) in enumerate(self.color_palette.items()):
            row = i // 5
            col = i % 5
            mood_button = ctk.CTkButton(
                master=mood_grid_frame,
                width=80, height=30,
                fg_color=color,
                hover_color=config.lighten_color(color, amount=config.DEFAULT_BRITHNESS_AMOUNT),
                text=mood,
                text_color="black",
                font=(config.APP_FONT, 15, "bold"),
                corner_radius=config.DEFAULT_CORNER_RADIUS,
                command=lambda c=color: self.on_mood_select_callback(c, self.clicked_date)
            )
            mood_button.grid(row=row, column=col, padx=5, pady=5)

            def right_click_delete(event, m=mood):
                confirm = messagebox.askyesno(
                    title="Delete Mood",
                    message=f"Are you sure you want to delete the '{m}' mood\n\n(This won't remove colors already on your calendar.)"
                )
                if confirm:
                    self.on_delete_mood_callback(m, self.clicked_date)

            # Bind right-click to the button
            # <Button-3> handle Windows & Linux
            mood_button.bind("<Button-3>", right_click_delete)
            # <Button-2> handle Mac
            mood_button.bind("<Button-2>", right_click_delete)


        # Add Mood Button
        total_moods = len(self.color_palette)
        add_row = total_moods // 5
        add_col = total_moods % 5
        add_mood_btn = ctk.CTkButton(
            master=mood_grid_frame,
            width=18, height=18,
            fg_color="#555555",
            hover_color="#777777",
            text="+",
            font=(config.APP_FONT, 18, "bold"),
            corner_radius=config.DEFAULT_CORNER_RADIUS,
            command=lambda: self.on_add_mood_callback(self.clicked_date)
        )
        add_mood_btn.grid(row=add_row, column=add_col, padx=10, pady=5)
