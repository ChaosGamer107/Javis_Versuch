import math
import time
import pygame

NUM_BANDS=48
CENTER_TEXT="NOVA"

_state={
    "bands":[],
    "text":"",
    "mode":"idle"
}

MODES={
    "idle":("",(90,110,150)),
    "listening":("Ich höre...",(80,200,140)),
    "thinking":("Nova denkt...",(240,190,80)),
    "speaking":("Nova spricht...",(70,170,255)),
}

BACKGROUND=(11,15,20)
CORE_COLOR=(16,22,30)
FIELD_COLOR=(24,30,38)
FIELD_BORDER=(48,58,70)
TEXT_COLOR=(225,232,240)
HINT_COLOR=(110,122,136)

def set_bands(values):

    if values is None:
        _state["bands"]=[]
    else:
        _state["bands"]=[max(0.0, min(1.0, float(v))) for v in values]

def set_text(text):
    _state["text"]=str(text)

def set_mode(mode):
    _state["mode"]=mode if mode in MODES else "idle"

def close():
    pygame.event.post(pygame.event.Event(pygame.QUIT))

def _fit(text, font, max_width):

    if font.size(text)[0] <= max_width:
        return text

    while text and font.size("_"+text)[0] > max_width:
        text=text[1:]

    return "_"+text

def _mix(color, amount):
    return tuple(int(c+(255-c)*amount) for c in color)

def _draw_visualizer(screen, center, radius, bands, color):

    count=len(bands)*2
    max_length=radius*0.9
    bar_width=max(2, int(radius*0.035))
    reach=int(radius+max_length+bar_width*4)

    now=time.time()
    overall=sum(bands)/len(bands)

    segments=[]

    for i in range(count):

        distance=min(i, count-1, len(bands)-1)
        band=len(bands)-1-distance

        idle=0.04+0.03*math.sin(now*2+i*0.5)

        value=max(bands[band], idle)

        angle=math.pi/2+2*math.pi*i/count
        dx=math.cos(angle)
        dy=math.sin(angle)

        inner=radius
        outer=radius+4+value*max_length

        segments.append((dx, dy, inner, outer, _mix(color, min(1.0, value)*0.6)))

    glow=pygame.Surface((reach*2, reach*2), pygame.SRCALPHA)

    for dx, dy, inner, outer, bar_color in segments:
        pygame.draw.line(
            glow,
            (*color, 40),
            (reach+dx*inner, reach+dy*inner),
            (reach+dx*outer, reach+dy*outer),
            bar_width*3
        )

    screen.blit(glow, (center[0]-reach, center[1]-reach))

    pygame.draw.circle(screen, CORE_COLOR, center, max(1, int(radius-12)))
    pygame.draw.circle(screen, _mix(color, 0.2), center, max(1, int(radius-12)), 2)

    dot_radius=radius-6+overall*6
    dot_color=_mix(color, 0.5)

    for k in range(90):
        a=2*math.pi*k/90
        pygame.draw.circle(
            screen,
            dot_color,
            (int(center[0]+math.cos(a)*dot_radius), int(center[1]+math.sin(a)*dot_radius)),
            2
        )

    for dx, dy, inner, outer, bar_color in segments:
        pygame.draw.line(
            screen,
            bar_color,
            (center[0]+dx*inner, center[1]+dy*inner),
            (center[0]+dx*outer, center[1]+dy*outer),
            bar_width
        )

def run():

    pygame.display.init()
    pygame.font.init()

    pygame.display.set_mode((720,640), pygame.RESIZABLE)
    pygame.display.set_caption("Nova")

    clock=pygame.time.Clock()

    font=pygame.font.SysFont("segoeui", 26)
    small_font=pygame.font.SysFont("segoeui", 20)
    title_font=pygame.font.SysFont("segoeui", 44, bold=True)

    title=title_font.render(CENTER_TEXT, True, TEXT_COLOR) if CENTER_TEXT else None

    shown=[0.0]*NUM_BANDS
    running=True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        screen=pygame.display.get_surface()
        width, height=screen.get_size()

        screen.fill(BACKGROUND)

        target=_state["bands"]

        for i in range(NUM_BANDS):

            goal=target[i] if i < len(target) else 0.0

            if goal > shown[i]:
                shown[i]+=(goal-shown[i]) *0.6
            else:
                shown[i]+=(goal-shown[i])*0.15

        label, color=MODES.get(_state["mode"], MODES["idle"])

        radius=max(50, min(width, height-160)*0.2)
        center=(width//2, (height-140)//2)

        _draw_visualizer(screen, center, radius, shown, color)

        if title:
            screen.blit(
                title,
                (center[0]-title.get_width()//2, center[1]-title.get_height()//2)
            )

        margin=24
        field=pygame.Rect(margin, height-margin-54, width-2*margin, 54)

        pygame.draw.rect(screen, FIELD_COLOR, field, border_radius=14)
        pygame.draw.rect(screen, FIELD_BORDER, field, width=2, border_radius=14)

        text=_state["text"]
        max_text_width=field.width-32

        if text:
            rendered=font.render(_fit(text, font, max_text_width), True, TEXT_COLOR)
        else:
            rendered=font.render("Sag etwas...", True, HINT_COLOR)

        screen.blit(rendered, (field.x+16, field.centery-rendered.get_height()//2))

        if label:
            status=small_font.render(label, True, HINT_COLOR)
            screen.blit(status, (field.x+4, field.y-status.get_height()-8))

        pygame.display.flip()
        clock.tick(60)

    pygame.display.quit()