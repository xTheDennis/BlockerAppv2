import customtkinter as ctk
from tkinter import messagebox
import hashlib
import sqlite3
import os

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, on_login_success, show_register_screen, app):
        super().__init__(master)

        self.master = master
        self.on_login_success = on_login_success
        self.show_register_screen = show_register_screen
        self.app = app 
        
        
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Keine Lust mehr auf Gambling?", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=40)

        self.label_subtitle = ctk.CTkLabel(self, text="Melde dich jetzt an", font=ctk.CTkFont(size=16))
        self.label_subtitle.pack(pady=(0, 40))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Benutzername")
        self.username_entry.pack(pady=10, ipadx=100)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", show="*")
        self.password_entry.pack(pady=10, ipadx=100)

        self.login_button = ctk.CTkButton(self, text="Anmelden", command=self.login)
        self.login_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

        self.register_label = ctk.CTkLabel(self, text="Noch kein Konto? Jetzt registrieren!", text_color="skyblue", cursor="hand2")
        self.register_label.pack(pady=(10, 0))
        self.register_label.bind("<Button-1>", self.open_register)

    def login(self):
        nutzer = self.username_entry.get()
        passwort = self.password_entry.get()

        if not nutzer or not passwort:
            self.status_label.configure(text="Bitte alle Felder ausfüllen.")
            return

        hashed_pw = hashlib.sha256(passwort.encode()).hexdigest()

        try:
            db_path = os.path.join(os.path.dirname(__file__), "..", "db", "FGambling.db")
            db_path = os.path.abspath(db_path)
            with sqlite3.connect(db_path, timeout=5) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id, password FROM User WHERE username = ?", (nutzer,))
                result = cur.fetchone()

                if result and result[1] == hashed_pw:
                    user_id = result[0]
                    self.app.current_user_id = user_id
                    self.status_label.configure(text="")
                    self.on_login_success()
                else:
                    self.status_label.configure(text="Falscher Benutzername oder Passwort.")

        except Exception as e:
            messagebox.showerror("Fehler", f"Datenbankfehler: {e}")

    def open_register(self, event):
        self.show_register_screen()
