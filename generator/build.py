#!/usr/bin/env python3
"""
Генератор анимированных SVG для профиля GitHub.

    python3 generator/build.py      → файлы появятся в assets/

GitHub показывает SVG как картинку: JS не работает, а CSS-анимации и SMIL работают.
Шрифты внутри картинки только системные, поэтому ширину строк фиксирует textLength,
а ASCII-баннер рисуется прямоугольниками и линиями, а не символами.
"""
from math import sin, cos, pi
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# --- палитра Tokyo Night ------------------------------------------------------
BG, BAR, LINE = "#1a1b26", "#16161e", "#292e42"
FG, DIM, MUTED = "#c0caf5", "#565f89", "#3b4261"
BLUE, CYAN, PURPLE = "#7aa2f7", "#7dcfff", "#bb9af7"
GREEN, YELLOW, ORANGE, RED, TEAL = "#9ece6a", "#e0af68", "#ff9e64", "#f7768e", "#73daca"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
W = 860


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def svg(w, h, body, defs="", css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xml:space="preserve">
<defs>{defs}</defs>
<style><![CDATA[
text{{font-family:{MONO};white-space:pre}}
.blink{{animation:blink 1s step-end infinite}}
@keyframes blink{{50%{{opacity:0}}}}
{css}
]]></style>
{body}
</svg>
"""


def window(w, h, title, body, defs="", css=""):
    """Окно терминала: заголовок с «светофором», скан-линии, виньетка, бегущий луч."""
    defs = f"""
<pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000" fill-opacity=".2"/></pattern>
<radialGradient id="vignette" r=".8"><stop offset=".55" stop-opacity="0"/><stop offset="1" stop-opacity=".45"/></radialGradient>
<linearGradient id="beam" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>{defs}"""
    css = f""".beam{{animation:beam 6s linear infinite}}
@keyframes beam{{from{{transform:translateY(-140px)}}to{{transform:translateY({h}px)}}}}
{css}"""
    body = f"""<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="36" fill="{BAR}"/><rect y="36" width="{w}" height="1" fill="{LINE}"/>
<circle cx="22" cy="18" r="6" fill="{RED}"/><circle cx="42" cy="18" r="6" fill="{YELLOW}"/><circle cx="62" cy="18" r="6" fill="{GREEN}"/>
<text x="{w / 2}" y="22.5" text-anchor="middle" font-size="12" fill="{DIM}">{esc(title)}</text>
{body}
<rect class="beam" width="{w}" height="140" fill="url(#beam)"/>
<rect width="{w}" height="{h}" fill="url(#scan)"/>
<rect width="{w}" height="{h}" fill="url(#vignette)"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13.5" stroke="{LINE}"/>"""
    return svg(w, h, body, defs, css)


def mono(x, y, parts, size=14, cw=None, attrs=""):
    """Строка моноширинного текста из цветных кусков [(текст, цвет), ...]."""
    cw = cw or size * 0.6
    text = "".join(t for t, _ in parts)
    spans = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in parts)
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" textLength="{f(len(text) * cw)}" '
            f'lengthAdjust="spacingAndGlyphs" {attrs}>{spans}</text>')


