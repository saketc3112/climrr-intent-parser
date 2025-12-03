# 📦 climrr_intent_parser

**`climrr_intent_parser`** provides utilities for parsing **natural-language climate queries**, extracting user **intent**, triggering **clarification rounds**, and mapping the parsed intent to precise **ClimRR dataset keys**.

It includes core functionalities for:

* **Intent parsing** (`parse_raw_intent`)
* **Clarification loop management** (`process_query_with_clarification`)
* **ClimRR data extraction** (`extract_relevant_data`)
* **Full ClimRR variable → CSV key mapping** (`FULL_KEY_MAP`, `get_final_data_key`)
* **Template parsing helpers** (`separate_vars_and_exprs`)

All logic from the original extraction and parsing functions is preserved exactly.

---

## Package Structure

```
climrr_intent_parser/
├── __init__.py
├── parsing/
│   ├── __init__.py
│   └── intent_processor.py
├── utils/
│   ├── __init__.py
│   └── constants.py
├── templater.py
├── helpers.py
├── pyproject.toml
└── README.md
```


---

## 🚀 Installation Instructions

### **Option 1 — Install locally (editable mode)**

If your folder contains:
climrr_intent_parser/pyproject.toml

Run:

```bash
pip install -e .
```


This installs the library in editable mode, so any updates inside the folder immediately reflect in Python imports.

### **Option 2 — Install directly from GitHub**
If the repository is hosted online:

```
pip install git+https://github.com/yourusername/climrr_intent_parser.git
```

Replace with your actual GitHub repo URL.
