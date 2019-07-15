%filter kinematic data
%edited by MEV 8/14/14
clear all;
close all;
clc;

%% Load Data
filename = 'C:\Users\MAE-MOBLLAB\Desktop\New folder\IKreach.mot';
delimiterIn = '\t';headerlinesIn = 7;
rawIK = importdata(filename,delimiterIn,headerlinesIn);
timevector = rawIK.data(:,1);

%% Filter design
windowSize = 30;
Hd=ones(1,windowSize)/windowSize;

%% Filter data 
for n=8:27
    filtered_IK(:,n) = filtfilt(Hd,1,rawIK.data(:,n));
end

%% Filtered data with time into matrix
data_together = [timevector,filtered_IK(:,8:27)];

%% Create column headers without r_x,r_y,r_z,t_x,t_y,t_z
new_textdata_headers=[rawIK.textdata(1,1);rawIK.textdata(2,1);rawIK.textdata(3,1);'nColumns=21';rawIK.textdata(5,1);rawIK.textdata(6,1)];
time_header=rawIK.textdata(7,1);
dof_headers=rawIK.textdata(7,8:27);
new_column_headers=[time_header,dof_headers];

%% Export filtered data to .mot file
fileID=fopen('C:\Users\MAE-MOBLLAB\Desktop\New folder\ikfiltered.sto','wt');
[M,N]=size(new_textdata_headers);
for i=1:M;
    for j=1:N;
fprintf(fileID,'%s\n',new_textdata_headers{i,j});
    end
end
[P,Q]=size(new_column_headers);
for k=1:P;
    for m=1:Q;
        fprintf(fileID,'%s\t',new_column_headers{k,m});
    end
end
fprintf(fileID,'\n');
fclose(fileID);
dlmwrite('C:\Users\MAE-MOBLLAB\Desktop\New folder\ikfiltered.sto',...
         data_together,'-append','delimiter','\t','newline','pc');
