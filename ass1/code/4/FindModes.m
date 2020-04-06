function [n11,n12,n21,n22,n31,n32,V,D,X] = FindModes(align_shape,mean_shape)
    abs_shape = align_shape - mean_shape;
    comb = [abs_shape(1,:,:) abs_shape(2,:,:)];
    X = zeros(size(comb,2),size(comb,3));
    for i = 1:size(comb,3)
        X(:,i) = comb(:,:,i);
    end
    [V,D] = eig(cov(X'));
    % To get descending eigenvalues
    V = fliplr(V);
    eigvals = flipud(diag(D));

    figure(3);
    hold on;
    title('Part c: Plot of variances');
    plot(eigvals);
    ylabel("Eigen value");
    xlabel("Mode of variation");
    hold off;
    sd3 = sqrt(eigvals(3));
    sd2 = sqrt(eigvals(2));
    sd1 = sqrt(eigvals(1));
    dev_1 = V(:,1);
    dev_shape1 = [dev_1(1:size(mean_shape,2))';dev_1(size(mean_shape,2)+1:end)'];
    dev_2 = V(:,2);
	dev_shape2 = [dev_2(1:size(mean_shape,2))';dev_2(size(mean_shape,2)+1:end)'];
    dev_3 = V(:,3);
	dev_shape3 = [dev_3(1:size(mean_shape,2))';dev_3(size(mean_shape,2)+1:end)'];
    n11 = mean_shape + 3*sd1*dev_shape1;
    n12 = mean_shape - 3*sd1*dev_shape1;
    n21 = mean_shape + 3*sd2*dev_shape2;
    n22 = mean_shape - 3*sd2*dev_shape2;
    n31 = mean_shape + 3*sd3*dev_shape3;
    n32 = mean_shape - 3*sd3*dev_shape3;

end