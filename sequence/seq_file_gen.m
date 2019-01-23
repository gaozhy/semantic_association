load('seq_id.mat');
load('alltrialid.mat');

for r = 1:4
    for i = 1:45
        Trial_ID(i,1)=seq_id(r,i);
        Probe(i,1)=alltrialid.Probe(seq_id(r,i));
        Target(i,1)=alltrialid.Target(seq_id(r,i));
        Cate(i,1)=alltrialid.Category(seq_id(r,i));
        Wlevel(i,1)=alltrialid.Wlevel(seq_id(r,i));
    end
    seq_data=table(Trial_ID,Probe,Target,Cate,Wlevel)
    filename=sprintf('stim_run%d.csv',r);
    writetable(seq_data,filename);
end
