# MATLAB Parameter Sweep Project

This project checks and packages your MATLAB grid-search code as a runnable mini-project.

## What was fixed
- Added the missing `find_switching_time` function.
- Kept your parameter sweep structure and target (1 ns) intact.
- Added a Python helper to generate sample output in environments without MATLAB/Octave.

## Project structure
- `src/optimize_switching_params.m` — main sweep script.
- `src/find_switching_time.m` — switching-time model function.
- `scripts/generate_sample_output.py` — output generator compatible with this logic.
- `docs/sample_output.txt` — captured output.

## Run
### MATLAB
```matlab
cd src
optimize_switching_params
```

### Python fallback (no MATLAB required)
```bash
python scripts/generate_sample_output.py
```
