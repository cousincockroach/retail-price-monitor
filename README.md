# Automated Retail Price Monitor & Analytics Dashboard

A production-grade, modular Python web scraping pipeline built to monitor, extract, and clean retail pricing data from dynamically rendered web applications. The system currently targets **Pick n Pay’s online specials catalog**, orchestrating headless browser execution to bypass client-side rendering walls and safely indexing relational data inside a localized SQLite system.

## System Architecture & Design Choices

This project is built following strict **Object-Oriented Programming (OOP)** rules and **Separation of Concerns (SoC)**. Rather than relying on a single loose script, the codebase is completely decoupled into independent layers:

1. **Configuration Layer (`config/`)**: Centralizes timeouts, custom desktop user-agents, database locations, and paths. Completely eliminates hardcoded magic strings across the engine.
2. **Scraping Engine Module (`src/scrapers/`)**: Manages browser lifecycles and parses raw web layout trees. It handles data extraction without needing to know anything about database schemas.
3. **Data Access Layer (`src/database/`)**: Abstracts all relational queries (`INSERT`, `UPDATE`, `UPSERT`).
4. **Utility Layer (`src/utils/`)**: Sanitizes volatile web data—normalizing whitespace layouts and using regular expressions (Regex) to scrub text data into arithmetic floats.
5. **Orchestrator Pipeline (`main.py`)**: Sits at the root level acting as the core conductor, passing structural outputs through each functional component safely.

---

##  Technology Stack

* **Language**: Python 3
* **Browser Automation Engine**: Playwright (Headless Chromium) — Chosen over standard `requests` pipelines to successfully execute and wait for asynchronous Angular client-side JavaScript painting routines.
* **HTML Parsing Architecture**: Beautiful Soup 4 — Leveraged for lightweight DOM traversal using resilient, class-agnostic semantic lookup fallbacks.
* **Data Cleansing Engine**: Python Regular Expressions (`re`) & Pandas.
* **Storage Layer**: SQLite 3 — Features an atomic `ON CONFLICT` upsert pattern to prevent record duplication over repeated daily execution cycles.

---

##  Project Directory Layout

```text
retail-price-monitor/
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Global properties, store URLs, paths, and timeouts
│
├── data/
│   └── retail_catalog.db     # Local SQLite relational database engine (git-ignored)
│
├── src/
│   ├── __init__.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py     # SQLite schema configurations and upsert routines
│   │
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── pnp_scraper.py    # Headless page execution and semantic DOM extractors
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Numerical Regex scrubbers and structural text cleansers
│
├── main.py                   # System core orchestrator and script gateway
├── requirements.txt          # Explicit system dependencies
└── README.md                 # Project workspace documentation