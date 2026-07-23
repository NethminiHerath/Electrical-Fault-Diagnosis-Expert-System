# Rule-Based Expert System Presentation Guide

## Project

**Electrical Fault Diagnosis and Protection Expert System**

The system diagnoses electrical faults from voltage, current, temperature, frequency, and operating-condition inputs. It provides a fault diagnosis, severity level, recommended actions, fired-rule explanation, and database history.

## Presentation Requirements

- Every group member must participate.
- Every member should explain a meaningful part of the system.
- Keep the presentation professional and well organized.
- Demonstrate the working system live.
- Be prepared to answer implementation questions.
- Presentation and live demonstration: **10 minutes**.
- Question and answer/viva: **5 minutes**.
- Total allocated time: **15 minutes**.

## Suggested Member Responsibilities

Divide the presentation so that every member has a clear speaking role:

1. Problem domain, objectives, and system overview.
2. Database design and database integration.
3. Knowledge base and rule categories.
4. Inference engine, forward chaining, conflicts, and metarules.
5. GUI demonstration, results, conclusion, and future improvements.

## Ten-Minute Presentation Structure

### 1. Problem Description and Objectives — 1 minute

Explain:

- Electrical equipment can develop overvoltage, undervoltage, overcurrent, overheating, overload, frequency, wiring, cooling, and possible short-circuit faults.
- Manual diagnosis can be slow and inconsistent.
- The objective is to provide quick, explainable fault diagnosis and protection recommendations.
- The system uses a GUI, a rule-based inference engine, and a MySQL database.

### 2. System Architecture — 45 seconds

Explain the flow:

```text
User Input → GUI → Rule Engine → Diagnosis and Recommendations
                    ↓
                 MySQL Database
                    ↓
              Diagnosis History
```

Mention the main files:

- `gui.py` — user interface and user interaction.
- `rules.py` — knowledge base, inference logic, conflict resolution, and metarules.
- `database.py` — MySQL connection, saving, migration, and history search.
- `main.py` — command-line rule-engine test.
- `inference_flow.md` — inference-flow diagram.

### 3. Database Design and Implementation — 1 minute

Explain that MySQL stores:

- Electrical readings: voltage, current, temperature, and frequency.
- Operating conditions: maintenance mode, emergency load, and fluctuation indicators.
- Diagnosis history: fault type, severity, actions, explanation, and timestamp.

Explain the relationship:

```text
readings (one reading) ──── one diagnosis_history record
```

Demonstrate that pressing **Diagnose Fault** saves a record and that **Search History** retrieves matching records.

Mention that the password is supplied through the `RBES_DB_PASSWORD` environment variable rather than being stored in the source code.

### 4. Knowledge Base: 21 IF–THEN Rules — 1 minute 30 seconds

State that the system contains rules R1–R21. Do not read every rule during the presentation; group them by purpose.

Examples:

```text
IF voltage < 200
THEN diagnose undervoltage and recommend reducing the load.
```

```text
IF current > 15 AND temperature > 80
THEN diagnose severe overload and recommend maintenance inspection.
```

```text
IF current > 25 AND voltage < 180
THEN suspect a short circuit and recommend tripping the breaker immediately.
```

Explain the rule categories:

- **Relation rules:** combine conditions, such as current and temperature.
- **Recommendation rules:** produce inspection or maintenance actions.
- **Directive rules:** recommend urgent actions such as shutdown or breaker isolation.
- **Strategy rules:** change the recommended response for maintenance mode or emergency load conditions.
- **Heuristic rules:** use engineering thresholds and cautious diagnoses such as “Possible Cooling Failure” or “Short Circuit Suspicion.”

### 5. Forward Chaining and Inference Process — 1 minute 30 seconds

Explain the process:

1. The GUI collects the input facts.
2. Initial facts are placed in working memory, such as `overcurrent_condition` or `normal_frequency_condition`.
3. Rules are evaluated in sequence.
4. When a rule condition is true, its conclusion is added to working memory.
5. The system records the fired rule and recommendation.
6. Metarules resolve the final diagnosis and action priority.
7. The GUI displays the diagnosis, severity, detected faults, recommendations, and rule explanation.

Use the diagram in `inference_flow.md` while explaining this section.

### 6. Conflict Situations and Metarules — 1 minute

Demonstrate that multiple rules may fire for one input.

Example input:

```text
Voltage: 170 V
Current: 30 A
Temperature: 88 °C
Frequency: 49 Hz
Emergency Load: enabled
Current Fluctuation: enabled
```

Several rules fire simultaneously, including undervoltage, overcurrent, overheating, overload, motor winding fault, and short-circuit suspicion.

Explain the metarules:

- **MR1:** Maintenance mode affects non-critical conditions.
- **MR2:** Emergency-load protection is prioritized for critical conditions.
- **MR3:** The highest-priority detected fault becomes the final diagnosis.

The fault-priority table selects the final fault. For example, short-circuit suspicion has higher priority than general overcurrent.

### 7. GUI Demonstration — 2 minutes

Demonstrate in this order:

1. Start the application using `python gui.py`.
2. Enter normal readings and click **Diagnose Fault**.
3. Show the normal diagnosis and low severity.
4. Enter a high-risk example with low voltage, high current, and high temperature.
5. Enable emergency load and current fluctuation.
6. Click **Diagnose Fault**.
7. Show the final diagnosis, severity, detected faults, recommended actions, and fired rules.
8. Click **Search History** and search for `Critical` or a fault name.
9. Show that previous diagnosis records are retrieved from MySQL.
10. Briefly explain the conflict resolution visible in the result.

Do not spend presentation time entering many test cases. Prepare the values in advance.

### 8. Conclusion and Future Improvements — 1 minute

Conclusion points:

- The system provides fast and explainable electrical fault diagnosis.
- The knowledge base contains more than the required 20 rules.
- The GUI allows input, inference execution, result display, and history search.
- MySQL provides persistent storage and retrieval.
- Metarules resolve multiple applicable faults.

Possible future improvements:

- Add user authentication and role-based access.
- Add charts for historical voltage, current, and temperature trends.
- Allow administrators to add and edit rules through the GUI.
- Add more electrical equipment types and domain-specific rules.
- Add automated unit tests and exportable diagnosis reports.
- Add sensor or IoT data integration.

## Viva Preparation Questions

Be prepared to answer:

1. Why was a rule-based system selected for this problem?
2. What is the difference between a fact and a rule?
3. How does forward chaining work in your system?
4. What happens when multiple rules fire at the same time?
5. How is the final diagnosis selected?
6. What are your metarules?
7. Give examples of recommendation, directive, strategy, and heuristic rules.
8. How does the GUI communicate with the rule engine?
9. How are readings and diagnoses stored in MySQL?
10. How does history search work?
11. What happens if the database connection fails?
12. What improvements would you make in a future version?

## Run Checklist Before Presentation

From PowerShell:

```powershell
cd "D:\RBES\Electrical Fault Diagnosis and Protection Expert System"
$env:RBES_DB_PASSWORD="your_mysql_password"
python gui.py
```

Before presenting, confirm:

- MySQL is running.
- The `fault_expert_system` database exists.
- The GUI starts without errors.
- A normal diagnosis works.
- A multi-fault diagnosis works.
- History search returns records.
- Every group member knows their section.
- The presentation stays within 10 minutes.
- The viva answers are divided among group members.
