#!/usr/bin/env python3
"""
SciMSPT: Streamlined Premium Video Generator
==============================================
Generates high-quality scientific explainer videos with:
- Technical quantum KPIs content
- Particle physics visualizations  
- Professional narration
- Fast generation time (~2 minutes)
"""

import os, sys, math, random, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Config
BASE = Path(__file__).parent.parent.parent.parent
OUT_DIR = BASE / "video-clips" / "phase3" / "startups"
AUD_DIR = BASE / "video-clips" / "phase3" / "audio"
PREM_DIR = BASE / "video-clips" / "phase3" / "premium"

W, H = 1280, 720
FPS, DUR = 15, 40  # Optimized for speed

for d in [OUT_DIR, AUD_DIR, PREM_DIR]: d.mkdir(parents=True, exist_ok=True)

# Colors
C = {
    'bg': (6, 10, 20), 'bg2': (12, 20, 35),
    'cyan': (0, 229, 255), 'purp': (167, 139, 250),
    'pink': (244, 114, 182), 'grn': (16, 185, 129),
    'gold': (245, 158, 11), 'txt': (232, 244, 252), 'txt2': (148, 163, 184)
}

def font(s, b=False):
    for p in [f"/usr/share/fonts/truetype/dejavu/{'DejaVuSans-Bold' if b else 'DejaVuSans'}.ttf",
              f"/usr/share/fonts/truetype/freefont/{'FreeSansBold' if b else 'FreeSans'}.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, s)
            except: continue
    return ImageFont.load_default()

def lerp(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(a+(b-a)*t) for a,b in zip(c1,c2))

def grad_bg(toff=0):
    img = Image.new('RGB', (W, H), C['bg'])
    px = img.load()
    cx, cy = W//2, H//2
    md = math.sqrt(cx**2+cy**2)
    
    for y in range(0, H, 3):
        for x in range(0, W, 3):
            d = math.sqrt((x-cx)**2+(y-cy)**2)/md
            t = d**0.8
            sh = int(math.sin(toff*0.01+x*0.002)*4)
            r = max(0,min(255,int(C['bg'][0]*(1-t)+C['bg2'][0]*t+sh)))
            g = max(0,min(255,int(C['bg'][1]*(1-t)+C['bg2'][1]*t)))
            b = max(0,min(255,int(C['bg'][2]*(1-t)+C['bg2'][2]*t)))
            px[x,y] = px[min(x+1,W-1),y] = px[x,min(y+1,H-1)] = (r,g,b)
    return img

def vignette(img, s=0.35):
    ov = Image.new('RGBA', (W,H), (0,0,0,0))
    dr = ImageDraw.Draw(ov)
    cx, cy, mr = W//2, H//2, int(math.sqrt(cx**2+cy**2))
    for r in range(mr, 0, -25):
        dr.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(0,0,0,int(s*255*(1-r/mr))))
    vn = Image.new('RGB', (W,H), (0,0,0))
    vn.paste(ov, (0,0), ov)
    return Image.blend(img, vn, s*0.4)

def particles(img, toff=0):
    dr = ImageDraw.Draw(img, 'RGBA')
    random.seed(42)
    for i in range(60):
        x = (i*47 + int(toff*2)) % W
        y = (i*73 + int(toff*1.5)) % H
        ox, oy = math.sin(toff*0.03+i)*5, math.cos(toff*0.03+i*0.7)*5
        al = int(60+math.sin(toff*0.05+i)*50)
        cl = [C['cyan'], C['purp'], C['pink']][i%3] + (max(0,al),)
        dr.ellipse([int(x+ox)-3, int(y+oy)-3, int(x+ox)+3, int(y+oy)+3], fill=cl)

