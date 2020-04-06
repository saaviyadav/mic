%% Get the best denoised image using Huber Denoising Algorithm


function [solution,rms] = HuberDenoising(noisy,changed,Noiseless,question)
    realimage  = abs(noisy);
    rms = zeros(1,5);
    j=1;  
    %% Optimal Parameters
    g = 0.001;
    a = 0.0001;
    for alpha = [a, 1.2*a,0.8*a]
        gamma = g;
        step = 1;
        solution = realimage;
        [cost, gradient] = HuberCostGrad(solution,realimage,alpha,gamma);
        oldcost = cost;
        i = 1;
        notchanged = 1;
        %costvector(1) = cost;
        newcostvector(1) =cost;
        k=1;
        while step > 1e-8 && (notchanged || cost/oldcost < 0.9999999999)
              temp = solution - step * gradient; 
              [newcost, newgradient] = HuberCostGrad(temp,realimage,alpha,gamma);
              if(j==1)
                costvector(k) = cost;
                newcostvector(end +1) = newcost;
                k = k+1;
               
              end
              if (newcost  < cost)
                 step = 1.1*step;
                 solution = temp;
                 oldcost = cost;
                 cost = newcost;
                 gradient = newgradient;
                 notchanged = 0;
              else 
                 step = step*0.5; 
                 notchanged = 1;
              end
                 i = i+1;
        end
        if(question == 0)
            solution = ((solution/(max(max(solution))))*255);
            rms(1,j) = RRMSE(Noiseless,solution);
        end
        
        if(j==1)
            figure;            
            changed(:,:,1) = solution;
            imshow(changed,[]);
            title('Huber Denoising');
        end
        j=j+1;
        
    end

    for gamma = [1.2*g,0.8*g]
        alpha = a;
        step = 1;
        solution = realimage;
        [cost, gradient] = QuadraticCostGrad(solution,realimage,alpha);
        oldcost = cost;
        i = 1;
        notchanged = 1;
        while step > 1e-8 && (notchanged || cost/oldcost < 0.9999)
              temp = solution - step * gradient; 
              [newcost, newgradient] = QuadraticCostGrad(temp,realimage,alpha);
              if (newcost  < cost)
                 step = 1.1*step;
                 solution = temp;
                 oldcost = cost;
                 cost = newcost;
                 gradient = newgradient;
                 notchanged = 0;
              else 
                 step = step*0.5; 
                 notchanged = 1;
              end
                 i = i+1;
        end
        if(question == 1)
            solution = ((solution/(max(max(solution))))*255);
            rms(1,j) = RRMSE(Noiseless,solution);
        end
       j=j+1;
    end

    
    
