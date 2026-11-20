/* LowLevel Labs site script: theme, menu, code blocks, table of contents, article search */
(function () {
  const root = document.documentElement;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // Theme toggle (initial theme is set inline in <head> to avoid a flash)
  const themeBtn = document.getElementById("themeBtn");
  if (themeBtn) {
    const sync = () => themeBtn.setAttribute("aria-label",
      root.dataset.theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    sync();
    themeBtn.addEventListener("click", () => {
      root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
      store.set("ll-theme", root.dataset.theme);
      sync();
    });
  }

  // Mobile menu
  const menuBtn = document.getElementById("menuBtn");
  const nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
  }

  // Code blocks: language label + copy button
  const langNames = { c: "C", cpp: "C++", armasm: "ARM asm", x86asm: "x86 asm", bash: "shell", shell: "shell",
    makefile: "Makefile", dts: "DTS", ld: "linker script", plaintext: "", text: "" };
  document.querySelectorAll("pre > code").forEach((code) => {
    const pre = code.parentElement;
    const m = (code.className || "").match(/language-(\w+)/);
    if (m && langNames[m[1]] !== "") pre.dataset.lang = langNames[m[1]] || m[1];
    if (navigator.clipboard) {
      const b = document.createElement("button");
      b.type = "button"; b.className = "copy"; b.textContent = "Copy";
      b.addEventListener("click", () => {
        navigator.clipboard.writeText(code.innerText).then(() => {
          b.textContent = "Copied"; setTimeout(() => (b.textContent = "Copy"), 1500);
        });
      });
      pre.appendChild(b);
    }
  });
  if (window.hljs) {
    document.querySelectorAll("pre > code[class*='language-']").forEach((el) => {
      if (!/language-(plaintext|text)/.test(el.className)) window.hljs.highlightElement(el);
    });
  }

  // "On this page" active section
  const tocLinks = [...document.querySelectorAll(".otp a")];
  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map(tocLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove("on"));
          const a = map.get(e.target.id); if (a) a.classList.add("on");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px" });
    map.forEach((_, id) => { const h = document.getElementById(id); if (h) obs.observe(h); });
  }

  // Article listing: search + topic filter
  const list = document.getElementById("articleList");
  if (list) {
    const rows = [...list.children];
    const input = document.getElementById("q");
    const chips = [...document.querySelectorAll(".chip")];
    const empty = document.getElementById("empty");
    const count = document.getElementById("count");
    let topic = new URLSearchParams(location.search).get("topic") || "all";
    const apply = () => {
      const q = (input.value || "").trim().toLowerCase();
      let n = 0;
      rows.forEach((li) => {
        const ok = (topic === "all" || li.dataset.topic === topic) && (!q || li.dataset.text.includes(q));
        li.hidden = !ok; if (ok) n++;
      });
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.topic === topic)));
      empty.hidden = n !== 0;
      count.textContent = n === 1 ? "1 article" : n + " articles";
    };
    chips.forEach((c) => c.addEventListener("click", () => {
      topic = c.dataset.topic;
      const u = new URL(location.href);
      topic === "all" ? u.searchParams.delete("topic") : u.searchParams.set("topic", topic);
      history.replaceState(null, "", u);
      apply();
    }));
    input.addEventListener("input", apply);
    apply();
  }
})();
