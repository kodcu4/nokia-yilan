import pygame, random, sys, traceback
import os

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snake_log.txt")
def log(msg):
    with open(LOG, "a") as f:
        f.write(str(msg) + "\n")

try:
    log("=== BASLADI ===")
    pygame.init()
    log("pygame.init OK")

    info = pygame.display.Info()
    EW = max(info.current_w if info.current_w > 0 else 1080, 400)
    EH = max(info.current_h if info.current_h > 0 else 2400, 700)
    log("Ekran: " + str(EW) + "x" + str(EH))

    COLS = 19; ROWS = 19
    CS   = int(EW * 0.95) // COLS
    GW   = CS * COLS; GH = CS * ROWS
    GX   = (EW - GW) // 2; GY = int(EH * 0.08)

    BS       = int(EW * 0.20)
    BTN_DIST = int(BS * 1.3)
    PCX      = EW // 2
    PCY      = GY + GH + int(EH * 0.20)
    CTRL_R   = int(EW * 0.07)
    CTRL_X   = EW - CTRL_R - 12
    CTRL_Y   = GY // 2

    C_BG   = (8,24,8);    C_CELL = (12,30,12);  C_WALL = (40,100,40)
    C_SH   = (56,135,56); C_SK   = (18,72,18)
    C_FD   = (200,50,50); C_FDP  = (230,90,90)
    C_BN   = (25,70,25);  C_BA   = (80,180,80);  C_BK  = (50,120,50)
    C_TXT  = (140,198,101); C_GOLD = (220,180,50); C_SILV = (160,200,160)
    C_RED  = (180,50,50); C_EN   = (70,148,70);  C_ENI  = (24,58,24)
    C_PINK = (255,105,180)

    FS = max(16, int(EW*.042)); FM = max(24, int(EW*.058))
    FL = max(32, int(EW*.085)); FA = max(38, int(EW*.100))
    log("Sabitler OK")

    MAPS = [
        [(1,1),(2,1),(3,1),(15,1),(16,1),(17,1),(1,17),(2,17),(3,17),(15,17),(16,17),(17,17)],
        [(7,3),(8,3),(9,3),(10,3),(11,3),(7,15),(8,15),(9,15),(10,15),(11,15),(1,8),(1,9),(1,10),(17,8),(17,9),(17,10)],
        [(9,3),(9,4),(9,5),(9,13),(9,14),(9,15),(3,9),(4,9),(5,9),(13,9),(14,9),(15,9),(1,1),(17,1),(1,17),(17,17)],
        [(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(3,12),(3,13),(3,14),(3,15),(3,16),(3,17),(15,12),(15,13),(15,14),(15,15),(15,16),(15,17),(6,9),(7,9),(8,9),(10,9),(11,9),(12,9)],
        [(2,3),(3,3),(4,3),(5,3),(7,6),(8,6),(9,6),(10,6),(12,9),(13,9),(14,9),(15,9),(7,12),(8,12),(9,12),(10,12),(2,15),(3,15),(4,15),(5,15),(14,3),(15,3),(16,3),(3,9),(4,9),(5,9)],
        [(9,2),(9,3),(9,4),(9,5),(9,6),(9,12),(9,13),(9,14),(9,15),(9,16),(2,9),(3,9),(4,9),(5,9),(6,9),(12,9),(13,9),(14,9),(15,9),(16,9),(2,2),(3,2),(2,3),(15,2),(16,2),(16,3),(2,15),(2,16),(3,16),(15,16),(16,16),(16,15),(5,5),(6,5),(5,6),(12,5),(13,5),(13,6),(5,12),(5,13),(6,13),(12,13),(13,13),(13,12)],
        [(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,11),(9,12),(9,13),(9,14),(9,15),(9,16),(9,17),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),(17,9),(5,5),(13,5),(5,13),(13,13)],
        [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(17,1),(16,2),(15,3),(14,4),(13,5),(12,6),(1,17),(2,16),(3,15),(4,14),(5,13),(6,12),(17,17),(16,16),(15,15),(14,14),(13,13),(12,12),(8,8),(9,8),(10,8),(8,10),(9,10),(10,10)],
        [(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,10),(3,11),(3,12),(3,13),(3,14),(3,15),(3,16),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,16),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,10),(12,11),(12,12),(12,13),(12,14),(12,15),(12,16),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),(15,10),(15,11),(15,12),(15,13),(15,14),(15,15),(15,16),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8)],
        [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(1,3),(2,3),(3,3),(4,3),(5,3),(7,3),(7,4),(7,5),(7,6),(7,7),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(17,3),(1,5),(1,6),(1,7),(1,8),(1,9),(3,5),(4,5),(5,5),(6,5),(9,5),(10,5),(11,5),(13,5),(13,6),(13,7),(13,8),(13,9),(15,5),(16,5),(17,5),(3,7),(4,7),(5,7),(9,7),(10,7),(11,7),(11,8),(11,9),(11,10),(11,11),(15,7),(16,7),(17,7),(1,11),(2,11),(3,11),(4,11),(5,11),(7,11),(8,11),(9,11),(13,11),(14,11),(15,11),(16,11),(17,11),(1,13),(1,14),(1,15),(1,16),(1,17),(3,13),(4,13),(5,13),(6,13),(7,13),(9,13),(10,13),(12,13),(13,13),(14,13),(15,13),(17,13),(17,14),(17,15),(17,16),(17,17),(3,15),(4,15),(5,15),(7,15),(8,15),(9,15),(10,15),(11,15),(12,15),(15,15),(16,15),(5,17),(6,17),(7,17),(8,17),(9,17),(10,17),(11,17),(12,17),(13,17)],
    ]
    LV_SPD = [160,145,145,130,130,115,115,105,95,85]

    BTN_POS = {
        "yukari": (PCX,            PCY - BTN_DIST),
        "asagi":  (PCX,            PCY + BTN_DIST),
        "sol":    (PCX - BTN_DIST, PCY),
        "sag":    (PCX + BTN_DIST, PCY),
    }

    def gp(ev):
        if ev.type in (pygame.FINGERDOWN, pygame.FINGERMOTION, pygame.FINGERUP):
            return (int(ev.x * EW), int(ev.y * EH))
        return ev.pos

    def mk_tile(fn):
        s = pygame.Surface((CS, CS)); fn(s); return s

    def t_wall(s):
        s.fill(C_CELL); br = max(2, CS//5)
        pygame.draw.rect(s, C_EN,  (1,1,CS-2,CS-2), border_radius=br)
        pygame.draw.rect(s, C_ENI, (4,4,CS-8,CS-8), border_radius=br)
        pygame.draw.line(s, (100,200,100), (3,3), (CS-5,3), 2)
        pygame.draw.line(s, (100,200,100), (3,3), (3,CS-5), 2)

    def t_empty(s): s.fill(C_CELL)

    def t_snake(s, head=False):
        s.fill(C_CELL); br = max(3, CS//4)
        pygame.draw.rect(s, C_SK, (1,1,CS-2,CS-2), border_radius=br+1)
        pygame.draw.rect(s, C_SH, (3,3,CS-6,CS-6), border_radius=br)
        if head:
            g = max(2, CS//8)
            pygame.draw.circle(s, (0,0,0), (g+3,g+3), g)
            pygame.draw.circle(s, (0,0,0), (CS-g-3,g+3), g)

    def t_food(s):
        s.fill(C_CELL); mx, my = CS//2, CS//2
        pygame.draw.circle(s, C_FD,  (mx,my), CS//2-1)
        pygame.draw.circle(s, C_FDP, (mx-max(1,CS//8), my-max(1,CS//8)), max(2,CS//6))

    def mk_bg(walls):
        TW = mk_tile(t_wall); TE = mk_tile(t_empty)
        s = pygame.Surface((EW, EH)); s.fill(C_BG)
        for cy in range(ROWS):
            for cx in range(COLS):
                s.blit(TW if (cx,cy) in walls else TE, (GX+cx*CS, GY+cy*CS))
        pygame.draw.rect(s, C_WALL, (GX-3,GY-3,GW+6,GH+6), 4)
        return s

    def mk_dpad(fa, act=None):
        s = pygame.Surface((EW,EH)); s.fill((1,2,3)); s.set_colorkey((1,2,3))
        half = BS//2; br = max(8, BS//6)
        sym = {"yukari":"^", "asagi":"v", "sol":"<", "sag":">"}
        for nm,(bx,by) in BTN_POS.items():
            col = C_BA if nm==act else C_BN
            pygame.draw.rect(s, (6,20,6),  (bx-half+5, by-half+5, BS, BS), border_radius=br)
            pygame.draw.rect(s, col,        (bx-half,   by-half,   BS, BS), border_radius=br)
            pygame.draw.rect(s, C_BK,       (bx-half,   by-half,   BS, BS), border_radius=br, width=4)
            t = fa.render(sym[nm], True, C_TXT)
            s.blit(t, t.get_rect(center=(bx,by)))
        return s

    def mk_ctrl(fm, paused):
        s = pygame.Surface((EW,EH)); s.fill((1,2,3)); s.set_colorkey((1,2,3))
        col = C_RED if paused else (30,80,30)
        pygame.draw.circle(s, col,   (CTRL_X, CTRL_Y), CTRL_R)
        pygame.draw.circle(s, C_TXT, (CTRL_X, CTRL_Y), CTRL_R, 2)
        t = fm.render(">" if paused else "||", True, C_TXT)
        s.blit(t, t.get_rect(center=(CTRL_X, CTRL_Y)))
        return s

    def hit_btn(pos):
        px,py = pos; best = None; bd = float('inf')
        z = int(BS * 0.58)
        for nm,(bx,by) in BTN_POS.items():
            if abs(px-bx) <= z and abs(py-by) <= z:
                d = (px-bx)**2 + (py-by)**2
                if d < bd: bd = d; best = nm
        return best

    def hit_ctrl(pos):
        px,py = pos
        return (px-CTRL_X)**2 + (py-CTRL_Y)**2 <= (CTRL_R*1.4)**2

    def spawn_food(sset, walls):
        while True:
            p = (random.randint(0,COLS-1), random.randint(0,ROWS-1))
            if p not in walls and p not in sset: return p

    def safe_start(walls):
        for bx,by in [(9,9),(5,5),(13,13),(5,13),(13,5),(3,3),(15,3),(3,15)]:
            b = [(bx-i,by) for i in range(4)]
            if not any(p in walls or p[0]<0 or p[0]>=COLS for p in b): return b
        for _ in range(3000):
            x,y = random.randint(3,COLS-5), random.randint(2,ROWS-3)
            b = [(x-i,y) for i in range(4)]
            if not any(p in walls or p[0]<0 for p in b): return b
        return [(9,9),(8,9),(7,9),(6,9)]

    def init_lv(lv):
        walls = frozenset(MAPS[lv])
        snake = safe_start(walls)
        food  = spawn_food(frozenset(map(tuple,snake)), walls)
        return snake, food, (1,0), walls

    log("Fonksiyonlar OK")

    screen = pygame.display.set_mode((EW, EH))
    log("display OK")
    pygame.display.set_caption("Nokia Yilan")
    clock = pygame.time.Clock()

    try:
        fs = pygame.font.SysFont("monospace", FS)
        fm = pygame.font.SysFont("monospace", FM, bold=True)
        fl = pygame.font.SysFont("monospace", FL, bold=True)
        fa = pygame.font.SysFont("monospace", FA, bold=True)
    except:
        fs = pygame.font.Font(None, FS+8)
        fm = pygame.font.Font(None, FM+8)
        fl = pygame.font.Font(None, FL+8)
        fa = pygame.font.Font(None, FA+8)
    log("Fontlar OK")

    TW = mk_tile(t_wall); TE = mk_tile(t_empty)
    TB = mk_tile(lambda s: t_snake(s, False))
    TF = mk_tile(t_food)
    log("Tile'lar OK")

    LF = pygame.font.SysFont("monospace", max(11, int(CS*0.52)), bold=True)

    def mk_letter_tile(ch, head=False):
        t = mk_tile(lambda s: t_snake(s, head))
        lt = LF.render(ch.upper(), True, C_PINK)
        t.blit(lt, lt.get_rect(center=(CS//2, CS//2)))
        return t

    OPP = {(0,-1):(0,1),(0,1):(0,-1),(-1,0):(1,0),(1,0):(-1,0)}
    DM  = {"yukari":(0,-1),"asagi":(0,1),"sol":(-1,0),"sag":(1,0)}
    STEP = pygame.USEREVENT + 1
    TEXTINPUT_EV = getattr(pygame, 'TEXTINPUT', -1)

    # ── İsim giriş ekranı ──────────────────────────────────
    log("Isim ekrani basliyor")
    isim = ""
    cur = True; ctick = 0
    OK_W = int(EW*0.5); OK_H = int(EH*0.08)
    OK_X = (EW-OK_W)//2; OK_Y = int(EH*0.55)

    pygame.key.start_text_input()

    isim_tamam = False
    while not isim_tamam:
        ctick += 1
        if ctick % 28 == 0: cur = not cur

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_BACKSPACE:
                    isim = isim[:-1]
                elif ev.key == pygame.K_RETURN and isim:
                    isim_tamam = True
            if ev.type == TEXTINPUT_EV and TEXTINPUT_EV != -1:
                for ch in ev.text:
                    if ch.isalpha() and len(isim) < 12:
                        isim += ch.upper()
            if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                px,py = gp(ev)
                if OK_X <= px <= OK_X+OK_W and OK_Y <= py <= OK_Y+OK_H and isim:
                    isim_tamam = True

        screen.fill(C_BG)
        t = fl.render("ADINI GIR", True, C_GOLD)
        screen.blit(t, t.get_rect(midtop=(EW//2, int(EH*0.07))))
        t2 = fm.render("Telefon klavyesiyle yaz", True, C_TXT)
        screen.blit(t2, t2.get_rect(midtop=(EW//2, int(EH*0.16))))
        t3 = fs.render("Yilanin uzerine yazilacak (max 12)", True, C_SILV)
        screen.blit(t3, t3.get_rect(midtop=(EW//2, int(EH*0.22))))

        bx2 = int(EW*.06); bw2 = int(EW*.88)
        by2 = int(EH*.30); bh2 = int(EH*.10)
        pygame.draw.rect(screen, (18,48,18), (bx2,by2,bw2,bh2), border_radius=14)
        pygame.draw.rect(screen, C_WALL,    (bx2,by2,bw2,bh2), border_radius=14, width=3)
        disp = isim + ("_" if cur else " ")
        it = fl.render(disp, True, C_PINK)
        screen.blit(it, it.get_rect(midleft=(bx2+20, by2+bh2//2)))
        ct = fs.render(str(len(isim))+"/12", True, C_SILV)
        screen.blit(ct, ct.get_rect(topright=(bx2+bw2-10, by2+bh2+6)))

        okcol = (35,100,35) if isim else (20,45,20)
        pygame.draw.rect(screen, okcol,  (OK_X,OK_Y,OK_W,OK_H), border_radius=14)
        pygame.draw.rect(screen, C_WALL, (OK_X,OK_Y,OK_W,OK_H), border_radius=14, width=3)
        ot = fm.render("TAMAM  >>", True, C_GOLD if isim else C_SILV)
        screen.blit(ot, ot.get_rect(center=(OK_X+OK_W//2, OK_Y+OK_H//2)))
        tip = fs.render("Klavye acilmazsa kutuya dokun", True, (80,130,80))
        screen.blit(tip, tip.get_rect(midtop=(EW//2, OK_Y+OK_H+12)))

        pygame.display.flip()
        clock.tick(60)

    pygame.key.stop_text_input()
    if not isim: isim = "OYUNCU"
    log("Isim: " + isim)

    # ── Oyun ───────────────────────────────────────────────
    def build_tiles(name, n):
        tiles = []
        for i in range(n):
            ch = name[i % len(name)]
            tiles.append(mk_letter_tile(ch, head=(i==0)))
        return tiles

    score  = 0
    eaten  = 0
    lv     = 0
    dead   = False
    won    = False
    transit= False
    waiting= True
    paused = False
    snake, food, direction, walls = init_lv(0)
    ntiles = build_tiles(isim, len(snake))
    nidx   = len(snake)
    bg     = mk_bg(walls)
    dpad_s = mk_dpad(fa, None)
    ctrl_s = mk_ctrl(fm, False)
    act    = None; pact = None
    pygame.time.set_timer(STEP, LV_SPD[0])
    log("Oyun dongusu basliyor")

    while True:
        act = None; do_step = False

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == STEP: do_step = True

            if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = gp(ev)
                if dead or won:
                    baslangic_lv = 0 if won else lv
                    score=0; eaten=0; lv=baslangic_lv; dead=False; won=False
                    transit=False; waiting=True; paused=False
                    snake,food,direction,walls = init_lv(lv)
                    ntiles=build_tiles(isim,len(snake)); nidx=len(snake)
                    bg=mk_bg(walls); dpad_s=mk_dpad(fa,None); ctrl_s=mk_ctrl(fm,False)
                    act=None; pact=None
                    pygame.time.set_timer(STEP,LV_SPD[0])
                    continue
                if transit:
                    snake,food,direction,walls = init_lv(lv)
                    ntiles=build_tiles(isim,len(snake)); nidx=len(snake)
                    bg=mk_bg(walls)
                    pygame.time.set_timer(STEP,LV_SPD[lv])
                    transit=False; waiting=True; continue
                if hit_ctrl(pos):
                    if not waiting:
                        paused = not paused
                        ctrl_s = mk_ctrl(fm, paused)
                    continue
                b = hit_btn(pos)
                if b:
                    nd = DM[b]
                    if nd != OPP.get(direction): direction = nd
                    waiting=False; paused=False
                    ctrl_s=mk_ctrl(fm,False); act=b

            if ev.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                if not dead and not won and not transit and not waiting and not paused:
                    pos = gp(ev)
                    b = hit_btn(pos)
                    if b:
                        nd = DM[b]
                        if nd != OPP.get(direction): direction = nd
                        act = b

            if ev.type == pygame.KEYDOWN and not dead and not transit:
                k = ev.key
                if k == pygame.K_SPACE and not waiting:
                    paused = not paused; ctrl_s = mk_ctrl(fm, paused)
                nd = None
                if k == pygame.K_UP:    nd = (0,-1)
                if k == pygame.K_DOWN:  nd = (0, 1)
                if k == pygame.K_LEFT:  nd = (-1,0)
                if k == pygame.K_RIGHT: nd = (1, 0)
                if nd and nd != OPP.get(direction):
                    direction=nd; waiting=False; paused=False; ctrl_s=mk_ctrl(fm,False)

        if do_step and not dead and not won and not transit and not waiting and not paused:
            hx,hy = snake[0]
            nx = (hx + direction[0]) % COLS
            ny = (hy + direction[1]) % ROWS
            head = (nx, ny)
            if head in walls:
                dead = True
            else:
                body = set(map(tuple, snake[:-1]))
                if head in body:
                    dead = True
                else:
                    snake.insert(0, head)
                    ch = isim[nidx % len(isim)]
                    ntiles.insert(0, mk_letter_tile(ch, True))
                    if len(ntiles) > 1:
                        ch2 = isim[(nidx-1) % len(isim)]
                        ntiles[1] = mk_letter_tile(ch2, False)
                    nidx += 1
                    if head == food:
                        score += 10 + lv*5; eaten += 1
                        food = spawn_food(frozenset(map(tuple,snake)), walls)
                        if eaten % 5 == 0:
                            if lv < 9:
                                lv += 1; transit = True
                                pygame.time.set_timer(STEP, LV_SPD[lv])
                            else:
                                won = True
                    else:
                        snake.pop()
                        if ntiles: ntiles.pop()

        if act != pact:
            dpad_s = mk_dpad(fa, act); pact = act

        screen.blit(bg, (0,0))
        screen.blit(TF, (GX+food[0]*CS, GY+food[1]*CS))
        for i,(cx,cy) in enumerate(snake):
            screen.blit(ntiles[i] if i < len(ntiles) else TB, (GX+cx*CS, GY+cy*CS))

        pygame.draw.rect(screen, C_BG, (0,0,EW,GY-3))
        screen.blit(fm.render("SKOR:" + str(score), True, C_TXT), (6, int(GY*.18)))
        lv_t = fm.render("LV" + str(lv+1) + "/10", True, C_GOLD)
        screen.blit(lv_t, lv_t.get_rect(midtop=(EW//2, int(GY*.18))))
        pr_t = fm.render(str(eaten%5) + "/5", True, C_SILV)
        screen.blit(pr_t, pr_t.get_rect(topright=(EW-CTRL_R*2-18, int(GY*.18))))
        bw = int(EW*.44); bx_ = (EW-bw)//2; by_ = int(GY*.80); bh = max(5, int(GY*.12))
        pygame.draw.rect(screen, (25,55,25), (bx_,by_,bw,bh), border_radius=3)
        d = int(bw * (eaten%5) / 5)
        if d > 0: pygame.draw.rect(screen, C_GOLD, (bx_,by_,d,bh), border_radius=3)
        screen.blit(ctrl_s, (0,0))
        screen.blit(dpad_s, (0,0))

        if waiting and not transit and not dead and not won:
            t = fm.render("Yon sec, basla!", True, C_GOLD)
            screen.blit(t, t.get_rect(center=(EW//2, GY+GH//2)))

        if paused:
            pr = pygame.Rect(EW//4, EH//3, EW//2, EH//7)
            pygame.draw.rect(screen, (5,15,5), pr, border_radius=14)
            pygame.draw.rect(screen, C_WALL,   pr, border_radius=14, width=3)
            t = fl.render("DURAKLATILDI", True, C_GOLD)
            screen.blit(t, t.get_rect(center=pr.center))

        def overlay(rows):
            ow = int(EW*.55); oh = int(GH*.52)
            ox = (EW-ow)//2;  oy = GY + int(GH*.24)
            pygame.draw.rect(screen, (4,14,4), (ox,oy,ow,oh), border_radius=14)
            pygame.draw.rect(screen, C_WALL,   (ox,oy,ow,oh), border_radius=14, width=3)
            cy_ = oy + oh//2
            for txt,dy,f,col in rows:
                t = f.render(txt, True, col)
                screen.blit(t, t.get_rect(center=(EW//2, cy_+dy)))

        if transit:
            overlay([("LEVEL TAM!",    -50, fl, C_GOLD),
                     ("LV"+str(lv+1)+" BASLIYOR", 10, fm, C_TXT),
                     ("Dokun...",        58, fm, (100,160,100))])
        if dead:
            overlay([("GAME OVER",     -60, fl, (210,60,60)),
                     ("LV "+str(lv+1), -10, fm, C_TXT),
                     ("SKOR:"+str(score), 38, fl, C_GOLD),
                     ("Dokun",           88, fm, (100,160,100))])
        if won:
            overlay([("TEBRIKLER!",     -70, fl, C_GOLD),
                     ("TUM LEVEL",      -18, fm, C_TXT),
                     ("BITTI!",          25, fm, C_TXT),
                     ("SKOR:"+str(score),72, fl, C_GOLD),
                     ("Dokun",          115, fm, (100,160,100))])

        nm_t = fs.render("Ad: " + isim, True, C_PINK)
        scre
