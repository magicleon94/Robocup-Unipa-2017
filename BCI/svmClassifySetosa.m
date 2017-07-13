load fisheriris
xdata = meas(51:end,3:4); %versicolor virginica
group = species(51:end);  %label
figure;
svmStruct = svmtrain(xdata,group,'ShowPlot',true);

Xnew = [5 2; 4 1.5];
species = svmclassify(svmStruct,Xnew,'ShowPlot',true)
hold on;
plot(Xnew(:,1),Xnew(:,2),'ro','MarkerSize',12);
hold off