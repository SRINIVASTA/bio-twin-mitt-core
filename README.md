# bio-twin-mitt-core

This repository serves as a self-contained core framework for implementing advanced manufacturing intelligence, latent variable soft sensors, and agentic decision-support workflows within a biopharmaceutical manufacturing context (Pharma 4.0). 

The architecture is explicitly optimized to ingest streaming industrial internet of things (IIoT) telemetry from an in-memory historian simulator, monitor multi-variable statistical process control (MSPC) boundaries via Principal Component Analysis (PCA), and generate Standard Operating Procedure (SOP) compliant diagnostic rationales using a localized Groq LLM agent loop.

---

## Repository Tree

```text
bio-twin-mitt-core/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── lint-and-test.yml          # Automated PEP8 / Black / Flake8 verification
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
│   └── processed/                     # Local data directories for snapshot data cache
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
│   │   │       └── kg_connector.py    # Local Knowledge Graph interface mapping
│   │   │
│   │   ├── domain/                    # --- Enterprise Business Logic ---
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_graph.py     # Structural Bioprocess ontological bounds
│   │   │   └── telemetry.py           # Strict Pydantic models for sensor validation
│   │   │
│   │   ├── infrastructure/            # --- Plant Telemetry Simulator ---
│   │   │   ├── __init__.py
│   │   │   └── telemetry_pi.py        # High-frequency IIoT stream simulator (Historian)
│   │   │
│   │   └── models/                    # --- Latent Variable Soft Sensors ---
│   │       ├── __init__.py
│   │       ├── pca_detector.py        # Multi-variable PCA anomaly detection engine
│   │       └── train.py               # Local historical training & tuning loops
│   │
│   └── ui/                            # --- User Interface Components ---
│       ├── __init__.py
│       ├── components/
│       │   ├── charts.py              # Plotly statistical control limit trends
│       │   └── status.py              # Color-coded GxP process alarm alerts
│       └── views/
│           └── dashboard.py           # Live operational execution console
│
├── tests/
│   ├── __init__.py
│   └── unit/                          # Core model math and schema tests
│       └── test_pca_math.py
│
├── .env.example                       # Local environment credential blueprint
├── .gitignore
├── app.py                             # Central Streamlit gateway routing file
├── pyproject.toml                     # Poetry ecosystem / tool parameters
└── requirements.txt                   # Pinned localized build packages
```

---

## Core System Architecture Breakdown

### 🤖 Agentic AI Subsystem (`src/mitt_core/agents/`)
* **`engine.py`:** Orchestrates the automated decision loop using the official `groq` SDK, executing low-latency inferences based on streaming process violations.
* **`prompts.py`:** Houses deterministic system prompt blueprints, critical alarm parsing matrices, and markdown response constraints to keep LLM outputs bounded and aligned with standard manufacturing workflows.
* **`tools/kg_connector.py`:** Bridges the AI loop with the local asset ontology, converting structured parameter boundaries into clear, descriptive plain-text context strings for the model.

### 🏭 Enterprise Domain Layer (`src/mitt_core/domain/`)
* **`knowledge_graph.py`:** Implements an in-memory semantic network mapping relationships between critical assets, equipment dependencies, Critical Process Parameters (CPPs), and Critical Quality Attributes (CQAs).
* **`telemetry.py`:** Leverages strict Pydantic schemas to validate and serialize data streams before they reach analytical or reporting engines.

### 🌐 Plant Telemetry Simulation (`src/mitt_core/infrastructure/`)
* **`telemetry_pi.py`:** Models a high-frequency plant data stream, generating normal bioprocess variables with realistic noise or active mechanical fault profiles on demand.

### 📈 Soft Sensors & Machine Learning (`src/mitt_core/models/`)
* **`pca_detector.py`:** Multivariable Principal Component Analysis engine that calculates real-time Hotelling’s T² and Squared Prediction Error (SPE) boundaries using historical training baseline envelopes.
* **`train.py`:** Automates local data cleaning, dimensions tracking, variance threshold check execution, and binary serialization (`.pkl`) of the soft sensor model.

### 🎨 User Interface Layer (`src/ui/`)
* **`components/status.py`:** Standardizes visual alert configurations, generating color-coded warning headers depending on specific statistical alarm types.
* **`components/charts.py`:** Constructs high-performance, interactive, and dark-themed Plotly charts showing score trajectories against calculated statistical Upper Control Limits (UCL).

---

## Getting Started: Local Deployment Lifecycle

Follow these three commands to spin up the entire self-contained framework locally:

```bash
# 1. Install localized mathematical, layout, and inference client packages
pip install streamlit plotly numpy scipy scikit-learn pandas groq pydantic pytest black flake8

# 2. Run the internal mathematical test suite to confirm model reliability
pytest tests/unit/test_pca_math.py

# 3. Initialize the real-time operational execution console
streamlit run app.py
```
