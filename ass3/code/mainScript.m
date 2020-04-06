clear;
close All;
noiseless = imread("../data/ChestPhantom.png");
im = noiseless;
x = zeros(size(im,1)*size(im,2),1);
for i = 1:size(im,1)
    x(1+(i-1)*size(im,2):i*size(im,2)) = im(i,:);
end
theta = 0:1:179;
rd = [];
im = (double(im)/255);
for i = 0:179
    radon_th = radon(im,i);
    rd = [rd; radon_th];
end
A = zeros(length(rd),length(x));
%%
tic;
[u,s,v] = svd(x,0);
A = rd*(v*inv(s)*(u'));
toc;
% %%
% [R,xp] = radon(im,[0:179]);
% imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
% xlabel('\theta (degrees)');
% ylabel('x''');
% colormap(gca,hot), colorbar;
%%
N1 = 185;
sinogram = A*x;
% sinogram = (sinogram/max(sinogram))*255;
std_gauss = 0.02*(max(sinogram)-min(sinogram));
noise = std_gauss*randn(size(sinogram));
sino_noise = sinogram+noise;
for i = 0:179
    h(:,i+1) = sino_noise(1+(i)*N1:(i+1)*N1,1);
end
% %%
% imshow(h,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
% xlabel('\theta (degrees)');
% ylabel('x''');
% colormap(gca,hot), colorbar;
%%
% Filtered Backprojection
L_max = floor(size(h, 1)/2);
L_max2 = floor(L_max/2);

shepp1 = myFilter(h, 'shepp', L_max);
shepp2 = myFilter(h, 'shepp', L_max2);
im1 = 0.5*iradon(shepp1, theta, 'linear', 'none', 1, size(im,1));
im2 = 0.5*iradon(shepp2, theta, 'linear', 'none', 1, size(im,1));
im1 = uint8((im1/(max(max(im1))))*255);
im2 = uint8((im2/(max(max(im2))))*255);
figure;
imshow(im1);
title("Filtered backprojection");
%%
%Tikhonov regularisation
lambda = 2;
n = 0.01*0.8;
x_old = randn(size(x));
tic;
for i =1:1000
    grad = A'*(A*x_old-sino_noise)+lambda*x_old;
    x_old = x_old-grad*n;
    display(norm(grad));
    if norm(grad)<1
        break;
    end
end
toc;
x_old(x_old<0) = 0;
x_old = (x_old/(max(max(x_old))))*255;
x_tikho = zeros(size(noiseless));
for i = 1:size(im,1)
    x_tikho(i,:) = x_old(1+(i-1)*size(im,2):i*size(im,2));
end
tikho_rms = RRMSE(double(noiseless),x_tikho);
%%
figure;
imshow(uint8(x_tikho));
title("Tikhonov regularisation");
%%
%Mrf priors
X = double(noiseless);
Y = 0.5*iradon(h, theta, 'linear', 'none', 1, size(im,1));
imageNoisy = im2double(Y);
changed = imageNoisy;
%%
%Quadratic prior
[Quadsolution, Quadrms] = QuadraticDenoising(imageNoisy,changed,X,0);

%%
%Huber prior
[Hubersolution, Huberrms] = HuberDenoising(imageNoisy,changed,X,1);

%%
%Discontinuity prior
[Discontinuitysolution, Discontinuityrms] = DiscontinuityAdaptiveDenoising(imageNoisy,changed,X,0);
