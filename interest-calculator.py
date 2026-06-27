import tkinter as tk

class InterestCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Interest Calculator")

        # Widgets for the form
        self.label_principal = tk.Label(root, text="Principal Amount:")
        self.label_interest_rate = tk.Label(root, text="Interest Rate (in %):")
        self.label_time_in_years = tk.Label(root, text="Time in Years:")
        self.entry_principal = tk.Entry(root)
        self.entry_interest_rate = tk.Entry(root)
        self.entry_time_in_years = tk.Entry(root)

        # Buttons to perform calculations
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate_interest)

        # Display the results
        self.result_label = tk.Label(root, text="")

        # Layout of widgets on the window
        self.label_principal.grid(row=0, column=0)
        self.entry_principal.grid(row=0, column=1)
        self.label_interest_rate.grid(row=1, column=0)
        self.entry_interest_rate.grid(row=1, column=1)
        self.label_time_in_years.grid(row=2, column=0)
        self.entry_time_in_years.grid(row=2, column=1)
        self.calculate_button.grid(row=3, columnspan=2)
        self.result_label.grid(row=4, columnspan=2)

    def calculate_interest(self):
        principal = float(self.entry_principal.get())
        interest_rate = float(self.entry_interest_rate.get()) / 100
        time_in_years = float(self.entry_time_in_years.get())

        # Calculate simple interest
        simple_interest = principal * (interest_rate * time_in_years)

        self.result_label.config(text=f"Simple Interest: ${simple_interest:.2f}")

# Create the main application window
root = tk.Tk()

# Instantiate the InterestCalculator class with this root window
calculator_window = InterestCalculator(root)

# Start the Tkinter event loop
root.mainloop()
