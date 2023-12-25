import math
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import tkinter as tk

class Projectile:
    def __init__(self, initial_velocity, launch_angle, gravity):
        self.initial_velocity = initial_velocity
        self.launch_angle = math.radians(launch_angle)
        self.gravity = gravity

class ProjectileSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Projectile Motion Simulator")
        self.unit_system_var = StringVar()
        self.num_projectiles_var = StringVar()
        self.results_text_var = StringVar()
        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Choose unit system (SI or US):").grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.unit_system_var).grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Enter the number of projectiles:").grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.num_projectiles_var).grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Simulate", command=self.simulate_projectiles).grid(row=2, column=0, columnspan=2, pady=20)

        Label(self.root, text="Results:").grid(row=3, column=0, columnspan=2, pady=10)
        Label(self.root, textvariable=self.results_text_var).grid(row=4, column=0, columnspan=2, pady=10)

    def simulate_projectiles(self):
        unit_system = self.unit_system_var.get().upper()
        num_projectiles = int(self.num_projectiles_var.get())

        projectiles = []
        results_list = []

        for i in range(num_projectiles):
            try:
                initial_velocity = float(input(f"Enter initial velocity ({get_velocity_unit(unit_system)}): "))
                launch_angle = float(input("Enter launch angle in degrees: "))
                gravity = float(input(f"Enter gravitational acceleration ({get_gravity_unit(unit_system)}): "))
                projectiles.append(Projectile(initial_velocity, launch_angle, gravity))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
                return

        for i, projectile in enumerate(projectiles, start=1):
            x_points, y_points, time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)

            plt.plot(x_points, y_points, label=f"Projectile {i}")

            results_text = (
                f"Projectile {i} - Time of Flight: {time_of_flight} {get_time_unit(unit_system)}, "
                f"Max Height: {max_height} {get_length_unit(unit_system)}, Range: {range_val} {get_length_unit(unit_system)}"
            )

            results_list.append(results_text)

        self.results_text_var.set("\n".join(results_list))

        plt.title("Projectile Motion")
        plt.xlabel(f"Horizontal Distance ({get_length_unit(unit_system)})")
        plt.ylabel(f"Vertical Distance ({get_length_unit(unit_system)})")
        plt.legend()
        plt.show()

        self.show_additional_info(projectiles, unit_system)

    def calculate_trajectory(self, projectile):
        time_of_flight = (2 * projectile.initial_velocity * math.sin(projectile.launch_angle)) / projectile.gravity
        max_height = (projectile.initial_velocity**2 * (math.sin(projectile.launch_angle))**2) / (2 * projectile.gravity)
        range_val = (projectile.initial_velocity**2 * math.sin(2 * projectile.launch_angle)) / projectile.gravity

        time_points = [i * 0.1 for i in range(int(time_of_flight * 10) + 1)]
        x_points = [projectile.initial_velocity * math.cos(projectile.launch_angle) * t for t in time_points]
        y_points = [
            projectile.initial_velocity * math.sin(projectile.launch_angle) * t - 0.5 * projectile.gravity * t**2
            for t in time_points
        ]

        return x_points, y_points, time_of_flight, max_height, range_val

    def show_additional_info(self, projectiles, unit_system):
        info_window = tk.Toplevel(self.root)
        info_window.title("Projectile Information")

        for i, projectile in enumerate(projectiles, start=1):
            time_of_flight, max_height, range_val = self.calculate_trajectory(projectile)[2:]
            info_label = Label(info_window, text=(
                f"Projectile {i} Information:\n"
                f"Time of Flight: {time_of_flight} {get_time_unit(unit_system)}\n"
                f"Max Height: {max_height} {get_length_unit(unit_system)}\n"
                f"Range: {range_val} {get_length_unit(unit_system)}"
            ))
            info_label.pack(pady=10)

def get_velocity_unit(unit_system):
    return "m/s" if unit_system == "SI" else "ft/s"

def get_gravity_unit(unit_system):
    return "m/s^2" if unit_system == "SI" else "ft/s^2"

def get_time_unit(unit_system):
    return "s" if unit_system == "SI" else "s"

def get_length_unit(unit_system):
    return "m" if unit_system == "SI" else "ft"

if __name__ == "__main__":
    root = Tk()
    app = ProjectileSimulatorGUI(root)
    root.mainloop()