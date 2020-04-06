function [mean_shape,align_shape] = FindMean(align_shape)
    ref = align_shape(:,:,1);
    for i = 2:size(align_shape,3)
        align_shape(:,:,i) = Align(ref,align_shape(:,:,i));
    end
    tol = 0.00001;
    prev_mean_shape = [];
    mean_shape = [];
    for t = 1:1000
        mean_shape = sum(align_shape(:,:,:),3);
        mean_norm = (sum(sum(mean_shape.^2))).^0.5;
        mean_shape = mean_shape/mean_norm;
%         size(mean_shape)
%         size(prev_mean_shape)
%         size(t)
        if t ~= 1 && sum(sum((mean_shape - prev_mean_shape).^2)) <= tol
            break;
        end
        t
        for i = 1:size(align_shape,3)
            align_shape(:,:,i) = Align(mean_shape,align_shape(:,:,i));
        end
        prev_mean_shape = mean_shape;
    end
end