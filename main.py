from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
import random

COLS = 19
ROWS = 19
LV_SPD = [0.16, 0.145, 0.145, 0.13, 0.13, 0.115, 0.115, 0.105, 0.095, 0.085]

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

OPP = {(0,-1):(0,1),(0,-1):(0,1),(-1,0):(1,0),(1,0):(-1,0),(0,1):(0,-1)}

class OyunAlani(Widget):
    def __init__(self, isim, **kw):
        super().__init__(**kw)
        self.isim = isim if isim else "OYUNCU"
        self.lv = 0
        self.skor = 0
        self.yenen = 0
        self.bekliyor = True
        self.bitti = False
        self.kazandi = False
        self.gecis = False
        self.zamanlayici = None
        self.etiketler = []
        self.baslat()
        self.bind(size=self._ciz, pos=self._ciz)

    def baslat(self):
        walls = set(map(tuple, MAPS[self.lv]))
        self.duvarlar = frozenset(walls)
        self.yilan = self._guvenli_baslangic()
        self.yon = (1, 0)
        self.yem = self._yem_olustur()
        self.isim_idx = len(self.yilan)
        if self.zamanlayici:
            self.zamanlayici.cancel()
        self.zamanlayici = Clock.schedule_interval(self._adim, LV_SPD[self.lv])
        self._ciz()

    def _guvenli_baslangic(self):
        for bx, by in [(9,9),(5,5),(13,13),(5,13),(13,5),(3,3),(15,3),(3,15)]:
            b = [(bx-i, by) for i in range(4)]
            if not any(p in self.duvarlar or p[0]<0 or p[0]>=COLS for p in b):
                return b
        return [(9,9),(8,9),(7,9),(6,9)]

    def _yem_olustur(self):
        yset = set(map(tuple, self.yilan))
        while True:
            p = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
            if p not in self.duvarlar and p not in yset:
                return p

    def _cs(self):
        return min(self.width * 0.95 / COLS, self.height * 0.72 / ROWS)

    def _alan_x(self):
        return self.x + (self.width - self._cs() * COLS) / 2

    def _alan_y(self):
        return self.y + self.height * 0.25

    def _hucre(self, cx, cy):
        cs = self._cs()
        return self._alan_x() + cx * cs, self._alan_y() + cy * cs

    def _adim(self, dt):
        if self.bekliyor or self.bitti or self.kazandi or self.gecis:
            return
        hx, hy = self.yilan[0]
        nx = (hx + self.yon[0]) % COLS
        ny = (hy + self.yon[1]) % ROWS
        head = (nx, ny)
        if head in self.duvarlar or head in set(map(tuple, self.yilan[:-1])):
            self.bitti = True
        else:
            self.yilan.insert(0, head)
            self.isim_idx += 1
            if head == self.yem:
                self.skor += 10 + self.lv * 5
                self.yenen += 1
                self.yem = self._yem_olustur()
                if self.yenen % 5 == 0:
                    if self.lv < 9:
                        self.lv += 1
                        self.gecis = True
                        if self.zamanlayici:
                            self.zamanlayici.cancel()
                    else:
                        self.kazandi = True
            else:
                self.yilan.pop()
        self._ciz()

    def _ciz(self, *args):
        self.canvas.clear()
        for lbl in self.etiketler:
            self.remove_widget(lbl)
        self.etiketler = []

        cs = self._cs()
        ax = self._alan_x()
        ay = self._alan_y()

        with self.canvas:
            # Arka plan
            Color(0.03, 0.09, 0.03)
            Rectangle(pos=self.pos, size=self.size)

            # Hücreler
            for cy in range(ROWS):
                for cx in range(COLS):
                    if (cx, cy) in self.duvarlar:
                        Color(0.16, 0.39, 0.16)
                    else:
                        Color(0.05, 0.12, 0.05)
                    Rectangle(pos=(ax+cx*cs+1, ay+cy*cs+1), size=(cs-2, cs-2))

            # Çerçeve
            Color(0.16, 0.39, 0.16)
            Line(rectangle=(ax, ay, cs*COLS, cs*ROWS), width=2)

            # Yem
            Color(0.78, 0.20, 0.20)
            ex, ey = self._hucre(*self.yem)
            Ellipse(pos=(ex+2, ey+2), size=(cs-4, cs-4))

            # Yılan
            for i, (cx, cy) in enumerate(self.yilan):
                if i == 0:
                    Color(0.22, 0.56, 0.22)
                else:
                    Color(0.07, 0.28, 0.07)
                px, py = self._hucre(cx, cy)
                Rectangle(pos=(px+1, py+1), size=(cs-2, cs-2))

        # Harfler
        for i, (cx, cy) in enumerate(self.yilan):
            harf = self.isim[(self.isim_idx - 1 - i) % len(self.isim)]
            px, py = self._hucre(cx, cy)
            lbl = Label(
                text=harf.upper(),
                font_size=max(10, cs * 0.52),
                bold=True,
                color=(1, 0.41, 0.71, 1),
                pos=(px, py),
                size=(cs, cs)
            )
            lbl._yilan = True
            self.add_widget(lbl)
            self.etiketler.append(lbl)

        # Skor ve level
        skor_lbl = Label(
            text="SKOR:" + str(self.skor),
            font_size=max(16, self.width * 0.045),
            bold=True,
            color=(0.55, 0.78, 0.40, 1),
            pos=(self.x, ay + cs * ROWS + 4),
            size=(self.width * 0.4, 40)
        )
        self.add_widget(skor_lbl)
        self.etiketler.append(skor_lbl)

        lv_lbl = Label(
            text="LV" + str(self.lv+1) + "/10",
            font_size=max(16, self.width * 0.045),
            bold=True,
            color=(0.86, 0.71, 0.20, 1),
            pos=(self.x + self.width * 0.35, ay + cs * ROWS + 4),
            size=(self.width * 0.3, 40)
        )
        self.add_widget(lv_lbl)
        self.etiketler.append(lv_lbl)

        ilerleme_lbl = Label(
            text=str(self.yenen % 5) + "/5",
            font_size=max(16, self.width * 0.045),
            bold=True,
            color=(0.63, 0.78, 0.63, 1),
            pos=(self.x + self.width * 0.65, ay + cs * ROWS + 4),
            size=(self.width * 0.35, 40)
        )
        self.add_widget(ilerleme_lbl)
        self.etiketler.append(ilerleme_lbl)

        ad_lbl = Label(
            text="Ad: " + self.isim,
            font_size=max(12, self.width * 0.035),
            color=(1, 0.41, 0.71, 1),
            pos=(self.x, ay + cs * ROWS + 44),
            size=(self.width, 30)
        )
        self.add_widget(ad_lbl)
        self.etiketler.append(ad_lbl)

        # D-pad
        pad_cx = self.x + self.width / 2
        pad_cy = self.y + self.height * 0.12
        bs = self.width * 0.18
        for nm, (ox, oy_off), sym in [
            ("yukari", (0, 1), "^"),
            ("asagi", (0, -1), "v"),
            ("sol", (-1, 0), "<"),
            ("sag", (1, 0), ">"),
        ]:
            bx = pad_cx + ox * bs * 1.4 - bs/2
            by = pad_cy + oy_off * bs * 1.4 - bs/2
            with self.canvas:
                Color(0.10, 0.27, 0.10)
                Rectangle(pos=(bx, by), size=(bs, bs))
                Color(0.16, 0.39, 0.16)
                Line(rectangle=(bx, by, bs, bs), width=2)
            btn_lbl = Label(
                text=sym,
                font_size=bs * 0.5,
                bold=True,
                color=(0.55, 0.78, 0.40, 1),
                pos=(bx, by),
                size=(bs, bs)
            )
            self.add_widget(btn_lbl)
            self.etiketler.append(btn_lbl)

        # Overlay mesajlar
        if self.bekliyor and not self.gecis and not self.bitti and not self.kazandi:
            self._overlay_lbl("Yon sec, basla!", (0.86, 0.71, 0.20, 1))
        if self.gecis:
            self._overlay_lbl("LEVEL TAM! Dokun...", (0.86, 0.71, 0.20, 1))
        if self.bitti:
            self._overlay_lbl("GAME OVER\nSKOR:" + str(self.skor) + "\nDokun", (0.82, 0.24, 0.24, 1))
        if self.kazandi:
            self._overlay_lbl("TEBRIKLER!\nSKOR:" + str(self.skor) + "\nDokun", (0.86, 0.71, 0.20, 1))

    def _overlay_lbl(self, txt, col):
        cs = self._cs()
        ay = self._alan_y()
        lbl = Label(
            text=txt,
            font_size=max(20, self.width * 0.055),
            bold=True,
            color=col,
            halign='center',
            pos=(self.x, ay + cs * ROWS * 0.35),
            size=(self.width, cs * ROWS * 0.3)
        )
        self.add_widget(lbl)
        self.etiketler.append(lbl)

    def on_touch_down(self, touch):
        if self.bitti or self.kazandi:
            self.skor = 0
            self.yenen = 0
            self.bitti = False
            self.kazandi = False
            self.bekliyor = True
            self.baslat()
            return True
        if self.gecis:
            self.gecis = False
            self.bekliyor = True
            self.baslat()
            return True

        cs = self._cs()
        pad_cx = self.x + self.width / 2
        pad_cy = self.y + self.height * 0.12
        bs = self.width * 0.18
        tx, ty = touch.x, touch.y

        for nm, (ox, oy_off), yon in [
            ("yukari", (0, 1),  (0, 1)),
            ("asagi",  (0, -1), (0, -1)),
            ("sol",    (-1, 0), (-1, 0)),
            ("sag",    (1, 0),  (1, 0)),
        ]:
            bx = pad_cx + ox * bs * 1.4 - bs/2
            by = pad_cy + oy_off * bs * 1.4 - bs/2
            if bx <= tx <= bx+bs and by <= ty <= by+bs:
                if yon != OPP.get(self.yon):
                    self.yon = yon
                    self.bekliyor = False
                return True
        return True


