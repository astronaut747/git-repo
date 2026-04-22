% optimize_switching_params.m
% Grid-searches magnetic parameters to find a switching time closest to 1 ns.

% Define the parameters and constants
D_range = linspace(30e-9, 50e-9, 10);
Ku_range = linspace(6e5, 8e5, 10);
MMss_range = linspace(0.9e6, 1.1e6, 10);
PP_range = linspace(0.5, 0.7, 10);
A = 1e-11;
alpha = 0.05;
gamma = 2.21e5;

% Define time vector and the range of charge current densities
time = linspace(0, 5e-9, 1000);
Je_target = 5e10;

% Initialize the best parameters found
best_params = struct('Ku', NaN, 'MMss', NaN, 'PP', NaN, 'D', NaN, 'switching_time', Inf);

% Loop through the parameter ranges
for D = D_range
    for Ku = Ku_range
        for MMss = MMss_range
            for PP = PP_range
                Hk = 2 * Ku / MMss;
                Je = Je_target;

                % Calculate the switching time for the current density
                switching_time = find_switching_time(Je, time, Hk, MMss, alpha, gamma, A, PP, D);

                % Check if the switching time is closer to 1 ns
                if abs(switching_time - 1e-9) < abs(best_params.switching_time - 1e-9)
                    best_params.Ku = Ku;
                    best_params.MMss = MMss;
                    best_params.PP = PP;
                    best_params.D = D;
                    best_params.switching_time = switching_time;
                end
            end
        end
    end
end

% Display the best parameters found
disp('Best parameters found:');
disp(best_params);
