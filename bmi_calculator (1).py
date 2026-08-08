"""
BMI Calculator
--------------
A simple, beginner-friendly Body Mass Index (BMI) Calculator built with
Python's built-in Tkinter library.

Author: (Your Name)
"""

import tkinter as tk
from tkinter import messagebox, font


# ---------------------------------------------------------------------------
# GLOBAL CONSTANTS
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 420
WINDOW_HEIGHT = 560

COLOR_UNDERWEIGHT = "blue"
COLOR_NORMAL = "green"
COLOR_OVERWEIGHT = "orange"
COLOR_OBESE = "red"


# ---------------------------------------------------------------------------
# VALIDATION FUNCTION
# ---------------------------------------------------------------------------
def validate_inputs(name, age_str, weight_str, height_str):
    """
    Validate all the fields entered by the user.
    Returns a tuple: (is_valid, age, weight, height, error_message)
    If is_valid is False, error_message explains what went wrong.
    """

    # 1. Check that no field is empty
    if name.strip() == "" or age_str.strip() == "" or \
            weight_str.strip() == "" or height_str.strip() == "":
        return False, None, None, None, "All fields must be filled in."

    # 2. Check that age, weight, and height are numeric
    try:
        age = float(age_str)
        weight = float(weight_str)
        height = float(height_str)
    except ValueError:
        return False, None, None, None, \
            "Age, Weight, and Height must be valid numbers."

    # 3. Check that age is positive
    if age <= 0:
        return False, None, None, None, "Age must be a positive number."

    # 4. Check that weight and height are greater than zero
    if weight <= 0:
        return False, None, None, None, "Weight must be greater than zero."

    if height <= 0:
        return False, None, None, None, "Height must be greater than zero."

    # If everything passed, the inputs are valid
    return True, age, weight, height, ""


# ---------------------------------------------------------------------------
# BMI CALCULATION FUNCTION
# ---------------------------------------------------------------------------
def calculate_bmi_value(weight_kg, height_cm):
    """
    Calculate BMI given weight in kilograms and height in centimeters.
    Formula: BMI = weight (kg) / height (m)^2
    """
    height_m = height_cm / 100  # convert cm to meters
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


# ---------------------------------------------------------------------------
# BMI CATEGORY FUNCTION
# ---------------------------------------------------------------------------
def get_bmi_category(bmi):
    """
    Return the BMI category, its display color, and a short health
    recommendation based on the calculated BMI value.
    """
    if bmi < 18.5:
        category = "Underweight"
        color = COLOR_UNDERWEIGHT
        recommendation = ("You are underweight. Consider a balanced diet "
                           "with more calories and consult a nutritionist.")
    elif 18.5 <= bmi <= 24.9:
        category = "Normal Weight"
        color = COLOR_NORMAL
        recommendation = ("Great job! Maintain your current healthy diet "
                           "and stay physically active.")
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        color = COLOR_OVERWEIGHT
        recommendation = ("You are overweight. Try regular exercise and a "
                           "balanced, portion-controlled diet.")
    else:  # bmi >= 30.0
        category = "Obese"
        color = COLOR_OBESE
        recommendation = ("Please consult a healthcare professional for "
                           "personalized advice and a suitable fitness plan.")

    return category, color, recommendation


