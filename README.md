# ⚡ FitLog Nutrition

A hyper-minimalist, high-end desktop nutrition tracker designed for devs who want to manage their macro targets without the visual noise of mainstream tracking apps. Built with an aesthetic monochrome dark theme, it wraps a powerful **Flask** and **MySQL** architecture inside a native desktop environment using **PyWebView**.

---

## 🖤 Features

*   **Matte Charcoal Interface:** Zero eye strain, zero clutter. Just pure data.
*   **Dynamic Objective Inversion:** The UI intelligently alters its progress colors based on whether you are **Bulking** (surplus target) or **Cutting** (strict calorie ceiling limit).
*   **Zero-Dependency Form Tracking:** Log nutrients directly beneath your metrics cards instantly.
*   **Mathematical Precision:** Employs **NumPy** for biometric calculations (Mifflin-St Jeor) and **Pandas** for processing rolling 7-day chronological data arrays.

---

## 🛠️ System Design & Lifecycle

Here is how the application orchestrates data across its decoupled stack under the hood:

```text
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