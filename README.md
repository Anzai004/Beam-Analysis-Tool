# Beam Analysis Tool
Numerical beam analysis tool built using Python for structural engineering calculations.

**Developed by:** Monjyeeman Dutta

---

## Overview

The Beam Analysis Tool is a Python-based engineering application developed to perform structural analysis of simply supported beams under common loading conditions.

The tool computes reaction forces, generates Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD), and plots the deflection curve using numerical methods.

This project demonstrates the integration of mechanical engineering principles with programming to create a practical analysis utility.

---

## Features

* Reaction force calculation
* Shear Force Diagram (SFD)
* Bending Moment Diagram (BMD)
* Deflection curve visualization
* Supports:
  * Point Load
  * Uniformly Distributed Load (UDL)
* Automatic unit conversion to SI
* Input validation safeguards
* Serviceability warning using L/250 deflection limit

---

## Requirements
- Python 3.10+

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Technologies Used

* Python
* NumPy
* Matplotlib

---

## Engineering Concepts Applied

* Euler–Bernoulli Beam Theory
* Static Equilibrium
* Load Distribution
* Structural Serviceability Criteria

---

## Why This Project Matters?

This tool was built to bridge theoretical mechanics with computational problem-solving.
It reflects an early effort toward engineering automation and analytical tool development.

---

## Future Improvements

* Multiple point loads
* Cantilever beam support
* GUI-based interface
* Exportable engineering reports

---

## How to Run

Install dependencies:

```bash
pip install numpy matplotlib
```

Run the script:

```bash
python beam_analysis_tool.py
```

---

## Author Note

This project was developed as a self-initiated effort to strengthen both programming skills and applied mechanical engineering knowledge.
