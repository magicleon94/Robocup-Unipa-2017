f1 = fopen('Calib_ACF.bin')
S = fread(f1,[7 inf], 'float32');
%S = S';
plot(S(5:7,:)');
figure;
plot(S');
