function [top, bottom, right, left] = CircularShift(X)
    top = X - circshift(X,1,1);
    bottom = X - circshift(X, -1,1);
    right = X - circshift(X, -1,2);
    left = X - circshift(X, 1,2);
end