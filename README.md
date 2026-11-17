# RexPilot — Chrome Dino Automation & Performance Lab

RexPilot is a Python-based Chrome Dinosaur automation and performance analysis application built with Selenium, Tkinter and data analysis libraries.

The project explores how configurable keyboard timing strategies perform across repeated Chrome Dino gameplay sessions.

Rather than relying on computer vision or obstacle recognition, RexPilot uses predefined timing-based playing profiles and records session results for comparative analysis.

## Features

- **Browser automation:** Control Chrome Dino using Selenium WebDriver.
- **Three playing strategies:** Conservative, Balanced and Aggressive.
- **Configurable gameplay:** Adjust jump duration, duck duration, action delays, waiting intervals and session duration.
- **JSON configuration:** Persist strategy selections and parameter settings.
- **Session management:** Start, pause, resume and stop gameplay sessions.
- **Performance logging:** Record session IDs, strategy settings, gameplay duration, final scores and timestamps in CSV.
- **Manual score collection:** Enter final scores after gameplay.
- **Benchmarking:** Compare strategy performance using average, highest and median scores.
- **Data visualisation:** Generate performance charts using Matplotlib.
- **Regression analysis:** Explore relationships between timing parameters and gameplay scores using Scikit-learn.
- **Tkinter dashboard:** Manage gameplay sessions and inspect performance history through a graphical interface.

## Technology Stack

| Technology | Application |
|---|---|
| Python 3.10 | Core programming language |
| Selenium | Browser automation |
| Tkinter | Desktop dashboard |
| JSON | Configuration persistence |
| CSV | Performance logging |
| Pandas | Data analysis |
| Matplotlib | Data visualisation |
| Scikit-learn | Exploratory regression analysis |

## Project Architecture

```text
RexPilot_Automation_Lab/
│
├── rexpilot/
│   ├── __init__.py
│   ├── dino_controller.py
│   ├── game_session.py
│   ├── playing_strategy.py
│   ├── conservative_strategy.py
│   ├── balanced_strategy.py
│   ├── aggressive_strategy.py
│   ├── session_manager.py
│   └── performance_logger.py
│
├── dashboard.py
├── main.py
├── config.json
├── requirements.txt
├── README.md
├── .gitignore
│
├── benchmark_test.py
├── benchmark_analysis.py
├── benchmark_visualizer.py
└── regression_analysis.py
```

Generated CSV files, virtual environments and visualisation outputs are created during execution and are excluded from version control.

## Installation

### Prerequisites

- Python 3.10
- Google Chrome
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd RexPilot_Automation_Lab
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch RexPilot

```bash
python dashboard.py
```

The application opens its Tkinter dashboard, from which users can select strategies, configure parameters and manage gameplay sessions.

## Configuration

RexPilot stores strategy parameters in `config.json`.

The configurable parameters include:

| Parameter | Description |
|---|---|
| jump_duration | Duration of the jump keyboard input |
| duck_duration | Duration of the duck keyboard input |
| delay_between_actions | Waiting time between scheduled actions |
| waiting_interval | Waiting time before the next action cycle |
| session_duration | Maximum configured session duration |

Three predefined profiles are provided:

- Conservative
- Balanced
- Aggressive

Their default parameters can be adjusted through the dashboard or configuration file.

## Performance Analysis

RexPilot records completed gameplay sessions in `sessions.csv`.

The recorded information includes:

- Session ID
- Selected strategy
- Jump duration
- Duck duration
- Session duration
- Final score
- Date and time

The analysis scripts provide additional functionality:

```bash
python benchmark_test.py
python benchmark_analysis.py
python benchmark_visualizer.py
python regression_analysis.py
```

`benchmark_test.py` generates synthetic demonstration records for testing the analysis pipeline. These records must not be interpreted as genuine gameplay results.

The analysis and visualisation scripts use the generated `benchmark_test.csv` file.

## Project Limitations

RexPilot is a timing-based browser automation and performance experimentation application.

It does not implement computer vision, OCR, neural networks or obstacle recognition.

Consequently:

- The playing strategies execute predefined keyboard-action sequences.
- The application does not identify approaching cacti or birds.
- Gameplay actions are not dynamically adjusted according to obstacle positions.
- Final scores are entered manually.
- Pausing RexPilot suspends its scheduled automation actions and session timer but does not freeze the Chrome Dino game engine.
- Regression experiments require sufficient genuine gameplay observations before meaningful performance conclusions can be drawn.

These limitations are intentional and define the project's current implementation scope.

## Future Improvements

Potential extensions include:

- More systematic strategy benchmarking.
- Improved gameplay timing experiments.
- Expanded statistical analysis.
- Additional session performance metrics.
- More advanced dashboard reporting.

## Author

**Anthony Omokpo**

RexPilot was developed as a Python software engineering and data analysis portfolio project, demonstrating browser automation, object-oriented programming, configuration management, data persistence, statistical analysis and visualisation.