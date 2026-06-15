def diagnose_fault(voltage, current, temperature, frequency,
                   maintenance_mode, emergency_load,
                   current_fluctuation, voltage_fluctuation):

    detected_faults = []
    actions = []
    fired_rules = []

    fault_priority = {
        "Short Circuit Suspicion": 1,
        "Critical Overtemperature": 2,
        "Extreme Overvoltage": 3,
        "Severe Overload": 4,
        "Equipment Overload": 5,
        "Possible Motor Winding Fault": 6,
        "Overcurrent": 7,
        "Overtemperature": 8,
        "Overvoltage": 9,
        "Supply Failure Suspicion": 10,
        "Possible Cooling Failure": 11,
        "Frequency Abnormality": 12,
        "Undervoltage": 13,
        "Possible Loose Connection": 14
    }

    severity_map = {
        "Short Circuit Suspicion": "Critical",
        "Critical Overtemperature": "Critical",
        "Extreme Overvoltage": "Critical",
        "Severe Overload": "Critical",
        "Equipment Overload": "Critical",
        "Possible Motor Winding Fault": "High",
        "Overcurrent": "High",
        "Overtemperature": "High",
        "Overvoltage": "High",
        "Supply Failure Suspicion": "High",
        "Possible Cooling Failure": "High",
        "Frequency Abnormality": "Medium",
        "Undervoltage": "Medium",
        "Possible Loose Connection": "Medium"
    }

    def add_fault(fault):
        if fault not in detected_faults:
            detected_faults.append(fault)

    if voltage > 250:
        add_fault("Overvoltage")
        actions.append("Inspect voltage stabilizer")
        fired_rules.append("R1: IF voltage > 250 THEN overvoltage")

    if voltage < 200:
        add_fault("Undervoltage")
        actions.append("Reduce load and check supply input")
        fired_rules.append("R2: IF voltage < 200 THEN undervoltage")

    if current > 15:
        add_fault("Overcurrent")
        actions.append("Disconnect load immediately")
        fired_rules.append("R3: IF current > 15 THEN overcurrent")

    if temperature > 80:
        add_fault("Overtemperature")
        actions.append("Inspect cooling system")
        fired_rules.append("R4: IF temperature > 80 THEN overheating")

    if frequency < 48 or frequency > 52:
        add_fault("Frequency Abnormality")
        actions.append("Check generator or power source")
        fired_rules.append("R5: IF frequency outside 48-52Hz THEN frequency fault")

    if temperature > 90:
        add_fault("Critical Overtemperature")
        actions.append("Emergency shutdown")
        fired_rules.append("R6: IF temperature > 90 THEN emergency shutdown")

    if voltage > 270:
        add_fault("Extreme Overvoltage")
        actions.append("Isolate sensitive equipment")
        fired_rules.append("R7: IF voltage > 270 THEN extreme overvoltage")

    if current > 15:
        actions.append("Check temperature after overcurrent")
        fired_rules.append("R8: IF overcurrent THEN check temperature")

    if current > 15 and temperature > 80:
        add_fault("Severe Overload")
        actions.append("Schedule maintenance inspection")
        fired_rules.append("R9: IF overcurrent AND overheating THEN severe overload")

    if current_fluctuation and temperature > 75:
        add_fault("Possible Motor Winding Fault")
        actions.append("Inspect motor winding")
        fired_rules.append("R10: IF current fluctuates AND temperature high THEN motor winding fault")

    if voltage_fluctuation and 48 <= frequency <= 52:
        add_fault("Possible Loose Connection")
        actions.append("Inspect wiring terminals")
        fired_rules.append("R11: IF voltage fluctuates AND frequency normal THEN loose connection")

    if temperature > 85 and current <= 15:
        add_fault("Possible Cooling Failure")
        actions.append("Check fan or ventilation")
        fired_rules.append("R12: IF temperature high AND current normal THEN cooling failure")

    if current > 25 and voltage < 180:
        add_fault("Short Circuit Suspicion")
        actions.append("Trip breaker immediately")
        fired_rules.append("R13: IF current > 25 AND voltage < 180 THEN short circuit")

    if current > 20 and temperature > 85:
        add_fault("Equipment Overload")
        actions.append("Remove excess load")
        fired_rules.append("R14: IF current > 20 AND temperature > 85 THEN equipment overload")

    if voltage < 180 and current < 5:
        add_fault("Supply Failure Suspicion")
        actions.append("Check main supply")
        fired_rules.append("R15: IF voltage < 180 AND current < 5 THEN supply failure")

    if current > 15:
        actions.append("Trip breaker")
        fired_rules.append("R16: IF overcurrent THEN trip breaker")

    if current > 15 and maintenance_mode:
        actions.append("Do not trip automatically during maintenance")
        fired_rules.append("R17: IF overcurrent AND maintenance mode THEN do not trip automatically")

    if voltage > 250 and emergency_load:
        actions.append("Keep emergency load active")
        fired_rules.append("R18: IF overvoltage AND emergency load THEN protect emergency load")

    if current > 15 and emergency_load:
        actions.append("Isolate non-critical loads first")
        fired_rules.append("R19: IF overcurrent AND emergency load THEN isolate non-critical loads")

    if temperature > 80 and emergency_load:
        actions.append("Keep emergency cooling active")
        fired_rules.append("R20: IF overheating AND emergency load THEN keep emergency cooling active")

    if voltage < 200 and maintenance_mode:
        actions.append("Record undervoltage as maintenance observation")
        fired_rules.append("R21: IF undervoltage AND maintenance mode THEN record observation")

    if not detected_faults:
        return "Normal", "Low", "System is operating normally", "No fault rule fired", "None"

    final_fault = min(detected_faults, key=lambda f: fault_priority[f])
    severity = severity_map[final_fault]

    if maintenance_mode and severity != "Critical":
        severity = "Maintenance"
        fired_rules.append("MR1: Maintenance rules have priority over non-critical protection rules")

    if emergency_load and severity == "Critical":
        fired_rules.append("MR2: Emergency load protection has highest priority")

    fired_rules.append("MR3: Highest priority detected fault is selected as final diagnosis")

    return (
        final_fault,
        severity,
        "; ".join(dict.fromkeys(actions)),
        "\n".join(fired_rules),
        ", ".join(detected_faults)
    )