function [aligned] = Align(ref,original)
count = 1;
    for i = 0:5:360
        mTheta = GenerateM(i);
        changed = mTheta*original;
        error(count) = sum(sum((ref - changed).^2));
        count = count+1;
    end
    [M, c] = min(error);
    theta = 5*(c-1);
    aligned = GenerateM(theta)*original;
end

function [mTheta] = GenerateM(theta)
    mTheta = [cos(theta) -sin(theta);sin(theta) cos(theta)];
end