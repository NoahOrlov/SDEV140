"""
BMI Calculator Pro - A Tkinter-based GUI application for calculating Body Mass Index
Author: Noah Caslin 
Date: 2/27/2025

A GUI application developed using Tkinter that calculates the Body Mass Index (BMI)
based on user input for height and weight. It supports both Metric and Imperial systems,
providing health classification and advice based on the BMI result.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

class BMICalculator:
    """
    Main application class handling BMI calculation and GUI management
    """

    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator Pro")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.setup_styles()
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize variables
        self.unit_system = tk.StringVar(value="Metric")
        self.height_unit = tk.StringVar(value="cm")
        self.weight_unit = tk.StringVar(value="kg")
        self.height_value = tk.StringVar()
        self.weight_value = tk.StringVar()
        self.bmi_result = tk.DoubleVar()
        self.bmi_category = tk.StringVar()

        self.create_main_window()

    def setup_styles(self):
        """Configure widget styles"""
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Result.TLabel', font=('Arial', 14))
        style.configure('TButton', font=('Arial', 12))
        style.configure('Calculate.TButton', font=('Arial', 12, 'bold'))

    def create_main_window(self):
        """Build the main input interface"""
        self.clear_frame()

        # Title and description
        ttk.Label(self.main_frame, text="BMI Calculator Pro", style='Header.TLabel'
                  ).grid(row=0, column=0, columnspan=3, pady=10, sticky='w')
        ttk.Label(self.main_frame,
                  text="Calculate your Body Mass Index (BMI) to assess your weight relative to your height.",
                  wraplength=450).grid(row=1, column=0, columnspan=3, pady=10, sticky='w')

        # Unit system selection
        unit_frame = ttk.LabelFrame(self.main_frame, text="Measurement System")
        unit_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')

        ttk.Radiobutton(unit_frame, text="Metric (kg, cm)", variable=self.unit_system,
                        value="Metric", command=self.update_unit_labels
                        ).grid(row=0, column=0, padx=20, pady=5, sticky='w')
        ttk.Radiobutton(unit_frame, text="Imperial (lb, in)", variable=self.unit_system,
                        value="Imperial", command=self.update_unit_labels
                        ).grid(row=0, column=1, padx=20, pady=5, sticky='w')

        # Height input
        ttk.Label(self.main_frame, text="Height:").grid(row=3, column=0, pady=10, sticky='w')
        ttk.Entry(self.main_frame, textvariable=self.height_value, width=10
                  ).grid(row=3, column=1, pady=10, sticky='w')
        ttk.Label(self.main_frame, textvariable=self.height_unit
                  ).grid(row=3, column=2, pady=10, sticky='w')

        # Weight input
        ttk.Label(self.main_frame, text="Weight:").grid(row=4, column=0, pady=10, sticky='w')
        ttk.Entry(self.main_frame, textvariable=self.weight_value, width=10
                  ).grid(row=4, column=1, pady=10, sticky='w')
        ttk.Label(self.main_frame, textvariable=self.weight_unit
                  ).grid(row=4, column=2, pady=10, sticky='w')

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text="Calculate BMI", command=self.calculate_bmi,
                    style='Calculate.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Clear", command=self.clear_inputs
                    ).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.exit_application
                    ).grid(row=0, column=2, padx=10)

        # Health emojis
        emoji_label = ttk.Label(self.main_frame, 
                              text="🏋♂💪🍎🏃♀", 
                              font=('Arial', 24))
        emoji_label.grid(row=6, column=0, columnspan=3, pady=20)

    def create_results_window(self):
        """Build the results display interface"""
        self.clear_frame()

        # Results header
        ttk.Label(self.main_frame, text="Your BMI Results", style='Header.TLabel'
                  ).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

        # BMI value
        ttk.Label(self.main_frame, text="Your BMI:", style='Result.TLabel'
                  ).grid(row=1, column=0, pady=10, sticky='w')
        ttk.Label(self.main_frame, textvariable=self.bmi_result,
                  style='Result.TLabel', font=('Arial', 16, 'bold')
                  ).grid(row=1, column=1, pady=10, sticky='w')

        # BMI category
        ttk.Label(self.main_frame, text="Classification:", style='Result.TLabel'
                  ).grid(row=2, column=0, pady=10, sticky='w')
        self.category_value_label = ttk.Label(self.main_frame, textvariable=self.bmi_category,
                                                 style='Result.TLabel', font=('Arial', 16, 'bold'))
        self.category_value_label.grid(row=2, column=1, pady=10, sticky='w')
        self.set_category_color()

        # Recommendation
        recommendation_frame = ttk.LabelFrame(self.main_frame, text="Health Recommendation")
        recommendation_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky='ew')
        ttk.Label(recommendation_frame, text=self.get_recommendation(), wraplength=450
                  ).grid(row=0, column=0, padx=10, pady=10)

        # BMI chart emojis
        chart_emojis = ttk.Label(self.main_frame, 
                               text="📊🏃♀🏋♂🍏⚖️❤️", 
                               font=('Arial', 24))
        chart_emojis.grid(row=4, column=0, columnspan=2, pady=10)

        # Navigation buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Back to Calculator", command=self.create_main_window
                  ).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.exit_application
                                     ).grid(row=0, column=1, padx=10)

    # ... (Keep all other methods unchanged below this point)

    def update_unit_labels(self):
        """Update measurement units based on selected system"""
        system = self.unit_system.get()
        self.height_unit.set("cm" if system == "Metric" else "in")
        self.weight_unit.set("kg" if system == "Metric" else "lb")

    def validate_input(self):
        """Validate user input values"""
        if not self.height_value.get() or not self.weight_value.get():
            messagebox.showerror("Input Error", "Please enter both height and weight values.")
            return False

        try:
            height = Decimal(self.height_value.get())
            weight = Decimal(self.weight_value.get())

            if height <= 0 or weight <= 0:
                messagebox.showerror("Input Error", "Values must be positive numbers.")
                return False

            system = self.unit_system.get()
            ranges = {
                "Metric": {"height": (50, 250), "weight": (20, 500)},
                "Imperial": {"height": (20, 100), "weight": (45, 1000)}
            }

            if not (ranges[system]["height"][0] < height < ranges[system]["height"][1]):
                messagebox.showerror("Input Error",
                                        f"Height must be between {ranges[system]['height'][0]} "
                                        f"and {ranges[system]['height'][1]} {self.height_unit.get()}")
                return False

            if not (ranges[system]["weight"][0] < weight < ranges[system]["weight"][1]):
                messagebox.showerror("Input Error",
                                        f"Weight must be between {ranges[system]['weight'][0]} "
                                        f"and {ranges[system]['weight'][1]} {self.weight_unit.get()}")
                return False

            return True

        except InvalidOperation:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return False

    def calculate_bmi(self):
        """Calculate and display BMI results"""
        if not self.validate_input():
            return

        try:
            height = float(self.height_value.get())
            weight = float(self.weight_value.get())

            if self.unit_system.get() == "Metric":
                bmi = weight / ((height / 100) ** 2)
            else:
                bmi = 703 * weight / (height ** 2)

            self.bmi_result.set(round(bmi, 1))
            self.bmi_category.set(self.classify_bmi(bmi))
            self.create_results_window()

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error: {str(e)}")

    def classify_bmi(self, bmi):
        """Determine BMI classification"""
        if bmi < 18.5: return "Underweight"
        if bmi < 25: return "Normal Weight"
        if bmi < 30: return "Overweight"
        return "Obese"

    def set_category_color(self):
        """Set color coding for BMI classification"""
        colors = {
            "Underweight": "blue",
            "Normal Weight": "green",
            "Overweight": "orange",
            "Obese": "red"
        }
        self.category_value_label.configure(
            foreground=colors.get(self.bmi_category.get(), "black"))

    def get_recommendation(self):
        """Generate health recommendation based on BMI"""
        recommendations = {
            "Underweight": "Consult a healthcare provider about healthy weight gain strategies.",
            "Normal Weight": "Maintain your healthy weight with balanced nutrition and exercise.",
            "Overweight": "Consider dietary improvements and increased physical activity.",
            "Obese": "Consult a healthcare provider for a weight management plan."
        }
        return recommendations.get(self.bmi_category.get(), "")

    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def clear_inputs(self):
        """Reset input fields"""
        self.height_value.set("")
        self.weight_value.set("")

    def exit_application(self):
        """Handle application exit"""
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
