"""Generate a sample output equivalent to optimize_switching_params.m."""


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

    best = {
        "Ku": float("nan"),
        "MMss": float("nan"),
        "PP": float("nan"),
        "D": float("nan"),
        "switching_time": float("inf"),
    }

    for d in d_range:
        for ku in ku_range:
            for mmss in mmss_range:
                for pp in pp_range:
                    hk = 2 * ku / mmss
                    switching_time = find_switching_time(
                        je_target, time, hk, mmss, alpha, gamma, a, pp, d
                    )
                    if abs(switching_time - 1e-9) < abs(best["switching_time"] - 1e-9):
                        best = {
                            "Ku": ku,
                            "MMss": mmss,
                            "PP": pp,
                            "D": d,
                            "switching_time": switching_time,
                        }

    print("Best parameters found:")
    for key in ["Ku", "MMss", "PP", "D", "switching_time"]:
        print(f"{key}: {best[key]:.12g}")


if __name__ == "__main__":
    main()
