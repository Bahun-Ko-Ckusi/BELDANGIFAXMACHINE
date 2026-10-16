/* The desk at the top of the page: three things you can turn and poke.
   Built from primitives, so there are no model files to download. */

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.min.js";

const canvas = document.getElementById("scene");
const picks = [...document.querySelectorAll(".pick")];
const readouts = [...document.querySelectorAll(".readout")];
const fallback = document.querySelector(".stage-fallback");
const calm = matchMedia("(prefers-reduced-motion: reduce)");

function giveUp(why) {
  if (why) console.warn("3D desk off:", why);
  canvas.remove();
  if (fallback) fallback.hidden = false;
  document.querySelector(".desk-bar")?.remove();
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
  renderer.toneMappingExposure = 1.1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 80);
  const aim = new THREE.Vector3();

  const BEIGE = 0xd3cab4, SLATE = 0x2a3032, INK = 0x0a0c0d, PAPER = 0xf3efe4;
  const CAP = 0xb4502c, GLOW = 0x2fd39a;

  /* ── light: one warm desk lamp, a cool bounce, and the screen ─────── */

  scene.add(new THREE.HemisphereLight(0x8d9aa3, 0x0b0e0f, 0.6));

  const lamp = new THREE.DirectionalLight(0xffe8cc, 2.6);
  lamp.position.set(2.6, 6.5, 3.8);
  lamp.castShadow = true;
  lamp.shadow.mapSize.set(1024, 1024);
  lamp.shadow.camera.near = 1;
  lamp.shadow.camera.far = 20;
  lamp.shadow.camera.left = lamp.shadow.camera.bottom = -6;
  lamp.shadow.camera.right = lamp.shadow.camera.top = 6;
  lamp.shadow.bias = -0.0008;
  lamp.shadow.radius = 4;
  scene.add(lamp);

  const bounce = new THREE.DirectionalLight(0x9fb8d6, 0.55);
  bounce.position.set(-5, 2.5, -1);
  scene.add(bounce);

  /* ── the desk ─────────────────────────────────────────────────────── */

  const desk = new THREE.Group();
  scene.add(desk);

  const mat = (color, rough = 0.5, extra = {}) =>
    new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: 0, ...extra });

  const solid = (geo, material, x = 0, y = 0, z = 0) => {
    const m = new THREE.Mesh(geo, material);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    return m;
  };

  const top = solid(new THREE.CylinderGeometry(3.6, 3.6, 0.28, 80), mat(0x2d3435, 0.8), 0, -0.14, 0);
  desk.add(top);
  const edge = new THREE.Mesh(new THREE.CylinderGeometry(3.62, 3.5, 0.5, 80, 1, true), mat(0x161a1b, 0.9));
  edge.position.y = -0.53;
  desk.add(edge);

  const items = {};
  function place(key, group, x, z) {
    group.position.set(x, 0, z);
    group.userData.key = key;
    group.userData.rest = 0;
    items[key] = group;
    desk.add(group);
  }

  /* 1. a beige office fax, the thing the company is named after */
  const fax = new THREE.Group();
  {
    const shell = mat(BEIGE, 0.55);
    fax.add(
      solid(new THREE.BoxGeometry(1.7, 0.5, 1.15), shell, 0, 0.25, 0),
      solid(new THREE.BoxGeometry(1.74, 0.06, 1.19), mat(0xc2b9a2, 0.5), 0, 0.5, 0)
    );
    const tray = solid(new THREE.BoxGeometry(1.46, 0.05, 0.74), mat(SLATE, 0.5), 0, 0.7, -0.27);
    tray.rotation.x = -0.36;
    const roll = solid(new THREE.CylinderGeometry(0.16, 0.16, 1.28, 28), mat(PAPER, 0.85), 0, 0.8, -0.5);
    roll.rotation.z = Math.PI / 2;
    const slot = solid(new THREE.BoxGeometry(1.22, 0.05, 0.1), mat(INK, 0.9), 0, 0.48, 0.42);
    const panel = solid(new THREE.BoxGeometry(0.62, 0.03, 0.34), mat(SLATE, 0.4), 0.42, 0.53, 0.12);
    const lcd = solid(new THREE.BoxGeometry(0.42, 0.012, 0.1), mat(0x6f8a5a, 0.3, { emissive: 0x5f7d48, emissiveIntensity: 0.35 }), 0.42, 0.548, 0.02);
    fax.add(tray, roll, slot, panel, lcd);
    for (let i = 0; i < 6; i++) {
      const k = solid(new THREE.BoxGeometry(0.075, 0.03, 0.06), mat(i === 5 ? CAP : 0xe9e3d3, 0.45),
        0.25 + (i % 3) * 0.11, 0.555, 0.15 + Math.floor(i / 3) * 0.09);
      fax.add(k);
    }
    const sheet = solid(new THREE.BoxGeometry(1.08, 0.012, 0.86), mat(PAPER, 0.95), 0, 0.48, 0.44);
    sheet.visible = false;
    for (let r = 0; r < 4; r++) {
      sheet.add(solid(new THREE.BoxGeometry(r === 0 ? 0.55 : 0.8 - r * 0.12, 0.014, 0.035), mat(0x2b2b2b, 0.9),
        -0.1 - (r === 0 ? 0.04 : 0), 0.007, -0.24 + r * 0.12));
    }
    fax.add(sheet);
    fax.userData.sheet = sheet;
    fax.userData.send = -1;
  }
  place("fax", fax, -1.9, 0.35);
  fax.rotation.y = 0.28;

  /* 2. a petri dish that fruits when poked */
  const dish = new THREE.Group();
  {
    const glass = new THREE.MeshPhysicalMaterial({
      color: 0xffffff, roughness: 0.06, metalness: 0,
      transparent: true, opacity: 0.22, transmission: 0.8, thickness: 0.4
    });
    dish.add(
      solid(new THREE.CylinderGeometry(0.94, 0.92, 0.1, 56), mat(0xcfd6d4, 0.35), 0, 0.05, 0),
      solid(new THREE.CylinderGeometry(0.86, 0.86, 0.1, 56), mat(0xe2d29a, 0.6), 0, 0.13, 0)
    );
    // mycelium spreading across the agar
    const myc = solid(new THREE.CircleGeometry(0.55, 40), mat(0xf6f3ea, 0.95), 0, 0.182, 0);
    myc.rotation.x = -Math.PI / 2;
    dish.add(myc);
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(0.96, 0.96, 0.28, 56, 1, true), glass);
    wall.position.y = 0.2;
    dish.add(wall);

    const caps = [];
    [[0.02, 0.0, 0.46, 1], [-0.36, 0.2, 0.32, 0.8], [0.32, -0.25, 0.27, 0.7], [0.18, 0.36, 0.2, 0.55]]
      .forEach(([x, z, h, s]) => {
        const shroom = new THREE.Group();
        shroom.add(solid(new THREE.CylinderGeometry(0.045, 0.07, h, 16), mat(0xf1ebdc, 0.75), 0, h / 2, 0));
        const cap = solid(new THREE.SphereGeometry(0.18, 28, 16, 0, Math.PI * 2, 0, Math.PI / 1.9), mat(CAP, 0.6), 0, h - 0.01, 0);
        cap.scale.set(1, 0.6, 1);
        const gills = solid(new THREE.CircleGeometry(0.175, 28), mat(0xd9c8a8, 0.9), 0, h - 0.012, 0);
        gills.rotation.x = Math.PI / 2;
        shroom.add(cap, gills);
        shroom.position.set(x, 0.18, z);
        shroom.rotation.z = (x) * 0.25;
        shroom.userData.size = s;
        shroom.scale.setScalar(0.001);
        dish.add(shroom);
        caps.push(shroom);
      });
    dish.userData.caps = caps;
    dish.userData.grow = -1;
  }
  place("dish", dish, -0.05, 1.05);

  /* 3. the screen the game is made on */
  const rig = new THREE.Group();
  {
    rig.add(
      solid(new THREE.BoxGeometry(0.7, 0.05, 0.45), mat(SLATE, 0.5), 0, 0.025, 0.05),
      solid(new THREE.BoxGeometry(0.12, 0.62, 0.08), mat(SLATE, 0.5), 0, 0.33, -0.08),
      solid(new THREE.BoxGeometry(1.86, 1.14, 0.09), mat(0x1c2123, 0.45), 0, 1.15, -0.05)
    );
    const screen = solid(new THREE.BoxGeometry(1.72, 1.0, 0.02), mat(0x050b0a, 0.7, {
      emissive: GLOW, emissiveIntensity: 0.08
    }), 0, 1.15, 0.005);
    rig.add(screen);
    // a few lines of "code" on the screen
    const codeMat = mat(0x8debc4, 0.6, { emissive: 0x8debc4, emissiveIntensity: 0.75 });
    [[0.9, 0], [0.6, 0.15], [0.75, 0.15], [0.4, 0.3], [0.85, 0.15], [0.5, 0]].forEach(([w, indent], i) => {
      const ln = new THREE.Mesh(new THREE.BoxGeometry(w, 0.04, 0.005), codeMat);
      ln.position.set(-0.7 + indent + w / 2, 1.52 - i * 0.13, 0.02);
      rig.add(ln);
    });
    const bar = new THREE.Mesh(new THREE.BoxGeometry(1.64, 0.05, 0.005),
      mat(GLOW, 0.3, { emissive: GLOW, emissiveIntensity: 2 }));
    bar.position.set(0, 1.6, 0.024);
    bar.visible = false;
    rig.add(bar);

    const spill = new THREE.PointLight(GLOW, 0.9, 3.6, 1.8);
    spill.position.set(0, 0.55, 0.9);   // low and forward: lights the desk, not the glass
    rig.add(spill);

    rig.rotation.y = -0.3;
    rig.userData.screen = screen;
    rig.userData.bar = bar;
    rig.userData.spill = spill;
    rig.userData.boot = -1;
  }
  place("rig", rig, 1.85, -0.2);

  /* ── picking and turning ──────────────────────────────────────────── */

  const ray = new THREE.Raycaster();
  const ptr = new THREE.Vector2();
  let hovered = null, selected = null;
  let spin = -0.12, spinTo = -0.12, tilt = 0, tiltTo = 0, drag = null, moved = 0, idle = 0;

  function hit(ev) {
    const r = canvas.getBoundingClientRect();
    ptr.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
    ptr.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(ptr, camera);
    const found = ray.intersectObjects(Object.values(items), true)[0];
    let o = found && found.object;
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
    readouts.forEach(p => p.classList.toggle("is-on", p.dataset.item === (key || "")));
    if (poke && key) play(key);
  }

  function play(key) {
    const it = items[key];
    if (key === "fax") { it.userData.send = 0; it.userData.sheet.visible = true; }
    if (key === "dish") { it.userData.grow = 0; it.userData.caps.forEach(c => c.scale.setScalar(0.001)); }
    if (key === "rig") it.userData.boot = 0;
    // swing the desk a little so the poked thing faces you
    spinTo = Math.max(-0.7, Math.min(0.7, -it.position.x * 0.16));
    idle = 0;
  }

  canvas.addEventListener("pointerdown", ev => {
    drag = { x: ev.clientX, y: ev.clientY, spin: spinTo, tilt: tiltTo };
    moved = 0;
    canvas.classList.add("is-grabbing");
    canvas.setPointerCapture(ev.pointerId);
  });

  canvas.addEventListener("pointermove", ev => {
    if (drag) {
      const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
      moved = Math.max(moved, Math.hypot(dx, dy));
      spinTo = Math.max(-0.8, Math.min(0.8, drag.spin + dx * 0.006));
      tiltTo = Math.max(-0.06, Math.min(0.14, drag.tilt + dy * 0.002));
      idle = 0;
      return;
    }
    hovered = hit(ev);
    canvas.classList.toggle("is-over", !!hovered);
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

  /* ── framing: desk to the right of the headline on wide layouts,
        centred and fitted to the width on phones ───────────────────── */

  const overlay = matchMedia("(min-width: 62rem)");
  const HALF_FOV = THREE.MathUtils.degToRad(15);   // half of the 30° vertical fov

  function size() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    const a = w / h;
    camera.aspect = a;
    const tanH = Math.tan(HALF_FOV) * a;           // horizontal half-angle

    if (overlay.matches) {
      // slide the camera sideways (no yaw) so the desk centre lands 73% across
      const d = 11.2;
      const shift = (2 * 0.73 - 1) * d * tanH;
      camera.position.set(-shift, d * 0.34, d);
      aim.set(-shift, 0.35, 0);
    } else {
      // back off until the three objects fit the width, with a little air
      const d = Math.max(8.8, 3.25 / tanH);
      camera.position.set(0, d * 0.36, d);
      aim.set(0, 0.45, 0);
    }
    camera.lookAt(aim);
    camera.updateProjectionMatrix();
  }
  overlay.addEventListener("change", size);
  new ResizeObserver(size).observe(canvas);
  size();

  let live = true;
  new IntersectionObserver(es => { live = es[0].isIntersecting; }, { threshold: 0.01 }).observe(canvas);

  const clock = new THREE.Clock();
  const easeOut = t => 1 - Math.pow(1 - t, 3);

  renderer.setAnimationLoop(() => {
    if (!live) return;
    try {
      // getDelta() advances the clock, so read it before elapsedTime
      const dt = Math.min(clock.getDelta(), 0.05);
      const t = clock.elapsedTime;

      idle += dt;
      if (!drag && !calm.matches && idle > 4) spinTo += Math.sin(t * 0.2) * 0.0005;
      spin += (spinTo - spin) * 0.08;
      tilt += (tiltTo - tilt) * 0.08;
      desk.rotation.y = spin;
      desk.rotation.x = tilt;

      for (const k in items) {
        const it = items[k];
        const want = (hovered === k ? 0.12 : 0) + (selected === k ? 0.05 : 0);
        it.userData.rest += (want - it.userData.rest) * 0.14;
        it.position.y = it.userData.rest;
      }

      // the fax prints a sheet
      const f = fax.userData;
      if (f.send >= 0) {
        f.send = Math.min(1, f.send + dt * 0.7);
        const p = easeOut(f.send);
        f.sheet.position.z = 0.44 + p * 1.0;
        f.sheet.position.y = 0.48 - p * 0.07;
        f.sheet.rotation.x = p * 0.18;
        if (f.send === 1) f.send = -1;
      }

      // the dish fruits, one mushroom after another
      const d = dish.userData;
      if (d.grow >= 0) {
        d.grow = Math.min(1, d.grow + dt * 0.45);
        d.caps.forEach((c, i) => {
          const p = Math.max(0, Math.min(1, (d.grow - i * 0.14) / 0.55));
          c.scale.setScalar(Math.max(0.001, easeOut(p) * c.userData.size));
        });
        if (d.grow === 1) d.grow = -1;
      }

      // the screen wakes up
      const r = rig.userData;
      if (r.boot >= 0) {
        r.boot = Math.min(1, r.boot + dt * 0.65);
        r.bar.visible = true;
        r.bar.position.y = 1.62 - r.boot * 0.95;
        const surge = Math.sin(r.boot * Math.PI);
        r.screen.material.emissiveIntensity = 0.08 + surge * 0.5;
        r.spill.intensity = 0.9 + surge * 2.2;
        if (r.boot === 1) { r.boot = -1; r.bar.visible = false; }
      } else {
        const hum = calm.matches ? 0 : Math.sin(t * 1.4) * 0.04;
        r.screen.material.emissiveIntensity = 0.08 + hum * 0.4;
        r.spill.intensity = 0.9 + hum * 3;
      }

      renderer.render(scene, camera);
    } catch (e) {
      renderer.setAnimationLoop(null);
      giveUp(e);
    }
  });

  show(null, false);
}

if (renderer) {
  try {
    boot();
  } catch (e) {
    renderer.setAnimationLoop(null);
    giveUp(e);
  }
}
