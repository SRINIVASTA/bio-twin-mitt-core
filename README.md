# 🧬 Bio-Twin Operational Execution Console
### Manufacturing Intelligence & Technology Transformation Framework Layer

This repository serves as a self-contained core framework for implementing advanced manufacturing intelligence, latent variable soft sensors, and agentic decision-support workflows within a biopharmaceutical manufacturing context (Pharma 4.0). 

The architecture is explicitly optimized to ingest streaming industrial internet of things (IIoT) telemetry from an in-memory historian simulator, monitor multi-variable statistical process control (MSPC) boundaries via a lightweight Principal Component Analysis (PCA) tracking matrix, and generate Standard Operating Procedure (SOP) compliant diagnostic rationales using a localized Groq LLM agent loop.

---

## Architecture Overview

### System Data Flow Architecture
The diagram below illustrates how raw plant data streams through the validation and statistical process control layers before reaching the low-latency agentic diagnostic engine:

```mermaid
graph TD
    subgraph Plant_Simulation_Layer [Plant Simulation Layer]
        A[telemetry_pi.py<br>IIoT Historian Simulator] -->|Raw Parameter Maps| B[telemetry.py<br>Pydantic Validator]
    end

    subgraph Analytical_Engine_Layer [Analytical Engine Layer]
        B -->|Validated Pydantic Payload| C[app.py<br>Central Gateway Routing]
        C -->|Feature Vector Matrix| D[pca_detector.py<br>High-Speed Tracking Engine]
        D -->|Compute Scores| E{SPC Limit Checker<br>Hotelling T² & SPE}
    end

    subgraph User_Interface_Layer [User Interface Layer]
        E -->|Safe State| F[status.py<br>Render Validated State]
        F --> G[charts.py<br>Render Stable Control Limits]
        C -->|Write Operation Tick| M[(Local CSV Audit Trail<br>Data Folder)]
    end

    subgraph Agentic_Decision_Support [Agentic AI Subsystem]
        E -->|Alarm Breach Tripped = True| H[engine.py<br>Groq Agent Runtime Engine]
        I[type-safe key mappings<br>Graph Ontology Layer] -->|Semantic Bounds & SOPs| H
        J[prompts.py<br>GxP System Blueprint Guidelines] --> H
        H -->|Deterministic Diagnostic API Call| K[Groq LLM Gateway Cluster<br>qwen/qwen3.8-27b]
        K -->|Return Actionable SOP Markdown| L[st.info Dashboard Report View]
    end

    style Plant_Simulation_Layer fill:#1e2235,stroke:#333,stroke-width:1px
    style Analytical_Engine_Layer fill:#141724,stroke:#0066CC,stroke-width:2px
    style User_Interface_Layer fill:#1e2235,stroke:#333,stroke-width:1px
    style Agentic_Decision_Support fill:#162b23,stroke:#00cc66,stroke-width:2px
```

### Anomaly Diagnostic Logic Flow
The Agentic Subsystem classifies multivariate breaches deterministically based on statistical projection matrices:

```mermaid
graph TD
    Start[Soft Sensor Inference Breach] --> Anomaly_Evaluation{Evaluate Alarm Arrays}
    
    Anomaly_Evaluation -->|T² Alarm = True <br> SPE Alarm = False| Shift[Process Drift / Kinetic Shift<br>Operating outside Golden Envelope]
    Anomaly_Evaluation -->|SPE Alarm = True| Outlier[Unmodeled Disturbance / Mechanical Fault<br>Structural or raw material variance]
    
    Shift -->|Process Shift Context| System_Prompt[Inject Graph Context & SOP Framework Constraints]
    Outlier -->|Unmodeled Outlier Context| System_Prompt
    
    System_Prompt --> Groq_Inference[Invoke Zero-Temperature Deterministic Completion]
    Groq_Inference --> Markdown_Report[Publish High-Priority Actionable SOP Deviation Report]
```

---

## Repository Tree