# --- ASCII-баннер (шрифт figlet «ANSI Shadow») ---------------------------------
FONT = {
    "I": ["██╗", "██║", "██║", "██║", "██║", "╚═╝"],
    "G": [" ██████╗ ", "██╔════╝ ", "██║  ███╗", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
    "O": [" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
    "R": ["██████╗ ", "██╔══██╗", "██████╔╝", "██╔══██╗", "██║  ██║", "╚═╝  ╚═╝"],
    "S": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
    "U": ["██╗   ██╗", "██║   ██║", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
    "K": ["██╗  ██╗", "██║ ██╔╝", "█████╔╝ ", "██╔═██╗ ", "██║  ██╗", "╚═╝  ╚═╝"],
    "H": ["██╗  ██╗", "██║  ██║", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
    "A": [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
    "N": ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
    "V": ["██╗   ██╗", "██║   ██║", "██║   ██║", "╚██╗ ██╔╝", " ╚████╔╝ ", "  ╚═══╝  "],
}


def box_char(c, x, y, w, h, d=1.6):
    """Двойные линии ═║╗╔╝╚ как path — одинаково в любом шрифте."""
    cx, cy, L, R, T, B = x + w / 2, y + h / 2, x, x + w, y, y + h
    segs = {
        "═": [[(L, cy - d), (R, cy - d)], [(L, cy + d), (R, cy + d)]],
        "║": [[(cx - d, T), (cx - d, B)], [(cx + d, T), (cx + d, B)]],
        "╗": [[(L, cy - d), (cx + d, cy - d), (cx + d, B)], [(L, cy + d), (cx - d, cy + d), (cx - d, B)]],
        "╔": [[(R, cy - d), (cx - d, cy - d), (cx - d, B)], [(R, cy + d), (cx + d, cy + d), (cx + d, B)]],
        "╝": [[(L, cy + d), (cx + d, cy + d), (cx + d, T)], [(L, cy - d), (cx - d, cy - d), (cx - d, T)]],
        "╚": [[(R, cy + d), (cx - d, cy + d), (cx - d, T)], [(R, cy - d), (cx + d, cy - d), (cx + d, T)]],
    }[c]
    return "".join("M" + "L".join(f"{f(px)} {f(py)}" for px, py in pts) for pts in segs)


def banner(text, x0, y0, cw, ch):
    """Возвращает SVG-группы букв (для поочерёдного появления) и ширину баннера."""
    groups, col = [], 0
    for ch_ in text:
        if ch_ == " ":
            col += 3
            continue
        glyph = FONT[ch_]
        gw = max(map(len, glyph))
        rects, path = [], ""
        for r, row in enumerate(glyph):
            c = 0
            while c < len(row):
                if row[c] == "█":
                    start = c
                    while c < len(row) and row[c] == "█":
                        c += 1
                    rects.append(f'<rect x="{f(x0 + (col + start) * cw)}" y="{f(y0 + r * ch)}" '
                                 f'width="{f((c - start) * cw + .3)}" height="{f(ch + .4)}"/>')
                    continue
                if row[c] != " ":
                    path += box_char(row[c], x0 + (col + c) * cw, y0 + r * ch, cw, ch)
                c += 1
        groups.append(f'<g class="L" style="animation-delay:{f(.25 + len(groups) * .07)}s">'
                      f'<path d="{path}" stroke="{MUTED}" stroke-width="1.1" fill="none"/>{"".join(rects)}</g>')
        col += gw
    return "\n".join(groups), col * cw


def typing(lengths, cw, t_type=.05, t_hold=1.9, t_erase=.016, t_gap=.35):
    """Тайминг печати и стирания нескольких фраз подряд: [(t, ширина)] на фразу + длина цикла."""
    per, t = [], 0.0
    for n in lengths:
        ev = [(t, 0.0)]
        ev += [(t + k * t_type, k * cw) for k in range(1, n + 1)]
        t += n * t_type + t_hold
        ev += [(t + k * t_erase, (n - k) * cw) for k in range(1, n + 1)]
        t += n * t_erase + t_gap
        per.append(ev)
    return per, t


def smil(attr, events, total, begin, base=0.0):
    """Дискретная SMIL-анимация атрибута по событиям [(t, значение)]."""
    ev = sorted(events)
    if ev[0][0] > 0:
        ev.insert(0, (0.0, 0.0))
    ev.append((total, ev[-1][1]))
    times, vals, last = [], [], -1.0
    for t, v in ev:
        k = round(t / total, 5)
        if k <= last:
            continue
        times.append(k)
        vals.append(f(base + v))
        last = k
    times[0] = 0
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{";".join(map(str, times))}" '
            f'dur="{f(total)}s" begin="{begin}s" repeatCount="indefinite" calcMode="discrete"/>')


# --- 1. Шапка ------------------------------------------------------------------
def header():
    h, cw, ch = 268, 7.8, 15.5
    name_w = 101 * cw
    x0, y0 = (W - name_w) / 2, 60
    letters, _ = banner("IGOR SUKHANOV", x0, y0, cw, ch)

    size, tcw = 14, 8.4
    prompt = [("igor", GREEN), ("@", FG), ("github", GREEN), (":", FG), ("~", BLUE), ("$ ", FG)]
    plen = sum(len(t) for t, _ in prompt) * tcw
    lx, l1, l2, l3 = x0, 190, 214, 244

    # строка 1: whoami печатается один раз
    who = "whoami"
    who_ev = [(1.0 + k * .09, k * tcw) for k in range(len(who) + 1)]
    who_anim = "".join(
        f'<set attributeName="width" to="{f(w_)}" begin="{f(t)}s" fill="freeze"/>' for t, w_ in who_ev)
    cur1 = "".join(f'<set attributeName="x" to="{f(lx + plen + w_)}" begin="{f(t)}s" fill="freeze"/>'
                   for t, w_ in who_ev)

    # строка 3: команды по кругу
    phrases = [
        ("npm run dev", "React · Redux · TypeScript"),
        ("nest start --watch", "Node.js · Express · NestJS"),
        ("psql -d app", "PostgreSQL · MongoDB"),
        ("swift build", "macOS apps after hours"),
        ("git push origin main", "ship it"),
    ]
    texts = [(cmd.ljust(21), "# " + com) for cmd, com in phrases]
    per, total = typing([len(a) + len(b) for a, b in texts], tcw)
    begin = 2.9
    clips, lines3 = [], []
    for i, ((cmd, com), ev) in enumerate(zip(texts, per)):
        clips.append(f'<clipPath id="t{i}"><rect x="{f(lx + plen)}" y="{l3 - 17}" width="0" height="24">'
                     f'{smil("width", ev, total, begin)}</rect></clipPath>')
        lines3.append(f'<g clip-path="url(#t{i})">{mono(lx + plen, l3, [(cmd, FG), (com, DIM)], size, tcw)}</g>')
    cursor3_ev = [e for ev in per for e in ev]

    defs = f"""
<linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="{f(x0)}" y1="0" x2="{f(x0 + 420)}" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".35" stop-color="{BLUE}"/><stop offset=".7" stop-color="{PURPLE}"/><stop offset="1" stop-color="{RED}"/>
  <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="840 0" dur="9s" repeatCount="indefinite"/>
</linearGradient>
<clipPath id="bandA"><rect x="0" y="{f(y0 + ch * 1)}" width="{W}" height="{f(ch * 1.6)}"/></clipPath>
<clipPath id="bandB"><rect x="0" y="{f(y0 + ch * 3.7)}" width="{W}" height="{f(ch * 1.1)}"/></clipPath>
<clipPath id="who"><rect x="{f(lx + plen)}" y="{l1 - 17}" width="0" height="24">{who_anim}</rect></clipPath>
{"".join(clips)}
<g id="name">{letters}</g>"""

    css = f""".L{{opacity:0;animation:drop .7s cubic-bezier(.2,.9,.3,1.25) forwards}}
@keyframes drop{{from{{opacity:0;transform:translateY(-18px)}}to{{opacity:1;transform:none}}}}
.main{{animation:jit 5s steps(1) 2.2s infinite}}
@keyframes jit{{0%,86%{{transform:none}}87%{{transform:translateX(3px)}}89%{{transform:translateX(-2px)}}91%,100%{{transform:none}}}}
.gA,.gB{{opacity:0}}
.gA{{animation:gA 5s steps(1) 2.2s infinite}}
.gB{{animation:gB 5s steps(1) 2.2s infinite}}
@keyframes gA{{0%,86%{{opacity:0}}87%{{opacity:.85;transform:translateX(-9px)}}89%{{opacity:.85;transform:translateX(6px)}}91%,100%{{opacity:0;transform:none}}}}
@keyframes gB{{0%,87%{{opacity:0}}88%{{opacity:.85;transform:translateX(11px)}}90%{{opacity:.85;transform:translateX(-5px)}}92%,100%{{opacity:0;transform:none}}}}
.fade{{opacity:0;animation:fade .5s ease-out forwards}}
@keyframes fade{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}"""

    body = f"""
<use href="#name" class="main" fill="url(#grad)"/>
<use href="#name" class="gA" fill="{CYAN}" clip-path="url(#bandA)"/>
<use href="#name" class="gB" fill="{RED}" clip-path="url(#bandB)"/>
<g class="fade" style="animation-delay:.6s">{mono(lx, l1, prompt, size, tcw)}</g>
<g clip-path="url(#who)">{mono(lx + plen, l1, [(who, FG)], size, tcw)}</g>
<rect class="blink" x="{f(lx + plen)}" y="{l1 - 14}" width="8" height="17" fill="{PURPLE}" visibility="hidden">
  <set attributeName="visibility" to="visible" begin=".6s"/><set attributeName="visibility" to="hidden" begin="1.9s" fill="freeze"/>{cur1}
</rect>
<g class="fade" style="animation-delay:1.9s">{mono(lx, l2, [("Igor ", FG), ('"Garik"', YELLOW), (" Sukhanov", FG), ("  ·  ", DIM), ("fullstack developer", CYAN), ("  ·  ", DIM), ("Voronezh", FG)], size, tcw)}</g>
<g class="fade" style="animation-delay:2.5s">{mono(lx, l3, prompt, size, tcw)}</g>
{"".join(lines3)}
<rect class="blink" x="{f(lx + plen)}" y="{l3 - 14}" width="8" height="17" fill="{PURPLE}" visibility="hidden">
  <set attributeName="visibility" to="visible" begin="2.5s" fill="freeze"/>{smil("x", cursor3_ev, total, begin, lx + plen)}
</rect>"""
    return window(W, h, "igor@github: ~", body, defs, css)


# --- 2. neofetch с вращающимся ASCII-бубликом ------------------------------------
def donut_frame(A, B, cols=48, rows=24):
    out, zb = [" "] * (cols * rows), [0.0] * (cols * rows)
    cA, sA, cB, sB = cos(A), sin(A), cos(B), sin(B)
    j = 0.0
    while j < 2 * pi:
        ct, st = cos(j), sin(j)
        i = 0.0
        while i < 2 * pi:
            sp, cp = sin(i), cos(i)
            hh = ct + 2
            D = 1 / (sp * hh * sA + st * cA + 5)
            t = sp * hh * cA - st * sA
            x = int(cols / 2 + 30 * D * (cp * hh * cB - t * sB))
            y = int(rows / 2 + 15 * D * (cp * hh * sB + t * cB))
            N = int(8 * ((st * sA - sp * ct * cA) * cB - sp * ct * sA - st * cA - cp * ct * sB))
            o = x + cols * y
            if 0 <= y < rows and 0 <= x < cols and D > zb[o]:
                zb[o] = D
                out[o] = ".,-~:;=!*#$@"[max(N, 0)]
            i += 0.02
        j += 0.07
    return ["".join(out[r * cols:(r + 1) * cols]) for r in range(rows)]


def about():
    h = 400
    frames_n, frame_dt = 60, .075
    total = frames_n * frame_dt
    dsize, dcw, dlh = 11, 6.6, 13.4
    dx, dy = 24, 50
    frames = []
    for k in range(frames_n):
        A = 1.0 + 2 * pi * k / frames_n * 2
        B = 0.5 + 2 * pi * k / frames_n
        rows = donut_frame(A, B)
        lines = []
        for r, row in enumerate(rows):
            s = row.rstrip()
            lead = len(s) - len(s.lstrip())
            s = s.lstrip()
            if s:
                lines.append(f'<text x="{f(dx + lead * dcw)}" y="{f(dy + (r + 1) * dlh)}" font-size="{dsize}" '
                             f'textLength="{f(len(s) * dcw)}" lengthAdjust="spacingAndGlyphs">{esc(s)}</text>')
        frames.append(f'<g class="fr" style="animation-delay:{f(k * frame_dt)}s">{"".join(lines)}</g>')

    ix, iy, lh, size, cw, keyw = 370, 76, 23, 13, 7.8, 100
    info = [
        ("Role", "Fullstack developer"),
        ("Frontend", "React · Redux Toolkit · React Hook Form · MUI"),
        ("Markup", "HTML5 · CSS3 · SASS · Pug"),
        ("Backend", "Node.js · Express · NestJS"),
        ("Database", "PostgreSQL · MongoDB"),
        ("Languages", "TypeScript · JavaScript · Swift"),
        ("Tools", "Git · GitHub · Bitbucket · Jira"),
        ("Lately", "macOS apps · PWA · AI agents & MCP"),
        ("Codewars", "SukhanovGarik · clan Yandex.Practicum"),
        ("Uptime", "on GitHub since Dec 2021"),
    ]
    rows = [mono(ix, iy, [("igor", PURPLE), ("@", FG), ("github", PURPLE)], 15, 9),
            f'<rect x="{ix}" y="{iy + 10}" width="{11 * 9}" height="2" fill="{MUTED}"/>']
    colors = [CYAN, BLUE, PURPLE, RED, ORANGE, YELLOW, GREEN, TEAL, CYAN, BLUE]
    for n, (k, v) in enumerate(info):
        y = iy + 34 + n * lh
        rows.append(f'<g class="ln" style="animation-delay:{f(.3 + n * .12)}s">'
                    f'{mono(ix, y, [(k, colors[n])], size, cw)}{mono(ix + keyw, y, [(v, FG)], size, cw)}</g>')
    by = iy + 34 + len(info) * lh - 4
    palette = [MUTED, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, FG]
    blocks = "".join(f'<rect x="{ix + n * 30}" y="{by}" width="30" height="16" fill="{c}"/>' for n, c in enumerate(palette))
    rows.append(f'<g class="ln" style="animation-delay:{f(.3 + len(info) * .12)}s">{blocks}</g>')

    defs = f"""
<linearGradient id="dg" gradientUnits="userSpaceOnUse" x1="{dx}" y1="{dy}" x2="{dx + 320}" y2="{dy + 320}">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/>
</linearGradient>"""
    css = f""".fr{{opacity:0;animation:fr {f(total)}s step-end infinite}}
@keyframes fr{{0%{{opacity:1}}{f(100 / frames_n)}%{{opacity:0}}}}
.ln{{opacity:0;animation:ln .45s ease-out forwards}}
@keyframes ln{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}"""
    body = f"""<g fill="url(#dg)">{"".join(frames)}</g>
{"".join(rows)}"""
    return window(W, h, "igor@github: ~ — neofetch", body, defs, css)


# --- 3. Схема стека: запрос бежит client → api → data и обратно -------------------
def stack():
    h, T = 330, 7.0
    bw, bh, by = 210, 128, 66
    xs = [30, 325, 620]
    boxes = [
        ("client", CYAN, ["React · Redux Toolkit", "React Hook Form", "MUI · SASS · Pug", "HTML5 · CSS3"]),
        ("api", PURPLE, ["Node.js", "Express · NestJS", "REST · WebSocket", "TypeScript"]),
        ("data", GREEN, ["PostgreSQL", "MongoDB"]),
    ]
    # (откуда, куда, полоса, старт, конец, цвет, лог)
    hops = [
        (0, 1, -1, 0.2, 1.1, CYAN, [("[client] ", CYAN), ("→ ", DIM), ("GET /api/users?active=true", FG)]),
        (1, 2, -1, 1.3, 2.2, PURPLE, [("[api]    ", PURPLE), ("→ ", DIM), ("SELECT * FROM users WHERE active", FG)]),
        (2, 1, 1, 2.6, 3.5, GREEN, [("[data]   ", GREEN), ("← ", DIM), ("42 rows", FG), (" in 3ms", DIM)]),
        (1, 0, 1, 3.7, 4.6, GREEN, [("[client] ", CYAN), ("← ", DIM), ("200 OK", GREEN), ("  application/json", DIM)]),
    ]
    mid = by + bh / 2
    pct = lambda t: f"{100 * t / T:.2f}%"
    parts, css = [], []

    for (name, color, items), x in zip(boxes, xs):
        parts.append(f'<rect class="box-{name}" x="{x}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{BAR}" stroke="{LINE}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x + 14}" y="{by - 9}" width="{len(name) * 7.8 + 22}" height="18" rx="4" fill="{BG}"/>')
        parts.append(mono(x + 25, by + 4.5, [(name, color)], 13, 7.8))
        for n, it in enumerate(items):
            parts.append(mono(x + 18, by + 34 + n * 24, [("› ", color), (it, FG)], 13, 7.8))

    # подсветка блока в момент прихода пакета
    arrivals = {}
    for a, b, _, s, e, c, _ in hops:
        arrivals.setdefault(b, []).append((e, c))
    for idx, ev in arrivals.items():
        name = boxes[idx][0]
        frames = ["0%{stroke:" + LINE + "}"]
        for e, c in ev:
            frames.append(f"{pct(e - .01)}{{stroke:{LINE}}}{pct(e)}{{stroke:{c}}}{pct(e + .7)}{{stroke:{LINE}}}")
        css.append(f".box-{name}{{animation:pulse-{name} {T}s linear infinite}}"
                   f"@keyframes pulse-{name}{{{''.join(frames)}100%{{stroke:{LINE}}}}}")

    # полосы-провода между блоками
    for k in range(2):
        x1, x2 = xs[k] + bw, xs[k + 1]
        for lane, col in ((-1, MUTED), (1, MUTED)):
            y = mid + lane * 12
            parts.append(f'<path class="wire" d="M{x1 + 4} {y}H{x2 - 4}" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 5"/>')
        parts.append(f'<path d="M{x2 - 10} {mid - 16}l6 4-6 4" stroke="{DIM}" stroke-width="1.5"/>')
        parts.append(f'<path d="M{x1 + 10} {mid + 8}l-6 4 6 4" stroke="{DIM}" stroke-width="1.5"/>')

    # пакеты
    for a, b, lane, s, e, c, _ in hops:
        y = mid + lane * 12
        x1 = xs[a] + bw + 4 if b > a else xs[a] - 4
        x2 = xs[b] - 4 if b > a else xs[b] + bw + 4
        kt = f"0;{s / T:.4f};{e / T:.4f};1"
        parts.append(
            f'<g opacity="0"><circle r="9" fill="{c}" fill-opacity=".18"/><circle r="4" fill="{c}"/>'
            f'<animateMotion path="M{x1} {y}H{x2}" keyPoints="0;0;1;1" keyTimes="{kt}" calcMode="linear" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{s / T:.4f};{(e - .02) / T:.4f};{e / T:.4f};1" dur="{T}s" repeatCount="indefinite"/></g>')

    # лог запросов
    ly = by + bh + 36
    parts.append(f'<rect x="30" y="{ly - 18}" width="{W - 60}" height="{4 * 22 + 16}" rx="8" fill="{BAR}"/>')
    for n, (_, _, _, s, _, _, line) in enumerate(hops):
        parts.append(f'<g class="log{n}">{mono(46, ly + 6 + n * 22, line, 13, 7.8)}</g>')
        css.append(f".log{n}{{opacity:0;animation:log{n} {T}s linear infinite}}"
                   f"@keyframes log{n}{{0%,{pct(s - .01)}{{opacity:0}}{pct(s)},{pct(T - .45)}{{opacity:1}}{pct(T - .1)},100%{{opacity:0}}}}")

    css.append(".wire{animation:march 1s linear infinite}@keyframes march{to{stroke-dashoffset:-18}}")
    return window(W, h, "~/stack — how a request travels through my code", "\n".join(parts), "", "\n".join(css))


# --- 4. Кнопки-ссылки -------------------------------------------------------------
def button(label, color):
    w, h = 180, 44
    text = "› " + label
    tx = (w - len(text) * 8.4 - 12) / 2
    defs = f"""<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="{LINE}"/><stop offset=".45" stop-color="{LINE}"/><stop offset=".5" stop-color="{color}"/><stop offset=".55" stop-color="{LINE}"/><stop offset="1" stop-color="{LINE}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="{2 * w} 0" dur="4s" repeatCount="indefinite"/>
</linearGradient>"""
    body = f"""<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="{BG}" stroke="url(#g)" stroke-width="2"/>
{mono(tx, 27.5, [("› ", color), (label, FG)], 14, 8.4)}
<rect class="blink" x="{f(tx + len(text) * 8.4 + 3)}" y="15" width="8" height="16" fill="{color}"/>"""
    return svg(w, h, body, defs)


# --- 5. Подвал: эквалайзер из «блочных символов» -----------------------------------
def footer():
    h, n, bw, gap = 120, 70, 8, 4
    x0 = (W - n * (bw + gap) + gap) / 2
    bars = []
    for k in range(n):
        dur = 0.9 + (k * 37 % 11) / 10
        delay = -((k * 53) % 17) / 10
        bars.append(f'<rect class="eq" x="{f(x0 + k * (bw + gap))}" y="16" width="{bw}" height="64" '
                    f'style="animation-duration:{f(dur)}s;animation-delay:{f(delay)}s"/>')
    defs = f"""<linearGradient id="eg" gradientUnits="userSpaceOnUse" x1="{f(x0)}" y1="0" x2="{f(W - x0)}" y2="0">
<stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<pattern id="seg" width="10" height="5" patternUnits="userSpaceOnUse"><rect width="10" height="3.5" fill="#fff"/></pattern>
<mask id="m"><rect width="{W}" height="{h}" fill="url(#seg)"/></mask>"""
    css = """.eq{transform-box:fill-box;transform-origin:bottom;animation:eq 1s ease-in-out infinite alternate}
@keyframes eq{0%{transform:scaleY(.08)}30%{transform:scaleY(.7)}60%{transform:scaleY(.3)}100%{transform:scaleY(1)}}"""
    body = f"""<g mask="url(#m)" fill="url(#eg)">{"".join(bars)}</g>
<text x="{W / 2}" y="108" text-anchor="middle" font-size="13" fill="{DIM}">thanks for stopping by · <tspan fill="{PURPLE}">exit 0</tspan></text>"""
    return svg(W, h, body, defs, css)


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "about.svg": about(),
        "stack.svg": stack(),
        "footer.svg": footer(),
        "btn-telegram.svg": button("telegram", CYAN),
        "btn-instagram.svg": button("instagram", RED),
        "btn-habr.svg": button("habr career", GREEN),
        "btn-hh.svg": button("hh.ru resume", YELLOW),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name:20} {len(content.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
