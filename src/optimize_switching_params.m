% optimize_switching_params.m
% Grid-searches magnetic parameters to find switching times close to target.

% Define the parameters and constants
D_range = linspace(30e-9, 50e-9, 10);
Ku_range = linspace(6e5, 8e5, 10);
MMss_range = linspace(0.9e6, 1.1e6, 10);
PP_range = linspace(0.5, 0.7, 10);
A = 1e-11;
alpha = 0.05;
gamma = 2.21e5;

% Define time vector, current, and objective target
time = linspace(0, 5e-9, 1000);
Je_target = 5e10;
target_switching_time = 1e-9;

% Initialize the best parameters found
best_params = struct('Ku', NaN, 'MMss', NaN, 'PP', NaN, 'D', NaN, ...
    'switching_time', Inf, 'error_to_target', Inf);

% Preallocate result arrays
num_cases = numel(D_range) * numel(Ku_range) * numel(MMss_range) * numel(PP_range);
Ku_all = zeros(num_cases, 1);
MMss_all = zeros(num_cases, 1);
PP_all = zeros(num_cases, 1);
D_all = zeros(num_cases, 1);
switching_time_all = zeros(num_cases, 1);
error_all = zeros(num_cases, 1);
case_index = 1;

% Loop through the parameter ranges
for D = D_range
    for Ku = Ku_range
        for MMss = MMss_range
            for PP = PP_range
                Hk = 2 * Ku / MMss;
                Je = Je_target;

                switching_time = find_switching_time(Je, time, Hk, MMss, alpha, gamma, A, PP, D);
                err = abs(switching_time - target_switching_time);

                Ku_all(case_index) = Ku;
                MMss_all(case_index) = MMss;
                PP_all(case_index) = PP;
                D_all(case_index) = D;
                switching_time_all(case_index) = switching_time;
                error_all(case_index) = err;
                case_index = case_index + 1;

                if err < best_params.error_to_target
                    best_params.Ku = Ku;
                    best_params.MMss = MMss;
                    best_params.PP = PP;
                    best_params.D = D;
                    best_params.switching_time = switching_time;
                    best_params.error_to_target = err;
                end
            end
        end
    end
end

% Build and save full sweep results
results_table = table(Ku_all, MMss_all, PP_all, D_all, switching_time_all, error_all, ...
    'VariableNames', {'Ku', 'MMss', 'PP', 'D', 'switching_time', 'error_to_target'});

results_table = sortrows(results_table, 'error_to_target', 'ascend');

output_dir = fullfile('..', 'docs');
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

writetable(results_table, fullfile(output_dir, 'sweep_results.csv'));

% Display the best and top candidates
disp('Best parameters found:');
disp(best_params);

disp('Top 5 candidates:');
disp(results_table(1:5, :));