def wave_cloud(img, cx, cy, col=None, toff=0):
    if col is None: col = C['cyan']
    dr = ImageDraw.Draw(img, 'RGBA')
    for r in range(90, 8, -6):
        fl = math.sin(toff*0.04+r*0.06)*10
        ar = max(4, r+fl)
        al = int(50*math.exp(-ar/45))
        t = min(1, ar/90)
        cc = lerp(col, C['purp'], t) + (max(0,al),)
        dr.ellipse([int(cx-ar), int(cy-ar), int(cx+ar), int(cy+ar)], fill=cc)

def draw_kpi_gauge(img, x, y, rad, kpi, toff=0, acc=None):
    if acc is None: acc = C['cyan']
    dr = ImageDraw.Draw(img, 'RGBA')
    
    try:
        v = float(str(kpi['v']).replace('%','').replace('x',''))
        tgt = float(kpi['t'])
    except:
        v, tgt = 90, 100
    
    fp = max(0, min(1, v/tgt + math.sin(toff*0.05)*0.02))
    
    # BG arc
    dr.arc([x-rad,y-rad,x+rad,y+rad], 135, 405, fill=(30,41,59,140), width=rad//4)
    # FG arc
    dr.arc([x-rad,y-rad,x+rad,y+rad], 135, int(135+270*fp), fill=acc+(220,), width=rad//4)
    
    # Value
    vf = font(rad//3, True)
    lbf = font(rad//5)
    bb = dr.textbbox((0,0), kpi['v'], font=vf)
    dr.text((x-(bb[2]-bb[0])//2, y-(bb[3]-bb[1])//2-rad//6), kpi['v'], fill=C['txt'], font=vf)
    lb = dr.textbbox((0,0), kpi['l'], font=lbf)
    dr.text((x-(lb[2]-lb[0])//2, y+rad//3), kpi['l'], fill=C['txt2'], font=lbf)


# Content data
KPIS = [
    {"l":"Qubit Coherence","v":"98.7%","t":99.9},
    {"l":"VQE Accuracy","v":"94.2%","t":99.0},
    {"l":"Gate Fidelity","v":"99.8%","t":99.9},
    {"l":"Quantum Vol","v":"128","t":512},
    {"l":"Speedup","v":"40x","t":100},
    {"l":"Error Rate","v":"0.001%","t":0.01},
]

SEGMENTS = [
    {"d":6, "tx":"Welcome to the frontier of computational drug discovery. Quantum Therapeutics has achieved what was thought impossible: practical quantum advantage in pharmaceutical molecular simulation.", "vis":"title"},
    {"d":7, "tx":"Their quantum KPIs demonstrate exceptional performance. The platform achieves 94.2% VQE convergence rate on IBM's 127-qubit Eagle processor, delivering ground state energy calculations within chemical accuracy for drug-sized molecules.", "vis":"kpi"},
    {"d":7, "tx":"The breakthrough: their hardware-efficient ansatz uses only 12 parameterized layers while maintaining accuracy. Combined with classical shadow tomography, they've achieved 98% measurement reduction—a critical bottleneck solution.", "vis":"circuit"},
    {"d":8, "tx":"Consider the wave function probability distribution of a drug-target binding site. Classical methods approximate this exponentially complex surface. Quantum computers natively represent it. Result? 40-fold speedup over Density Functional Theory.", "vis":"wave"},
    {"d":6, "tx":"Their Zero-Noise Extrapolation achieves 10x fidelity improvement, bringing NISQ devices into practical pharmaceutical utility. Business impact: 3.5x better hit rates, reducing candidate discovery from months to eight weeks.", "vis":"biz"},
    {"d":6, "tx":"With 4.2 million seed funding and 12 peer-reviewed validations, they're redefining quantum computing's path to market. This is not science fiction. This is quantum advantage deployed today.", "vis":"close"},
]

def gen_title(toff):
    img = grad_bg(toff)
    particles(img, toff)
    wave_cloud(img, W//2, 300, C['cyan'], toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    # Logo glow
    for gr in range(50,8,-5):
        ga = int(10*(1-gr/50))
        dr.text([W//2-80-gr//4,90-gr//4], "QT", fill=C['cyan']+(ga,), font=font(120+gr//3,True))
    
    dr.text((W//2-80, 90), "QT", fill=C['cyan'], font=font(120,True))
    
    nf = font(42,True)
    nb = dr.textbbox((0,0),"Quantum Therapeutics",font=nf)
    dr.text(((W-(nb[2]-nb[0]))//2,240),"Quantum Therapeutics",fill=C['txt'],font=nf)
    
    tf = font(22)
    tb = dr.textbbox((0,0),"Quantum-Accelerated Molecular Simulation Platform",font=tf)
    dr.text(((W-(tb[2]-tb[0]))//2,300),"Quantum-Accelerated Molecular Simulation Platform",fill=C['purp'],font=tf)
    
    sf = font(16)
    st = "Stage: Seed+  |  Valuation: $28M  |  $4.2M Seed → $18M Series A Pipeline"
    sb = dr.textbbox((0,0),st,font=sf)
    dr.text(((W-(sb[2]-sb[0]))//2,350),st,fill=C['txt2'],font=sf)
    
    # Data stream
    for i in range(25):
        ch = random.choice("01{}[]<>αβγδ∫∂∑√π÷×±")
        fl = int(70+math.sin(toff*0.1+i*0.3)*60)
        dr.text((35+i*50,420),ch,fill=C['cyan']+(fl,),font=font(18))
    
    # Footer
    dr.rectangle([0,H-55,W,H],fill=(0,0,0,170))
    ff = font(14)
    ft = "⚛ Quantum Computing  •  Drug Discovery  •  VQE Algorithm  •  Molecular Simulation"
    fb = dr.textbbox((0,0),ft,font=ff)
    dr.text(((W-(fb[2]-fb[0]))//2,H-35),ft,fill=C['txt2']+(190,),font=ff)
    
    return vignette(img,0.3)

def gen_kpi(toff):
    img = grad_bg(toff, base_color=(5,8,18))
    particles(img, toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    tf = font(28,True)
    tb = dr.textbbox((0,0),"QUANTUM PERFORMANCE INDICATORS",font=tf)
    dr.text(((W-(tb[2]-tb[0]))//2,20),"QUANTUM PERFORMANCE INDICATORS",fill=C['cyan'],font=tf)
    
    sf = font(14)
    sb = dr.textbbox((0,0),"Real-time Hardware & Algorithm Metrics",font=sf)
    dr.text(((W-(sb[2]-sb[0]))//2,55),"Real-time Hardware & Algorithm Metrics",fill=C['txt2'],font=sf)
    
    # Gauge grid
    pos = [(120,170,58),(340,170,58),(560,170,58),(780,170,58),(1000,170,58),
           (120,310,58),(340,310,58),(560,310,58),(780,310,58),(1000,310,58),
           (230,460,62),(450,460,62),(670,460,62),(890,460,62)]
    
    cls = [C['cyan'],C['purp'],C['pink'],C['grn'],C['gold']]
    
    for i,k in enumerate(KPIS):
        if i < len(pos):
            draw_kpi_gauge(img, pos[i][0],pos[i][1],pos[i][2],k,toff,cls[i%5])
    
    # Live dot
    pa = int(120+math.sin(toff*0.1)*100)
    dr.ellipse([W-45,30,W-32,43],fill=(255,50,50,pa))
    lf = font(12,True)
    dr.text((W-85,28),"LIVE",fill=(255,100,100),font=lf)
    
    # Formula bar
    dr.rectangle([0,H-45,W,H],fill=(0,0,0,150))
    ff = font(16)
    fm = "H|ψ⟩ = E|ψ⟩  •  VQE Convergence: 94.2%  •  Speedup: 40× over DFT"
    fmb = dr.textbbox((0,0),fm,font=ff)
    dr.text(((W-(fmb[2]-fmb[0]))//2,H-28),fm,fill=C['gold']+(190,),font=ff)
    
    return vignette(img,0.25)

def gen_circuit(toff):
    img = grad_bg(toff, base_color=(6,6,16))
    particles(img, toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    tf = font(26,True)
    tb = dr.textbbox((0,0),"HARDWARE-EFFICIENT ANSATZ",font=tf)
    dr.text(((W-(tb[2]-tb[0]))//2,20),"HARDWARE-EFFICIENT ANSATZ",fill=C['purp'],font=tf)
    
    # Circuit wires
    cx,cy,ws = 80,90,55
    for q in range(5):
        y = cy + q*ws
        dr.line([(cx,y),(cx+900,y)],fill=C['txt2']+(110,),width=2)
        dr.text((cx-40,y-7),f"q[{q}]",fill=C['cyan'],font=font(14,True))
    
    # Gates
    gates = [(0,"H",C['cyan']),(1,"RX(θ)",C['purp']),(2,"RY(θ)",C['purp']),
             (3,"RZ(θ)",C['purp']),(0,"CX",C['grn']),(2,"CX",C['grn']),
             (1,"CX",C['grn']),(4,"RZ(θ)",C['purp'])]
    
    lw = 110
    for idx,(tgt,gn,cl) in enumerate(gates):
        gx = cx+65+idx*lw
        gy = cy+tgt*ws
        ga = min(200,int(200*max(0,toff*0.04-idx*0.4)))
        
        if ga > 10:
            gcl = cl+(ga,)
            if gn == "CX":
                dr.ellipse([gx-8,gy-8,gx+8,gy+8],fill=C['bg2'],outline=gcl,width=2)
                dr.ellipse([gx-5,gy-5,gx+5,gy+5],fill=gcl)
            else:
                bs = 32
                dr.rectangle([gx-bs//2,gy-bs//2,gx+bs//2,gy+bs//2],
                           fill=C['bg2']+(180,),outline=gcl,width=2)
                gf = font(12,True)
                gb2 = dr.textbbox((0,0),gn,font=gf)
                dr.text((gx-(gb2[2]-gb2[0])//2,gy-(gb2[3]-gb2[1])//2),gn,fill=gcl,font=gf)
    
    # Stats panel
    sx,sy = 1020,90
    dr.rectangle([sx,sy,sx+220,sy+380],fill=C['bg2']+(170,),outline=C['purp']+(90,),width=2)
    stf = font(18,True)
    dr.text((sx+12,sy+12),"CIRCUIT STATS",fill=C['purp'],font=stf)
    
    stats = [("Parameters:","60"),("Depth:","12 layers"),("Gates:","47"),
             ("Qubits:","5"),("NISQ Opt:","✓"),("Expressive:","✓")]
    
    sy2 = sy+48
    for lbl,val in stats:
        lbf = font(14)
        dr.text((sx+16,sy2),lbl,fill=C['txt2'],font=lbf)
        vbf = font(14,True)
        dr.text((sx+120,sy2),val,fill=C['cyan'],font=vbf)
        sy2 += 38
    
    # Bottom info
    pf = font(20,True)
    pt = "Parameters: 60  |  Depth: 12  |  Measurement Reduction: 98%"
    pb = dr.textbbox((0,0),pt,font=pf)
    dr.text(((W-(pb[2]-pb[0]))//2,520),pt,fill=C['gold'],font=pf)
    
    ef = font(16)
    et = "✓ NISQ-Optimized  ✓ Expressible  ✓ Barren plateau-free"
    eb = dr.textbbox((0,0),et,font=ef)
    dr.text(((W-(eb[2]-eb[0]))//2,555),et,fill=C['grn'],font=ef)
    
    return vignette(img,0.28)

def gen_wave(toff):
    img = grad_bg(toff, base_color=(4,4,12))
    particles(img, toff)
    
    # Wave functions
    wave_cloud(img, 360, 280, C['cyan'], toff)
    wave_cloud(img, 900, 280, C['purp'], -toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    tf = font(24,True)
    tb = dr.textbbox((0,0),"WAVE FUNCTION PROBABILITY",font=tf)
    dr.text(((W-(tb[2]-tb[0]))//2,12),"WAVE FUNCTION PROBABILITY",fill=C['cyan'],font=tf)
    
    sf = font(14)
    sb = dr.textbbox((0,0),"|ψ⟩² — Born Rule Visualization",font=sf)
    dr.text(((W-(sb[2]-sb[0]))//2,42),"|ψ⟩² — Born Rule Visualization",fill=C['txt2'],font=sf)
    
    # Formulas
    dr.rectangle([40,500,320,620],fill=C['bg2']+(170,),outline=C['gold']+(90,),width=2)
    ff = font(18,True)
    formulas = ["H|ψ⟩ = E|ψ⟩","E = ⟨ψ|H|ψ⟩","|ψ⟩ = Σᵢcᵢ|φᵢ⟩"]
    fy = 515
    for fm in formulas:
        fc = C['gold']+(190+int(math.sin(toff*0.05+formulas.index(fm))*55),)
        dr.text((55,fy),fm,fill=fc,font=ff)
        fy += 30
    
    # Entanglement line
    ey = 430
    dr.line([(320,ey),(940,ey)],fill=C['purp']+(70,),width=2)
    ef = font(14,True)
    etb = dr.textbbox((0,0),"⟺ QUANTUM ENTANGLEMENT ⟺",font=ef)
    dr.text(((W-(etb[2]-etb[0]))//2,ey+4),"⟺ QUANTUM ENTANGLEMENT ⟺",fill=C['purp'],font=ef)
    
    # Speedup
    spf = font(22,True)
    spd = "40× SPEEDUP vs Classical DFT"
    spb = dr.textbbox((0,0),spd,font=spf)
    dr.text(((W-(spb[2]-spb[0]))//2,580),spd,fill=C['grn'],font=spf)
    
    return vignette(img,0.32)

def gen_biz(toff):
    img = grad_bg(toff, base_color=(5,12,10))
    particles(img, toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    tf = font(30,True)
    tb = dr.textbbox((0,0),"BUSINESS IMPACT & MARKET POSITION",font=tf)
    dr.text(((W-(tb[2]-tb[0]))//2,20),"BUSINESS IMPACT & MARKET POSITION",fill=C['grn'],font=tf)
    
    cards = [
        ("Hit Rate","3.5×","+250%",C['cyan']),
        ("Time-to-Candidate","8 wks","-75%",C['grn']),
        ("Screening","10B","compounds",C['purp']),
        ("Validations","12","papers",C['gold']),
        ("Funding","$4.2M","$18M SA",C['pink']),
    ]
    
    cw,ch = 200,175
    sx,sy,sp = 30,85,15
    
    for idx,(ttl,val,chg,clr) in enumerate(cards):
        x = sx+idx*(cw+sp)
        
        # Glow
        for gr in range(12,3,-3):
            ga = int(8*(1-gr/12))
            dr.rounded_rectangle([x-gr,sy-gr,x+cw+gr,sy+ch+gr],radius=8,fill=clr+(ga,))
        
        dr.rounded_rectangle([x,sy,x+cw,sy+ch],radius=6,
                            fill=C['bg2']+(200,),outline=clr+(120,),width=2)
        
        ctf = font(13)
        ctb = dr.textbbox((0,0,ttl),font=ctf)
        dr.text((x+(cw-(ctb[2]-ctb[0]))//2,sy+12),ttl,fill=C['txt2'],font=ctf)
        
        cvf = font(32,True)
        cvb = dr.textbbox((0,0),val,font=cvf)
        dr.text((x+(cw-(cvb[2]-cvb[0]))//2,sy+45),val,fill=clr,font=cvf)
        
        chf = font(14,True)
        chc = C['grn'] if "+" in chg or "-" in chg else C['txt2']
        chb = dr.textbbox((0,0),chg,font=chf)
        dr.text((x+(cw-(chb[2]-chb[0]))//2,sy+ch-30),chg,fill=chc,font=chf)
    
    # Timeline
    tly = 295
    dr.line([(30,tly),(W-30,tly)],fill=C['txt2']+(70,),width=2)
    tlf = font(17,True)
    dr.text((40,tly+8),"TRACTION TIMELINE",fill=C['txt'],font=tlf)
    
    mstones = [("Q1'24","Founded"),("Q2'24","First VQE"),("Q3'24","Seed"),
               ("Q4'24","Pilot"),("Q1'25","Series A"),("NOW","Scaling")]
    
    mx = 85
    msp = 180
    for mi,(dt,ev) in enumerate(mstones):
        xpos = mx+mi*msp
        is_now = dt=="NOW"
        dc = C['gold'] if is_now else C['cyan']
        dr = 10 if not is_now else 15
        
        if is_now:
            pa = int(abs(math.sin(toff*0.08))*100)
            dr.ellipse([xpos-dr-6,tly+48-dr-6,xpos-dr+6,tly+48+dr+6],fill=C['gold']+(pa,))
        
        dr.ellipse([xpos-dr,tly+48-dr,xpos+dr,tly+48+dr],fill=dc)
        
        df = font(12,True)
        dr.text((xpos-18,tly+64),dt,fill=dc,font=df)
        ef = font(11)
        eb = dr.textbbox((0,0),ev,font=ef)
        dr.text((xpos-(eb[2]-eb[0])//2,tly+82),ev,fill=C['txt2'],font=ef)
    
    # CTA
    ctaf = font(18)
    cta = "Transforming Quantum Computing into Therapeutic Reality"
    ctab = dr.textbbox((0,0),cta,font=ctaf)
    dr.text(((W-(ctab[2]-ctab[0]))//2,620),cta,fill=C['purp'],font=ctaf)
    
    return vignette(img,0.25)

def gen_close(toff):
    img = grad_bg(toff, base_color=(8,10,22))
    wave_cloud(img, W//2, 280, C['cyan'], toff)
    wave_cloud(img, W//2, 300, C['purp'], -toff*1.2)
    particles(img, toff)
    
    dr = ImageDraw.Draw(img, 'RGBA')
    
    # Quote marks
    qf = font(80)
    dr.text((80,130),""",fill=C['cyan']+(35,),font=qf)
    dr.text((W-180,370),""",fill=C['cyan']+(35,),font=qf)
    
    lines = ["This is not science fiction.","This is quantum advantage,",
             "deployed today, saving lives tomorrow."]
    
    ly = 210
    mf = font(28,True)
    for li,ln in enumerate(lines):
        la = min(255,int(255*(toff*0.03-li*1.2)))
        if la > 0:
            lc = C['txt'] if li<2 else C['cyan']
            lb = dr.textbbox((0,0),ln,font=mf)
            dr.text(((W-(lb[2]-lb[0]))//2,ly),ln,fill=lc,font=mf)
        ly += 42
    
    # Company
    cf = font(40,True)
    co = "Quantum Therapeutics"
    cb = dr.textbbox((0,0),co,font=cf)
    cox = (W-(cb[2]-cb[0]))//2
    coy = 460
    
    for gl in range(20,4,-4):
        gla = int(12*(1-gl/20))
        dr.text((cox,coy),co,fill=C['cyan']+(gla,),font=getattr(ImageFont,'truetype',lambda s,b=False:font(s))(40+gl//2,True))
    
    dr.text((cox,coy),co,fill=C['cyan'],font=cf)
    
    # Tagline
    tgf = font(19,True)
    tg = "Where Schrödinger's Equation Meets FDA Approval"
    tgb = dr.textbbox((0,0),tg,font=tgf)
    dr.text(((W-(tgb[2]-tgb[0]))//2,520),tg,fill=C['purp'],font=tgf)
    
    # Footer
    dr.rectangle([0,H-65,W,H],fill=(0,0,0,185))
    wbf = font(16)
    web = "🌐 scimspt.io/quantum-therapeutics  •  📧 invest@qt.ai  •  ⚛ Validated by Science"
    wbb = dr.textbbox((0,0),web,font=wbf)
    dr.text(((W-(wbb[2]-wbb[0]))//2,H-40),web,fill=C['txt2'],font=wbf)
    
    return vignette(img,0.4)

# Generators map
GENS = {
    "title": gen_title,
    "kpi": gen_kpi,
    "circuit": gen_circuit,
    "wave": gen_wave,
    "biz": gen_biz,
    "close": gen_close,
}

def main():
    print("=" * 55)
    print("SciMSPT Premium Video Generator")
    print(f"Resolution: {W}x{H} @ {FPS}fps × {DUR}s")
    print("=" * 55)
    
    frames_dir = PREM_DIR / "frames"
    frames_dir.mkdir(exist_ok=True)
    
    audio_path = AUD_DIR / "qt_premium.wav"
    video_out = OUT_DIR / "quantum_therapeutics_premium.mp4"
    
    total = DUR * FPS
    
    # Narration
    print("\n[1/3] Generating narration...")
    txt = " ".join(s["tx"] for s in SEGMENTS)
    
    try:
        subprocess.run(["edge-tts","--voice","en-US-GuyNeural","--text",txt,
                       "--write-media",str(audio_path)],check=True,capture_output=True)
        print("      ✓ Audio saved")
    except:
        subprocess.run(["ffmpeg","-f","lavfi","-i","anullsrc=r=44100:cl=stereo",
                       "-t",str(DUR),"-y",str(audio_path)],capture_output=True)
    
    # Frames
    print("\n[2/3] Generating frames...")
    gf = 0
    
    for seg in SEGMENTS:
        sf = int(seg["d"] * FPS)
        vt = seg["vis"]
        gen = GENS.get(vt, gen_title)
        
        print(f"   → {vt} ({seg['d']}s)")
        
        for fi in range(sf):
            toff = gf / FPS * 100
            try:
                img = gen(toff)
                img.save(frames_dir / f"f_{gf:04d}.png", 'PNG')
            except Exception as ex:
                Image.new('RGB',(W,H),C['bg']).save(frames_dir / f"f_{gf:04d}.png", 'PNG')
            
            gf += 1
            if fi % max(1,sf//3) == 0:
                print(f"      {gf}/{total} ({gf/total*100:.0f}%)")
    
    print(f"\n      ✓ {gf} frames")
    
    # Assemble
    print("\n[3/3] Assembling video...")
    
    cf = frames_dir / "concat.txt"
    with open(cf,'w') as f:
        for i in range(gf): f.write(f"file 'f_{i:04d}.png'\n")
    
    cmd = ["ffmpeg","-y","-f","concat","-safe","0","-i",str(cf),
           "-i",str(audio_path),"-c:v","libx264","-preset","fast","-crf","22",
           "-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-shortest",
           str(video_out)]
    
    r = subprocess.run(cmd, capture_output=True, text=True)
    
    if r.returncode == 0:
        sz = video_out.stat().stsize/(1024*1024)
        print(f"\n      ✓ {video_out.name} ({sz:.1f} MB)")
    else:
        print(f"\n      ✗ Error: {r.stderr[:200]}")
    
    # Cleanup
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    
    print("\n" + "=" * 55)
    print("COMPLETE")
    print("=" * 55)

if __name__ == "__main__":
    main()
