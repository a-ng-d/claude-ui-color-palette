# Report template

The readability report is one HTML file assembled from three parts, in this order:

1. the `report-head` block below, verbatim
2. the report data JSON (see the data contract in `SKILL.md`), with every `<` written as `<`
3. the `report-tail` block below, verbatim

The page renders itself in the browser: color-space conversions, WCAG levels, readability scores and the synthesis are computed by the inline script, so the same data always gives the same document. It needs no network access.

Do not edit the blocks when assembling a report. Change them here, then regenerate the reports.

```html report-head
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Readability report</title>
<style>
:root{--bg:#fbfbfa;--surface:#fff;--ink:#1d1d1f;--muted:#6b6b70;--line:#e4e4e7;
--ok:#1f7a4d;--ok-bg:#e6f4ec;--warn:#8a5a00;--warn-bg:#fdf3dc;--bad:#b42318;--bad-bg:#fde8e7}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--surface:#1f1f22;--ink:#ededef;
--muted:#a0a0a8;--line:#323236;--ok:#6fd39c;--ok-bg:#16301f;--warn:#f0c46b;--warn-bg:#33280f;
--bad:#ff8a80;--bad-bg:#3a1714}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
main{max-width:1180px;margin:0 auto;padding:40px 16px 64px}
h1{font-size:28px;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:20px;margin:40px 0 12px}
h3{font-size:15px;margin:28px 0 8px;display:flex;align-items:center;gap:8px}
p{margin:0 0 8px}.muted{color:var(--muted)}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--muted);margin-top:8px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}
.kpi b{display:block;font-size:26px;font-variant-numeric:tabular-nums}
.kpi span{color:var(--muted);font-size:12px}
.verdict{display:inline-block;padding:2px 10px;border-radius:99px;font-weight:600;font-size:13px}
.v-Excellent,.v-Good{background:var(--ok-bg);color:var(--ok)}
.v-Fair{background:var(--warn-bg);color:var(--warn)}.v-Poor{background:var(--bad-bg);color:var(--bad)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.card ul{margin:6px 0 0;padding-left:18px}.card li{margin:3px 0}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:980px;font-variant-numeric:tabular-nums}
table.narrow{min-width:640px}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:600}
tr:last-child td{border-bottom:0}
.sw{display:inline-flex;align-items:center;justify-content:center;width:64px;height:30px;border-radius:6px;font-weight:600;font-size:12px;border:1px solid rgba(127,127,127,.25)}
.dot{width:14px;height:14px;border-radius:4px;display:inline-block;vertical-align:-2px;border:1px solid rgba(127,127,127,.3)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
.tag{display:inline-block;padding:1px 7px;border-radius:5px;font-size:11.5px;font-weight:600}
.t-AAA,.t-AA,.t-ok{background:var(--ok-bg);color:var(--ok)}
.t-AA18,.t-mid{background:var(--warn-bg);color:var(--warn)}.t-FAIL,.t-bad{background:var(--bad-bg);color:var(--bad)}
.src td{font-weight:600}
footer{margin-top:40px;color:var(--muted);font-size:12px}
@media print{body{background:#fff}.scroll{overflow:visible}table{min-width:0;font-size:10px}h2{break-after:avoid}.card,.kpi{break-inside:avoid}}
</style>
</head>
<body>
<main id="app"><noscript>This report renders with JavaScript. Open it in a browser with scripts enabled.</noscript></main>
<script id="report-data" type="application/json">
```

