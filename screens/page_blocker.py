import customtkinter as ctk
import threading
import time
import winsound
import os
import sqlite3
import win32gui
import win32process
import psutil
import pygetwindow as gw
import tkinter as tk

DANGEROUS_SITES = []
BROWSERS_TO_KILL = ["chrome.exe", "msedge.exe", "opera.exe"]

class PageBlocker(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.running = True

        # GUI
        ctk.CTkLabel(self, text="🔒 FGambling Blocker", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 10))
        self.status_label = ctk.CTkLabel(self, text="Status: Aktiv", text_color="green", font=ctk.CTkFont(size=20, weight="bold"))
        self.status_label.pack(pady=(10, 20))

        ctk.CTkLabel(self, text="Aktuell blockierte Seiten:", font=ctk.CTkFont(size=16)).pack()
        self.listbox = ctk.CTkTextbox(self, height=120, width=400)
        self.listbox.configure(state="disabled")
        self.listbox.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Weitere Seite hinzufügen:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack()
        self.new_site_entry = ctk.CTkEntry(input_frame, width=260, placeholder_text="z. B. bet365.com")
        self.new_site_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(input_frame, text="Hinzufügen", command=self.add_site).pack(side="left")

        self.load_blocked_sites_from_db()

        # Thread starten
        self.monitor_thread = threading.Thread(target=self.monitor_windows, daemon=True)
        self.monitor_thread.start()

    def refresh_listbox(self):
        self.listbox.configure(state="normal")
        self.listbox.delete("0.0", "end")
        for site in DANGEROUS_SITES:
            self.listbox.insert("end", f"{site}\n")
        self.listbox.configure(state="disabled")

    def add_site(self):
        new_site = self.new_site_entry.get().strip().lower()
        user_id = self.app.current_user_id
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "FGambling.db"))

        if new_site and new_site not in DANGEROUS_SITES:
            try:
                with sqlite3.connect(db_path) as conn:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO BlockedSites (user_id, site) VALUES (?, ?)", (user_id, new_site))
                DANGEROUS_SITES.append(new_site)
                self.refresh_listbox()
                self.new_site_entry.delete(0, "end")
            except Exception as e:
                print("Fehler beim Speichern:", e)

    def load_blocked_sites_from_db(self):
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "FGambling.db"))
        user_id = self.app.current_user_id

        try:
            with sqlite3.connect(db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT site FROM BlockedSites WHERE user_id = ?", (user_id,))
                urls = [row[0] for row in cur.fetchall()]
                DANGEROUS_SITES.clear()
                DANGEROUS_SITES.extend(urls)
                self.refresh_listbox()
                print(f"📛 Geladene Blockseiten: {DANGEROUS_SITES}")
        except Exception as e:
            print("Fehler beim Laden der Blockliste:", e)

    def get_process_name_from_hwnd(self, hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name().lower()
        except Exception as e:
            print("Fehler beim Ermitteln des Prozesses:", e)
            return ""

    def monitor_windows(self):
        print("🔍 Überwachung gestartet!")
        while self.running:
            try:
                def callback(hwnd, _):
                    if not win32gui.IsWindowVisible(hwnd):
                        return
                    title = win32gui.GetWindowText(hwnd).lower()
                    process_name = self.get_process_name_from_hwnd(hwnd)

                    if process_name in BROWSERS_TO_KILL:
                        for site in DANGEROUS_SITES:
                            if site.replace(".com", "") in title:
                                print(f"[!] BLOCKIERT in {process_name}: {site}")
                                threading.Thread(target=self.play_warning_sound).start()
                                threading.Thread(target=self.show_warning_overlay).start()
                                self.kill_blocking_window(hwnd)
                                return  

                win32gui.EnumWindows(callback, None)

            except Exception as e:
                print("Fehler im Blocker:", e)

            time.sleep(1)

    def play_warning_sound(self):
        for _ in range(3):
            winsound.Beep(1000, 800)

    def show_warning_overlay(self, *args):
        
        root = tk.Tk()
        root.title("⚠️ WARNUNG ⚠️")
        root.attributes('-topmost', True)
        root.configure(bg='red')
        root.geometry("500x200+600+300")  

        label = tk.Label(root, text="❌ KEIN GLÜCKSSPIEL!", font=("Arial", 20, "bold"), bg="red", fg="black")
        label.pack(expand=True)

        root.after(5000, lambda: root.destroy())
        root.mainloop()

    def kill_blocking_window(self, hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            name = proc.name()
            print(f"💀 Gekillt: {name} (PID: {pid}) wegen Fenster: {win32gui.GetWindowText(hwnd)}")
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
            print("Fehler beim gezielten Schließen:", e)
