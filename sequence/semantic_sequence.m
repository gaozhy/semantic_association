wlevel=[zeros(60,1);ones(24,1)*1;ones(16,1)*2;ones(8,1)*3;ones(24,1)*4;
    ones(8,1)*5;ones(16,1)*6;ones(24,1)*7];
clevel=[zeros(60,1);ones(40,1);ones(40,1)*2;ones(40,1)*3];
all_id=[1:180]';

all_info=[all_id,wlevel,clevel];

w0_id=all_info(wlevel==0,1);
w1_id=all_info(wlevel==1,1);
w2_id=all_info(wlevel==2,1);
w3_id=all_info(wlevel==3,1);
w4_id=all_info(wlevel==4,1);
w5_id=all_info(wlevel==5,1);
w6_id=all_info(wlevel==6,1);
w7_id=all_info(wlevel==7,1);
tmp0=randperm(60);
run_trial_id=[];
for w = 0:7
    num_wl=length(all_info(wlevel==w,1));
    wl_id=all_info(wlevel==w,1);
        
    tmp=randperm(num_wl)';
    run_tmp=zeros(4,num_wl/4);
    for r=1:4
        run_tmp(r,:)=wl_id(tmp((r-1)*num_wl/4+1:r*num_wl/4));
    end
    run_trial_id=[run_trial_id,run_tmp]
    filename=sprintf('wlevel%d_tmp.mat',w);
    eval(sprintf('save %s run_tmp',filename));
        
end

for i = 1:4
    tmp=randperm(45);
    for j=1:45
        seq_id(i,j)=run_trial_id(i,tmp(j));
    end
end
