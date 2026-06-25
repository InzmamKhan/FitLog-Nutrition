# ⚡ FitLog Nutrition

A hyper-minimalist, high-end desktop nutrition tracker designed for devs who want to manage their macro targets without the visual noise of mainstream tracking apps. Built with an aesthetic monochrome dark theme, it wraps a powerful **Flask** and **MySQL** architecture inside a native desktop environment using **PyWebView**.

---

## 🖤 Features

*   **Dynamic Objective Inversion:** The UI intelligently alters its progress colors based on whether you are **Bulking** (surplus target) or **Cutting** (strict calorie ceiling limit).
*   **Zero-Dependency Form Tracking:** Log nutrients directly beneath your metrics cards instantly.
*   **Mathematical Precision:** Employs **NumPy** for biometric calculations (Mifflin-St Jeor) and **Pandas** for processing rolling 7-day chronological data arrays.

---

## 🛠️ System Design & Lifecycle

Here is how the application orchestrates data across its decoupled stack under the hood:


[ User Interface ]  ---> Logs Metrics --->  [ Flask Controller ]
 (PyWebView App)                              (server/routes.py)
        ^                                             |
        | Renders Jinja Template                      v Uses
        +----------------------------------- [ Core Modules Tier ]
                                              /                \
                             (core/calculations.py)        (core/db_queries.py)
                                     |                              |
                                  Math Engine                 MySQL Connector
                                (NumPy & Pandas)               (Context Manager)
                                                                    |
                                                                    v Writes To
                                                             [ MySQL Database ]


### 🔁 Execution Lifecycle

1. **Initialization (`run.py`):** The app spins up a background thread to run a local Flask web server instance, then instantly spawns a native desktop frame pointing directly to it.
2. **Environment Sync (`config.py`):** Explicitly extracts variables from `.env` with zero heavy external tracking dependencies.
3. **Data Isolation Context (`core/db_connection.py`):** Implements a crisp Context Manager wrapper that handles resource allocation, query configuration, and cleans up socket leaks automatically.
4. **Mathematical Processing (`core/calculations.py`):** Matrix arrays are processed on the fly via vector structures, avoiding brittle native Python loops.

---

### 🗄️ Database Schema Mapping

The core storage tier tracks data using two clean, related tables with zero indexing bloat:


  +-----------------------+             +-----------------------+
  |       USER_DATA       |             |     TRACK_RECORD      |
  +-----------------------+             +-----------------------+
  | User_ID (PK)          | <---------\ | Record_ID (PK)        |
  | Name                  |           | | User_ID (FK)          |
  | Body_Weight           |           \- | Log_Date (Unique Key) |
  | Height                |             | Calories              |
  | Age                   |             | Protein / Carbs / Fats|
  | Gender / Activity     |             | Footsteps             |
  | Objective             |             +-----------------------+
  +-----------------------+