```text
bio-twin-mitt-core/
│
├── .github/
│   └── workflows/
│       └── lint-and-test.yml          # Automated PEP8 / Pytest CI verification
│
├── .streamlit/
│   ├── config.toml                    # Production UI styling, theme colors, & timeouts
│   └── secrets.toml                   # Local storage container for GROQ_API_KEY
│
├── config/
│   ├── __init__.py
│   └── base.py                        # Centralized application constants & parameter limits
│
├── data/
│   └── processed/                     # Stores local running history audit sheets
│
├── docker/
│   └── Dockerfile.app                 # Multi-stage production Streamlit web container
│
├── src/
│   ├── mitt_core/
│   │   ├── __init__.py
│   │   │
│   │   ├── agents/                    # --- Agentic AI Subsystem ---
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # Groq LLM autonomous loop manager
│   │   │   ├── prompts.py             # System prompt blueprints and SOP constraints
│   │   │   └── tools/
│   │   │       ├── __init__.py
│   │   │       └── kg_connector.py    # Local asset interface mapping logic
│   │   │
│   │   ├── domain/                    # --- Enterprise Business Logic ---
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_graph.py     # Structural Bioprocess ontological bounds
│   │   │   └── telemetry.py           # Strict Pydantic models for sensor validation
│   │   │
│   │   ├── infrastructure/            # --- Plant Telemetry Simulator ---
│   │   │   ├── __init__.py
│   │   │   ├── local_csv_exporter.py  # Local mock dataset provisioner utility
│   │   │   └── telemetry_pi.py        # High-frequency IIoT stream simulator (Historian)
│   │   │
│   │   └── models/                    # --- Latent Variable Soft Sensors ---
│   │       ├── __init__.py
│   │       ├── pca_detector.py        # Multi-variable PCA anomaly detection engine
│   │       └── train.py               # Local historical training & tuning loops
│   │
│   └── ui/                            # --- User Interface Components ---
│       ├── __init__.py
│       └── components/
│           ├── charts.py              # Plotly statistical control limit trends
│           └── status.py              # Color-coded GxP process alarm alerts
│
├── tests/
│   ├── __init__.py
│   └── unit/                          # Core model math and schema tests
│       └── test_pca_math.py
│
├── .env.example                       # Local environment credential blueprint
├── .gitignore
├── app.py                             # Central Streamlit layout entrypoint
└── requirements.txt                   # Pinned localized build packages
```

---

## Core System Architecture Breakdown

### 🤖 Agentic AI Subsystem (`src/mitt_core/agents/`)
* **`engine.py`:** Orchestrates the automated decision loop using the official `groq` SDK, executing low-latency inferences using a **30-second throttling guard** to eliminate 429 token limits.
* **`prompts.py`:** Houses deterministic system prompt blueprints, critical alarm parsing matrices, and markdown response constraints to keep LLM outputs bounded and aligned with standard manufacturing workflows.
* **`tools/kg_connector.py`:** Bridges the AI loop with the local asset ontology, converting structured parameter boundaries into clear, descriptive plain-text context strings for the model.

### 🏭 Enterprise Domain Layer (`src/mitt_core/domain/`)
* **`knowledge_graph.py`:** Implements an in-memory semantic network mapping relationships between critical assets, equipment dependencies, Critical Process Parameters (CPPs), and Critical Quality Attributes (CQAs).
* **`telemetry.py`:** Leverages strict Pydantic schemas to validate and serialize data streams before they reach analytical or reporting engines.

### 🌐 Plant Telemetry Simulation (`src/mitt_core/infrastructure/`)
* **`telemetry_pi.py`:** Models a high-frequency plant data stream, generating normal bioprocess variables with realistic noise or active mechanical fault profiles on demand.
* **`local_csv_exporter.py`:** Standardizes mock environment setups by auto-generating a 500-row timeline CSV that maps directly to target bioprocess tag arrays.

### 📈 Soft Sensors & Machine Learning (`src/mitt_core/models/`)
* **`pca_detector.py`:** Multivariable tracking engine that calculates real-time Hotelling’s T² and Squared Prediction Error (SPE) boundaries using frozen calculation variance parameters to eliminate dynamic runtime exceptions.
* **`train.py`:** Ingests local processed reference spreadsheet documents, isolates feature columns, validates non-null row matrices, and serializes optimized parameters directly to static disk binary blocks (`.pkl`).

### 🎨 User Interface Layer (`src/ui/components/`)
* **`status.py`:** Standardizes visual alert configurations, generating color-coded warning headers depending on specific statistical alarm types and writing live data strings directly down into an offline `.csv` log.
* **`charts.py`:** Constructs high-performance, interactive, and dark-themed Plotly charts showing score trajectories against calculated statistical Upper Control Limits (UCL).

---

## Getting Started: Local Deployment Lifecycle

Follow these terminal commands to provision data, train the models, and spin up the entire self-contained framework locally:

```bash
# 1. Install localized mathematical, layout, and inference client packages
pip install streamlit plotly numpy scipy scikit-learn pandas groq pydantic pytest black flake8

# 2. Provision the local mock timeline dataset file (500 historical rows)
python src/mitt_core/infrastructure/local_csv_exporter.py

# 3. Execute the training loop to calibrate the PCA matrix and export the pickle model
python src/mitt_core/models/train.py

# 4. Initialize the real-time operational execution console dashboard
streamlit run app.py
```
