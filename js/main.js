/* ========================
   AUTOHAUS - Main JS
   ======================== */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sticky Header ──────────────────────────────────
  const header = document.getElementById('header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Mobile Menu ────────────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';

      const spans = hamburger.querySelectorAll('span');
      if (isOpen) {
        spans[0].style.cssText = 'transform:translateY(7px) rotate(45deg)';
        spans[1].style.cssText = 'opacity:0; transform:scaleX(0)';
        spans[2].style.cssText = 'transform:translateY(-7px) rotate(-45deg)';
      } else {
        spans.forEach(s => s.style.cssText = '');
      }
    });

    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
        hamburger.querySelectorAll('span').forEach(s => s.style.cssText = '');
      });
    });
  }

  // ── Scroll-to-Top ──────────────────────────────────
  const scrollTopBtn = document.getElementById('scrollTop');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Intersection Observer (fade-up) ────────────────
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach(el => observer.observe(el));
  }

  // ── Active Nav Link ────────────────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });

  // ── Smooth anchor scroll ───────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const id = anchor.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        const offset = 90;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // ── Counter animation ──────────────────────────────
  const counters = document.querySelectorAll('.hero-stat-num');
  if (counters.length) {
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(c => countObserver.observe(c));
  }

  function animateCounter(el) {
    const text = el.textContent;
    const match = text.match(/(\d+)/);
    if (!match) return;

    const target = parseInt(match[1]);
    const suffix = text.replace(/[\d]+/, '');
    const duration = 1500;
    const start = performance.now();

    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * target);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
  }

  // ── Filter checkboxes (boutique) ───────────────────
  const filterCheckboxes = document.querySelectorAll('.filter-checkbox input[type="checkbox"]');
  filterCheckboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.parentElement.textContent.trim().startsWith('Toutes') ||
          cb.parentElement.textContent.trim().startsWith('Tous')) {
        if (cb.checked) {
          const siblings = cb.closest('.filter-options').querySelectorAll('input[type="checkbox"]');
          siblings.forEach(s => {
            if (s !== cb) s.checked = false;
          });
        }
      } else {
        const allCb = cb.closest('.filter-options').querySelector('input:first-of-type');
        if (allCb && cb.checked) allCb.checked = false;
      }
    });
  });

  // ── Pagination buttons hover ───────────────────────
  document.querySelectorAll('.footer-bottom-links a, .footer-links a').forEach(link => {
    link.addEventListener('mouseenter', function() {
      this.style.paddingLeft = '4px';
    });
    link.addEventListener('mouseleave', function() {
      this.style.paddingLeft = '';
    });
  });

  // ── Vehicle photo thumbnails ───────────────────────
  document.querySelectorAll('.b-thumb').forEach(thumb => {
    thumb.addEventListener('click', () => {
      const card = thumb.closest('.b-card');
      card.querySelector('.b-main-img').src = thumb.src;
      card.querySelectorAll('.b-thumb').forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

});