class YilanApp(App):
    def build(self):
        Window.clearcolor = (0.03, 0.09, 0.03, 1)
        self.duzen = FloatLayout()
        self._isim_ekrani()
        return self.duzen

    def _isim_ekrani(self):
        self.duzen.clear_widgets()

        baslik = Label(
            text="ADINI GIR",
            font_size=48,
            bold=True,
            color=(0.86, 0.71, 0.20, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.78},
            size_hint=(1, 0.1)
        )
        self.duzen.add_widget(baslik)

        aciklama = Label(
            text="Yilanin uzerine yazilacak (max 12)",
            font_size=22,
            color=(0.55, 0.78, 0.40, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.68},
            size_hint=(1, 0.08)
        )
        self.duzen.add_widget(aciklama)

        self.isim_kutu = TextInput(
            hint_text="Isminizi girin...",
            font_size=36,
            multiline=False,
            background_color=(0.07, 0.19, 0.07, 1),
            foreground_color=(1, 0.41, 0.71, 1),
            cursor_color=(1, 0.41, 0.71, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            size_hint=(0.85, 0.09)
        )
        self.duzen.add_widget(self.isim_kutu)

        tamam_btn = Button(
            text="TAMAM >>",
            font_size=32,
            bold=True,
            background_color=(0.14, 0.39, 0.14, 1),
            color=(0.86, 0.71, 0.20, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.42},
            size_hint=(0.5, 0.09)
        )
        tamam_btn.bind(on_press=self._oyunu_baslat)
        self.duzen.add_widget(tamam_btn)
        self.isim_kutu.bind(on_text_validate=self._oyunu_baslat)

    def _oyunu_baslat(self, *args):
        isim = self.isim_kutu.text.strip()[:12]
        if not isim:
            isim = "OYUNCU"
        self.duzen.clear_widgets()
        oyun = OyunAlani(
            isim=isim,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.duzen.add_widget(oyun)


if __name__ == '__main__':
    YilanApp().run()
                
