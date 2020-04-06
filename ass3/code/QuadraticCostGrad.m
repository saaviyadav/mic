%% Get the Cost and Gradient using Quadratic Denoising Algorithm

function [cost, gradient] = QuadraticCostGrad(data,noisy,alpha)
    %best alpha Quadratic Prior = 0.07
    [penalty_top, penalty_bottom, penalty_right, penalty_left] = CircularShift(data);
    cost = (1-alpha)*(data - noisy).^2  + alpha*(penalty_top.^2 + penalty_bottom.^2 + penalty_right.^2 + penalty_left.^2); 
    cost  = norm(cost,'fro');
    gradient = 2*(1-alpha)*(data - noisy) + alpha*2*(penalty_top + penalty_bottom + penalty_right + penalty_left);
end


