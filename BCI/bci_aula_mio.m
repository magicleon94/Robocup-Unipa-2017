a = fopen('Calib_tramonte_3x3_RC_2017_05_25_12_37_51.bin');
A = fread(a,[11 inf],'float32')';
%ERP evento 1 e 4
% i marker sono nella colonna numero 10

erp4 = A(:,10) == 4;
erp1 = A(:,10) == 1;

res1 = A(erp4,:);
res2 = A(erp1,:);

C = [res1 res2];
plot(A(C,:))