# ---------------------------------------------------------------------------
# MAIN APPLICATION CLASS
# ---------------------------------------------------------------------------
class BMICalculatorApp:
    """
    Main class that builds and manages the BMI Calculator GUI.
    Using a class keeps our widgets and variables organized in one place.
    """

    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_fonts()
        self.create_widgets()

    # -----------------------------------------------------------------
    # WINDOW SETUP
    # -----------------------------------------------------------------
    def setup_window(self):
        """Configure the main window: title, size, and center it."""
        self.root.title("BMI Calculator")
        self.root.resizable(False, False)  # make window non-resizable

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y_position = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_position}+{y_position}"
        )
        self.root.configure(bg="#f0f4f7")

        # Pressing Enter anywhere in the window triggers the calculation
        self.root.bind("<Return>", lambda event: self.on_calculate_click())

        # Handle the window's "X" close button like the Exit button
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit_click)

    # -----------------------------------------------------------------
    # FONT SETUP
    # -----------------------------------------------------------------
    def create_fonts(self):
        """Define fonts used throughout the application."""
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=11)
        self.entry_font = font.Font(family="Helvetica", size=11)
        self.button_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.small_font = font.Font(family="Helvetica", size=10)

    # -----------------------------------------------------------------
    # WIDGET CREATION
    # -----------------------------------------------------------------
    def create_widgets(self):
        """Create and arrange all widgets using frames for clean layout."""

        # ---------- Title ----------
        title_label = tk.Label(
            self.root, text="BMI Calculator",
            font=self.title_font, bg="#f0f4f7", fg="#2c3e50"
        )
        title_label.pack(pady=(20, 10))

        # ---------- Input Frame ----------
        input_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        input_frame.pack(padx=20, pady=10, fill="x")

        # Dictionary to store Tkinter StringVars for each field
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        # Create each labeled input row
        self.create_input_row(input_frame, "Name:", self.name_var, row=0)
        self.create_input_row(input_frame, "Age (years):", self.age_var, row=1)
        self.create_input_row(input_frame, "Weight (kg):", self.weight_var, row=2)
        self.create_input_row(input_frame, "Height (cm):", self.height_var, row=3)

        # ---------- Button Frame ----------
        button_frame = tk.Frame(self.root, bg="#f0f4f7")
        button_frame.pack(pady=15)

        calculate_button = tk.Button(
            button_frame, text="Calculate BMI", font=self.button_font,
            bg="#3498db", fg="white", width=13, command=self.on_calculate_click
        )
        calculate_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(
            button_frame, text="Clear", font=self.button_font,
            bg="#95a5a6", fg="white", width=13, command=self.on_clear_click
        )
        clear_button.grid(row=0, column=1, padx=5)

        exit_button = tk.Button(
            button_frame, text="Exit", font=self.button_font,
            bg="#e74c3c", fg="white", width=13, command=self.on_exit_click
        )
        exit_button.grid(row=0, column=2, padx=5)

        # ---------- Result Frame ----------
        result_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        result_frame.pack(padx=20, pady=10, fill="both", expand=True)

        result_title = tk.Label(
            result_frame, text="Result",
            font=self.label_font, bg="#ffffff", fg="#2c3e50"
        )
        result_title.pack(pady=(10, 5))

        # Label showing the numeric BMI value
        self.bmi_value_label = tk.Label(
            result_frame, text="BMI: --",
            font=self.result_font, bg="#ffffff", fg="#2c3e50"
        )
        self.bmi_value_label.pack(pady=5)

        # Label showing the BMI category (color-coded)
        self.category_label = tk.Label(
            result_frame, text="Category: --",
            font=self.result_font, bg="#ffffff", fg="#2c3e50"
        )
        self.category_label.pack(pady=5)

        # Label showing the health recommendation
        self.recommendation_label = tk.Label(
            result_frame, text="",
            font=self.small_font, bg="#ffffff", fg="#34495e",
            wraplength=340, justify="center"
        )
        self.recommendation_label.pack(pady=(5, 10), padx=10)

    def create_input_row(self, parent, label_text, text_variable, row):
        """
        Helper function to create one row containing a label and an
        entry field. This avoids repeating the same code four times.
        """
        label = tk.Label(
            parent, text=label_text, font=self.label_font,
            bg="#ffffff", fg="#2c3e50", anchor="w"
        )
        label.grid(row=row, column=0, sticky="w", padx=15, pady=10)

        entry = tk.Entry(
            parent, textvariable=text_variable, font=self.entry_font,
            width=18, relief="solid", bd=1
        )
        entry.grid(row=row, column=1, padx=15, pady=10)

    # -----------------------------------------------------------------
    # BUTTON ACTIONS
    # -----------------------------------------------------------------
    def on_calculate_click(self):
        """
        Called when the user clicks 'Calculate BMI' or presses Enter.
        Validates input, calculates BMI, and displays the result.
        """
        name = self.name_var.get()
        age_str = self.age_var.get()
        weight_str = self.weight_var.get()
        height_str = self.height_var.get()

        # Validate all fields first
        is_valid, age, weight, height, error_message = validate_inputs(
            name, age_str, weight_str, height_str
        )

        if not is_valid:
            messagebox.showerror("Invalid Input", error_message)
            return

        # Calculate BMI and determine category
        bmi = calculate_bmi_value(weight, height)
        category, color, recommendation = get_bmi_category(bmi)

        # Update the result section of the GUI
        self.bmi_value_label.config(text=f"BMI: {bmi}")
        self.category_label.config(text=f"Category: {category}", fg=color)
        self.recommendation_label.config(text=recommendation)

    def on_clear_click(self):
        """Reset all input fields and the result section."""
        self.name_var.set("")
        self.age_var.set("")
        self.weight_var.set("")
        self.height_var.set("")

        self.bmi_value_label.config(text="BMI: --", fg="#2c3e50")
        self.category_label.config(text="Category: --", fg="#2c3e50")
        self.recommendation_label.config(text="")

    def on_exit_click(self):
        """Ask for confirmation, then close the application."""
        confirm = messagebox.askyesno(
            "Exit Confirmation", "Are you sure you want to exit?"
        )
        if confirm:
            self.root.destroy()


# ---------------------------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------------------------
def main():
    """Create the main window and start the Tkinter event loop."""
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
