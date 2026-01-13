# Flip It!! (In Progress)

Flip It!! is a Python-based simulation tool that models coin flips and dice rolls using object-oriented design and a 
state-machine driven workflow. It is built to be extensible, testable, and easy to experiment with.

---

## Purpose
Flip It!! is a simple Python program designed to simulate coin flips and dice rolls. The program demonstrates how clean
object-oriented programming can be used to model probabilistic systems like coins and dice. This allows users to easily 
switch between them or even create their 'rollable' object without changing the core program logic.

This project serves as a sandbox for:
* Validation-heavy user input
* State machine control flow
* Future data analysis and AI-assisted insights

---

## Features
* Simulate coin flip and dice rolls
* Swap between fair and weighted objects
* Centralized input validation and exit handling
* State machine driven control flow
* PyTest-based unit tests
* Designed for easy extension (new objects, analytics, AI)

---

## Skills Showcase
This project showcases the following skills:
* Object-Oriented Programming (inheritance, polymorphism)
* State machine for complex logic flow
* Unit tests using PyTest
* Input validation and error handling techniques
* Python virtual environment and dependency management

---

## Project Structure

```text
CoinFlipProgram/
│── flipit_objects/
    ├── base_object.py
    └── default_objects.py
├── flip_it.py
├── input_helpers.py
├── requirements.txt
├── test_cases.py
```

---

## Code Breakdown
The code is organized into several files:
* **input_helpers.py**: Centralized validating user input and handling restarts and exits
* **flipit_objects/base_object.py**: Base class for all objects, including coins and dice. The BaseObject class contains the roll method that all classes use.
* **flipit_objects/default_objects.py**: Classes for classic coins and dice, as well as an illegal (ie weighted) coin and dice.
* **flip_it.py**: Contains the main program logic including the application entry point. Uses a state machine that manages user interaction and updates the current object being used.


---

## How To Run

### Prerequisites
* Python 3.10+
* Git

### Setup
1) First clone this repo to where you would like it to be: `git clone https://github.com/ReginaOfTech/CoinFlipProgram.git`
2) Once the code is on your machine, change your working directory into the 'CoinFlipProgram' folder
3) Create a new virtual environment: `python -m venv .venv`
```bash
git clone https://github.com/ReginaOfTech/CoinFlipProgram.git
cd CoinFlipProgram
python -m venv .venv
```

### Activate Virtual Environment
4) Activate the virtual environment

**Windows**
```text
.venv/Scripts/Activate
```

**macOs / Linux**
```bash
source .venv/bin/activate
```

### Install Dependencies
5) Install neccessary libraries
```bash
pip install -r requirements.txt
```

### Run the Program
6) Now execute the FlipIt.py file and have fun
```bash
python flip_it.py
```

---

## Design Overview
* **OOP Abstraction:** Coins and dice share a common base class (BaseObject), allowing new objects to be included without modifying core logic
* **State Machine:** User interaction is manager through explicite states stored in an enum, making complex input flow easier to reason about and extend.
* **Validation First:** All user input is validated centrally to reduce duplication, edge-case errors, and mitigate future development bugs

---

## Roadmap/TODO

### Near-Term
* Clean up `get_user_object()` for maintainability
* Improve `analyze_results()` error handling (empty result sets)
* Keep test coverage aligned with updates
* Maintain requirements.txt for easy installation on other devices
  * `pip freeze > requirements.txt`

### Mid-Term
* Move analytics logic into a dedicated module
* Add basic statistical analysis

### Exploratory
* Integrate local LLM analysis via Ollama
* Experiment with AI-assisted insights on roll results

---

## Testing
Run tests with the following:
```bash
pytest
```