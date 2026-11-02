# bio-twin-mitt-core

This repository serves as the core framework for implementing advanced AI, latent variable soft sensors, and agentic decision-support workflows within a pharmaceutical manufacturing context (Pharma 4.0). 

The architecture is explicitly designed to handle high-frequency IIoT streams, interface with manufacturing historians, leverage knowledge graphs for automated Standard Operating Procedure (SOP) compliance, and run multi-variable statistical process control (MSPC).

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
│       ├── lint-and-test.yml          # Automated PEP8 / Black / Flake8 verification
│       ├── streamlit-app-deploy.yml   # CI/CD pipeline targeting Streamlit Cloud
│       └── deploy-sagemaker-ecr.yml   # Multi-stage CI/CD to AWS ECR & SageMaker
│
├── .streamlit/
│   └── config.toml                    # Production UI styling, theme colors, & timeouts
│
├── config/
│   ├── __init__.py
│   ├── base.py                        # Central deployment configurations
│   ├── dev.py                         # Local/Sandbox specifications
│   └── prod.py                        # Immutable production parameters
│
├── data/
│   ├── external/                      # Immutable snapshot exports from cloud storage
│   ├── interim/                       # Intermediate transformations / feature matrices
│   └── processed/                     # Normalized datasets optimized for model inputs
│
├── docker/
│   ├── Dockerfile.app                 # Multi-stage production Streamlit web container
│   └── Dockerfile.model               # Hardened AWS SageMaker processing container
│
├── docs/
│   ├── architecture/                  # System blueprints, visual graphs, and designs
│   └── validation/                    # GMP documentation (IQ/OQ protocols & trace matrices)
│
├── src/
│   ├── mitt_core/
│   │   ├── __init__.py
│   │   │
│   │   ├── agents/                    # --- Agentic AI Subsystem ---
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # Autonomous workflow manager & state handlers
│   │   │   ├── prompts.py             # System prompt blueprints and SOP constraints
│   │   │   └── tools/
│   │   │       ├── __init__.py
│   │   │       ├── kg_connector.py    # Graph query execution mappings
│   │   │       └── pi_system.py       # Interface translating agent tasks to sensor hooks
│   │   │
│   │   ├── domain/                    # --- Enterprise Business Logic ---
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_graph.py     # Abstract Knowledge Graph structures
│   │   │   └── telemetry.py           # Strict Pydantic models for sensor contracts
│   │   │
│   │   ├── infrastructure/            # --- External Integration Interfaces (IIoT) ---
│   │   │   ├── __init__.py
│   │   │   ├── telemetry_pi.py        # High-frequency IIoT stream simulator (Historian)
│   │   │   ├── aws_sagemaker.py       # SageMaker training and batch pipeline endpoints
│   │   │   └── snowflake_db.py        # Secure data layer queries using SQL
│   │   │
│   │   └── models/                    # --- Latent Variable Soft Sensors ---
│   │       ├── __init__.py
│   │       ├── pca_detector.py        # Multi-variable PCA anomaly detection engine
│   │       └── train.py               # Offline hyperparameter tuning scripts
│   │
│   └── ui/                            # --- User Interface Components ---
│       ├── __init__.py
│       ├── components/
│       │   ├── charts.py              # Custom Plotly control limits visualizations
│       │   └── status.py              # Dynamic GxP alarm system notifications
│       └── views/
│           ├── dashboard.py           # Live operational execution console
│           └── analytical_hub.py      # Offline validation review station
│
├── tests/
│   ├── __init__.py
│   ├── unit/                          # Core model math and schema tests
│   │   ├── test_pca_math.py
│   │   └── test_telemetry_schema.py
│   ├── integration/                   # Agent loop and network dependency validations
│   │   ├── test_agent_tools.py
│   │   └── test_snowflake_read.py
│   └── performance/                   # High-frequency data stress handling checks
│       └── test_stream_latency.py
│
├── .env.example                       # Environment credential blueprint
├── .gitignore
├── app.py                             # Central Streamlit gateway routing file
├── pyproject.toml                     # Poetry ecosystem / tool parameters
├── README.md                          # Technical deployment and operational runbook
└── requirements.txt                   # Pinned build packages
```

---

## Core System Architecture Breakdown

### 🤖 Agentic AI Subsystem (`src/mitt_core/agents/`)
* **`engine.py`:** Manages the state machine and autonomous execution loop. Evaluates streaming process parameters against encoded recipes.
* **`prompts.py`:** Houses systemic guidelines, critical boundary criteria, and strict regulatory limits. Ensures the LLM engine strictly acts as a decision support layer without violating baseline guardrails.
* **`tools/`:** Provides the agent with actionable execution interfaces. `pi_system.py` maps semantic agent queries directly onto physical or simulated operational telemetry tags, while `kg_connector.py` maps knowledge relationships.

### 🏭 Enterprise Domain & Business Logic (`src/mitt_core/domain/`)
* **`knowledge_graph.py`:** Implements abstract node-edge relationships defining critical process parameters (CPPs), critical quality attributes (CQAs), equipment configurations, and inter-batch processing limits.
* **`telemetry.py`:** Leverages strict Pydantic schemas to validate data parsing layers. Ensures all streaming datasets conform to strict sensor payload layouts before hitting analytical engines.

### 🌐 IIoT & External Cloud Interfaces (`src/mitt_core/infrastructure/`)
* **`telemetry_pi.py`:** Simulates a high-frequency PI Historian server data-stream. Feeds real-time multi-variable snapshots into operational loops.
* **`snowflake_db.py`:** Orchestrates analytical querying structures against enterprise cloud instances to retrieve historical batch footprints.
* **`aws_sagemaker.py`:** Manages analytical loop training updates, tracking operational parameter states and managing real-time inferences.

### 📈 Soft Sensors & Machine Learning (`src/mitt_core/models/`)
* **`pca_detector.py`:** Principal Component Analysis (PCA) multi-variable monitoring engine. Projects high-dimensional sensor environments (e.g., spectroscopy arrays) onto low-dimensional latent spaces to monitor Hotelling’s T² and Squared Prediction Error (SPE) bounds.
