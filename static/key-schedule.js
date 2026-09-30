/*
 * DES Key Schedule Visualizer (Section 3)
 * Mounts into #key-schedule. Gets the schedule from the Flask endpoint
 * POST /api/key-schedule (crypto_engine.get_key_schedule).
 */
(function () {
  'use strict';

  const SAMPLE_KEY = '133457799BBCDFF1';
  const $ = (id) => document.getElementById(id);
  let data = null;   // current schedule
  let shown = 0;     // number of rounds revealed (0-16)

  // ---- helpers -----------------------------------------------------------
  const group = (bits, n, cls) => {
    let out = '';
    for (let i = 0; i < bits.length; i += n) {
      out += '<span class="grp">' + (cls ? cls(bits.slice(i, i + n), i) : bits.slice(i, i + n)) + '</span>';
    }
    return out;
  };
  const bitsToHex = (b) => b.match(/.{4}/g).map(x => parseInt(x, 2).toString(16)).join('').toUpperCase();

  async function fetchSchedule(key) {
    let res, body;
    try {
      res = await fetch('/api/key-schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: key })
      });
      body = await res.json();
    } catch (e) {
      throw new Error('Could not reach the server. Is the Flask app running?');
    }
    if (!res.ok || body.error) throw new Error(body && body.error ? body.error : 'Server error ' + res.status + '.');
    const okShape = Array.isArray(body.round_keys_binary) && body.round_keys_binary.length === 16 && /^[01]{48}$/.test(body.round_keys_binary[0]) &&
      Array.isArray(body.c) && body.c.length === 17 && Array.isArray(body.d) && body.d.length === 17 &&
      Array.isArray(body.shifts) && /^[01]{64}$/.test(body.original_64) && /^[01]{56}$/.test(body.pc_1);
    if (!okShape) throw new Error('The server returned the key schedule in an unexpected format.');
    return { keyBits: body.original_64, pc1: body.pc_1, C: body.c, D: body.d, shifts: body.shifts, roundKeys: body.round_keys_binary };
  }

  function validate(raw) {
    const key = raw.replace(/\s+/g, '').replace(/^0x/i, '');  // ignore spaces and a leading 0x
    if (!key) return { error: 'Please enter a DES key.' };
    if (!/^[0-9a-fA-F]+$/.test(key)) return { error: 'Key must contain only hex characters (0-9, A-F).' };
    if (key.length !== 16) return { error: 'Key must be exactly 16 hex characters (64 bits). You entered ' + key.length + '.' };
    return { key: key.toUpperCase() };
  }

  // ---- rendering ---------------------------------------------------------
  function renderStatic() {
    // Parity bit = every 8th bit of the 64-bit key (dropped by PC-1)
    $('ks-key64').innerHTML = group(data.keyBits, 8, (g) => g.slice(0, 7) + '<i class="parity">' + g[7] + '</i>');
    $('ks-key64-hex').textContent = bitsToHex(data.keyBits);
    $('ks-key56').innerHTML = group(data.pc1, 7);
    $('ks-c0').innerHTML = group(data.C[0], 7);
    $('ks-d0').innerHTML = group(data.D[0], 7);
    $('ks-rounds').innerHTML = data.roundKeys.map((k, i) => {
      const n = data.shifts[i];
      const wrap = (bits) => bits.slice(0, 28 - n) + '<i class="ks-wrap">' + bits.slice(28 - n) + '</i>';
      return '<tr id="ks-row-' + (i + 1) + '" hidden>' +
        '<th scope="row">' + (i + 1) + '</th>' +
        '<td>' + n + '</td>' +
        '<td class="bits">' + wrap(data.C[i + 1]) + '</td>' +
        '<td class="bits">' + wrap(data.D[i + 1]) + '</td>' +
        '<td class="bits">' + group(k, 6) + '</td>' +
        '<td class="hex">' + bitsToHex(k) + '</td></tr>';
    }).join('');
    $('ks-keys').innerHTML = data.roundKeys.map((k, i) =>
      '<li id="ks-k-' + (i + 1) + '" hidden><b>K' + (i + 1) + '</b><code>' + bitsToHex(k) + '</code></li>').join('');
  }

  function update() {
    for (let i = 1; i <= 16; i++) {
      const on = i <= shown;
      $('ks-row-' + i).hidden = !on;
      $('ks-k-' + i).hidden = !on;
      $('ks-row-' + i).classList.toggle('current', i === shown && shown < 16);
    }
    $('ks-progress').textContent = shown === 0 ? 'Start at C0 / D0, then step through the rounds.'
      : 'Showing round ' + shown + ' of 16 (C' + shown + ', D' + shown + ' → K' + shown + ')';
    $('ks-prev').disabled = shown === 0;
    $('ks-next').disabled = shown === 16;
    $('ks-stage').hidden = false;
  }

  // ---- actions -----------------------------------------------------------
  function showError(msg) {
    const err = $('ks-error');
    err.textContent = msg.indexOf('❌') === 0 ? msg : '❌ Error: ' + msg;
    err.hidden = false;
    $('ks-stage').hidden = true;
  }

  let reqId = 0;
  async function generate() {
    const v = validate($('ks-input').value);
    if (v.error) { showError(v.error); return; }
    const id = ++reqId;
    $('ks-generate').disabled = true;
    try {
      const s = await fetchSchedule(v.key);
      if (id !== reqId) return;
      data = s;
      $('ks-error').hidden = true;
      renderStatic();
      shown = 0;
      update();
    } catch (e) {
      if (id === reqId) showError(e.message);
    } finally {
      if (id === reqId) $('ks-generate').disabled = false;
    }
  }

  function init() {
    if (!$('key-schedule')) return;
    const input = $('ks-input'), count = $('ks-key-count'), btn = $('ks-generate');
    function sync() {
      const v = input.value.toUpperCase();
      if (v !== input.value) input.value = v;
      const ok = v.length === 16 && /^[0-9A-F]+$/.test(v);
      count.textContent = v.length + '/16';
      count.classList.toggle('ok', ok);
      btn.disabled = !ok;
    }
    input.addEventListener('input', sync);
    sync();
    btn.addEventListener('click', generate);
    $('ks-input').addEventListener('keydown', (e) => { if (e.key === 'Enter') generate(); });
    $('ks-sample').addEventListener('click', () => { input.value = SAMPLE_KEY; sync(); generate(); });
    $('ks-prev').addEventListener('click', () => { if (data && shown > 0) { shown--; update(); } });
    $('ks-next').addEventListener('click', () => { if (data && shown < 16) { shown++; update(); } });
    $('ks-all').addEventListener('click', () => { if (data) { shown = 16; update(); } });
    $('ks-reset').addEventListener('click', () => { if (data) { shown = 0; update(); } });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
