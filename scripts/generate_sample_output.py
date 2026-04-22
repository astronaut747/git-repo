"""Generate a sample output equivalent to optimize_switching_params.m.

Also writes full sweep results to docs/sweep_results.csv.
"""

from csv import DictWriter


def linspace(start, stop, num):
    if num == 1:
        return [start]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]


def find_switching_time(je, time, hk, mmss, alpha, gamma, a, pp, d):
    if je <= 0 or hk <= 0 or mmss <= 0 or pp <= 0 or d <= 0:
        return float("inf")

    reference_time = 1e-9
    reference_hk = 1.4
    reference_m = 1.0e6
    reference_d = 40e-9
    reference_p = 0.6
    reference_je = 5e10

    exchange_factor = 1 + 1e10 * a
    damping_factor = max(alpha / 0.05, 1e-6)
    gyro_factor = max(2.21e5 / gamma, 1e-6)

    raw_time = (
        reference_time
        * (reference_hk / hk)
        * (mmss / reference_m)
        * (reference_p / pp)
        * (reference_je / je)
        * (reference_d / d)
        * exchange_factor
        * damping_factor
        * gyro_factor
    )

    if raw_time < time[0] or raw_time > time[-1]:
        return float("inf")

    return min(time, key=lambda t: abs(t - raw_time))


def main():
    d_range = linspace(30e-9, 50e-9, 10)
    ku_range = linspace(6e5, 8e5, 10)
    mmss_range = linspace(0.9e6, 1.1e6, 10)
    pp_range = linspace(0.5, 0.7, 10)

    a = 1e-11
    alpha = 0.05
    gamma = 2.21e5
    time = linspace(0.0, 5e-9, 1000)
    je_target = 5e10
    target_switching_time = 1e-9

    best = {
        "Ku": float("nan"),
        "MMss": float("nan"),
        "PP": float("nan"),
        "D": float("nan"),
        "switching_time": float("inf"),
        "error_to_target": float("inf"),
    }

    results = []

    for d in d_range:
        for ku in ku_range:
            for mmss in mmss_range:
                for pp in pp_range:
                    hk = 2 * ku / mmss
                    switching_time = find_switching_time(
                        je_target, time, hk, mmss, alpha, gamma, a, pp, d
                    )
                    err = abs(switching_time - target_switching_time)

                    entry = {
                        "Ku": ku,
                        "MMss": mmss,
                        "PP": pp,
                        "D": d,
                        "switching_time": switching_time,
                        "error_to_target": err,
                    }
                    results.append(entry)

                    if err < best["error_to_target"]:
                        best = entry

    results.sort(key=lambda row: row["error_to_target"])

    with open("docs/sweep_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = DictWriter(
            file,
            fieldnames=["Ku", "MMss", "PP", "D", "switching_time", "error_to_target"],
        )
        writer.writeheader()
        writer.writerows(results)

    print("Best parameters found:")
    for key in ["Ku", "MMss", "PP", "D", "switching_time", "error_to_target"]:
        print(f"{key}: {best[key]:.12g}")

    print("\nTop 5 candidates:")
    for idx, row in enumerate(results[:5], start=1):
        print(
            f"{idx}. Ku={row['Ku']:.6g}, MMss={row['MMss']:.6g}, "
            f"PP={row['PP']:.6g}, D={row['D']:.6g}, "
            f"t={row['switching_time']:.12g}, err={row['error_to_target']:.12g}"
        )


if __name__ == "__main__":
    main()
