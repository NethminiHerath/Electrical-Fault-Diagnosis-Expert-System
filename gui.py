import customtkinter as ctk
from rules import diagnose_fault
from database import save_diagnosis, get_diagnosis_history

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FaultExpertSystemGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Electrical Fault Diagnosis Expert System")
        self.geometry("1250x850")
        self.configure(fg_color="#071A2F")

        self.title_label = ctk.CTkLabel(
            self,
            text="Electrical Fault Diagnosis Expert System",
            font=("Segoe UI", 28, "bold"),
            text_color="#EAF6FF"
        )
        self.title_label.pack(pady=(22, 5))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Rule-Based Electrical Fault Detection and Protection Advisor",
            font=("Segoe UI", 14),
            text_color="#8ECDF8"
        )
        self.subtitle_label.pack(pady=(0, 15))

        self.main_frame = ctk.CTkFrame(self, fg_color="#0B2545", corner_radius=18)
        self.main_frame.pack(fill="x", padx=25, pady=10)

        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#123A63", corner_radius=15)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        self.option_frame = ctk.CTkFrame(self.main_frame, fg_color="#123A63", corner_radius=15)
        self.option_frame.pack(side="right", fill="both", expand=True, padx=18, pady=18)

        self.create_inputs()
        self.create_options()
        self.create_buttons()
        self.create_output_box()

    def create_inputs(self):
        heading = ctk.CTkLabel(
            self.input_frame,
            text="Input Readings",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAF6FF"
        )
        heading.grid(row=0, column=0, columnspan=2, pady=(15, 20))

        self.voltage_entry = self.create_entry("Voltage (V)", 1)
        self.current_entry = self.create_entry("Current (A)", 2)
        self.temperature_entry = self.create_entry("Temperature (°C)", 3)
        self.frequency_entry = self.create_entry("Frequency (Hz)", 4)

    def create_entry(self, label_text, row):
        label = ctk.CTkLabel(
            self.input_frame,
            text=label_text,
            font=("Segoe UI", 14),
            text_color="#D6EEFF"
        )
        label.grid(row=row, column=0, padx=25, pady=12, sticky="w")

        entry = ctk.CTkEntry(
            self.input_frame,
            width=260,
            height=40,
            fg_color="#071A2F",
            border_color="#4DA3D9",
            text_color="#FFFFFF",
            placeholder_text="Enter value"
        )
        entry.grid(row=row, column=1, padx=25, pady=12)

        return entry

    def create_options(self):
        heading = ctk.CTkLabel(
            self.option_frame,
            text="System Conditions",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAF6FF"
        )
        heading.pack(pady=(15, 22))

        self.maintenance_var = ctk.BooleanVar()
        self.emergency_var = ctk.BooleanVar()
        self.current_fluctuation_var = ctk.BooleanVar()
        self.voltage_fluctuation_var = ctk.BooleanVar()

        self.create_checkbox("Maintenance Mode", self.maintenance_var)
        self.create_checkbox("Emergency Load", self.emergency_var)
        self.create_checkbox("Current Fluctuation", self.current_fluctuation_var)
        self.create_checkbox("Voltage Fluctuation", self.voltage_fluctuation_var)

    def create_checkbox(self, text, variable):
        checkbox = ctk.CTkCheckBox(
            self.option_frame,
            text=text,
            variable=variable,
            font=("Segoe UI", 14),
            text_color="#D6EEFF",
            fg_color="#1E88E5",
            hover_color="#42A5F5",
            border_color="#8ECDF8"
        )
        checkbox.pack(anchor="w", padx=55, pady=14)

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="#071A2F")
        button_frame.pack(pady=18)

        self.diagnose_button = ctk.CTkButton(
            button_frame,
            text="Diagnose Fault",
            width=190,
            height=44,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#1E88E5",
            hover_color="#42A5F5",
            command=self.diagnose
        )
        self.diagnose_button.grid(row=0, column=0, padx=18)

        self.history_button = ctk.CTkButton(
            button_frame,
            text="View History",
            width=190,
            height=44,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#1565C0",
            hover_color="#42A5F5",
            command=self.show_history
        )
        self.history_button.grid(row=0, column=1, padx=18)

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=190,
            height=44,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#0D47A1",
            hover_color="#1976D2",
            command=self.clear_fields
        )
        self.clear_button.grid(row=0, column=2, padx=18)

    def create_output_box(self):
        output_frame = ctk.CTkFrame(self, fg_color="#0B2545", corner_radius=18)
        output_frame.pack(fill="both", expand=True, padx=25, pady=(5, 25))

        output_label = ctk.CTkLabel(
            output_frame,
            text="Diagnosis Output",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAF6FF"
        )
        output_label.pack(pady=(15, 8))

        self.output_box = ctk.CTkTextbox(
            output_frame,
            width=1150,
            height=430,
            fg_color="#061426",
            text_color="#EAF6FF",
            border_color="#1E88E5",
            border_width=1,
            corner_radius=12,
            font=("Consolas", 13),
            wrap="word"
        )
        self.output_box.pack(padx=20, pady=(5, 20), fill="both", expand=True)

    def diagnose(self):
        try:
            voltage = float(self.voltage_entry.get())
            current = float(self.current_entry.get())
            temperature = float(self.temperature_entry.get())
            frequency = float(self.frequency_entry.get())

            result = diagnose_fault(
                voltage=voltage,
                current=current,
                temperature=temperature,
                frequency=frequency,
                maintenance_mode=self.maintenance_var.get(),
                emergency_load=self.emergency_var.get(),
                current_fluctuation=self.current_fluctuation_var.get(),
                voltage_fluctuation=self.voltage_fluctuation_var.get()
            )

            save_diagnosis(
                voltage=voltage,
                current=current,
                temperature=temperature,
                frequency=frequency,
                maintenance_mode=self.maintenance_var.get(),
                emergency_load=self.emergency_var.get(),
                diagnosis=result[0],
                severity=result[1],
                actions=result[2],
                explanation=result[3]
            )

            actions = [action.strip() for action in result[2].split(";") if action.strip()]
            faults = [fault.strip() for fault in result[4].split(",") if fault.strip()]

            fault_text = ""
            for fault in faults:
                fault_text += f"• {fault}\n"

            action_text = ""
            for action in actions:
                action_text += f"• {action}\n"

            self.output_box.delete("1.0", "end")
            self.output_box.insert(
                "end",
                f"FINAL DIAGNOSIS\n"
                f"==============================\n"
                f"{result[0]}\n\n"
                f"SEVERITY\n"
                f"==============================\n"
                f"{result[1]}\n\n"
                f"DETECTED FAULTS\n"
                f"==============================\n"
                f"{fault_text}\n"
                f"RECOMMENDED ACTIONS\n"
                f"==============================\n"
                f"{action_text}\n"
                f"RULE EXPLANATION\n"
                f"==============================\n"
                f"{result[3]}"
            )

        except ValueError:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", "Please enter valid numeric values for all input fields.")

    def show_history(self):
        records = get_diagnosis_history()

        self.output_box.delete("1.0", "end")
        self.output_box.insert(
            "end",
            "DIAGNOSIS HISTORY\n"
            "==============================\n\n"
        )

        if not records:
            self.output_box.insert("end", "No records found.")
            return

        for record in records:
            self.output_box.insert(
                "end",
                f"Date     : {record[0]}\n"
                f"Fault    : {record[1]}\n"
                f"Severity : {record[2]}\n"
                f"------------------------------\n"
            )

    def clear_fields(self):
        self.voltage_entry.delete(0, "end")
        self.current_entry.delete(0, "end")
        self.temperature_entry.delete(0, "end")
        self.frequency_entry.delete(0, "end")

        self.maintenance_var.set(False)
        self.emergency_var.set(False)
        self.current_fluctuation_var.set(False)
        self.voltage_fluctuation_var.set(False)

        self.output_box.delete("1.0", "end")


if __name__ == "__main__":
    app = FaultExpertSystemGUI()
    app.mainloop()