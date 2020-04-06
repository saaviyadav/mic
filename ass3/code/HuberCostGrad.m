%% Get the Cost and Gradient using Huber Denoising Algorithm


function [cost ,gradient] = HuberCostGrad(data,noisy,alpha,gamma)

    %alpha = 0.95
    %gamma = 0.0025;
    %RRMSE = 0.2360
    [penalty_top, penalty_bottom, penalty_left, penalty_right] = CircularShift(data);    

    cost = (penalty_top.^2 * 0.5) .* (abs(penalty_top) <= gamma) + (gamma*abs(penalty_top)-0.5*gamma^2).*(abs(penalty_top) > gamma);
    cost = cost + (penalty_bottom.^2 * 0.5) .* (abs(penalty_bottom) <= gamma) + (gamma*abs(penalty_bottom)-0.5*gamma^2).*(abs(penalty_bottom) > gamma) ;
    cost = cost + (penalty_right.^2 * 0.5) .* (abs(penalty_right) <= gamma) + (gamma*abs(penalty_right)-0.5*gamma^2).*(abs(penalty_right) > gamma);
    cost = cost + (penalty_left.^2 * 0.5) .* (abs(penalty_left) <= gamma) + (gamma*abs(penalty_left)-0.5*gamma^2).*(abs(penalty_left) > gamma);
    cost = alpha*cost + (1-alpha)*((data - noisy).^2);
    cost = norm(cost , 'fro');   

    gradient = (abs(penalty_top) <= gamma).* penalty_top + (abs(penalty_bottom) <= gamma).* penalty_bottom + (abs(penalty_right) <= gamma).* penalty_right+(abs(penalty_left) <= gamma).* penalty_left;
    gradient = gradient + (abs(penalty_top) > gamma).* (gamma * sign(penalty_top)) + (abs(penalty_bottom) > gamma) .* (gamma * sign(penalty_bottom))+ (abs(penalty_right) > gamma) .* (gamma * sign(penalty_right)) + (abs(penalty_left) > gamma) .* (gamma * sign(penalty_left));
    gradient = gradient*alpha + 2*(1-alpha)*(data - noisy); 
end    