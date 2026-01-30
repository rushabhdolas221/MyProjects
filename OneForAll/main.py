import tkinter as tk
from tkinter import messagebox

# ---------- COLORS ----------
PRIMARY = "#2563EB"
BG = "#F8FAFC"
CARD = "#FFFFFF"
TEXT = "#111827"


# ---------- LOGIN SCREEN ----------
class LoginScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)

        tk.Label(
            self,
            text="One For All",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=60)

        tk.Label(
            self,
            text="Housing • Travel • Services",
            bg=BG,
            fg="#6B7280"
        ).pack(pady=5)

        tk.Label(self, text="Your Name", bg=BG).pack(pady=15)
        tk.Entry(self, width=30).pack(pady=5)

        tk.Button(
            self,
            text="Login",
            width=25,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            command=lambda: app.show_screen(HomeScreen)
        ).pack(pady=40)


# ---------- HOME SCREEN ----------
class HomeScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)

        tk.Label(
            self,
            text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg=BG
        ).pack(pady=30)

        self.card("🏠 Housing", lambda: app.show_screen(HousingScreen))
        self.card("🚗 Carpool", lambda: app.show_screen(TravelScreen))
        self.card("🛠 Local Services", lambda: app.show_screen(ServicesScreen))

    def card(self, text, action):
        frame = tk.Frame(self, bg=CARD, bd=0, relief="flat")
        frame.pack(pady=12, padx=30, fill="x")

        tk.Button(
            frame,
            text=text,
            font=("Segoe UI", 14),
            bg=CARD,
            fg=TEXT,
            relief="flat",
            command=action
        ).pack(pady=18)


# ---------- HOUSING ----------
class HousingScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)

        tk.Label(self, text="Housing", font=("Segoe UI", 22, "bold"), bg=BG).pack(pady=30)

        self.action("Pay Rent", "Rent paid successfully")
        self.action("Maintenance Request", "Maintenance request sent")

        self.back(app)

    def action(self, text, msg):
        tk.Button(
            self,
            text=text,
            width=25,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            command=lambda: messagebox.showinfo("Success", msg)
        ).pack(pady=10)

    def back(self, app):
        tk.Button(
            self,
            text="⬅ Back",
            bg=BG,
            relief="flat",
            command=lambda: app.show_screen(HomeScreen)
        ).pack(pady=30)


# ---------- TRAVEL ----------
class TravelScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)

        tk.Label(self, text="Carpool", font=("Segoe UI", 22, "bold"), bg=BG).pack(pady=30)

        self.action("Create Ride", "Ride created")
        self.action("Join Ride", "Ride joined")

        self.back(app)

    def action(self, text, msg):
        tk.Button(
            self,
            text=text,
            width=25,
            bg=PRIMARY,
            fg="white",
            relief="flat",
            command=lambda: messagebox.showinfo("Carpool", msg)
        ).pack(pady=10)

    def back(self, app):
        tk.Button(
            self,
            text="⬅ Back",
            bg=BG,
            relief="flat",
            command=lambda: app.show_screen(HomeScreen)
        ).pack(pady=30)


# ---------- SERVICES ----------
class ServicesScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)

        tk.Label(self, text="Local Services", font=("Segoe UI", 22, "bold"), bg=BG).pack(pady=30)

        self.service("Plumber")
        self.service("Electrician")
        self.service("Cleaner")

        self.back(app)

    def service(self, name):
        tk.Button(
            self,
            text=name,
            width=25,
            bg=CARD,
            fg=TEXT,
            relief="flat",
            command=lambda: messagebox.showinfo("Service", f"{name} booked")
        ).pack(pady=8)

    def back(self, app):
        tk.Button(
            self,
            text="⬅ Back",
            bg=BG,
            relief="flat",
            command=lambda: app.show_screen(HomeScreen)
        ).pack(pady=30)


# ---------- MAIN APP ----------
class OneForAllApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("One For All")
        self.geometry("400x700")
        self.configure(bg=BG)

        self.frames = {}

        for Screen in (
            LoginScreen,
            HomeScreen,
            HousingScreen,
            TravelScreen,
            ServicesScreen
        ):
            frame = Screen(self)
            self.frames[Screen] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_screen(LoginScreen)

    def show_screen(self, screen):
        self.frames[screen].tkraise()


# ---------- RUN ----------
if __name__ == "__main__":
    app = OneForAllApp()
    app.mainloop()
