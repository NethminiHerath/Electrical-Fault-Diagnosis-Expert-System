from rules import diagnose_fault

result = diagnose_fault(
    voltage=170,
    current=30,
    temperature=88,
    frequency=49,
    maintenance_mode=False,
    emergency_load=True,
    current_fluctuation=True,
    voltage_fluctuation=False
)

print("Final Diagnosis:", result[0])
print("Severity:", result[1])
print("Action:", result[2])
print("Explanation:")
print(result[3])
print("Detected Faults:", result[4])