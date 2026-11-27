"""Shared frame for article covers (1200x630 SVG).

Usage from a script:
    import sys; sys.path.insert(0, "tools")
    from cover_frame import frame, C
    svg = frame(("Title line 1", "Title line 2"), "Subtitle", "CODE  /  Topic", diagram_svg)

The diagram is placed by the caller, normally in the right half (x 600..1140).
Available classes: t1 t2 chip brand l s m ms box cu te amb lc lt lm dash tc tt ta;
arrow markers: url(#ac) copper, url(#at) teal, url(#am) grey.
Render to PNG with tools/render_covers.py.
"""

C = dict(BG="#0f1b2d", GRID="#18283d", TXT="#e9eef5", MUTED="#9aa8ba", CU="#f08a4b",
         TE="#43c2b8", AM="#f2b65a", BOX="#15253a", ST="#34465d")


def frame(title_lines, subtitle, chip, diagram):
    c = C
    t1, t2 = title_lines
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<defs>
  <pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{c['GRID']}" stroke-width="1"/></pattern>
  <marker id="ac" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['CU']}"/></marker>
  <marker id="at" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['TE']}"/></marker>
  <marker id="am" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c['MUTED']}"/></marker>
  <style>
    .t1{{font:600 60px 'IBM Plex Sans Condensed';fill:{c['TXT']};letter-spacing:-0.5px}}
    .t2{{font:500 30px 'IBM Plex Sans Condensed';fill:{c['MUTED']}}}
    .chip{{font:500 18px 'IBM Plex Mono';fill:{c['CU']}}}
    .brand{{font:600 22px 'IBM Plex Sans Condensed';fill:{c['TXT']}}}
    .l{{font:500 17px 'IBM Plex Sans';fill:{c['TXT']}}}
    .s{{font:400 14px 'IBM Plex Sans';fill:{c['MUTED']}}}
    .m{{font:500 15px 'IBM Plex Mono';fill:{c['TXT']}}}
    .ms{{font:400 13px 'IBM Plex Mono';fill:{c['MUTED']}}}
    .box{{fill:{c['BOX']};stroke:{c['ST']};stroke-width:1.5}}
    .cu{{fill:#3a2416;stroke:{c['CU']};stroke-width:2}}
    .te{{fill:#123331;stroke:{c['TE']};stroke-width:2}}
    .amb{{fill:#352711;stroke:{c['AM']};stroke-width:2}}
    .lc{{fill:none;stroke:{c['CU']};stroke-width:2.5}}
    .lt{{fill:none;stroke:{c['TE']};stroke-width:2.5}}
    .lm{{fill:none;stroke:{c['MUTED']};stroke-width:1.8}}
    .dash{{stroke-dasharray:7 6}}
    .tc{{fill:{c['CU']}}} .tt{{fill:{c['TE']}}} .ta{{fill:{c['AM']}}}
  </style>
</defs>
<rect width="1200" height="630" fill="{c['BG']}"/>
<rect width="1200" height="630" fill="url(#g)"/>
<rect x="0" y="0" width="1200" height="6" fill="{c['CU']}"/>
<text class="chip" x="64" y="88">{chip}</text>
<text class="t1" x="64" y="168">{t1}</text>
<text class="t1" x="64" y="236">{t2}</text>
<text class="t2" x="64" y="292">{subtitle}</text>
<g transform="translate(64,548)">
  <g transform="rotate(-8 8 14)"><rect x="0" y="0" width="7" height="18" rx="2" fill="{c['CU']}"/><rect x="11" y="4" width="7" height="11" rx="2" fill="{c['CU']}"/><rect x="0" y="22" width="7" height="11" rx="2" fill="{c['CU']}"/><rect x="11" y="19" width="7" height="18" rx="2" fill="{c['CU']}"/></g>
  <text class="brand" x="32" y="26">LowLevel <tspan fill="{c['CU']}">Labs</tspan></text>
  <text class="s" x="190" y="25">lowlevellabs.in</text>
</g>
{diagram}
</svg>
'''
