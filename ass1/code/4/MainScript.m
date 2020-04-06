%%
tic;
clear;
close all;
clc;
filename = "../../data/brain/csv/"
for i = 1:40
    data_shapes(:,:,i) = load(filename+"Points mri_image_"+int2str(i)+".csv")';
end
align_shape = data_shapes;
for i = 1:size(data_shapes,3)
    sum_x = sum(data_shapes(1,:,i))/size(data_shapes,2);
    sum_y = sum(data_shapes(2,:,i))/size(data_shapes,2);
    align_shape(1,:,i) = align_shape(1,:,i) - sum_x;
    align_shape(2,:,i) = align_shape(2,:,i) - sum_y;
    norm = sum(sum(align_shape(:,:,i).^2));
    norm = norm^0.5;
    align_shape(:,:,i) = align_shape(:,:,i)/norm;
end
[mean_shape,align_shape] = FindMean(align_shape);
%%
figure;
for i = 1:size(data_shapes,3)
    plot(data_shapes(1,:,i),data_shapes(2,:,i),'.','MarkerSize',10);
    hold on;
    plot(data_shapes(1,:,i),data_shapes(2,:,i));
    hold on;
end
title('Part a: Initial pointsets');
hold off;
%%
figure;
plot(mean_shape(1,:),mean_shape(2,:),'LineWidth',3);
hold on;
for i = 1:size(data_shapes,3)
    plot(align_shape(1,:,i),align_shape(2,:,i),'.');
    hold on;
end
legend("Mean shape");
title("Part b: Mean shape and aligned pointsets");
save('../../results/Brain_Aligned_pointset.mat','align_shape');
save('../../results/Brain_Mean_shape_.mat','mean_shape');
hold off;
%%
[first_1,first_2,sec_1,sec_2,third_1,third_2,V,D,X] = FindModes(align_shape,mean_shape);
save('../../results/Brain_Mode1+3sd.mat','first_1');
save('../../results/Brain_Mode1-3sd.mat','first_2');
save('../../results/Brain_Mode2+3sd.mat','sec_1');
save('../../results/Brain_Mode2-3sd.mat','sec_2');
save('../../results/Brain_Mode3+3sd.mat','third_1');
save('../../results/Brain_Mode3-3sd.mat','third_2');
%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(first_1(1,:),first_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(first_2(1,:),first_2(2,:));
title("Mean-3sd");
suptitle("First mode");
hold off;

%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(sec_1(1,:),sec_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(sec_2(1,:),sec_2(2,:));
title("Mean-3sd");
suptitle("Second mode");
hold off;
%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(third_1(1,:),third_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(third_2(1,:),third_2(2,:));
title("Mean-3sd");
suptitle("Third mode");
hold off;
%%
error = sum(sum((mean_shape - align_shape).^2,1),2);
[~,in1] = min(error);
error = sum(sum((first_1 - align_shape).^2,1),2);
[~,in11] = min(error);
error = sum(sum((first_2 - align_shape).^2,1),2);
[~,in12] = min(error);
pause(1);
%%
figure;
im = imread("../../data/brain/data/mri_image_"+int2str(in1)+".png");
imshow(im);
hold on;
plot(data_shapes(1,:,in1),data_shapes(2,:,in1),'-rx','LineWidth',2);
title("Pointset is closest to the mean shape");
hold off;
pause(1);
%%
figure;
im = imread("../../data/brain/data/mri_image_"+int2str(in11)+".png");
imshow(im);
hold on;
plot(data_shapes(1,:,in11),data_shapes(2,:,in11),'-bx','LineWidth',2);
title("Pointset is closest to the mean shape +3sd");
hold off;
pause(1);
%%
figure;
im = imread("../../data/brain/data/mri_image_"+int2str(in12)+".png");
imshow(im);
hold on;
plot(data_shapes(1,:,in12),data_shapes(2,:,in12),'-gx','LineWidth',2);
title("Pointset is closest to the mean shape - 3sd");
hold off;
