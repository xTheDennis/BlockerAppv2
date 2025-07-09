import customtkinter as ctk
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FGambling")
        self.geometry("600x400")
        self.resizable(False, False)

        self.current_user_id = None
        self.show_login_screen()

    def show_login_screen(self):
        if hasattr(self, "register_screen"):
            self.register_screen.pack_forget()

        self.login_screen = LoginScreen(master=self, on_login_success=self.start_main_window, show_register_screen=self.show_register_screen, app=self)
        self.login_screen.pack(expand=True, fill="both")

    def show_register_screen(self):
        self.login_screen.pack_forget()
        self.register_screen = RegisterScreen(master=self, on_register_success=self.show_login_screen, show_login_screen=self.show_login_screen, app=self)
        self.register_screen.pack(expand=True, fill="both")


    def start_main_window(self):
        from screens.main_window import MainWindow
        self.login_screen.pack_forget()
        self.main_window = MainWindow(master=self, app=self)
        self.main_window.pack(fill="both", expand=True)
 


if __name__ == "__main__":
    app = App()
    app.mainloop()
