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
