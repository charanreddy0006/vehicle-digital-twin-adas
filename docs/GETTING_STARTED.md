# Getting Started

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## First simulation

```powershell
python -m autotwin.cli --scenario highway --duration 30
```

## ADAS demonstration

```powershell
python -m autotwin.cli --scenario emergency_braking --duration 15
```

## Dashboard

```powershell
streamlit run dashboard/app.py
```

## Tests

```powershell
pytest -q
```

## Recommended reading order

1. `autotwin/core/models.py`
2. `autotwin/vehicle/vehicle.py`
3. `autotwin/sensors/sensor_suite.py`
4. `autotwin/perception/fusion.py`
5. `autotwin/adas/modules.py`
6. `autotwin/simulation/engine.py`
7. `dashboard/app.py`
