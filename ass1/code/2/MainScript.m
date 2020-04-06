%%
clc; clear; close all;
tic;
data = load("../../data/hand/data.mat");
data_shapes = data.shapes;
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
title('Part a: Initial pointset');

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
save('../../results/Hand_Aligned_pointset.mat','align_shape');
save('../../results/Hand_Mean_shape_.mat','mean_shape');
%%
[first_1,first_2,sec_1,sec_2,third_1,third_2,V,D,X] = FindModes(align_shape,mean_shape);
save('../../results/Hand_Mode1+3sd.mat','first_1');
save('../../results/Hand_Mode1-3sd.mat','first_2');
save('../../results/Hand_Mode2+3sd.mat','sec_1');
save('../../results/Hand_Mode2-3sd.mat','sec_2');
save('../../results/Hand_Mode3+3sd.mat','third_1');
save('../../results/Hand_Mode3-3sd.mat','third_2');
%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(first_1(1,:),first_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(first_2(1,:),first_2(2,:));
title("Mean-3sd");
suptitle("First mode");

%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(sec_1(1,:),sec_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(sec_2(1,:),sec_2(2,:));
title("Mean-3sd");
suptitle("Second mode");
%%
figure;
subplot(1,3,1);plot(mean_shape(1,:),mean_shape(2,:));
title("Mean");
subplot(1,3,2);plot(third_1(1,:),third_1(2,:));
title("Mean+3sd");
subplot(1,3,3);plot(third_2(1,:),third_2(2,:));
title("Mean-3sd");
suptitle("Third mode");
%%
error = sum(sum((mean_shape - align_shape).^2,1),2);
[~,in1] = min(error);
error = sum(sum((first_1 - align_shape).^2,1),2);
[~,in11] = min(error);
error = sum(sum((first_2 - align_shape).^2,1),2);
[~,in12] = min(error);
%%
figure;
plot(mean_shape(1,:),mean_shape(2,:));
hold on;
plot(align_shape(1,:,in1),align_shape(2,:,in1),'-rx','LineWidth',2);
title("Pointset is closest to the mean shape");
legend("mean shape","Pointset");
%%
figure;
plot(first_1(1,:),first_1(2,:));
hold on;
plot(align_shape(1,:,in11),align_shape(2,:,in11),'-bx','LineWidth',2);
title("Pointset is closest to the mean shape +3sd");
legend("mean shape+3sd","Pointset");
%%
figure;
plot(first_2(1,:),first_2(2,:));
hold on;
plot(align_shape(1,:,in12),align_shape(2,:,in12),'-gx','LineWidth',2);
title("Pointset is closest to the mean shape -3sd");
legend("mean shape -3sd","Pointset");
title("Pointset is closest to the mean shape - 3sd");
