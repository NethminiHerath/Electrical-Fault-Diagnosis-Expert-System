# Inference Flow Diagram

```mermaid
flowchart TD
    A[User enters voltage, current, temperature, frequency and conditions] --> B[GUI validates numeric input]
    B --> C[Load initial facts into working memory]
    C --> D[Forward-chaining pass 1: evaluate sensor threshold rules R1-R7]
    D --> E[Assert derived facts and collect fired rules/actions]
    E --> F[Forward-chaining pass 2: evaluate relation and diagnostic rules R8-R15]
    F --> G[Assert detected faults and collect recommendations]
    G --> H[Forward-chaining pass 3: evaluate strategy/directive rules R16-R21]
    H --> I[Working memory now contains all asserted facts and fired rules]
    I --> J[Apply metarules MR1-MR3]
    J --> K[Resolve actions and select highest-priority fault]
    K --> L[Display diagnosis, severity, detected faults, actions and fired-rule explanation]
    L --> M[Save readings and diagnosis history to MySQL]
```

The working memory contains initial observations such as `overcurrent_condition`
and `normal_frequency_condition`. Rules add derived fault facts, and later rules
use those facts when selecting additional diagnoses and recommendations.
