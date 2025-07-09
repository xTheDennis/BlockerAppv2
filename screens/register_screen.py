import customtkinter as ctk
import hashlib
import sqlite3
import os

class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master, on_register_success, show_login_screen, app):
        super().__init__(master)
        self.master = master
        self.on_register_success = on_register_success
        self.show_login_screen = show_login_screen
        self.app = app 

        self.label_title = ctk.CTkLabel(self, text="Registrieren", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.pack(pady=(60, 10))

        self.label_subtitle = ctk.CTkLabel(self, text="Erstelle jetzt dein Konto", font=ctk.CTkFont(size=16))
        self.label_subtitle.pack(pady=(0, 40))

      
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(pady=10)
        self.entry_username = ctk.CTkEntry(row1, placeholder_text="Benutzername", width=180)
        self.entry_username.pack(side="left", padx=10)
        self.entry_email = ctk.CTkEntry(row1, placeholder_text="E-Mail", width=180)
        self.entry_email.pack(side="left", padx=10)

        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(pady=10)
        self.entry_password = ctk.CTkEntry(row2, placeholder_text="Passwort", show="*", width=180)
        self.entry_password.pack(side="left", padx=10)
        self.entry_confirm_password = ctk.CTkEntry(row2, placeholder_text="Passwort bestätigen", show="*", width=180)
        self.entry_confirm_password.pack(side="left", padx=10)

        self.register_button = ctk.CTkButton(self, text="Konto erstellen", command=self.register)
        self.register_button.pack(pady=(10, 20))

        self.login_label = ctk.CTkLabel(self, text="Schon ein Konto? Hier anmelden!", text_color="skyblue")
        self.login_label.pack()
        self.login_label.bind("<Button-1>", self.back_to_login)

        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.pack(pady=10)

    def register(self):
        nutzer = self.entry_username.get()
        email = self.entry_email.get()
        passwort = self.entry_password.get()
        passwort2 = self.entry_confirm_password.get()

        if not nutzer or not email or not passwort or not passwort2:
            self.message_label.configure(text="Bitte fülle alle Felder aus.")
            return

        if passwort != passwort2:
            self.message_label.configure(text="Passwörter stimmen nicht überein!")
            return

        hashed_pw = hashlib.sha256(passwort.encode()).hexdigest()

        try:
            db_path = os.path.join("db", "FGambling.db")
            with sqlite3.connect(db_path) as conn:
                cur = conn.cursor()

                cur.execute("SELECT * FROM User WHERE username = ?", (nutzer,))
                if cur.fetchone():
                    self.message_label.configure(text="Benutzername bereits vergeben!")
                    return

                cur.execute("INSERT INTO User (username, password, email) VALUES (?, ?, ?)",
                            (nutzer, hashed_pw, email))
                conn.commit()

            self.message_label.configure(text="Benutzer erfolgreich registriert", text_color="green")
            self.on_register_success()

        except Exception as e:
            self.message_label.configure(text=f"Fehler: {str(e)}", text_color="red")

    def back_to_login(self, event=None):
        self.show_login_screen()
