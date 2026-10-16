"""Minimal GitHub profile; original ASCII renderer inspired by web-media."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import markdown
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'; F=Path('C:/Windows/Fonts')
W,H=960,360
mono=ImageFont.truetype(str(F/'consola.ttf'),12)
small=ImageFont.truetype(str(F/'consola.ttf'),15)
big=ImageFont.truetype(str(F/'arialbd.ttf'),37)
glyph=ImageFont.truetype(str(F/'simsun.ttc'),260)
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
d.text((480,159),'田漢',font=glyph,fill=255,anchor='mm',stroke_width=3)
pw,ph=7,10; cols,rows=math.ceil(W/pw),math.ceil(H/ph)
m=np.asarray(mask.resize((cols,rows),Image.Resampling.BOX))/255
yy,xx=np.mgrid[0:rows,0:cols]; ramp=' .:-=+*xo%#@'
palette=[]
for i in range(64):
 t=i/63;palette.extend([int(4+226*t**2),int(7+238*t**1.2),int(13+242*t**.65)])
palette += [0]*(768-len(palette));pal=Image.new('P',(1,1));pal.putpalette(palette)
frames=[]
for fi in range(48):
 phase=math.tau*fi/48
 image=Image.new('RGB',(W,H),(4,7,13));d=ImageDraw.Draw(image)
 n=(np.sin(xx*.17+phase)+np.cos(yy*.37-phase))/2
 sweep=(np.cos(xx/cols*math.tau-phase)+1)/2
 wave=(np.sin(xx*.11+yy*.31-phase)+1)/2
 for y in range(rows):
  for x in range(cols):
   px,py=x*pw,y*ph
   if py<40 or py>282:continue
   ink=m[y,x]
   offset=int(7*math.sin(phase)*math.exp(-((py-(155+60*math.sin(phase)))/12)**2))
   v=ink*(.5+.26*(n[y,x]+1)/2+.3*sweep[y,x]**8)
   if ink<.1:v=(.07+.18*wave[y,x])*sweep[y,x] if (x*17+y*23)%13<3 else 0
   if v<.045:continue
   ch=ramp[min(len(ramp)-1,int(v*(len(ramp)-1)))];v=min(1,v)
   color=(int(4+226*v**2),int(7+238*v**1.2),int(13+242*v**.65))
   d.text((px+offset,py),ch,font=mono,fill=color)
 image=Image.blend(image,image.filter(ImageFilter.GaussianBlur(6)),.12);d=ImageDraw.Draw(image)
 d.line((28,37,932,37),fill=(22,46,73))
 d.text((28,14),'TIAN HAN',font=small,fill=(193,221,247))
 d.text((932,14),'ARTIST / RESEARCHER',font=small,fill=(91,140,188),anchor='ra')
 d.text((480,297),'MAKE THE INVISIBLE VISIBLE.',font=big,fill=(225,240,255),anchor='mt')
 d.text((480,341),'ANIMATION  /  MEDIA ART  /  INTERACTION',font=small,fill=(91,166,237),anchor='mm')
 frames.append(image.quantize(palette=pal,dither=Image.Dither.NONE))
frames[0].save(A/'tianhan-ascii-v2.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=2)
frames[12].convert('RGB').save(A/'tianhan-static-v2.png',optimize=True)
web='https://openc2023.github.io/web-media/'
for lang,identity,labels in [('en','Animation PhD · Media Artist · Busan',['Portfolio','Experiments','Identity']),('zh','动画博士 · 媒体艺术家 · 釜山',['作品集','交互实验','品牌资源']),('ko','애니메이션 박사 · 미디어 아티스트 · 부산',['포트폴리오','인터랙티브 실험','브랜드 자료'])]:
 file={'en':'README.md','zh':'README.zh-CN.md','ko':'README.ko.md'}[lang]
 text=f'''<a href="{web}"><img src="assets/tianhan-ascii-v2.gif" alt="田漢 / TIAN HAN — flowing blue ASCII" width="100%"></a>

<p align="center">{identity}</p>

<p align="center"><a href="{web}">{labels[0]} ↗</a> &nbsp; / &nbsp; <a href="{web}#elsewhere">{labels[1]} ↗</a> &nbsp; / &nbsp; <a href="https://img.7studio.org/">{labels[2]} ↗</a></p>

<p align="center"><sub><a href="README.md">EN</a> · <a href="README.zh-CN.md">中文</a> · <a href="README.ko.md">한국어</a></sub></p>
'''
 (ROOT/file).write_text(text,encoding='utf-8')
 css='body{margin:0;background:#0d1117;color:#c9d1d9;font:15px/1.7 Arial,"Microsoft YaHei","Malgun Gothic",sans-serif}main{max-width:850px;margin:35px auto;padding:25px;border:1px solid #30363d;border-radius:6px}a{color:#58a6ff;text-decoration:none}img{max-width:100%;height:auto}sub{font-size:11px}p{margin:18px 0}@media(max-width:600px){main{margin:12px;padding:15px}p{font-size:12px}}'
 page='<!doctype html><html lang="'+{'en':'en','zh':'zh-CN','ko':'ko'}[lang]+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tian Han — Minimal profile</title><style>'+css+'</style><main>'+markdown.markdown(text)+'</main></html>'
 for a,b in [('README.zh-CN.md','preview-zh.html'),('README.ko.md','preview-ko.html'),('README.md','preview.html')]:page=page.replace('href="'+a+'"','href="'+b+'"')
 (ROOT/({'en':'preview.html','zh':'preview-zh.html','ko':'preview-ko.html'}[lang])).write_text(page,encoding='utf-8')
print('Built minimal profile, 48-frame loop:',(A/'tianhan-ascii-v2.gif').stat().st_size,'bytes')
