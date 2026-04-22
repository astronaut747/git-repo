function switching_time = find_switching_time(Je, time, Hk, MMss, alpha, gamma, A, PP, D)
% find_switching_time
% Heuristic switching-time model used to make parameter sweeps executable.
% This is not a full micromagnetic LLG solver.

if Je <= 0 || Hk <= 0 || MMss <= 0 || PP <= 0 || D <= 0
    switching_time = Inf;
    return;
end

% Empirical scaling around the 1 ns target using provided parameters.
reference_time = 1e-9;
reference_Hk = 1.4;
reference_M = 1.0e6;
reference_D = 40e-9;
reference_P = 0.6;
reference_Je = 5e10;

exchange_factor = 1 + 1e10 * A;          % weak A dependence
damping_factor = max(alpha / 0.05, 1e-6); % higher alpha slows switching
gyro_factor = max(2.21e5 / gamma, 1e-6);  % higher gamma speeds switching

raw_time = reference_time ...
    * (reference_Hk / Hk) ...
    * (MMss / reference_M) ...
    * (reference_P / PP) ...
    * (reference_Je / Je) ...
    * (reference_D / D) ...
    * exchange_factor ...
    * damping_factor ...
    * gyro_factor;

% Bound to the simulation window; if outside, treat as non-switching.
if raw_time < time(1) || raw_time > time(end)
    switching_time = Inf;
else
    [~, idx] = min(abs(time - raw_time));
    switching_time = time(idx);
end
end
