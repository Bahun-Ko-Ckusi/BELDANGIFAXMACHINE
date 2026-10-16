/* The desk in the hero: three objects you can turn and poke.
   Everything here is built from primitives — no model files to download. */

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.min.js";

const canvas = document.getElementById("scene");
const hint = document.getElementById("hint");
const picks = [...document.querySelectorAll(".pick")];
const readouts = [...document.querySelectorAll(".readout")];
const fallback = document.querySelector(".stage-fallback");

const calm = matchMedia("(prefers-reduced-motion: reduce)");
const night = matchMedia("(prefers-color-scheme: dark)");

function giveUp(why) {
  if (why) console.warn("3D hero off:", why);
  canvas.remove();
  if (hint) hint.remove();
  if (fallback) fallback.hidden = false;
}

let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
} catch (e) {
  giveUp(e);
}

function boot() {
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 80);
  camera.position.set(0, 2.75, 7.6);
  camera.lookAt(0, 0.85, 0);

  /* ── palette, in step with the page ───────────────────────────────── */

  const skin = {
    day:   { deck: 0xe6eae8, rim: 0xffffff, sky: 0xffffff, ground: 0x97a3a0, key: 2.1, fill: 0.5 },
    night: { deck: 0x1d2322, rim: 0x2b3331, sky: 0x9fb2c9, ground: 0x101414, key: 1.7, fill: 0.7 }
  };
  const BLUE = 0x1038b5, HOT = 0xc8156b, SHELL = 0x1a1d1d, PAPER = 0xf4f6f5;

  /* ── light ────────────────────────────────────────────────────────── */

  const hemi = new THREE.HemisphereLight(0xffffff, 0x97a3a0, 0.55);
  scene.add(hemi);

  const key = new THREE.DirectionalLight(0xffffff, 2.1);
  key.position.set(3.4, 6.2, 4.2);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.near = 1;
  key.shadow.camera.far = 20;
  key.shadow.camera.left = key.shadow.camera.bottom = -6;
  key.shadow.camera.right = key.shadow.camera.top = 6;
  key.shadow.bias = -0.0008;
  key.shadow.radius = 3;
  scene.add(key);

  const fill = new THREE.DirectionalLight(0xdfe8ff, 0.5);
  fill.position.set(-4.5, 2.5, -2);
  scene.add(fill);

  /* ── the desk ─────────────────────────────────────────────────────── */

  const desk = new THREE.Group();
  desk.position.y = -0.55;
  scene.add(desk);

  const deckMat = new THREE.MeshStandardMaterial({ color: skin.day.deck, roughness: 0.78, metalness: 0 });
  const deck = new THREE.Mesh(new THREE.CylinderGeometry(3.5, 3.5, 0.34, 72), deckMat);
  deck.position.y = -0.17;
  deck.receiveShadow = true;
  desk.add(deck);

  const rimMat = new THREE.MeshStandardMaterial({ color: skin.day.rim, roughness: 0.5 });
  const rim = new THREE.Mesh(new THREE.TorusGeometry(3.5, 0.045, 10, 80), rimMat);
  rim.rotation.x = Math.PI / 2;
  rim.position.y = 0.002;
  desk.add(rim);

  const mat = (color, rough = 0.5, extra = {}) =>
    new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: 0, ...extra });

  const solid = (geo, material, x = 0, y = 0, z = 0) => {
    const m = new THREE.Mesh(geo, material);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    return m;
  };

  const items = {};
  function place(key, group, x, z) {
    group.position.set(x, 0, z);
    group.userData.key = key;
    group.userData.rest = 0;
    items[key] = group;
    desk.add(group);
  }

  /* 1. the fax machine the company is named after */
  const fax = new THREE.Group();
  {
    const shell = mat(SHELL, 0.42);
    const body = solid(new THREE.BoxGeometry(1.7, 0.52, 1.15), shell, 0, 0.26, 0);
    const lip = solid(new THREE.BoxGeometry(1.74, 0.07, 1.19), mat(0x2c3130, 0.35), 0, 0.53, 0);
    const tray = solid(new THREE.BoxGeometry(1.5, 0.06, 0.78), mat(0x232827, 0.4), 0, 0.72, -0.26);
    tray.rotation.x = -0.34;
    const slot = solid(new THREE.BoxGeometry(1.25, 0.05, 0.12), mat(0x07090a, 0.9), 0, 0.5, 0.42);
    const roll = solid(new THREE.CylinderGeometry(0.17, 0.17, 1.3, 24), mat(PAPER, 0.85), 0, 0.82, -0.5);
    roll.rotation.z = Math.PI / 2;

    const sheet = solid(new THREE.BoxGeometry(1.1, 0.012, 0.82), mat(PAPER, 0.95), 0, 0.5, 0.45);
    sheet.visible = false;
    // a line of blue toner, so you can see the page is printed on
    const strip = solid(new THREE.BoxGeometry(0.62, 0.014, 0.05), mat(BLUE, 0.6), -0.12, 0.013, -0.06);
    sheet.add(strip);

    fax.add(body, lip, tray, slot, roll, sheet);
    for (let i = 0; i < 3; i++) {
      const b = solid(new THREE.SphereGeometry(0.055, 18, 14), mat(i === 0 ? HOT : 0x8d9796, 0.35), -0.5 + i * 0.17, 0.57, 0.14);
      fax.add(b);
    }
    const dial = solid(new THREE.TorusGeometry(0.13, 0.035, 10, 28), mat(BLUE, 0.4), 0.5, 0.57, 0.1);
    dial.rotation.x = Math.PI / 2;
    fax.add(dial);
    fax.userData.sheet = sheet;
    fax.userData.send = -1;
  }
  place("fax", fax, -1.95, 0.25);

  /* 2. a petri dish that fruits when you poke it */
  const dish = new THREE.Group();
  {
    const glass = new THREE.MeshPhysicalMaterial({
      color: 0xffffff, roughness: 0.08, metalness: 0,
      transparent: true, opacity: 0.3, transmission: 0.75, thickness: 0.4
    });
    const base = solid(new THREE.CylinderGeometry(0.92, 0.9, 0.12, 48), mat(0xd9dedc, 0.5), 0, 0.06, 0);
    const agar = solid(new THREE.CylinderGeometry(0.84, 0.84, 0.11, 48), mat(0xe8dfb8, 0.55), 0, 0.14, 0);
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(0.94, 0.94, 0.3, 48, 1, true), glass);
    wall.position.y = 0.22;
    dish.add(base, agar, wall);

    const caps = [];
    const spots = [[0, 0, 0.42], [-0.35, 0.22, 0.3], [0.33, -0.26, 0.26]];
    spots.forEach(([x, z, h]) => {
      const shroom = new THREE.Group();
      const stem = solid(new THREE.CylinderGeometry(0.045, 0.07, h, 16), mat(0xf0ead8, 0.72), 0, h / 2, 0);
      const cap = solid(new THREE.SphereGeometry(0.17, 24, 16, 0, Math.PI * 2, 0, Math.PI / 1.85), mat(0xb0472a, 0.62), 0, h, 0);
      cap.scale.set(1, 0.62, 1);
      shroom.add(stem, cap);
      shroom.position.set(x, 0.19, z);
      shroom.scale.setScalar(0.001);
      dish.add(shroom);
      caps.push(shroom);
    });
    dish.userData.caps = caps;
    dish.userData.grow = -1;
  }
  place("dish", dish, -0.1, 0.9);

  /* 3. the screen the game is made on */
  const rig = new THREE.Group();
  {
    const stand = solid(new THREE.CylinderGeometry(0.34, 0.42, 0.07, 32), mat(0x2c3130, 0.45), 0, 0.035, 0);
    const neck = solid(new THREE.CylinderGeometry(0.075, 0.085, 0.5, 20), mat(0x2c3130, 0.45), 0, 0.3, 0);
    const back = solid(new THREE.BoxGeometry(1.8, 1.12, 0.1), mat(SHELL, 0.45), 0, 1.12, -0.02);
    const screen = solid(new THREE.BoxGeometry(1.66, 0.98, 0.03), mat(0x0a1a16, 0.25, {
      emissive: 0x16c08a, emissiveIntensity: 0.45
    }), 0, 1.12, 0.045);
    const bar = solid(new THREE.BoxGeometry(1.5, 0.07, 0.01), mat(0x16c08a, 0.3, {
      emissive: 0x16c08a, emissiveIntensity: 1.6
    }), 0, 1.12, 0.07);
    bar.castShadow = false;
    rig.add(stand, neck, back, screen, bar);
    rig.rotation.y = -0.22;
    rig.userData.screen = screen;
    rig.userData.bar = bar;
    rig.userData.boot = -1;
  }
  place("rig", rig, 1.9, -0.1);

  /* ── skin swap for light / dark ───────────────────────────────────── */

  function dress() {
    const s = night.matches ? skin.night : skin.day;
    deckMat.color.setHex(s.deck);
    rimMat.color.setHex(s.rim);
    hemi.color.setHex(s.sky);
    hemi.groundColor.setHex(s.ground);
    key.intensity = s.key;
    fill.intensity = s.fill;
  }
  dress();
  night.addEventListener("change", dress);

  /* ── picking and turning ──────────────────────────────────────────── */

  const ray = new THREE.Raycaster();
  const ptr = new THREE.Vector2();
  let hovered = null, selected = "fax";
  let spin = 0, spinTo = 0, tilt = 0, drag = null, moved = 0;

  function hit(ev) {
    const r = canvas.getBoundingClientRect();
    ptr.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
    ptr.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(ptr, camera);
    const found = ray.intersectObjects(Object.values(items), true)[0];
    if (!found) return null;
    let o = found.object;
    while (o && !o.userData.key) o = o.parent;
    return o ? o.userData.key : null;
  }

  function show(key, poke) {
    selected = key;
    picks.forEach(b => {
      const on = b.dataset.item === key;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", String(on));
    });
    readouts.forEach(p => p.classList.toggle("is-on", p.dataset.item === key));
    if (poke) play(key);
  }

  function play(key) {
    const it = items[key];
    if (key === "fax") { it.userData.send = 0; it.userData.sheet.visible = true; }
    if (key === "dish") { it.userData.grow = 0; it.userData.caps.forEach(c => c.scale.setScalar(0.001)); }
    if (key === "rig") it.userData.boot = 0;
    spinTo = -it.position.x * 0.12;
  }

  canvas.addEventListener("pointerdown", ev => {
    drag = { x: ev.clientX, y: ev.clientY, spin, tilt };
    moved = 0;
    canvas.classList.add("is-grabbing");
    canvas.setPointerCapture(ev.pointerId);
  });

  canvas.addEventListener("pointermove", ev => {
    if (drag) {
      const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
      moved = Math.max(moved, Math.hypot(dx, dy));
      spinTo = drag.spin + dx * 0.006;
      spinTo = Math.max(-0.72, Math.min(0.72, spinTo));
      tilt = Math.max(-0.07, Math.min(0.16, drag.tilt + dy * 0.0022));
      return;
    }
    const k = hit(ev);
    hovered = k;
    canvas.classList.toggle("is-over", !!k);
  });

  function letGo(ev) {
    if (!drag) return;
    canvas.classList.remove("is-grabbing");
    const tap = moved < 7;
    drag = null;
    if (tap) {
      const k = hit(ev);
      if (k) show(k, true);
    }
  }
  canvas.addEventListener("pointerup", letGo);
  canvas.addEventListener("pointercancel", letGo);
  canvas.addEventListener("pointerleave", () => { hovered = null; canvas.classList.remove("is-over"); });

  picks.forEach(b => b.addEventListener("click", () => show(b.dataset.item, true)));

  /* ── frame loop ───────────────────────────────────────────────────── */

  function size() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(size).observe(canvas);
  size();

  let live = true;
  new IntersectionObserver(es => { live = es[0].isIntersecting; }, { threshold: 0.01 }).observe(canvas);

  const clock = new THREE.Clock();
  const easeOut = t => 1 - Math.pow(1 - t, 3);

  renderer.setAnimationLoop(() => {
    if (!live) return;
    try {
    // getDelta() advances the clock, so read it first and take t from the clock after
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;

    if (!drag && !calm.matches) spinTo += Math.sin(t * 0.22) * 0.0006;
    spin += (spinTo - spin) * 0.08;
    desk.rotation.y = spin;
    desk.rotation.x += (tilt - desk.rotation.x) * 0.08;

    for (const k in items) {
      const it = items[k];
      const want = (hovered === k ? 0.14 : 0) + (selected === k ? 0.06 : 0);
      it.userData.rest += (want - it.userData.rest) * 0.12;
      const bob = calm.matches ? 0 : Math.sin(t * 1.1 + it.position.x) * 0.012;
      it.position.y = it.userData.rest + bob;
    }

    /* the fax prints a sheet */
    if (fax.userData.send >= 0) {
      fax.userData.send = Math.min(1, fax.userData.send + dt * 0.75);
      const p = easeOut(fax.userData.send);
      fax.userData.sheet.position.z = 0.45 + p * 0.95;
      fax.userData.sheet.position.y = 0.5 - p * 0.06;
      fax.userData.sheet.rotation.x = p * 0.16;
      if (fax.userData.send === 1) fax.userData.send = -1;
    }

    /* the dish fruits */
    if (dish.userData.grow >= 0) {
      dish.userData.grow = Math.min(1, dish.userData.grow + dt * 0.5);
      dish.userData.caps.forEach((c, i) => {
        const p = Math.max(0, Math.min(1, (dish.userData.grow - i * 0.18) / 0.6));
        c.scale.setScalar(Math.max(0.001, easeOut(p)));
      });
      if (dish.userData.grow === 1) dish.userData.grow = -1;
    }

    /* the screen boots */
    const scan = rig.userData.bar;
    if (rig.userData.boot >= 0) {
      rig.userData.boot = Math.min(1, rig.userData.boot + dt * 0.6);
      const p = rig.userData.boot;
      scan.visible = true;
      scan.position.y = 1.6 - p * 0.95;
      rig.userData.screen.material.emissiveIntensity = 0.45 + Math.sin(p * Math.PI) * 0.75;
      if (p === 1) { rig.userData.boot = -1; scan.visible = false; rig.userData.screen.material.emissiveIntensity = 0.45; }
    } else if (!calm.matches) {
      rig.userData.screen.material.emissiveIntensity = 0.42 + Math.sin(t * 1.6) * 0.05;
      scan.visible = false;
    } else {
      scan.visible = false;
    }

      renderer.render(scene, camera);
    } catch (e) {
      renderer.setAnimationLoop(null);
      giveUp(e);
    }
  });

  show("fax", false);
}

if (renderer) {
  try {
    boot();
  } catch (e) {
    renderer.setAnimationLoop(null);
    giveUp(e);
  }
}
