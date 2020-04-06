function [solution,rms] = QuadraticDenoising(noisy,changed,Noiseless,question)
    realimage  = abs(noisy);
    rms = zeros(1,3);
    j=1;
    %% Optimal Parameters
    best_alpha = 0.001;
    
    for alpha = [best_alpha, 1.2*best_alpha ,0.8*best_alpha]
        step = 1;
        solution = realimage;
        [cost, gradient] = QuadraticCostGrad(solution,realimage,alpha);
        oldcost = cost;
        i = 1;
        notchanged = 1;
        k=1;
        %costvector(1) = cost;
        newcostvector(1) = cost;
        while step > 1e-8 && (notchanged || cost/oldcost < 0.9999)
              temp = solution - step * gradient; 
              [newcost, newgradient] = QuadraticCostGrad(temp,realimage,alpha);
              
              if(j==1)
                costvector(k) = cost;
                newcostvector(end +1) = newcost;
                k=k+1; 
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
            % this is for best alpha
            figure;  
            changed = solution;
            imshow(changed,[]);
%             colormap(gca,hot), colorbar;
            title('Quadratic Denoising');
            
        end
        j=j+1;
    end

    
    
