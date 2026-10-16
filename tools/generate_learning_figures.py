"""Generate original didactic SVGs using only the Python standard library."""
from pathlib import Path
from math import sin, pi
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT = 'Segoe UI, Microsoft YaHei, Noto Sans CJK SC, sans-serif'

def start(title, desc, height=480):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">', f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>', f'<style>text{{font-family:{FONT};fill:#182b49}} .small{{font-size:16px}} .title{{font-size:26px;font-weight:600}}</style>', '<rect width="100%" height="100%" fill="#f8fafc"/>', f'<text x="40" y="43" class="title">{escape(title)}</text>']

def label(svg,x,y,s,cls='small'):
 svg.append(f'<text x="{x}" y="{y}" class="{cls}">{escape(s)}</text>')

def trace(svg, fn, x0, y0, width, amplitude, tmax, color, points=600):
 coords=' '.join(f'{x0+width*i/(points-1):.2f},{y0-amplitude*fn(tmax*i/(points-1)):.2f}' for i in range(points))
 svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2"/>')

def save(name,svg):
 (OUT/name).write_text('\n'.join(svg+['</svg>'])+'\n',encoding='utf-8')

s=start('采样边界：每周期两个点并不保证恢复任意相位', '人工60赫兹正弦以120赫兹从过零点采样，全部采样点为零。')
label(s,40,82,'人工60 Hz正弦；采样率120 Hz；相位从过零点开始')
s.append('<line x1="60" y1="230" x2="940" y2="230" stroke="#cbd5e1"/>')
trace(s,lambda t:sin(2*pi*60*t),60,230,880,100,0.05,'#2563eb')
for i in range(7):
 s.append(f'<circle cx="{60+880*(i/120)/0.05:.2f}" cy="230" r="5" fill="#e15c3a"/>')
label(s,60,370,'蓝线：连续信号   红点：采到的样本（均为0）')
label(s,60,405,'实际降采样还要给抗混叠滤波的过渡带留余量。')
save('sampling_aliasing.svg',s)

s=start('参考与秩：通道数不等于独立信息数量','三个参考示例展示共同参考抵消、平均参考约束和复制通道不能增加秩。')
panels=[('共同参考','A′ = A − R','B′ = B − R','A′ − B′ = A − B'),('两通道平均参考','A′ = (A − B) / 2','B′ = (B − A) / 2','A′ + B′ = 0：至多一个独立维度'),('增加虚拟通道','C = A + B','C由A、B决定','三通道仍只有至多两个独立维度')]
for k,p in enumerate(panels):
 x=30+k*325
 s.append(f'<rect x="{x}" y="110" width="310" height="250" rx="12" fill="white" stroke="#cbd5e1"/>')
 label(s,x+18,148,p[0])
 for j,v in enumerate(p[1:]): label(s,x+18,205+j*50,v)
label(s,40,415,'重参考、插值或补零不会凭空恢复已经丢失的独立信号。')
save('reference_rank.svg',s)

s=start('基线校正：减去一个均值只改变偏移','人工线性漂移做基线均值相减后仍保持相同斜率。')
label(s,40,82,'人工信号 x(t)=2+0.8t；基线窗口为0到1秒，均值为2.4')
for y in [170,280,390]: s.append(f'<line x1="70" y1="{y}" x2="930" y2="{y}" stroke="#e2e8f0"/>')
trace(s,lambda t:2+0.8*t,70,350,860,40,4,'#2563eb')
trace(s,lambda t:2+0.8*t-2.4,70,350,860,40,4,'#df6b37')
label(s,70,410,'蓝：校正前   橙：校正后；斜率均为0.8，未被消除')
label(s,70,445,'示意的时间和幅度单位任意；不是实际脑电数据。')
save('baseline_drift.svg',s)

s=start('坏通道与坏时间段：观察问题占据的范围','四条人工信号分别展示节律、持续平直、局部突变和局部高频干扰。',640)
funcs=[('节律示意',lambda t:0.65*sin(2*pi*5*t),'#2563eb'),('持续平直',lambda t:0.0,'#b45309'),('局部突变',lambda t:0.4*sin(2*pi*5*t)+(2.1 if 0.9<t<1.1 else 0),'#dc2626'),('局部高频干扰',lambda t:0.4*sin(2*pi*5*t)+(0.7*sin(2*pi*32*t) if 0.7<t<1.4 else 0),'#7c3aed')]
for i,(name,fn,color) in enumerate(funcs):
 y=150+110*i
 label(s,40,y-43,name)
 s.append(f'<line x1="70" y1="{y}" x2="930" y2="{y}" stroke="#cbd5e1"/>')
 trace(s,fn,70,y,860,27,2,color,1200)
label(s,40,600,'人工形态示例；真实信号往往混合多种来源，不能仅凭形状自动定性。')
save('artifact_examples.svg',s)
print(f'Generated 4 original SVGs in {OUT}')
