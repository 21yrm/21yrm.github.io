(() => {
  "use strict";
  document.documentElement.classList.add("js");

  document.querySelectorAll('a[href^="http"]').forEach((link) => {
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  });

  const menu = document.querySelector(".menu-toggle");
  const navigation = document.getElementById("nav-links");
  const mobile = window.matchMedia("(max-width: 760px)");
  const setMenu = (open) => {
    menu.setAttribute("aria-expanded", String(open));
    navigation.classList.toggle("is-open", open);
    menu.querySelector("span").textContent = open ? "−" : "＋";
  };
  menu.addEventListener("click", () => setMenu(menu.getAttribute("aria-expanded") !== "true"));
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
      setMenu(false);
      menu.focus();
    }
  });
  mobile.addEventListener("change", () => setMenu(false));

  const progress = document.getElementById("scroll-progress");
  const links = [...navigation.querySelectorAll('a[href^="#"]')];
  const sections = [...document.querySelectorAll("main > section[id]")];
  let scrollPending = false;
  const updateScroll = () => {
    const distance = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${distance > 0 ? (window.scrollY / distance) * 100 : 0}%`;
    let current = "hero";
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= 180) current = section.id;
    }
    links.forEach((link) => {
      const active = link.hash === `#${current}`;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    scrollPending = false;
  };
  const scheduleScroll = () => {
    if (!scrollPending) {
      scrollPending = true;
      requestAnimationFrame(updateScroll);
    }
  };
  window.addEventListener("scroll", scheduleScroll, { passive: true });
  window.addEventListener("resize", scheduleScroll, { passive: true });
  updateScroll();

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const revealTargets = [...document.querySelectorAll(
    ".hero-name, .hero-social, .about-content, .portrait, .section-header, " +
    ".news-item, .news-archive > summary, .pub-card, .background-title, " +
    ".education-card, .internship-card"
  )];
  if (!reducedMotion.matches && "IntersectionObserver" in window && Element.prototype.animate) {
    const animations = new Set();
    const reveal = (element, delay = 0, animate = true) => {
      if (!element.classList.contains("reveal-pending")) return;
      element.classList.remove("reveal-pending");
      observer.unobserve(element);
      if (!animate) return;
      const animation = element.animate([
        { opacity: 0, transform: "translateY(22px)" },
        { opacity: 1, transform: "translateY(0)" }
      ], { duration: 1000, delay, easing: "cubic-bezier(.22, 1, .36, 1)", fill: "backwards" });
      animations.add(animation);
      animation.onfinish = () => animations.delete(animation);
    };
    const observer = new IntersectionObserver((entries) => {
      entries.filter((entry) => entry.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
        .forEach((entry, index) => reveal(entry.target, Math.min(index, 3) * 110));
    }, { threshold: 0, rootMargin: "0px 0px -24px 0px" });
    revealTargets.forEach((element) => {
      element.classList.add("reveal-pending");
      observer.observe(element);
    });
    document.addEventListener("focusin", (event) => {
      const element = event.target.closest(".reveal-pending");
      if (element) reveal(element, 0, false);
      animations.forEach((animation) => {
        if (animation.effect.target.contains(event.target)) animation.finish();
      });
    });
    reducedMotion.addEventListener("change", () => {
      if (!reducedMotion.matches) return;
      observer.disconnect();
      revealTargets.forEach((element) => element.classList.remove("reveal-pending"));
      animations.forEach((animation) => animation.cancel());
      animations.clear();
    });
  }

  // A brief, local point-field reveal; it settles instead of running forever.
  const canvas = document.getElementById("research-field");
  const context = canvas?.getContext("2d");
  if (!context) return;
  let width = 0;
  let height = 0;
  let frame = 0;
  let start = 0;
  let finished = reducedMotion.matches;

  const draw = (phase = 1) => {
    context.clearRect(0, 0, width, height);
    const rotation = .18 + phase * .14;
    const scale = Math.min(width, height) * .36;
    const points = [];
    for (let ring = 0; ring < 36; ring++) {
      const v = (ring / 36) * Math.PI * 2;
      for (let step = 0; step < 76; step++) {
        const u = (step / 76) * Math.PI * 2;
        const radius = 1 + .23 * Math.cos(v);
        const x = radius * Math.cos(u);
        const y = .38 * Math.sin(v) + .2 * Math.sin(u * 3);
        const z = radius * Math.sin(u);
        const rx = x * Math.cos(rotation) + z * Math.sin(rotation);
        const rz = -x * Math.sin(rotation) + z * Math.cos(rotation);
        const ry = y * .76 - rz * .65;
        const depth = y * .65 + rz * .76;
        const tilt = -.4;
        points.push({
          x: (rx * Math.cos(tilt) - ry * Math.sin(tilt)) * scale + width * .5,
          y: (rx * Math.sin(tilt) + ry * Math.cos(tilt)) * scale + height * .49,
          depth
        });
      }
    }
    points.sort((a, b) => a.depth - b.depth);
    points.forEach(({ x, y, depth }) => {
      const intensity = (depth + 1.2) / 2.4;
      context.fillStyle = `rgba(195,250,139,${.08 + intensity * .47})`;
      context.beginPath();
      context.arc(x, y, .6 + intensity * .75, 0, Math.PI * 2);
      context.fill();
    });
  };

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
  };
  const animate = (time) => {
    if (finished) return;
    if (!start) start = time;
    const progress = Math.min((time - start) / 3400, 1);
    draw(1 - Math.pow(1 - progress, 3));
    if (progress < 1) frame = requestAnimationFrame(animate);
    else finished = true;
  };
  const settle = () => {
    finished = true;
    cancelAnimationFrame(frame);
    draw();
  };
  new ResizeObserver(resize).observe(canvas);
  resize();
  if (!finished) frame = requestAnimationFrame(animate);
  reducedMotion.addEventListener("change", settle);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) settle();
  });
})();
