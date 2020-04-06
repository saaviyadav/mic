 function [ h_filtered ] = myFilter( h, method, val)
    ft = double(fftshift(fft(h), 1));
    cx = floor(size(ft, 1)/2);
    m  = size(ft, 1);
    n  = size(ft, 2);
    
    % filter contains 1-D values of |w|
    filter_s = double(abs((1-cx):(m-cx)));
    
    % Choose the value of L first
    L = val;
    
    rectangle = double(filter_s <= L);
    
    % Choose the method
    if strcmp(method, 'ramlak'),
        f = 1;
    elseif strcmp(method, 'shepp'),
        f = sinc(0.5*pi/L*filter_s);
    elseif strcmp(method, 'cos'),
        f = cos(0.5*pi/L*filter_s);
    else
        fprintf('Error');
    end
    
%     fprintf('Used %s filter\n', method);
    filter_s = filter_s.*rectangle.*f;
    % The one going to be applied on the fourier transform
    final_filt = double(repmat(filter_s, n, 1)');
        
    ft = ft.*final_filt;
    h_filtered = real(ifft(ifftshift(ft, 1)));
    
 end