%% Get the Cost and Gradient using Discontinuity Adaptive Denoising Algorithm

function [cost, gradient] = DiscontinuityAdaptiveCostGrad(data,noisy,alpha,gamma)
    
    [penalty_top, penalty_bottom, penalty_left, penalty_right] = CircularShift(data);
    cost = (1-alpha)*(data - noisy).^2 + alpha * gamma * (abs(penalty_top)+abs(penalty_bottom) + abs(penalty_right) + abs(penalty_left))-gamma^2 * alpha * (log(1+abs(penalty_top)/gamma) + log(1+abs(penalty_bottom)/gamma) + log(1+abs(penalty_right)/gamma) + log(1+abs(penalty_left)/gamma));
    cost = norm(cost, 'fro');
    gradient = 2*(1-alpha)*(data - noisy) + alpha * gamma * (penalty_top./(gamma + abs(penalty_top)) + penalty_bottom./(gamma + abs(penalty_bottom)) + penalty_right./(gamma + abs(penalty_right)) + penalty_left./(gamma + abs(penalty_left)));
end 