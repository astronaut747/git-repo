# MATLAB Parameter Sweep Project

This repo packages your MATLAB sweep as a reusable mini-project for parameter tuning.

## What this is useful for
- Finding `D`, `Ku`, `MMss`, and `PP` combinations that hit a target switching time.
- Exporting full sweep results so you can post-process, plot, or optimize further.
- Running a fallback workflow in Python when MATLAB/Octave is unavailable.

## Project structure
- `src/optimize_switching_params.m` — main sweep script with CSV export.
- `src/find_switching_time.m` — switching-time model function.
- `scripts/generate_sample_output.py` — Python fallback runner and CSV exporter.
- `docs/sample_output.txt` — captured console output.
- `docs/sweep_results.csv` — full sorted sweep results.

## Run
### MATLAB
```matlab
cd src
optimize_switching_params
```

### Python fallback
```bash
python scripts/generate_sample_output.py | tee docs/sample_output.txt
```

## Notes
- The current switching model is heuristic so the sweep is runnable end-to-end.
- Replace `find_switching_time` with your physical/LLG model when ready.
