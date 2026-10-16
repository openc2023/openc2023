"""6-second particle assembly and character decoding, for GitHub profile GIF."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import numpy as np
import math
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'assets';F=Path('C:/Windows/Fonts')
W,H,N=960,360,75
font=ImageFont.truetype(str(F/'simsun.ttc'),254)
mono=ImageFont.truetype(str(F/'consola.ttf'),11)
label=ImageFont.truetype(str(F/'consola.ttf'),14)
name=ImageFont.truetype(str(F/'consola.ttf'),38)
mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
md.text((480,154),'田漢',font=font,fill=255,anchor='mm',stroke_width=4)
coverage=np.asarray(mask)
rng=np.random.default_rng(717)
points=[]
for y in range(45,282,5):
 for x in range(190,770,5):
  if coverage[y,x]>80:points.append((x,y))
target=np.array(points,dtype=float); count=len(target)
scatter=np.column_stack((rng.uniform(25,935,count),rng.uniform(48,278,count)))
curve=rng.uniform(-80,80,(count,2));phase=rng.uniform(0,math.tau,count)
delay=rng.uniform(0,.19,count); char_ids=rng.integers(0,12,count)
palette=[]
for i in range(96):
 v=i/95;palette.extend([round(4+233*v**2),round(7+241*v**1.1),round(13+242*v**.55)])
palette += [0]*(768-len(palette));pal=Image.new('P',(1,1));pal.putpalette(palette)
def smooth(v):
 v=np.clip(v,0,1);return v*v*(3-2*v)
frames=[]; originals=[]
alphabet='07S#%X@*+<>/'
for frame in range(N):
 t=frame/(N-1)
 if t<.13: amount=np.zeros(count);state='FORM';decode=1
 elif t<.39:
  amount=smooth(((t-.13)/.26-delay)/.81);state='DISPERSE';decode=max(0,1-(t-.13)/.12)
 elif t<.79:
  amount=1-smooth(((t-.39)/.40-delay)/.81);state='DECODE';decode=np.clip((t-.52)/.24,0,1)
 else:amount=np.zeros(count);state='FORM';decode=1
 motion=np.sin(amount*math.pi)
 pos=target+(scatter-target)*amount[:,None]+curve*motion[:,None]
 pos[:,0]=np.clip(pos[:,0],20,940);pos[:,1]=np.clip(pos[:,1],48,275)
 im=Image.new('RGB',(W,H),(4,7,13));d=ImageDraw.Draw(im)
 # Dim, periodic orbital dust anchors the field while the letter particles move.
 for k in range(100):
  angle=k*2.399963+t*math.tau
  x=480+430*math.cos(angle)*(k/100)**.5;y=161+109*math.sin(angle)*(k/100)**.5
  d.point((x,y),fill=(9,24,43))
 glow=Image.new('RGB',(W,H));g=ImageDraw.Draw(glow)
 for k,(x,y) in enumerate(pos):
  a=float(amount[k]);v=(.62+.33*((target[k,0]-190)/580))*(1-.58*a)
  c=(round(4+233*v*v),round(7+241*v**1.1),round(13+242*v**.55))
  if k%7==0 and a>.06:
   ch=alphabet[(int(char_ids[k])+frame//3)%len(alphabet)]
   d.text((x-3,y-4),ch,font=mono,fill=c)
  else:d.rectangle((x,y,x+2,y+2),fill=c)
  if .02<a<.98 and k%9==0:
   dx,dy=target[k]-scatter[k];length=max(1,math.hypot(dx,dy));size=9*math.sin(a*math.pi)
   d.line((x,y,x-dx/length*size,y-dy/length*size),fill=(15,66,115),width=1)
  if k%4==0:g.ellipse((x-2,y-2,x+3,y+3),fill=tuple(int(q*.38) for q in c))
 im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(4)));d=ImageDraw.Draw(im)
 d.text((28,15),'TIAN HAN  /  MEDIA ART',font=label,fill=(102,161,219))
 d.text((932,15),state,font=label,fill=(102,161,219),anchor='ra')
 d.line((28,37,932,37),fill=(18,39,61))
 desired='TIAN HAN';chars=[]
 for j,ch in enumerate(desired):
  chars.append(ch if ch==' ' or decode>j/len(desired) else alphabet[(frame//2+j*3)%len(alphabet)])
 d.text((480,298),''.join(chars),font=name,fill=(216,237,255),anchor='mt')
 originals.append(im);frames.append(im.quantize(palette=pal,dither=Image.Dither.NONE))
frames[0].save(A/'tianhan-particles-v3.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=2)
originals[0].save(A/'tianhan-particles-static.png',optimize=True)
sheet=Image.new('RGB',(1920,720))
for i,idx in enumerate([0,25,43,60]):sheet.paste(originals[idx],((i%2)*960,(i//2)*360))
sheet.save(ROOT/'particles-stages.jpg')
for file in ['README.md','README.zh-CN.md','README.ko.md']:
 p=ROOT/file;s=p.read_text(encoding='utf-8').replace('tianhan-ascii-v2.gif','tianhan-particles-v3.gif').replace('flowing blue ASCII','particle assembly and character decoding');p.write_text(s,encoding='utf-8')
for file in ['preview.html','preview-zh.html','preview-ko.html']:
 p=ROOT/file;s=p.read_text(encoding='utf-8').replace('tianhan-ascii-v2.gif','tianhan-particles-v3.gif');p.write_text(s,encoding='utf-8')
p=ROOT/'SETUP.md';s=p.read_text(encoding='utf-8').replace('tianhan-ascii-v2.gif','tianhan-particles-v3.gif').replace('tianhan-static-v2.png','tianhan-particles-static.png').replace('48 帧，4.8 秒','75 帧，6 秒').replace('source/build_minimal.py','source/build_particles.py');p.write_text(s,encoding='utf-8')
gif=Image.open(A/'tianhan-particles-v3.gif');duration=0
for i in range(gif.n_frames):gif.seek(i);duration+=gif.info['duration']
assert duration==6000 and gif.info['loop']==0
print('Particles:',count,'Duration:',duration,'GIF bytes:',(A/'tianhan-particles-v3.gif').stat().st_size)