```html report-tail
</script>
<script>
(function () {
  'use strict';

  // ---- Color-space conversions (chroma-js parity: Lab/LCH in D65) ----
  function hexToRgb(hex) {
    var h = String(hex).replace('#', '');
    if (h.length === 3 || h.length === 4) h = h.split('').map(function (c) { return c + c; }).join('');
    return [0, 2, 4].map(function (i) { return parseInt(h.slice(i, i + 2), 16); });
  }
  function lin(c) { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function labF(t) {
    var t0 = 4 / 29, t1 = 6 / 29, t2 = 3 * t1 * t1, t3 = t1 * t1 * t1;
    return t > t3 ? Math.cbrt(t) : t / t2 + t0;
  }
  function rgbToLab(rgb) {
    var r = lin(rgb[0]), g = lin(rgb[1]), b = lin(rgb[2]);
    var x = labF((0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.950470);
    var y = labF(0.2126729 * r + 0.7151522 * g + 0.0721750 * b);
    var z = labF((0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.088830);
    return [Math.max(0, 116 * y - 16), 500 * (x - y), 200 * (y - z)];
  }
  function rgbToOklab(rgb) {
    var r = lin(rgb[0]), g = lin(rgb[1]), b = lin(rgb[2]);
    var l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    var m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    var s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [
      0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
      1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
      0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    ];
  }
  function polar(v) {
    var c = Math.hypot(v[1], v[2]);
    var h = (Math.atan2(v[2], v[1]) * 180 / Math.PI + 360) % 360;
    return [v[0], c, Math.round(c * 10000) === 0 ? null : h];
  }
  function hue(h) { return h === null ? 'none' : h.toFixed(1) + '°'; }
  function hslHsv(rgb) {
    var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255;
    var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn, h = null;
    if (d !== 0) {
      if (mx === r) h = (60 * ((g - b) / d) + 360) % 360;
      else if (mx === g) h = 60 * ((b - r) / d) + 120;
      else h = 60 * ((r - g) / d) + 240;
    }
    var l = (mx + mn) / 2;
    return { h: h, sl: d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1)), l: l, sv: mx === 0 ? 0 : d / mx, v: mx };
  }
  var SPACE_LABELS = {
    OKLCH: 'OKLCH (L C H)', LCH: 'LCH (L C H)', LAB: 'Lab (L a b)', OKLAB: 'OKLab (L a b)',
    HSL: 'HSL', HSV: 'HSV', RGB: 'RGB', CMYK: 'CMYK'
  };
  var FALLBACK_SPACE = 'OKLCH'; // HSLUV, P3 and HEX are shown in OKLCH
  function pct1(v) { return (v * 100).toFixed(1) + '%'; }
  function spaceValue(hex, space) {
    var rgb = hexToRgb(hex), p, v, k;
    switch (space) {
      case 'OKLCH': p = polar(rgbToOklab(rgb)); return pct1(p[0]) + ' ' + p[1].toFixed(3) + ' ' + hue(p[2]);
      case 'LCH': p = polar(rgbToLab(rgb)); return p[0].toFixed(1) + ' ' + p[1].toFixed(1) + ' ' + hue(p[2]);
      case 'LAB': v = rgbToLab(rgb); return v.map(function (x) { return x.toFixed(1); }).join(' ');
      case 'OKLAB': v = rgbToOklab(rgb); return pct1(v[0]) + ' ' + v[1].toFixed(3) + ' ' + v[2].toFixed(3);
      case 'HSL': v = hslHsv(rgb); return hue(v.h) + ' ' + Math.round(v.sl * 100) + '% ' + Math.round(v.l * 100) + '%';
      case 'HSV': v = hslHsv(rgb); return hue(v.h) + ' ' + Math.round(v.sv * 100) + '% ' + Math.round(v.v * 100) + '%';
      case 'RGB': return rgb.join(' ');
      case 'CMYK':
        v = rgb.map(function (c) { return c / 255; });
        k = 1 - Math.max(v[0], v[1], v[2]);
        if (k >= 1) return '0% 0% 0% 100%';
        return v.map(function (c) { return Math.round((1 - c - k) / (1 - k) * 100) + '%'; }).join(' ') + ' ' + Math.round(k * 100) + '%';
      default: return spaceValue(hex, FALLBACK_SPACE);
    }
  }

  // ---- Scoring (shared with ui-color-palette-audit-palette) ----
  var APCA_MAX = 108;
  function wcagLevel(r) { return r >= 7 ? 'AAA' : r >= 4.5 ? 'AA' : r >= 3 ? 'AA18' : 'FAIL'; }
  var WCAG_LABELS = { AAA: 'AAA', AA: 'AA', AA18: 'AA large', FAIL: 'Fail' };
  var USAGE_LABELS = {
    FLUENT_TEXT: 'Fluent text', CONTENT_TEXT: 'Content text', BODY_TEXT: 'Body text', HEADLINES: 'Headlines',
    SPOT_TEXT: 'Spot text', NON_TEXT: 'Non-text', AVOID: 'Avoid', UNKNOWN: 'Unknown'
  };
  function readability(lc, weight) {
    var f = weight < 400 ? 0.85 : weight > 500 ? 1.15 : 1;
    return Math.round(Math.min(100, Math.abs(lc) / APCA_MAX * 100 * f));
  }
  function verdict(s) { return s >= 90 ? 'Excellent' : s >= 75 ? 'Good' : s >= 50 ? 'Fair' : 'Poor'; }
  function num(v) { v = Number(v); return isFinite(v) ? v : 0; }
  function get(o, path) { return path.reduce(function (a, k) { return a && a[k] !== undefined ? a[k] : undefined; }, o); }

  function analyze(row) {
    var sides = {};
    ['light', 'dark'].forEach(function (side) {
      var ratio = num(get(row, ['textContrast', 'wcag', side, 'ratio']));
      var lc = num(get(row, ['textContrast', 'apca', side, 'lc']));
      sides[side] = {
        ratio: ratio, level: wcagLevel(ratio), lc: lc,
        usage: get(row, ['textContrast', 'apca', side, 'recommendedUsage']) || 'UNKNOWN',
        read400: readability(lc, 400), read700: readability(lc, 700)
      };
    });
    var best = Math.abs(sides.dark.lc) > Math.abs(sides.light.lc) ? 'dark' : 'light';
    if (sides.dark.ratio !== sides.light.ratio) {
      var bestW = sides.dark.ratio > sides.light.ratio ? 'dark' : 'light';
      if (wcagLevel(sides[bestW].ratio) !== wcagLevel(sides[best].ratio)) best = bestW;
    }
    var maxRatio = Math.max(sides.light.ratio, sides.dark.ratio);
    var maxLc = Math.max(Math.abs(sides.light.lc), Math.abs(sides.dark.lc));
    var ui = num(get(row, ['contrast', 'wcag', 'ratio']));
    return {
      sides: sides, best: best, wcagPass: maxRatio >= 4.5, apcaPass: maxLc >= 60,
      globalPass: maxRatio >= 4.5 && maxLc >= 60, aaa: maxRatio >= 7, deadZone: maxRatio < 3,
      readability: Math.max(sides.light.read400, sides.dark.read400), uiRatio: ui, uiPass: ui >= 3
    };
  }
  function pct(part, total) { return total ? Math.round(part / total * 100) : 0; }
  function count(list, key) { return list.filter(function (a) { return a[key]; }).length; }
  function scoreBlock(list) {
    var n = list.length, w = count(list, 'wcagPass'), a = count(list, 'apcaPass');
    var wr = pct(w, n), ar = pct(a, n);
    return {
      shades: n, wcagPass: w, wcagRate: wr, apcaPass: a, apcaRate: ar, aaa: count(list, 'aaa'),
      globalScore: Math.round((wr + ar) / 2), deadZone: count(list, 'deadZone'),
      readabilityIndex: n ? Math.round(list.reduce(function (s, x) { return s + x.readability; }, 0) / n) : 0
    };
  }

  // ---- Rendering ----
  function esc(v) {
    return String(v === undefined || v === null ? '' : v).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function lcTag(lc) {
    var a = Math.abs(lc), c = a >= 60 ? 'ok' : a >= 45 ? 'mid' : 'bad';
    return '<span class="tag t-' + c + '">Lc ' + a.toFixed(1) + '</span>';
  }
  function wcagTag(s) { return '<span class="tag t-' + s.level + '">' + s.ratio.toFixed(2) + ':1 · ' + WCAG_LABELS[s.level] + '</span>'; }
  function readTag(v) { var c = v >= 56 ? 'ok' : v >= 42 ? 'mid' : 'bad'; return '<span class="tag t-' + c + '">' + v + '%</span>'; }
  function verdictTag(s) { var v = verdict(s); return '<span class="verdict v-' + v + '">' + s + '% · ' + v + '</span>'; }

  function table(items, space, text) {
    var head = '<tr><th>Shade</th><th>Swatch</th><th>Hex</th><th>' + esc(SPACE_LABELS[space]) + '</th>' +
      '<th>WCAG · light text</th><th>WCAG · dark text</th><th>APCA · light text</th><th>APCA · dark text</th>' +
      '<th>Readability 400 / 700</th><th>Best text</th><th>UI vs bg</th></tr>';
    var body = items.map(function (it) {
      var r = it.row, a = it.a, fg = text[a.best], b = a.sides[a.best], src = r.type === 'source color';
      return '<tr class="' + (src ? 'src' : '') + '"><td>' + esc(r.shade) + (src ? ' ★' : '') + '</td>' +
        '<td><span class="sw" style="background:' + esc(r.hex) + ';color:' + esc(fg) + '">Aa</span></td>' +
        '<td class="mono">' + esc(String(r.hex).toUpperCase()) + '</td>' +
        '<td class="mono">' + esc(spaceValue(r.hex, space)) + '</td>' +
        '<td>' + wcagTag(a.sides.light) + '</td><td>' + wcagTag(a.sides.dark) + '</td>' +
        '<td>' + lcTag(a.sides.light.lc) + ' <span class="muted">' + esc(USAGE_LABELS[a.sides.light.usage] || '') + '</span></td>' +
        '<td>' + lcTag(a.sides.dark.lc) + ' <span class="muted">' + esc(USAGE_LABELS[a.sides.dark.usage] || '') + '</span></td>' +
        '<td>' + readTag(b.read400) + ' ' + readTag(b.read700) + '</td>' +
        '<td><span class="dot" style="background:' + esc(fg) + '"></span> ' + (a.best === 'dark' ? 'Dark' : 'Light') + '</td>' +
        '<td><span class="tag t-' + (a.uiPass ? 'ok' : 'bad') + '">' + a.uiRatio.toFixed(2) + ':1</span></td></tr>';
    }).join('');
    return '<div class="scroll"><table><thead>' + head + '</thead><tbody>' + body + '</tbody></table></div>';
  }

  function findings(perColor, overall) {
    var out = [];
    function label(c) { return '<b>' + esc(c.theme) + ' · ' + esc(c.name) + '</b>'; }
    function plural(list) { return (list.length > 1 ? 'shades ' : 'shade ') + list.join(', '); }
    var ranked = perColor.slice().sort(function (x, y) { return y.score.globalScore - x.score.globalScore; });
    if (ranked.length > 1 && ranked[0].score.globalScore !== ranked[ranked.length - 1].score.globalScore) {
      var lo = ranked[ranked.length - 1];
      out.push('Strongest color: ' + label(ranked[0]) + ' (' + ranked[0].score.globalScore + '%) — weakest: ' +
        label(lo) + ' (' + lo.score.globalScore + '%).');
    }
    perColor.forEach(function (c) {
      function shades(test) { return c.items.filter(function (it) { return test(it.a); }).map(function (it) { return esc(it.row.shade); }); }
      var mid = shades(function (a) { return a.wcagPass && !a.apcaPass; });
      if (mid.length) out.push(label(c) + ': ' + plural(mid) + ' pass WCAG AA but stay under APCA Lc 60 — keep them for headlines, large or bold text.');
      var dead = shades(function (a) { return a.deadZone; });
      if (dead.length) out.push(label(c) + ': ' + plural(dead) + ' stay below 3:1 with both text colors — reserve them for decoration or large surfaces without text.');
      var dark = shades(function (a) { return a.best === 'dark' && a.globalPass; });
      var light = shades(function (a) { return a.best === 'light' && a.globalPass; });
      var parts = [];
      if (dark.length) parts.push('dark text on ' + dark.join(', '));
      if (light.length) parts.push('light text on ' + light.join(', '));
      if (parts.length) out.push(label(c) + ' — body text safe with ' + parts.join('; ') + '.');
    });
    if (overall.shades && overall.aaa === 0) out.push('No shade reaches WCAG AAA (7:1) with either text color.');
    return out;
  }

  function render(data) {
    var palette = data.palette || {};
    var space = String(palette.colorSpace || 'LCH').toUpperCase();
    var shown = SPACE_LABELS[space] ? space : FALLBACK_SPACE;
    var themes = {};
    (data.themes || []).forEach(function (t) { if (t && t.name) themes[t.name] = t; });
    var rows = Array.isArray(data.rows) ? data.rows : [];
    if (!rows.length) return '<p>No palette rows in the report data.</p>';

    var groups = [], index = {};
    rows.forEach(function (r) {
      var key = (r.theme || 'None') + '\u0000' + (r.color || '');
      if (!index[key]) { index[key] = { theme: r.theme || 'None', name: r.color || '', rows: [] }; groups.push(index[key]); }
      index[key].rows.push(r);
    });

    var perColor = [], all = [], sections = [], currentTheme = null, themeCount = 0;
    groups.forEach(function (g) {
      var t = themes[g.theme] || {}, tc = t.textColors || {};
      var text = { light: tc.light || '#FFFFFF', dark: tc.dark || '#000000' };
      var items = g.rows.map(function (r) { return { row: r, a: analyze(r) }; });
      var shadeItems = items.filter(function (it) { return it.row.type !== 'source color'; });
      var score = scoreBlock(shadeItems.map(function (it) { return it.a; }));
      shadeItems.forEach(function (it) { all.push(it.a); });
      perColor.push({ theme: g.theme, name: g.name, items: shadeItems, score: score });
      if (g.theme !== currentTheme) {
        currentTheme = g.theme; themeCount++;
        var bg = t.paletteBackground || '#FFFFFF';
        sections.push('<h2>Theme · ' + esc(g.theme) + '</h2><p class="muted">Background <span class="dot" style="background:' +
          esc(bg) + '"></span> <span class="mono">' + esc(bg) + '</span> · light text <span class="mono">' + esc(text.light) +
          '</span> · dark text <span class="mono">' + esc(text.dark) + '</span></p>');
      }
      var src = g.rows.filter(function (r) { return r.type === 'source color'; })[0];
      sections.push('<h3>' + (src ? '<span class="dot" style="background:' + esc(src.hex) + '"></span>' : '') + esc(g.name) +
        ' ' + verdictTag(score.globalScore) + '</h3>' + table(items, shown, text));
    });

    var overall = scoreBlock(all), v = verdict(overall.globalScore), syn = data.synthesis || {};
    var headline = syn.headline || (v + ' overall readability: ' + overall.wcagPass + ' of ' + overall.shades +
      ' shades carry WCAG AA body text and ' + overall.apcaPass + ' reach APCA Lc 60 with at least one text color.');
    var recos = Array.isArray(syn.recommendations) ? syn.recommendations : [];
    var preset = palette.preset && typeof palette.preset === 'object' ? (palette.preset.name || palette.preset.id) : palette.preset;
    var meta = ['Color space · ' + esc(space)];
    if (shown !== space) meta.push('values shown in ' + shown);
    if (preset) meta.push('Preset · ' + esc(preset));
    if (palette.algorithmVersion) meta.push('Algorithm · ' + esc(palette.algorithmVersion));
    meta.push('Themes · ' + themeCount);
    meta.push('Generated · ' + esc(data.generatedAt || new Date().toISOString().slice(0, 10)));
    var kpis = [
      [overall.globalScore + '%', 'Global contrast score'],
      [overall.wcagRate + '%', 'WCAG 2.2 AA · ' + overall.wcagPass + '/' + overall.shades + ' shades'],
      [overall.apcaRate + '%', 'APCA body text · ' + overall.apcaPass + '/' + overall.shades + ' shades'],
      [overall.readabilityIndex + '%', 'Readability index (400)'],
      [String(overall.aaa), 'Shades reaching AAA'],
      [String(overall.deadZone), 'Shades unusable for text']
    ];
    var name = palette.name || 'Untitled palette';
    document.title = name + ' — Readability report';

    return '<p class="muted">UI Color Palette · Readability report</p><h1>' + esc(name) + '</h1>' +
      (palette.description ? '<p class="muted">' + esc(palette.description) + '</p>' : '') +
      '<div class="meta">' + meta.map(function (m) { return '<span>' + m + '</span>'; }).join('') + '</div>' +
      '<h2>Synthesis <span class="verdict v-' + v + '">' + v + '</span></h2>' +
      '<div class="kpis">' + kpis.map(function (k) { return '<div class="kpi"><b>' + k[0] + '</b><span>' + esc(k[1]) + '</span></div>'; }).join('') + '</div>' +
      '<div class="card"><p><b>' + esc(headline) + '</b></p><ul>' +
      findings(perColor, overall).map(function (f) { return '<li>' + f + '</li>'; }).join('') + '</ul>' +
      (recos.length ? '<p style="margin-top:12px"><b>Recommendations</b></p><ul>' + recos.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ul>' : '') +
      '</div><h2>By color</h2><div class="scroll"><table class="narrow"><thead><tr><th>Theme</th><th>Color</th><th>Global</th>' +
      '<th>WCAG AA</th><th>APCA Lc 60</th><th>Readability</th><th>No-text shades</th><th>Verdict</th></tr></thead><tbody>' +
      perColor.map(function (c) {
        return '<tr><td>' + esc(c.theme) + '</td><td>' + esc(c.name) + '</td><td>' + c.score.globalScore + '%</td><td>' +
          c.score.wcagRate + '%</td><td>' + c.score.apcaRate + '%</td><td>' + c.score.readabilityIndex + '%</td><td>' +
          c.score.deadZone + '</td><td><span class="verdict v-' + verdict(c.score.globalScore) + '">' + verdict(c.score.globalScore) + '</span></td></tr>';
      }).join('') + '</tbody></table></div>' + sections.join('') +
      '<h2>Method</h2><div class="card muted">' +
      '<p><b>WCAG 2.2</b> — contrast ratio of the light and dark text colors on each shade (SC 1.4.3 / 1.4.6: AA ≥ 4.5:1, AAA ≥ 7:1, “AA large” ≥ 3:1 for text ≥ 24px or ≥ 18.66px bold). “UI vs bg” is the shade against the theme background, checked against SC 1.4.11 (non-text contrast ≥ 3:1). These thresholds are unchanged from WCAG 2.1.</p>' +
      '<p><b>APCA</b> — lightness contrast Lc (the method drafted for WCAG 3, not yet a W3C standard) with the engine’s recommended usage: fluent text ≥ 90, content text ≥ 75, body text ≥ 60, headlines ≥ 45, spot text ≥ 30, non-text ≥ 15.</p>' +
      '<p><b>Readability</b> — |Lc| rescaled to 100 (Lc 108 = 100%), × 0.85 below weight 400, × 1.15 above 500, capped at 100%, for the best text color. Same formula as the plugin’s contrast report.</p>' +
      '<p><b>Global contrast score</b> — average of the WCAG AA pass rate and the APCA Lc 60 pass rate; a shade passes when at least one of the two text colors meets the threshold. Source colors (★) are listed but not counted. Verdict: Excellent ≥ 90%, Good ≥ 75%, Fair ≥ 50%, Poor below.</p>' +
      '<p>Contrast values come from the UI Color Palette API. Color-space values are derived from the hex with the engine’s formulas.</p></div>' +
      '<footer>Generated with the UI Color Palette plugin for Claude.</footer>';
  }

  var app = document.getElementById('app');
  try {
    app.innerHTML = render(JSON.parse(document.getElementById('report-data').textContent));
  } catch (e) {
    app.innerHTML = '<p>The report data could not be read: ' + esc(e.message) + '</p>';
  }
})();
</script>
</body>
</html>
```
