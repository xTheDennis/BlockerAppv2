import customtkinter as ctk
from screens.page_blocker import PageBlocker

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content_area = ctk.CTkFrame(self)
        self.content_area.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar, text="Menü", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.btn_blocker = ctk.CTkButton(self.sidebar, text="Blocker", command=self.show_blocker)
        self.btn_blocker.pack(pady=10, fill="x", padx=10)

        self.btn_settings = ctk.CTkButton(self.sidebar, text="Einstellungen", command=self.show_coming_soon)
        self.btn_settings.pack(pady=10, fill="x", padx=10)

        self.btn_profile = ctk.CTkButton(self.sidebar, text="Profil", command=self.show_coming_soon)
        self.btn_profile.pack(pady=10, fill="x", padx=10)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout)
        self.btn_logout.pack(pady=40, fill="x", padx=10)

        
        self.active_page = None
        self.show_blocker()

    def clear_content(self):
        if self.active_page:
            self.active_page.pack_forget()
            self.active_page.destroy()
            self.active_page = None

    def show_blocker(self):
        self.clear_content()
        self.active_page = PageBlocker(self.content_area, app=self.app)
        self.active_page.pack(fill="both", expand=True)

    def show_coming_soon(self):
        self.clear_content()
        frame = ctk.CTkFrame(self.content_area)
        label = ctk.CTkLabel(frame, text="🔧 Kommt bald...", font=ctk.CTkFont(size=18))
        label.pack(expand=True)
        frame.pack(fill="both", expand=True)
        self.active_page = frame

    def logout(self):
        self.master.main_window.pack_forget()
        from screens.login_screen import LoginScreen
        self.master.login_screen = LoginScreen(master=self.master, on_login_success=self.master.start_main_window)
        self.master.login_screen.pack(fill="both", expand=True)
