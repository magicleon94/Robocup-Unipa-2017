f1 = fopen('Calib_tramonte_3x3_RC_2017_05_25_12_37_51.bin');
A = fread(f1,[11 inf],'float32');
A = A';
plot(A);
%sull'asse delle x abbiamo i campioni. 
%la mostra frequenza ? 256 Hz
%ERP evento 1 e 4
%tali marker sono nella colonna numero 10

col4 = A(:,10) == 4;
c4 = find(col4);
col1 = A(:, 10) == 1;
c1 = find(col1);

C = [c1 c4];
figure;
plot(A(C,:));