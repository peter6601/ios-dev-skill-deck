#!/usr/bin/env python3
"""ai-review / consensus deck — 'signals & gates', speaker-led, 20 slides. Sister of the ios-dev transit-map deck."""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE.parent / "consensus" / "index.html")
BASE = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "index.html"
src = BASE.read_text()  # reuse the series' stage CSS, controller and inline editor from the ios-dev deck
CSS = re.search(r"<style>(.*?)</style>", src, re.S).group(1) + r"""
.card .ct{font:900 38px/1.25 var(--cjk)}
.card p{font:500 28px/1.55 var(--cjk)}
.cmdline{font:700 24px/1.6 var(--mono);color:var(--cream)}
"""
JS = (re.search(r"<script>(.*?)</script>", src, re.S).group(1)
      .replace("ios-dev-skill-路網圖.html", "ai-review-號誌與閘門.html").replace("iosdev-transit-deck:", "aireview-signal-deck:"))
QR = (HERE / "qr-aireview.svg").read_text()  # segno: make("https://github.com/peter6601/ai-review").svg_inline(scale=10, border=0)

SECS = [("文件審查", "l7"), ("程式碼審查", "l5"), ("實測", "l1")]
SEC_COLOR = {"開場": "ink", **dict(SECS)}
slides = []


def hdr(sec):
    return f'<header class="hdr"><span>AI-REVIEW · 號誌與閘門</span><span class="sec"><i></i>{sec}</span><span class="pg"></span></header>'


def add(body, sec, acc=None):
    style = f"--sec:var(--{SEC_COLOR[sec]})" + (f";--acc:var(--{acc})" if acc else "")
    slides.append(f'<section class="slide" style="{style}">\n{hdr(sec)}\n{body}\n</section>')


def svg(inner):
    return f'<svg class="map" viewBox="0 0 1920 1080" aria-hidden="true">{inner}</svg>'


def ln(d, c, delay=.3, w=12):
    return f'<path class="ln" pathLength="1" style="stroke:var(--{c});--d:{delay}s;stroke-width:{w}px" d="{d}"/>'


def stn(x, y, r=18, c="ink", w=6, d=.6):
    return f'<circle class="stn pop" style="stroke:var(--{c});stroke-width:{w}px;--d:{d}s" cx="{x}" cy="{y}" r="{r}"/>'


