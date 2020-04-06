%% Gives solutions and RRMSE values for all the three denoising algorithms

clc;
clear;
close ALL;

X = imread("../data/histology_noiseless.png");
Y = imread("../data/histology_noisy.png");
imNoiseless = X;
imageNoisy = im2double(rgb2ycbcr(Y));
X = im2double(rgb2ycbcr(X));
imageNoisy = im2double(imageNoisy);

changed = imageNoisy;
figure;
imshow(ycbcr2rgb(changed));
title('Noisy Image');
%%
[Quadsolution, Quadrms] = QuadraticDenoising(imageNoisy(:,:,1),changed,X(:,:,1),0);

%%
[HuberSolution, Huberrms] = HuberDenoising(imageNoisy(:,:,1),changed,X(:,:,1),0);
%%
[DiscontinuitySolution, Discontinuityrms] = DiscontinuityAdaptiveDenoising(imageNoisy(:,:,1),changed,X(:,:,1),0);


