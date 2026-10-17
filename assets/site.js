// Elrhea Clinic — header menu, dropdown, reveal-on-scroll
(function () {
  document.documentElement.classList.add("js");

  var header = document.querySelector(".site-header");
  var nav = document.getElementById("site-nav");
  var toggle = document.querySelector(".menu-toggle");
  var mobile = window.matchMedia("(max-width: 940px)");

  function onScroll() {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  function setMenu(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".menu-label").textContent = open ? "Tutup" : "Menu";
    document.body.style.overflow = open ? "hidden" : "";
  }
  toggle.addEventListener("click", function () {
    setMenu(!nav.classList.contains("is-open"));
  });
  mobile.addEventListener("change", function () { setMenu(false); });
  nav.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () { if (nav.classList.contains("is-open")) setMenu(false); });
  });

  // Dropdowns: click/tap/keyboard everywhere, hover on desktop pointers
  var items = document.querySelectorAll(".nav-item");
  function closeAll(except) {
    items.forEach(function (item) {
      if (item === except) return;
      item.classList.remove("is-open");
      item.querySelector(".nav-trigger").setAttribute("aria-expanded", "false");
    });
  }
  items.forEach(function (item) {
    var trigger = item.querySelector(".nav-trigger");
    function set(open) {
      item.classList.toggle("is-open", open);
      trigger.setAttribute("aria-expanded", String(open));
    }
    trigger.addEventListener("click", function () {
      var open = !item.classList.contains("is-open");
      closeAll(item);
      set(open);
    });
    item.addEventListener("mouseenter", function () {
      if (!mobile.matches && window.matchMedia("(hover: hover)").matches) { closeAll(item); set(true); }
    });
    item.addEventListener("mouseleave", function () {
      if (!mobile.matches && window.matchMedia("(hover: hover)").matches) set(false);
    });
    item.addEventListener("focusout", function (e) {
      if (!mobile.matches && !item.contains(e.relatedTarget)) set(false);
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav-item")) closeAll();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var open = document.querySelector(".nav-item.is-open");
    if (open) { closeAll(); open.querySelector(".nav-trigger").focus(); }
    else if (nav.classList.contains("is-open")) { setMenu(false); toggle.focus(); }
  });

  // Reveal on scroll
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("is-in"); });
  }
})();