def text(x, y, s, size=28, weight=700, c="ink", anchor="middle", font="cjk"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{weight} {size}px var(--{font});fill:var(--{c})">{s}</text>'


def signal(x, y, lit="l4", d=.5, scale=1.0):
    """A three-aspect railway signal head on a post; `lit` is the glowing aspect colour."""
    s = scale
    w, h = 54 * s, 140 * s
    out = f'<g class="pop" style="--d:{d}s"><rect x="{x - 4 * s}" y="{y}" width="{8 * s}" height="{110 * s}" fill="var(--ink)"/>'
    out += f'<rect x="{x - w / 2}" y="{y - h}" width="{w}" height="{h}" rx="{14 * s}" fill="var(--ink)"/>'
    for i, c in enumerate(["l1", "l2", "l4"]):
        cy = y - h + 26 * s + i * 44 * s
        on = c == lit
        out += f'<circle cx="{x}" cy="{cy}" r="{15 * s}" fill="{"var(--" + c + ")" if on else "#3b3a36"}"/>'
    return out + "</g>"


def gate(x, y, label, sub, c="l2", d=.8, big=False):
    """A level-crossing style gate: a striped bar across the track."""
    h = 120 if big else 96
    out = f'<g class="pop" style="--d:{d}s"><rect x="{x - 14}" y="{y - h / 2}" width="28" height="{h}" rx="8" fill="#fff" stroke="var(--{c})" stroke-width="7"/>'
    for k in range(3):
        yy = y - h / 2 + 14 + k * (h - 28) / 2
        out += f'<rect x="{x - 9}" y="{yy - 6}" width="18" height="12" fill="var(--{c})"/>'
    out += "</g>"
    out += text(x, y - h / 2 - 18, label, 26, 900, c) + text(x, y + h / 2 + 36, sub, 22, 700, "muted", font="mono")
    return out


def title(s, top=150, size=88, kicker=None):
    k = f'<p class="kicker reveal" style="top:{top - 52}px">{kicker}</p>' if kicker else ""
    return k + f'<h2 class="title reveal" style="top:{top}px;font-size:{size}px">{s}</h2>'


def T(x, y, w, inner, size=30, d=.2, extra=""):
    return f'<p class="abs reveal" style="left:{x}px;top:{y}px;width:{w}px;font:500 {size}px/1.55 var(--cjk);color:var(--ink2);--d:{d}s;{extra}">{inner}</p>'


def card(x, y, w, h, inner, stripe=None, d=.2, pad="30px 40px", extra=""):
    st = f"border-left:20px solid var(--{stripe});" if stripe else ""
    hh = f"height:{h}px;" if h else ""
    return f'<div class="card reveal" style="left:{x}px;top:{y}px;width:{w}px;{hh}padding:{pad};{st}--d:{d}s;{extra}">{inner}</div>'


def sign(n, name, en, sec):
    col = SEC_COLOR[sec]
    xs = [400, 960, 1520]
    parts = [ln("M400 860 H1520", "ink", .25, 10)]
    for i, (lab, c) in enumerate(SECS):
        x = xs[i]
        if i + 1 < n:
            parts.append(f'<circle class="pop" style="--d:.5s" cx="{x}" cy="860" r="16" fill="var(--ink)"/>' + text(x, 935, lab, 26, 500, "muted"))
        elif i + 1 == n:
            parts.append(f'<circle class="pop" style="--d:.7s" cx="{x}" cy="860" r="34" fill="#fff" stroke="var(--{c})" stroke-width="12"/>'
                         + text(x, 940, lab, 32, 800, c) + text(x, 800, "你在這裡", 24, 700, c, font="mono"))
        else:
            parts.append(stn(x, 860, 16, "ink", 6, .5) + text(x, 935, lab, 26, 500, "muted"))
    add(f"""
<p class="sign-top reveal">SECTION {n:02d} / 03</p>
<div class="sign-band reveal" style="--d:.1s"><span class="sign-num">{n}</span>
  <div><h2 class="sign-name">{name}</h2><p class="sign-en">{en}</p></div></div>
{svg(''.join(parts))}""", sec)


def statement(sec, acc, kicker, big, lead, lit="l1"):
    inner = ln("M-20 940 H1940", "ink", .3, 14) + signal(1640, 935, lit, .9, .9)
    add(f"""
<p class="kicker reveal" style="top:220px">{kicker}</p>
<h2 class="big reveal" style="top:280px;--d:.1s">{big}</h2>
<p class="lead reveal" style="top:665px;width:1440px;--d:.25s">{lead}</p>
{svg(inner)}""", sec, acc)


# ================================================================== SLIDES
# 01 封面 ---------------------------------------------------------------
inner = ln("M150 760 H1770", "ink", .3, 12) + stn(150, 760, 18, "ink", 6, .3)
inner += ln("M620 760 C 620 560, 1080 560, 1080 760", "l3", .7, 10)
inner += signal(520, 750, "l1", .5)
inner += text(850, 560, "Claude 回修（最多 6 圈）", 26, 800, "l3") + stn(850, 610, 12, "l3", 5, 1.0)
inner += gate(1420, 760, "人工放行", "approve-code", "l2", 1.2, True)
inner += f'<circle class="term pop" style="stroke:var(--ink);--d:1.4s" cx="1770" cy="760" r="22"/>' + text(1770, 840, "合併", 30, 800)
inner += text(150, 830, "你的變更", 28, 800) + text(520, 900, "Codex 審查", 26, 800) + text(520, 932, "唯讀", 22, 700, "muted", font="mono")
add(f"""
<h1 class="abs reveal" style="left:104px;top:150px;font:900 120px/1.14 var(--cjk);--d:.05s">Codex 審、Claude 修，<br><span class="amber">人放行</span>。</h1>
<p class="abs reveal" style="left:110px;top:445px;font:500 32px/1.5 var(--cjk);color:var(--ink2);--d:.15s"><b style="font-family:var(--latin);color:var(--ink)">ai-review</b>：Claude Code × Codex 的本機共識審查工作流</p>
{svg(inner)}
<p class="abs reveal mono muted" style="left:110px;top:1000px;font-size:22px;font-weight:700;letter-spacing:.04em;--d:.5s">github.com/peter6601/ai-review</p>""", "開場", "l2")

# 02 為什麼 -------------------------------------------------------------
statement("開場", "l2", "起點 · WHY", 'AI 可以互相檢查，<br>但不會替<span class="amber">人類放行</span>。',
          "讓另一家模型來審，看到的盲點不同；可是 Codex 說 PASS，也不代表就是對的。<br><b>所以這條線的最後一道閘門，永遠留給人。</b>", "l2")

# 03 三個角色 -----------------------------------------------------------
roles = [("l4", "Codex", "號誌", "唯讀審查：只回 findings，不改任何東西。"),
         ("l3", "Claude", "回修班", "只在程式碼審查裡修，最多六輪；每次修完都重新測試、重新審。"),
         ("l2", "你", "站長", "逐條取捨文件 findings；程式碼的最後核准只能由你來按。")]
icons = (signal(330, 470, "l4", .4, .8)
         + ln("M820 420 C 820 330, 1100 330, 1100 420 C 1100 510, 820 510, 820 420", "l3", .5, 10)
         + gate(1540, 420, "", "", "l2", .6))
body = title("三個角色，各管一段", 150, 88) + svg(icons) + "".join(
    card(110 + i * 580, 560, 540, 330, f'<p class="ct" style="color:var(--{c})">{n}<span style="font:700 26px var(--cjk);color:var(--muted);margin-left:14px">{r}</span></p><p style="margin-top:16px">{t}</p>', c, .3 + i * .1)
    for i, (c, n, r, t) in enumerate(roles))
add(body, "開場")

# 04 兩個入口 -----------------------------------------------------------
doc = ["文件", "Codex 唯讀審", "你逐條取捨", "Claude 改採納項", "再審"]
code = ["你的變更", "跑驗證", "Codex 審", "Claude 修", "你核准"]
inner = ln("M560 430 H1780", "l7", .3, 12) + ln("M560 720 H1780", "l5", .4, 12)
for i, s in enumerate(doc):
    x = 640 + i * 280
    inner += (stn(x, 430, 22 if s.startswith("你") else 16, "l2" if s.startswith("你") else "ink", 8 if s.startswith("你") else 6, .7 + i * .08)
              + text(x, 395, s, 26, 800, "l2" if s.startswith("你") else "ink"))
for i, s in enumerate(code):
    x = 640 + i * 280
    you = s.startswith("你")
    inner += (stn(x, 720, 22 if you else 16, "l2" if you else "ink", 8 if you else 6, .8 + i * .08) + text(x, 685, s, 26, 800, "l2" if you else "ink"))
body = title("兩個入口", 150, 88) + svg(inner) + \
    f'<div class="abs reveal" style="left:110px;top:380px;width:420px;--d:.2s"><p style="font:800 34px/1.2 var(--mono);color:var(--l7)">consensus-plan</p><p class="small" style="font:500 26px/1.5 var(--cjk);color:var(--muted);margin-top:8px">文件已寫好、還沒有 code</p></div>' + \
    f'<div class="abs reveal" style="left:110px;top:670px;width:420px;--d:.3s"><p style="font:800 34px/1.2 var(--mono);color:var(--l5)">consensus-review</p><p style="font:500 26px/1.5 var(--cjk);color:var(--muted);margin-top:8px">功能、分支或 bug fix 已完成</p></div>' + \
    T(110, 900, 1700, '選哪個入口，<b style="color:var(--ink)">看 code 在不在</b>，不看流程走到哪。', 34, .9)
add(body, "開場")

# 05 SECTION 1 ---------------------------------------------------------
sign(1, "文件審查", "CONSENSUS-PLAN · DOC REVIEW", "文件審查")

# 06 文件審查路線 -------------------------------------------------------
st6 = [(220, "凍結文件與 lens", "init doc", False), (520, "Codex 審一次", "唯讀", False), (820, "findings 報告", "寫在文件旁", False),
       (1120, "你逐條取捨", "採納／不採納／自己改", True), (1420, "Claude 只改採納項", "你看過 diff", True), (1720, "再審", "re-review", False)]
inner = ln("M150 560 H1790", "l7", .3, 12)
for i, (x, a, b, you) in enumerate(st6):
    inner += stn(x, 560, 24 if you else 18, "l2" if you else "ink", 9 if you else 6, .6 + i * .1)
inner += ('<path class="pop" style="--d:1.4s" d="M1720 590 C 1700 760, 560 760, 525 592" fill="none" stroke="var(--l7)" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"/>'
          + text(1120, 795, "文件改過才能再審；沒改會被拒", 24, 700, "l7"))
body = title("文件審查：Codex 只讀，人來決定", 150, 80) + svg(inner) + "".join(
    f'<div class="abs reveal" style="left:{x - 150}px;top:{450 if i % 2 == 0 else 390}px;width:300px;text-align:center;--d:{.7 + i * .1:.2f}s">'
    f'<p style="font:900 30px/1.25 var(--cjk);color:{"var(--l2)" if you else "var(--ink)"}">{a}</p><p style="font:500 22px/1.4 var(--mono);color:var(--muted);margin-top:4px">{b}</p></div>'
    for i, (x, a, b, you) in enumerate(st6)) + \
    T(110, 860, 1700, '審查過程不改原文件、不跑測試、不寫 code；<b style="color:var(--ink)">findings 本身就是交付物。</b>', 32, 1.5)
add(body, "文件審查", "l7")

# 07 三種 lens ----------------------------------------------------------
lenses = [("requirement", "需求規格", "有沒有洞？", "沒寫到的行為、沒定義的邊界、沒人測得了的驗收條件。"),
          ("direction", "設計文件", "方向對嗎？", "它排除了什麼、有沒有更便宜的做法、是不是在解沒人有的問題。"),
          ("implementation", "實作規格", "跟現有 code 對得上嗎？", "它假設的名稱、契約、呼叫點，和悄悄矛盾的地方。")]
body = title("一次審一種角度：lens", 150, 88) + "".join(
    card(110 + i * 580, 300, 540, 470, f'<p style="font:800 30px/1.2 var(--mono);color:var(--l7);margin:0">{a}</p><p style="font:700 26px/1.4 var(--cjk);color:var(--muted);margin-top:6px">{b}</p>'
         f'<p class="ct" style="margin-top:26px">{q}</p><p style="margin-top:14px">{t}</p>', None, .2 + i * .1) for i, (a, b, q, t) in enumerate(lenses)) + \
    T(110, 830, 1700, '一份檔案其實是兩份文件，就審兩次；參考資料最多 5 段、16,000 tokens，<b style="color:var(--ink)">要指到精確的章節</b>。', 30, .6)
add(body, "文件審查", "l7")

# 08 逐條取捨 -----------------------------------------------------------
tri = [("l4", "採納", "Claude 只改這幾條，不順手改別的。"), ("l1", "不採納", "理由用你的話，寫進文件的「已知取捨」段。"), ("l3", "自己改", "你動手；Claude 不碰。")]
body = title("逐條取捨，Claude 只改你採納的", 150, 80) + "".join(
    card(110 + i * 580, 300, 540, 300, f'<p class="ct" style="color:var(--{c})">{a}</p><p style="margin-top:16px">{t}</p>', c, .2 + i * .1) for i, (c, a, t) in enumerate(tri)) + \
    f'<h3 class="abs reveal" style="left:110px;top:680px;font:900 60px/1.35 var(--cjk);--d:.6s">你核過 diff 才再審，<span class="amber">不自動循環</span>。</h3>' + \
    T(110, 800, 1700, '文件審查沒有「核准」這件事：Codex 的 PASS 只是一次仔細的閱讀，不是放行。', 30, .7)
add(body, "文件審查", "l7")

# 09 SECTION 2 ---------------------------------------------------------
sign(2, "程式碼審查", "CONSENSUS-REVIEW · CODE", "程式碼審查")

# 10 審查迴圈 -----------------------------------------------------------
inner = ln("M150 640 H600", "ink", .3, 12) + ln("M1250 640 H1780", "ink", .9, 12)
inner += f'<ellipse class="ln" pathLength="1" style="stroke:var(--l3);--d:.5s;stroke-width:12px" cx="925" cy="640" rx="325" ry="170"/>'
inner += stn(200, 640, 18, "ink", 6, .4) + text(200, 700, "init", 26, 800, font="mono") + text(200, 734, "凍結範圍", 22, 500, "muted")
inner += gate(420, 640, "閘門 1", "approve-review", "l3", .5)
for (x, y, a, c) in [(700, 520, "跑驗證", "ink"), (1150, 520, "Codex 審", "l4"), (925, 810, "Claude 修", "l3")]:
    inner += stn(x, y, 20, c, 7, .8) + text(x, y - 34 if y < 640 else y + 50, a, 30, 900, c if c != "ink" else "ink")
inner += text(925, 650, "同一個 run 裡", 26, 700, "muted") + text(925, 686, "最多 6 圈", 34, 900, "l3")
inner += '<path class="pop" style="--d:1.0s" d="M1130 755 L1290 840" stroke="var(--l1)" stroke-width="6" stroke-dasharray="10 10" fill="none"/>'
inner += gate(1330, 860, "閘門 2", "approve-risk", "l1", 1.0)
inner += text(1330, 990, "高風險修改才停", 22, 700, "l1")
inner += gate(1480, 640, "閘門 3", "approve-code", "l2", 1.1, True)
inner += f'<circle class="term pop" style="stroke:var(--ink);--d:1.3s" cx="1740" cy="640" r="22"/>' + text(1740, 710, "合併／PR", 26, 800)
body = title("程式碼審查：一圈一圈，直到你放行", 150, 80) + svg(inner) + \
    T(110, 950, 1700, 'Codex 永遠先看 code；Claude 修完一定重跑驗證、再給 Codex 審。', 28, 1.4)
add(body, "程式碼審查", "l5")

# 11 開工前六樣 ---------------------------------------------------------
six = [("Repo", "目標 worktree 的絕對路徑"), ("Base", "明確給，不猜 main、HEAD 或 merge base"), ("Brief", "一兩句話：這個改動原本要做到什麼"),
       ("Profile", "ios 或 generic，建立前先講給你聽"), ("聚焦的驗證指令", "至少一個針對這次的測試；不接受冒煙測試、整包測試頂替"),
       ("iOS preflight", "三個 specialist 的 findings，init 時一起交")]
body = title("開跑前，要先湊齊這六樣", 150, 88) + "".join(
    card(110 + (i % 3) * 580, 300 + (i // 3) * 300, 540, 270, f'<p style="font:900 26px/1 var(--latin);color:var(--l5);margin:0">{i + 1:02d}</p><p class="ct" style="margin-top:14px">{a}</p><p style="margin-top:10px;font-size:26px">{b}</p>', None, .15 + i * .06)
    for i, (a, b) in enumerate(six)) + \
    T(110, 920, 1700, '缺什麼就問人，<b style="color:var(--ink)">不從 branch 或 diff 猜</b>。', 30, .6)
add(body, "程式碼審查", "l5")

# 12 三道閘門 -----------------------------------------------------------
gates = [("l3", "閘門 1", "approve-review", "核准審查範圍", "可 --auto"), ("l1", "閘門 2", "approve-risk", "核准高風險修改", "可 --auto"),
         ("l2", "閘門 3", "approve-code", "最終核准", "永遠人工，沒有 --auto")]
inner = ln("M110 470 H1810", "ink", .3, 10) + "".join(gate(400 + i * 560, 470, "", "", c, .5 + i * .15, i == 2) for i, (c, *_r) in enumerate(gates))
body = title("三道閘門，只有最後一道不能自動", 150, 80) + svg(inner) + "".join(
    f'<div class="abs reveal" style="left:{400 + i * 560 - 250}px;top:560px;width:500px;text-align:center;--d:{.6 + i * .12:.2f}s">'
    f'<p style="font:900 34px/1.2 var(--cjk);color:var(--{c})">{a}</p><p style="font:800 28px/1.4 var(--mono);margin-top:8px">{b}</p>'
    f'<p style="font:600 28px/1.5 var(--cjk);color:var(--ink2);margin-top:6px">{t}</p>'
    f'<p style="display:inline-block;margin-top:14px;padding:6px 16px;border-radius:999px;border:3px solid var(--{c if i == 2 else "muted"});font:800 22px/1.2 var(--cjk);color:var(--{c if i == 2 else "muted"})">{z}</p></div>'
    for i, (c, a, b, t, z) in enumerate(gates)) + \
    T(110, 880, 1700, '自動核准全域限流 <b style="color:var(--ink)">60 秒最多 5 次</b>；紀錄寫 <span class="mono">agent:auto-approval</span>，不冒充人。', 30, 1.0)
add(body, "程式碼審查", "l5")

# 13 聯鎖 ---------------------------------------------------------------
statement("程式碼審查", "l5", "聯鎖 · INTERLOCKING", '路線一變，<br><span class="hl">號誌就失效</span>。',
          "核准綁定當下的 base 與完整 patch；code 一改，舊核准就作廢。<br>claude、codex 的執行檔在建立時記下指紋；<br>驗證指令不經 shell，只允許可信任路徑上的工具。")

# 14 SECTION 3 ---------------------------------------------------------
sign(3, "實測兩個月", "FIELD DATA · 152 RUNS", "實測")

# 15 數字 ---------------------------------------------------------------
facts = [(330, "152", "個 run", "排除 12 個測試用"), (760, "210", "輪 Codex 審查", "plan／review／doc"), (1190, "567", "條 findings", "blocker 90、major 416"), (1620, "95%", "要求修改", "PASS 只出現 4 次")]
inner = ln("M110 720 H1810", "ink", .3, 12) + "".join(stn(x, 720, 24, "l1", 9, .6 + i * .1) for i, (x, *_r) in enumerate(facts))
body = title("兩個月的實測", 150, 88) + T(110, 265, 1700, '2026-08-03 到 10-07，作者日常開發的 iOS 與工具專案。', 30, .1) + svg(inner) + "".join(
    f'<p class="abs reveal" style="left:{x - 230}px;top:520px;width:460px;text-align:center;font:900 140px/1 var(--latin);color:var(--l1);--d:{.5 + i * .1:.2f}s">{n}</p>'
    f'<div class="abs reveal" style="left:{x - 230}px;top:775px;width:460px;text-align:center;--d:{.7 + i * .1:.2f}s"><p style="font:800 34px/1.3 var(--cjk)">{a}</p><p style="font:500 24px/1.5 var(--cjk);color:var(--muted);margin-top:4px">{b}</p></div>'
    for i, (x, n, a, b) in enumerate(facts)) + \
    T(110, 950, 1700, '同一份文件出現過這輪要改、下輪 PASS——<b style="color:var(--ink)">PASS 不等於正確</b>，人工終審不能拿掉。', 28, 1.1)
add(body, "實測", "l1")

# 16 blocker -----------------------------------------------------------
bar = ('<g class="pop" style="--d:.6s"><rect x="110" y="700" width="1606" height="70" rx="12" fill="var(--l7)"/>'
       '<rect x="1716" y="700" width="94" height="70" rx="12" fill="var(--l5)"/></g>'
       + text(130, 748, "文件階段 85", 30, 900, "white", "start") + text(1763, 820, "程式碼 5", 26, 900, "l5"))
add(f"""
<p class="kicker reveal" style="top:200px">最划算的審查</p>
<h2 class="big reveal" style="top:255px;font-size:120px;--d:.1s">90 個 blocker，<br><span class="hl">85 個</span>在寫 code 前抓到。</h2>
{svg(bar)}
<p class="lead reveal" style="top:850px;width:1700px;--d:.4s">舊 plan 模式 23 個＋文件審查 62 個；程式碼審查只多抓到 5 個。<b>能在文件上抓的，就別等到 code。</b></p>""", "實測", "l7")


# 17–19 三個坑 ----------------------------------------------------------
def pit(n, head, before, cause, fix, after, acc):
    inner = ln("M110 560 H1810", "ink", .3, 10)
    inner += signal(330, 545, "l1", .5, .9) + signal(1590, 545, "l4", 1.1, .9)
    inner += f'<g class="pop" style="--d:.8s"><rect x="890" y="520" width="140" height="80" rx="40" fill="#fff" stroke="var(--{acc})" stroke-width="9"/></g>'
    body = title(head, 150, 76, f"坑 {n}") + svg(inner) + \
        f'<div class="abs reveal" style="left:110px;top:640px;width:540px;--d:.5s"><p style="font:800 26px/1.2 var(--mono);color:var(--l1)">改之前</p><p style="font:700 32px/1.45 var(--cjk);margin-top:10px">{before}</p></div>' + \
        f'<div class="abs reveal" style="left:690px;top:640px;width:540px;--d:.8s"><p style="font:800 26px/1.2 var(--mono);color:var(--{acc})">怎麼改</p><p style="font:600 28px/1.5 var(--cjk);color:var(--ink2);margin-top:10px">{fix}</p></div>' + \
        f'<div class="abs reveal" style="left:1270px;top:640px;width:540px;--d:1.1s"><p style="font:800 26px/1.2 var(--mono);color:var(--l4)">改之後</p><p style="font:700 32px/1.45 var(--cjk);margin-top:10px">{after}</p></div>' + \
        T(110, 300, 1700, cause, 30, .3)
    add(body, "實測", acc)


pit(1, "規則對，交接的形狀錯了",
    "29 個 iOS 審查卡在「等 preflight」，<b>0 次</b>交成功",
    "三個 specialist 的報告要在 run 開始後，由人手組成一份七個欄位都不能錯的 JSON 再交；錯了就 exit 2。驗證器沒寫錯，是交接的形狀錯了。",
    "改成建立 run 時一起交：三個 specialist 各吐一段 JSON，主 session 只負責包起來。",
    "之後 10 個審查有 <b>9 個</b>帶著 preflight 開跑", "l3")
pit(2, "閘門被挪動，run 就停死",
    "114 個 run 有 <b>31 個</b>（27%）停在「審查門檻被移動」",
    "判斷「這是新問題還是修出來的問題」靠比對 finding 的英文字串，而且從沒告訴 Codex 有這個約定。",
    "finding 帶上有型別的來源（已存在／修出來的／新發現），產生時就被 schema 強制。",
    "之後 23 個 run，<b>0 次</b>", "l5")
pit(3, "讓 AI 修文件，反而走不到終點",
    "舊 plan 模式 49 個 run，<b>只有 1 個</b>走到人工審查",
    "審完由 Claude 自動修文件、再審：外部呼叫失敗和「門檻被移動」大多卡在修復這一側。",
    "拿掉自動修復：Codex 只讀審查，人取捨後，Claude 才改被採納的那幾條。",
    "文件審查 15 個 run，<b>10 個</b>走到人工審查", "l7")

# 20 收尾 ---------------------------------------------------------------
inner = ln("M-20 1000 H1940", "ink", .2, 12) + signal(300, 990, "l4", .5, .7) + signal(900, 990, "l4", .6, .7) + gate(1500, 1000, "", "", "l2", .7)
add(f"""
{svg(inner)}
<h2 class="big reveal" style="top:180px;font-size:150px;--d:.1s">AI 互相檢查，<br><span class="amber">人類</span>最後放行。</h2>
<div class="term-card reveal" style="left:110px;top:560px;width:1180px;--d:.3s">
  <p class="c" style="font-size:20px;margin-bottom:10px"># 安裝</p>
  <p class="cmdline">git clone https://github.com/peter6601/ai-review.git<br>cd ai-review &amp;&amp; python3 install_skills.py --apply</p>
  <p class="c" style="font-size:20px;margin:16px 0 10px"># 在 Claude Code 或 Codex 裡說</p>
  <p class="cmdline">使用 consensus-plan 審查 docs/spec.md</p></div>
<div class="abs reveal" style="left:1380px;top:180px;width:430px;height:500px;background:#fff;border:5px solid var(--ink);border-radius:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px;--d:.35s">
  <div style="width:320px;height:320px">{QR.replace('<svg ', '<svg style="width:320px;height:320px;max-width:none;max-height:none" ')}</div>
  <p style="font:700 18px/1 var(--mono);color:var(--muted)">github.com/peter6601/ai-review</p></div>
<p class="abs reveal" style="left:1380px;top:720px;width:430px;text-align:center;font:600 24px/1.5 var(--cjk);color:var(--muted);--d:.5s">系列：<a href="../" style="color:var(--l3)">ios-dev 路網圖</a>・<a href="../vibe/" style="color:var(--l4)">vibe 直達車</a></p>""", "開場", "l2")

assert len(slides) == 20, len(slides)
HTML = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Codex 審、Claude 修，人放行 — ai-review</title>
<meta name="description" content="ai-review 共識審查工作流簡報：Codex 唯讀審查、Claude 有限修復、人類最後放行。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Overpass:wght@400;600;700;800;900&family=Overpass+Mono:wght@500;700&family=Noto+Sans+TC:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="edit-hotzone" aria-hidden="true"></div>
<button class="edit-toggle" id="editToggle" title="編輯模式 (E)">編輯 (E)</button>
<div class="toast" id="toast" role="status"></div>
<div class="deck-viewport">
<main class="deck-stage" id="deckStage" aria-label="ai-review 簡報">
{chr(10).join(slides)}
</main>
<div class="progress" id="progress"></div>
</div>
<script>{JS}</script>
</body>
</html>
"""
pathlib.Path(OUT).write_text(HTML)
print(f"wrote {OUT}: {len(slides)} slides")
