import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_gui.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS bmi (
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def calculate_bmi():
    try:
        name = name_entry.get()
        w = weight_slider.get()
        h = height_slider.get() / 100

        if name == "":
            messagebox.showerror("Error", "Enter Name")
            return

        bmi = round(w / (h * h), 2)

        if bmi < 18.5:
            status = "Underweight"
        elif bmi < 25:
            status = "Normal"
        elif bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"

        bmi_label.config(text=f"BMI: {bmi}")
        status_label.config(text=status)

        cur.execute(
            "INSERT INTO bmi VALUES (?,?,?,?,?)",
            (name, w, h * 100, bmi, datetime.datetime.now())
        )
        conn.commit()

    except:
        messagebox.showerror("Error", "Calculation Failed")

def show_graph():
    name = name_entry.get()
    cur.execute("SELECT bmi, date FROM bmi WHERE name=?", (name,))
    data = cur.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No BMI records found")
        return

    bmi = [i[0] for i in data]
    dates = [i[1] for i in data]

    plt.plot(dates, bmi, marker="o")
    plt.title(f"BMI Trend – {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x600")
root.configure(bg="#EAF6F6")

tk.Label(root, text="BMI CALCULATOR",
         font=("Arial", 18, "bold"),
         bg="#EAF6F6").pack(pady=10)

# Name
tk.Label(root, text="Name", bg="#EAF6F6").pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Cards Frame
card = tk.Frame(root, bg="#EAF6F6")
card.pack(pady=20)

# Weight Card
weight_frame = tk.Frame(card, bg="white", bd=2, relief="groove")
weight_frame.grid(row=0, column=0, padx=10)

tk.Label(weight_frame, text="Weight (kg)",
         font=("Arial", 12), bg="white").pack()
weight_value = tk.Label(weight_frame, text="60",
                        font=("Arial", 24), bg="white")
weight_value.pack()

weight_slider = tk.Scale(weight_frame, from_=30, to=150,
                         orient="horizontal", bg="white",
                         command=lambda v: weight_value.config(text=v))
weight_slider.set(60)
weight_slider.pack()

# Height Card
height_frame = tk.Frame(card, bg="white", bd=2, relief="groove")
height_frame.grid(row=0, column=1, padx=10)

tk.Label(height_frame, text="Height (cm)",
         font=("Arial", 12), bg="white").pack()
height_value = tk.Label(height_frame, text="170",
                        font=("Arial", 24), bg="white")
height_value.pack()

height_slider = tk.Scale(height_frame, from_=120, to=210,
                         orient="horizontal", bg="white",
                         command=lambda v: height_value.config(text=v))
height_slider.set(170)
height_slider.pack()

# Result
bmi_label = tk.Label(root, text="BMI: --",
                     font=("Arial", 14), bg="#EAF6F6")
bmi_label.pack()

status_label = tk.Label(root, text="Status",
                        font=("Arial", 14, "bold"),
                        bg="#EAF6F6")
status_label.pack()

# Buttons
tk.Button(root, text="Calculate BMI",
          command=calculate_bmi).pack(pady=5)

tk.Button(root, text="View BMI Trend",
          command=show_graph).pack(pady=5)

root.mainloop()
