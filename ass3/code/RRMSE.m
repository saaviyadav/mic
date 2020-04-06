function [rms] = RRMSE(Noiseless,Noisy) % A,B are 2D matrix
    rms = sqrt(sum(sum((Noiseless-Noisy).^2)))/ sqrt(sum(sum(Noiseless.^2)));
end