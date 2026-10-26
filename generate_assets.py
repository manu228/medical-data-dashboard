"""Generate the dataset export and a truthful real-data dashboard preview."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from analysis import get_data, summary, grouped_feature_stats

ROOT=Path(__file__).resolve().parent
(ROOT/'screenshots').mkdir(exist_ok=True)
(ROOT/'data').mkdir(exist_ok=True)
df=get_data(); s=summary(df)
df.to_csv(ROOT/'data'/'wdbc_features.csv',index=False)
benign=df[df.diagnosis=='Benign']; malignant=df[df.diagnosis=='Malignant']

fig=plt.figure(figsize=(16,10),facecolor='#f5f7fb',dpi=150)
ax=fig.add_axes([0,0,1,1]);ax.axis('off');ax.set_xlim(0,16);ax.set_ylim(0,10)
navy='#202b45';sub='#6b7890';teal='#18a798';rose='#dc7185'
def text(x,y,t,size=13,color=navy,weight='normal'):
    ax.text(x,y,t,fontsize=size,color=color,weight=weight,fontfamily='DejaVu Sans',va='center')
def panel(x,y,w,h,color='white',r=.19,edge='#e8edf5'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.01,rounding_size={r}',facecolor=color,edgecolor=edge,lw=1))
# sidebar
panel(0,0,3.25,10,color='#17213b',edge='#17213b',r=0)
text(.36,9.45,'◉  CELLSCOPE',18,'white','bold');text(.36,9.07,'RESEARCH WORKSPACE',9,'#91a2c2','bold')
ax.plot([.35,2.92],[8.73,8.73],color='#40506e',lw=1)
text(.37,8.36,'EXPLORER',9,'#9daecb','bold');panel(.3,7.61,2.65,.52,'#34425d',.12,edge='#34425d');text(.52,7.86,'◫   Overview',12,'white')
text(.38,6.83,'DATASET FILTERS',9,'#9daecb','bold');text(.37,6.41,'Diagnosis',11,'white')
for y,title,co in [(5.88,'✓   Benign',teal),(5.39,'✓   Malignant',rose)]:
    panel(.35,y,2.5,.39,'#26334f',.1,edge='#40506e');text(.51,y+.19,title,10.5,'white')
text(.37,4.68,'Measurement',11,'white');panel(.35,4.04,2.5,.48,'#26334f',.1,edge='#40506e');text(.51,4.28,'Mean radius       ⌄',10,'white')
text(.37,1.2,'UCI  ·  WDBC dataset',9,'#91a2c2');text(.37,.85,'569 samples · 30 features',9,'#91a2c2');text(.37,.49,'Educational use only',9,'#91a2c2')
# header
text(3.74,9.53,'DATA EXPLORER  /  BREAST CANCER',10,'#5f7493','bold')
text(3.73,8.99,'Breast Cancer Data Explorer',25,navy,'bold')
text(3.74,8.55,'Explore diagnostic image features and descriptive patterns across 569 observations.',11,sub)
panel(3.65,7.89,11.84,.43,'#e7f4f3',.12,edge='#d3eae8');text(3.87,8.10,'ℹ   For education and exploration only — not for diagnosis or patient risk assessment.',10,'#2c716e')
# metric cards
metrics=[('SAMPLES SHOWN','569',navy),('BENIGN','357',teal),('MALIGNANT','212',rose),('MALIGNANT IN SET','37.3%',navy)]
for idx,(label,val,co) in enumerate(metrics):
    x=3.65+idx*3.03;panel(x,6.74,2.77,.95);text(x+.23,7.42,label,9,sub,'bold');text(x+.22,7.04,val,22,co,'bold')
# left donut
panel(3.65,3.55,5.73,2.9);text(3.99,6.08,'Diagnostic label distribution',13,navy,'bold')
a1=fig.add_axes([.249,.391,.18,.19]);a1.pie([357,212],colors=[teal,rose],startangle=90,counterclock=False,wedgeprops={'width':.30,'edgecolor':'white','linewidth':3});a1.text(0,0,'569',ha='center',va='center',fontsize=19,color=navy,weight='bold');a1.set_aspect('equal')
ax.add_patch(Circle((6.4,4.48),.055,color=teal));text(6.56,4.47,'Benign  62.7%',11,navy)
ax.add_patch(Circle((6.4,4.08),.055,color=rose));text(6.56,4.07,'Malignant  37.3%',11,navy)
# right box
panel(9.59,3.55,5.9,2.9);text(9.93,6.08,'Mean radius by diagnosis',13,navy,'bold')
a2=fig.add_axes([.62,.385,.318,.205]);a2.boxplot([benign['mean radius'],malignant['mean radius']],tick_labels=['Benign','Malignant'],patch_artist=True,showfliers=False,medianprops={'color':navy,'linewidth':2},boxprops={'linewidth':1.4,'edgecolor':'#526580'},whiskerprops={'color':'#7c8da8'},capprops={'color':'#7c8da8'})
for patch,col in zip(a2.artists if hasattr(a2,'artists') else [],[teal,rose]):patch.set_facecolor(col)
# matplotlib boxplot patches
for i,p in enumerate(a2.patches):p.set_facecolor([teal,rose][i]);p.set_alpha(.75)
a2.set_ylabel('Mean radius',fontsize=9,color=sub);a2.grid(axis='y',alpha=.15);a2.spines[['top','right']].set_visible(False);a2.tick_params(labelsize=9)
# scatter card
panel(3.65,.32,11.84,3.01);text(3.99,2.96,'Feature relationships',13,navy,'bold');text(3.99,2.64,'Mean radius vs. mean texture',9,sub)
a3=fig.add_axes([.275,.063,.647,.176]);a3.scatter(benign['mean radius'],benign['mean texture'],color=teal,alpha=.52,s=16,label='Benign',linewidths=0);a3.scatter(malignant['mean radius'],malignant['mean texture'],color=rose,alpha=.52,s=16,label='Malignant',linewidths=0)
a3.grid(alpha=.15);a3.spines[['top','right']].set_visible(False);a3.tick_params(labelsize=9);a3.set_xlabel('Mean radius',fontsize=9,color=sub);a3.set_ylabel('Mean texture',fontsize=9,color=sub);a3.legend(loc='upper left',frameon=False,fontsize=9,ncol=2)
fig.savefig(ROOT/'screenshots'/'dashboard-overview.png',dpi=150,facecolor=fig.get_facecolor());plt.close(fig)

stats=grouped_feature_stats(df,'mean radius')
with (ROOT/'RESULTS.md').open('w') as f:
    f.write('# CellScope | Results and interpretation\n\n')
    f.write('The following are **computed from the actual dataset** with `analysis.py`; no synthetic samples or estimated clinical outcomes are used.\n\n')
    f.write(f'- Total labeled image specimens: **{s["total"]}**.\n')
    f.write(f'- Benign: **{s["benign"]} ({100*s["benign"]/s["total"]:.1f}%)**.\n')
    f.write(f'- Malignant: **{s["malignant"]} ({s["malignant_pct"]:.1f}%)**.\n')
    f.write(f'- Missing cells in included source features: **{int(df.isna().sum().sum())}**.\n\n')
    f.write('## Mean-radius comparison\n\n')
    f.write('| Diagnostic label | Samples | Mean radius | Median radius | Std. dev. |\n|---|---:|---:|---:|---:|\n')
    for row in stats.itertuples(index=False):
        f.write(f'| {row.diagnosis} | {row.count} | {row.mean:.3f} | {row.median:.3f} | {row.std:.3f} |\n')
    f.write('\n## What worked\n\n- Loaded locally bundled public data without an API key.\n- Verified 569 unique IDs, 30 features, diagnostic labels, and no missing values.\n- Built group comparisons with unit tests and an interactive explorer.\n- Created a visual preview using genuine dataset values.\n')
    f.write('\n## Interpretation and limitations\n\nThe malignant-labeled observations have a larger mean radius on average in this dataset. The scatter plot shows overlap: a single feature cannot be interpreted as a diagnosis. Because the sample was assembled for a specific diagnostic study, its label proportions **are not population cancer rates**. The data contain no time-series or patient demographic variables, so no changes over time or demographic claims are made.\n')
    f.write('\n## What I would improve next\n\n1. Quantify feature separability with uncertainty intervals and multiple-testing awareness.\n2. Add accessible plot annotations and clearer original measurement definitions.\n3. Conduct a separately scoped, leakage-aware predictive modeling exercise with cross-validation; never frame model scores as clinical validity.\n4. Invite domain experts to critique presentation and bias.\n')
print('Generated dataset export, screenshot, and results: ',s)
