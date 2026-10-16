"""Build the profile's original ASCII banner and three-language Markdown.

Visual source: https://openc2023.github.io/web-media/
Typography is rasterized from installed fonts; no scripts are needed in GitHub.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import markdown

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets';ASSETS.mkdir(exist_ok=True,parents=True)
FONTS=Path('C:/Windows/Fonts')
mono=ImageFont.truetype(str(FONTS/'consola.ttf'),12)
small=ImageFont.truetype(str(FONTS/'consola.ttf'),14)
title=ImageFont.truetype(str(FONTS/'arialbd.ttf'),54)
sub=ImageFont.truetype(str(FONTS/'consola.ttf'),17)
cjk=ImageFont.truetype(str(FONTS/'simsun.ttc'),190)
W,H=960,300
mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
md.text((723,150),'田漢',font=cjk,fill=255,anchor='mm',stroke_width=1)
pw,ph=7,11
cols,rows=math.ceil(W/pw),math.ceil(H/ph)
m=np.asarray(mask.resize((cols,rows),Image.Resampling.BOX))/255
yy,xx=np.mgrid[0:rows,0:cols]
ramp=' .:-=+*xo%#@'
frames=[]
palette=[]
for i in range(32):
 t=i/31
 palette.extend([round(6+108*t),round(8+177*t),round(12+243*t)])
palette += [0]*(768-len(palette))
for fi in range(40):
 phase=math.tau*fi/40
 im=Image.new('RGB',(W,H),(6,8,12));d=ImageDraw.Draw(im)
 n=(np.sin(xx*.19+phase)+np.cos(yy*.35-phase))/2
 wave=(np.sin(xx*.09+yy*.13-phase)+1)/2
 for y in range(rows):
  for x in range(cols):
   px,py=x*pw,y*ph
   if px<490:
    if (x*13+y*7)%29==0:
     v=.06+.07*wave[y,x]
     d.text((px,py),'.',font=mono,fill=(12,23,round(35+v*70)))
    continue
   v=m[y,x]*(.76+.2*n[y,x])
   if m[y,x]<.1 and (x*17+y*23)%11==0:v=.08+.08*wave[y,x]
   if v<.07:continue
   ch=ramp[min(len(ramp)-1,max(0,int(v*(len(ramp)-1))))]
   color=(round(19+95*v),round(40+145*v),round(65+190*v))
   d.text((px,py),ch,font=mono,fill=color)
 d.line((32,40,928,40),fill=(28,44,62))
 d.text((32,16),'~/tianhan',font=small,fill=(114,185,255))
 d.text((928,16),'ART / RESEARCH / CODE',font=small,fill=(118,139,162),anchor='ra')
 d.text((32,81),'TIAN HAN',font=title,fill=(232,240,249))
 d.text((35,156),'ANIMATION + MEDIA ART',font=sub,fill=(114,185,255))
 d.text((35,189),'Research. Create. Interact.',font=small,fill=(147,163,181))
 d.line((32,254,928,254),fill=(28,44,62))
 d.text((32,270),'BUSAN, KR',font=small,fill=(147,163,181))
 d.text((928,270),'WORDS INTO PIXELS',font=small,fill=(147,163,181),anchor='ra')
 pal=Image.new('P',(1,1));pal.putpalette(palette)
 frames.append(im.quantize(palette=pal,dither=Image.Dither.NONE))
frames[0].save(ASSETS/'tianhan-ascii.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=2)
frames[0].convert('RGB').save(ASSETS/'tianhan-static.png',optimize=True)

links={'web':'https://openc2023.github.io/web-media/','repo':'https://github.com/openc2023/web-media','studio':'https://github.com/openc2023/7S','identity':'https://img.7studio.org/','content':'https://github.com/openc2023/content','orcid':'https://orcid.org/0009-0004-8437-134X'}
intro={
'en':('English','Animation PhD · Media Artist · Busan, South Korea','I explore animation imagery, immersive media art and urban regeneration, bringing research into moving images and interactive experiences.','Chinese and Korean research, translation and creative collaboration.','Selected projects','Explore','Research & practice','Immersive media · Projection mapping · Generative art · Animation research · Interactive installations','Papers & publications','Full portfolio','Static banner','Repository / Source'),
'zh':('中文','动画博士 · 媒体艺术家 · 韩国釜山','研究漫画动画图像、沉浸式媒体艺术与城市再生，把研究方法带入影像和交互体验。','支持中韩双语研究、翻译与创作协作。','精选项目','浏览','研究与实践','沉浸式媒体 · 投影映射 · 生成艺术 · 动画研究 · 互动装置','论文与出版','完整作品集','静态横幅','仓库 / 源码'),
'ko':('한국어','애니메이션 박사 · 미디어 아티스트 · 대한민국 부산','만화·애니메이션 이미지, 몰입형 미디어아트와 도시재생을 연구하며, 그 방법을 영상과 인터랙티브 경험으로 확장합니다.','중국어·한국어 연구, 번역 및 창작 협업이 가능합니다.','주요 프로젝트','둘러보기','연구와 작업','몰입형 미디어 · 프로젝션 매핑 · 제너러티브 아트 · 애니메이션 연구 · 인터랙티브 설치','논문과 출판','전체 포트폴리오','정적 배너','저장소 / 소스')}
descs={
'en':['Personal portfolio, ASCII experiments and interactive media works.','STUDIO 7 / 07S website and portfolio project.','C / SPLIT brand assets: 18 SVG and PNG variants with editable Illustrator source.'],
'zh':['个人作品集、ASCII 字符实验与网页互动作品。','STUDIO 7 / 07S 网站与作品展示项目。','C / SPLIT 品牌资源：18 款 SVG、PNG 与可编辑 Illustrator 源文件。'],
'ko':['개인 포트폴리오, ASCII 실험과 웹 인터랙티브 작업.','STUDIO 7 / 07S 웹사이트 및 포트폴리오 프로젝트.','C / SPLIT 브랜드 자료: SVG·PNG 18종과 편집 가능한 Illustrator 원본.']}
for lang,t in intro.items():
 filename={'en':'README.md','zh':'README.zh-CN.md','ko':'README.ko.md'}[lang]
 nav='[English](README.md) · [中文](README.zh-CN.md) · [한국어](README.ko.md)'
 text=f'''{nav}

[![TIAN HAN — animated blue ASCII identity](assets/tianhan-ascii.gif)]({links['web']})

# 田漢 / Tian Han / 티앤한

**{t[1]}**

{t[2]}

{t[3]}

[Portfolio]({links['web']}) · [Interactive works]({links['web']}#elsewhere) · [STUDIO 7]({links['studio']}) · [ORCID]({links['orcid']})

## {t[4]}

| Project | {'简介' if lang=='zh' else '소개' if lang=='ko' else 'About'} | {t[5]} |
| :-- | :-- | :-- |
| **web-media** | {descs[lang][0]} | [Live]({links['web']}) · [Code]({links['repo']}) |
| **STUDIO 7 / 07S** | {descs[lang][1]} | [Code]({links['studio']}) |
| **C / SPLIT Identity** | {descs[lang][2]} | [Live]({links['identity']}) · [Code]({links['content']}) |

## {t[6]}

{t[7]}

[{t[8]}]({links['web']}#papers) · [{t[9]}](https://art717.notion.site/box)

---

<sub>[{t[10]}](assets/tianhan-static.png) · [{t[11]}](https://github.com/openc2023/openc2023)</sub>
'''
 (ROOT/filename).write_text(text,encoding='utf-8')
 css='''body{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.6 Arial,"Microsoft YaHei","Malgun Gothic",sans-serif}main{max-width:850px;margin:32px auto;padding:32px;border:1px solid #30363d;border-radius:6px}a{color:#58a6ff;text-decoration:none}img{max-width:100%;height:auto}h1{font-size:30px;border-bottom:1px solid #30363d;padding-bottom:14px}h2{font-size:22px;margin-top:28px;border-bottom:1px solid #30363d;padding-bottom:8px}table{width:100%;border-collapse:collapse}td,th{border:1px solid #30363d;padding:10px;text-align:left}hr{border:0;border-top:1px solid #30363d;margin:26px 0}sub{color:#8b949e}@media(max-width:600px){main{margin:12px;padding:18px}table{font-size:12px}td,th{padding:7px}h1{font-size:24px}}'''
 page='<!doctype html><html lang="'+{'en':'en','zh':'zh-CN','ko':'ko'}[lang]+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tian Han — GitHub profile preview</title><style>'+css+'</style><main>'+markdown.markdown(text,extensions=['tables'])+'</main></html>'
 # Local preview replaces language links with HTML equivalents. Markdown stays GitHub-native.
 for a,b in [('README.zh-CN.md','preview-zh.html'),('README.ko.md','preview-ko.html'),('README.md','preview.html')]:page=page.replace('href="'+a+'"','href="'+b+'"')
 (ROOT/({'en':'preview.html','zh':'preview-zh.html','ko':'preview-ko.html'}[lang])).write_text(page,encoding='utf-8')
print('Built 3 READMEs, 40-frame GIF and static PNG.')
print('GIF bytes:',(ASSETS/'tianhan-ascii.gif').stat().st_size)
