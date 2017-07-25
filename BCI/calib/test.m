function [trainingSet, trainingLabels] = test(fname, interest,shiftRect)
f1 = fopen(fname);
S = fread(f1,[7 inf], 'float32');
%S = S';
%interest = [1,4];

trainingSet = [];
trainingLabels = [];

A = contiguous(S(6,:),[1,2,3,4,5,6]);
meanS = mean(S(1:3,:));
meanS = (meanS - min(meanS))/(max(meanS)-min(meanS));
for i = 1:6
    cella = A(i,2);
    positions = cella{1};
    for j = 1: size(positions,1)
        %v = mean(S(1:3,positions(j,1) + shiftRect:positions(j,2) + shiftRect));
        v = meanS(positions(j,1) + shiftRect:positions(j,2) + shiftRect);
        trainingSet = [trainingSet; v];
        if any(interest == i)
            trainingLabels = [trainingLabels; 1];
        else
            trainingLabels = [trainingLabels; 0];
        end
    end
end


    
%plot(S(5:7,1:3000)');
%figure;
%plot(S(1:4, 1:3000)');
