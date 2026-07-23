import customtkinter as ctk
from rules import diagnose_fault
from database import save_diagnosis, get_diagnosis_history

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FaultExpertSystemGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Electrical Fault Diagnosis Expert System")
        self.geometry("1280x980")
        self.configure(fg_color="#071A2F")

        self.page_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#071A2F",
            corner_radius=0
        )
        self.page_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.page_frame,
            text="Electrical Fault Diagnosis Expert System",
            font=("Segoe UI", 28, "bold"),
            text_color="#EAF6FF"
        )
        self.title_label.pack(pady=(18, 4))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Rule-Based Electrical Fault Detection and Protection Advisor",
            font=("Segoe UI", 14),
            text_color="#8ECDF8"
        )
        self.subtitle_label.pack(pady=(0, 12))

        self.main_frame = ctk.CTkFrame(self.page_frame, fg_color="#0B2545", corner_radius=18)
        self.main_frame.pack(fill="x", padx=25, pady=8)

        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#123A63", corner_radius=15)
        self.input_frame.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        self.option_frame = ctk.CTkFrame(self.main_frame, fg_color="#123A63", corner_radius=15)
        self.option_frame.pack(side="right", fill="both", expand=True, padx=18, pady=18)

        self.create_inputs()
        self.create_options()
        self.create_buttons()
        self.create_output_area()

    def create_inputs(self):
        heading = ctk.CTkLabel(
            self.input_frame,
            text="Input Readings",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAF6FF"
        )
        heading.grid(row=0, column=0, columnspan=2, pady=(15, 20))

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

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
        label.grid(row=row, column=0, padx=25, pady=12, sticky="e")

        entry = ctk.CTkEntry(
            self.input_frame,
            width=260,
            height=40,
            fg_color="#071A2F",
            border_color="#4DA3D9",
            text_color="#FFFFFF",
            placeholder_text="Enter value"
        )
        entry.grid(row=row, column=1, padx=25, pady=12, sticky="w")

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
        button_frame = ctk.CTkFrame(self.page_frame, fg_color="#071A2F")
        button_frame.pack(pady=15)

        button_style = {
            "width": 190,
            "height": 44,
            "corner_radius": 12,
            "font": ("Segoe UI", 15, "bold"),
            "fg_color": "#1E88E5",
            "hover_color": "#42A5F5"
        }

        self.diagnose_button = ctk.CTkButton(
            button_frame,
            text="Diagnose Fault",
            command=self.diagnose,
            **button_style
        )
        self.diagnose_button.grid(row=0, column=0, padx=18)

        self.history_button = ctk.CTkButton(
            button_frame,
            text="View History",
            command=self.show_history,
            **button_style
        )
        self.history_button.grid(row=0, column=1, padx=18)

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            **button_style
        )
        self.clear_button.grid(row=0, column=2, padx=18)

    def create_output_area(self):
        self.output_frame = ctk.CTkFrame(self.page_frame, fg_color="#0B2545", corner_radius=18)
        self.output_frame.pack(fill="x", padx=25, pady=(5, 25))

        output_label = ctk.CTkLabel(
            self.output_frame,
            text="Diagnosis Output",
            font=("Segoe UI", 18, "bold"),
            text_color="#EAF6FF"
        )
        output_label.pack(pady=(15, 10))

        search_frame = ctk.CTkFrame(self.output_frame, fg_color="#0E3158", corner_radius=12)
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.history_search_entry = ctk.CTkEntry(
            search_frame,
            width=520,
            height=36,
            placeholder_text="Search fault, severity, or action",
            fg_color="#071A2F",
            border_color="#4DA3D9",
            text_color="#FFFFFF",
            placeholder_text_color="#8ECDF8"
        )
        self.history_search_entry.pack(side="left", fill="x", expand=True, padx=(12, 10), pady=12)
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Search History",
            width=150,
            command=self.show_history
        )
        self.search_button.pack(side="left", padx=(0, 12), pady=12)

        self.summary_frame = ctk.CTkFrame(self.output_frame, fg_color="#0E3158", corner_radius=14)
        self.summary_frame.pack(fill="x", padx=20, pady=(0, 12))

        self.diagnosis_card = self.create_summary_card(
            self.summary_frame,
            "Final Diagnosis",
            ""
        )
        self.diagnosis_card.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        self.severity_card = self.create_summary_card(
            self.summary_frame,
            "Severity",
            ""
        )
        self.severity_card.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)

        self.details_frame = ctk.CTkFrame(self.output_frame, fg_color="#0B2545")
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.faults_card, self.faults_box = self.create_text_card(
            self.details_frame,
            "Detected Faults"
        )
        self.faults_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0, 12))

        self.actions_card, self.actions_box = self.create_text_card(
            self.details_frame,
            "Recommended Actions"
        )
        self.actions_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=(0, 12))

        self.explanation_card, self.explanation_box = self.create_text_card(
            self.details_frame,
            "Rule Explanation"
        )
        self.explanation_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 0))

        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=1)
        self.details_frame.grid_rowconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(1, weight=2)

    def create_summary_card(self, parent, title, value):
        card = ctk.CTkFrame(parent, fg_color="#061426", corner_radius=14, border_width=1, border_color="#1E88E5")

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color="#8ECDF8"
        )
        title_label.pack(anchor="w", padx=18, pady=(14, 4))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            text_color="#EAF6FF"
        )
        value_label.pack(anchor="w", padx=18, pady=(0, 16))

        return card

    def create_text_card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color="#061426", corner_radius=14, border_width=1, border_color="#1E88E5")

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 15, "bold"),
            text_color="#8ECDF8"
        )
        title_label.pack(anchor="w", padx=16, pady=(12, 5))
        card.title_label = title_label
        card.default_title = title

        textbox = ctk.CTkTextbox(
            card,
            fg_color="#061426",
            text_color="#EAF6FF",
            font=("Segoe UI", 13),
            corner_radius=8,
            border_width=0,
            wrap="word"
        )
        textbox.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        return card, textbox

    def show_diagnosis_view(self):
        if not self.summary_frame.winfo_manager():
            self.summary_frame.pack(fill="x", padx=20, pady=(0, 12))

        self.explanation_card.title_label.configure(text=self.explanation_card.default_title)
        self.faults_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=(0, 12))
        self.actions_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=(0, 12))
        self.explanation_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 0))

    def show_history_view(self):
        self.summary_frame.pack_forget()
        self.faults_card.grid_remove()
        self.actions_card.grid_remove()
        self.explanation_card.title_label.configure(text="History")
        self.explanation_card.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 12))

    def update_summary_card(self, card, value, color="#EAF6FF"):
        labels = card.winfo_children()
        value_label = labels[1]
        value_label.configure(text=value, text_color=color)

    def set_textbox_content(self, textbox, content):
        textbox.delete("1.0", "end")
        textbox.insert("end", content)

    def normalize_severity(self, severity):
        allowed = {"Low", "Medium", "High", "Critical"}
        severity_text = str(severity).strip().title()
        return severity_text if severity_text in allowed else "Medium"

    def diagnose(self):
        try:
            self.show_diagnosis_view()

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

            normalized_severity = self.normalize_severity(result[1])

            save_diagnosis(
                voltage=voltage,
                current=current,
                temperature=temperature,
                frequency=frequency,
                maintenance_mode=self.maintenance_var.get(),
                emergency_load=self.emergency_var.get(),
                diagnosis=result[0],
                severity=normalized_severity,
                actions=result[2],
                explanation=result[3],
                current_fluctuation=self.current_fluctuation_var.get(),
                voltage_fluctuation=self.voltage_fluctuation_var.get()
            )

            actions = [action.strip() for action in result[2].split(";") if action.strip()]
            faults = [fault.strip() for fault in result[4].split(",") if fault.strip()]

            fault_text = "\n".join(f"• {fault}" for fault in faults)
            action_text = "\n".join(f"• {action}" for action in actions)

            severity_color = "#EAF6FF"
            if normalized_severity == "Critical":
                severity_color = "#FF6B6B"
            elif normalized_severity == "High":
                severity_color = "#FFA94D"
            elif normalized_severity == "Medium":
                severity_color = "#FFD43B"
            elif normalized_severity == "Low":
                severity_color = "#69DB7C"

            self.update_summary_card(self.diagnosis_card, result[0])
            self.update_summary_card(self.severity_card, normalized_severity, severity_color)

            self.set_textbox_content(self.faults_box, fault_text)
            self.set_textbox_content(self.actions_box, action_text)
            self.set_textbox_content(self.explanation_box, result[3])

        except ValueError:
            self.update_summary_card(self.diagnosis_card, "Input Error", "#FF6B6B")
            self.update_summary_card(self.severity_card, "Invalid", "#FF6B6B")
            self.set_textbox_content(self.faults_box, "")
            self.set_textbox_content(self.actions_box, "")
            self.set_textbox_content(self.explanation_box, "Please enter valid numeric values for all input fields.")
        except Exception as exc:
            self.update_summary_card(self.diagnosis_card, "Database Error", "#FF6B6B")
            self.update_summary_card(self.severity_card, "Not Saved", "#FF6B6B")
            self.set_textbox_content(self.faults_box, "")
            self.set_textbox_content(self.actions_box, "")
            self.set_textbox_content(self.explanation_box, f"The diagnosis could not be saved. Check the database connection.\n\n{exc}")

    def show_history(self):
        try:
            search_term = self.history_search_entry.get().strip()
            records = get_diagnosis_history(search_term or None)
        except Exception as exc:
            self.show_history_view()
            self.set_textbox_content(self.explanation_box, f"History could not be loaded. Check the database connection.\n\n{exc}")
            return

        self.show_history_view()

        if not records:
            self.set_textbox_content(self.explanation_box, "No records found.")
            return

        history_text = ""
        for record in records:
            history_severity = self.normalize_severity(record[2])
            history_text += (
                f"________________________________\n\n"
                f"Date     : {record[0]}\n"
                f"Fault    : {record[1]}\n"
                f"Severity : {history_severity}\n"
            
            )
        self.set_textbox_content(self.explanation_box, history_text)

    def clear_fields(self):
        self.show_diagnosis_view()

        self.voltage_entry.delete(0, "end")
        self.current_entry.delete(0, "end")
        self.temperature_entry.delete(0, "end")
        self.frequency_entry.delete(0, "end")
        self.history_search_entry.delete(0, "end")

        self.maintenance_var.set(False)
        self.emergency_var.set(False)
        self.current_fluctuation_var.set(False)
        self.voltage_fluctuation_var.set(False)

        self.update_summary_card(self.diagnosis_card, "")
        self.update_summary_card(self.severity_card, "")

        self.set_textbox_content(self.faults_box, "")
        self.set_textbox_content(self.actions_box, "")
        self.set_textbox_content(self.explanation_box, "")


if __name__ == "__main__":
    app = FaultExpertSystemGUI()
    app.mainloop()
