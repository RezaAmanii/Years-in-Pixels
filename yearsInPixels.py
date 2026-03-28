import customtkinter as ctk
from PIL import Image
from tkinter.colorchooser import askcolor
from src.dataManager import DataManager
from src import config
from src.UI.calendar_view import CalendarView
from src.UI.detail_view import DetailView
from datetime import date

class MainController(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry(config.APP_WINDOW_SIZE)
        self.title(config.APP_TITLE)
        self.resizable(False, False)


        # Initialize the Data
        self.dataManager = DataManager(config.USER_DATA_FILENAME, config.DEFAULT_DATA)
        self.user_data = self.dataManager.load_users_data()


        # Load Icons to pass to views
        self.icons = {
            'back': ctk.CTkImage(
                light_image=Image.open("Icons/back_button_light.png"),
                dark_image=Image.open("Icons/back_button_dark.png"),
                size=(20, 20)
            ),

            'clear': ctk.CTkImage(
                light_image=Image.open("Icons/clear.png"),
                dark_image=Image.open("Icons/clear.png"),
                size=(30, 30)
            )
        }


        # Initialize views
        self.detail_view = None
        self.calendar_view = CalendarView(
            master=self,
            user_entries=self.user_data["entries"],
            on_pixel_click_callback=self.show_detail_view
        )
        self.calendar_view.pack(fill="both", expand=True)


    def show_detail_view(self, clicked_date: date):
        self.calendar_view.pack_forget()

        if self.detail_view is not None:
            self.detail_view.destroy()

        self.detail_view = DetailView(
            master=self,
            clicked_date=clicked_date,
            user_entries=self.user_data["entries"],
            color_palette=self.user_data["palette"],
            icons=self.icons,
            on_back_callback=self.show_calendar_view,
            on_clear_callback=self.handle_clear_mood,
            on_mood_select_callback=self.handle_mood_select,
            on_add_mood_callback=self.handle_add_mood
        )
        self.detail_view.pack(expand=True, fill="both")


    def show_calendar_view(self):
        if self.detail_view is not None:
            self.detail_view.pack_forget()
        self.calendar_view.pack(fill="both", expand=True)


    def handle_mood_select(self, color: str, clicked_date: date):
        stringed_date = config.string_the_date(clicked_date)

        # Update the data
        self.user_data['entries'][stringed_date] = color
        self.dataManager.update_users_data(self.user_data)

        # Update views
        self.calendar_view.update_pixel_color(clicked_date, color)
        if self.detail_view is not None:
            self.detail_view.pixel_preview.configure(fg_color=color)


    def handle_clear_mood(self, clicked_date: date):
        stringed_date = config.string_the_date(clicked_date)

        # Update the data
        self.user_data["entries"].pop(stringed_date, None)
        self.dataManager.update_users_data(self.user_data)

        # Update views
        self.calendar_view.update_pixel_color(clicked_date, config.DEFAULT_BOX_COLOR)
        self.show_detail_view(clicked_date)


    def handle_add_mood(self, clicked_date: date):
        dialog = ctk.CTkInputDialog(text="Enter the name of your new mood:", title="Add Custom Mood")
        mood_name = dialog.get_input()

        if mood_name and mood_name.strip() != "":
            chosen_color = askcolor(title=f"Choose a color for '{mood_name}'")
            hex_color = chosen_color[1]

            if hex_color:
                # Update the data
                self.user_data['palette'][mood_name] = hex_color
                self.dataManager.update_users_data(self.user_data)

                # Refreshing DetailView to show the new button
                self.show_detail_view(clicked_date)



if __name__ == "__main__":
    app = MainController()
    app.mainloop()
