/* ================================================================
   LuxeShop — Main JavaScript
================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initSearch();
  initScrollReveal();
  initBackToTop();
  initRippleEffects();
  initFlashMessages();
  initFAQ();
  initSideCart();
  closeSideCartOnOutsideClick();
});

// ── Navbar ──────────────────────────────────────────────────────
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');

  if (!navbar) return;

  // Scroll effect
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });

  // Hamburger toggle
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('open');
    });

    // Close on link click
    mobileMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
      });
    });
  }

  // Highlight active link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
}

// ── Search Overlay ───────────────────────────────────────────────
function initSearch() {
  const searchBtn = document.getElementById('searchBtn');
  const searchOverlay = document.getElementById('searchOverlay');
  const closeSearch = document.getElementById('closeSearch');
  const searchInput = document.getElementById('searchInput');

  if (!searchBtn || !searchOverlay) return;

  searchBtn.addEventListener('click', () => {
    searchOverlay.classList.add('open');
    setTimeout(() => searchInput?.focus(), 100);
  });

  closeSearch?.addEventListener('click', closeSearchOverlay);

  searchOverlay.addEventListener('click', e => {
    if (e.target === searchOverlay) closeSearchOverlay();
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSearchOverlay();
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchOverlay.classList.add('open');
      setTimeout(() => searchInput?.focus(), 100);
    }
  });

  function closeSearchOverlay() {
    searchOverlay.classList.remove('open');
  }
}

// ── Scroll Reveal ────────────────────────────────────────────────
function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  elements.forEach(el => observer.observe(el));
}

// ── Back to Top ──────────────────────────────────────────────────
function initBackToTop() {
  const btn = document.getElementById('backToTop');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── Ripple Effect ────────────────────────────────────────────────
function initRippleEffects() {
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - rect.left - size/2}px;top:${e.clientY - rect.top - size/2}px`;
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });
}

// ── Flash Messages (Django) ──────────────────────────────────────
function initFlashMessages() {
  const messages = document.querySelectorAll('.django-message');
  messages.forEach(msg => {
    const closeBtn = msg.querySelector('.message-close');
    closeBtn?.addEventListener('click', () => msg.remove());

    // Auto-dismiss after 4s
    setTimeout(() => {
      msg.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(30px)';
      setTimeout(() => msg.remove(), 400);
    }, 4000);
  });
}

// ── FAQ Toggle ───────────────────────────────────────────────────
function initFAQ() {
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const answer = q.nextElementSibling;
      const isOpen = q.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-question').forEach(fq => {
        fq.classList.remove('open');
        fq.nextElementSibling?.classList.remove('open');
      });

      if (!isOpen) {
        q.classList.add('open');
        answer?.classList.add('open');
      }
    });
  });
}

// ── Side Cart ────────────────────────────────────────────────────
function initSideCart() {
  const openBtns = document.querySelectorAll('[data-open-cart]');
  const overlay = document.getElementById('cartOverlay');
  const sideCart = document.getElementById('sideCart');
  const closeBtn = document.getElementById('closeCart');

  openBtns.forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      openCart();
    });
  });

  closeBtn?.addEventListener('click', closeCart);
  overlay?.addEventListener('click', closeCart);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeCart();
  });
}

function openCart() {
  document.getElementById('cartOverlay')?.classList.add('open');
  document.getElementById('sideCart')?.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  document.getElementById('cartOverlay')?.classList.remove('open');
  document.getElementById('sideCart')?.classList.remove('open');
  document.body.style.overflow = '';
}

function closeSideCartOnOutsideClick() {
  // Handled by overlay click listener above
}

// ── Add to Cart (AJAX) ───────────────────────────────────────────
function addToCart(productId, quantity = 1, btn = null) {
  const csrfToken = getCsrfToken();

  if (btn) {
    btn.classList.add('loading');
    btn.disabled = true;
  }

  fetch(`/cart/add/${productId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: `quantity=${quantity}`,
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        updateCartBadge(data.cart_count);
        showToast(data.message || 'Added to cart!', 'success');
        openCart();
        refreshCartContents();
      }
    })
    .catch(() => showToast('Something went wrong. Please try again.', 'error'))
    .finally(() => {
      if (btn) {
        btn.classList.remove('loading');
        btn.disabled = false;
      }
    });
}

// ── Toggle Wishlist (AJAX) ───────────────────────────────────────
function toggleWishlist(productId, btn) {
  const csrfToken = getCsrfToken();

  fetch(`/wishlist/toggle/${productId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: '',
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        const icon = btn.querySelector('i');
        if (data.in_wishlist) {
          icon?.classList.remove('far');
          icon?.classList.add('fas');
          btn.classList.add('active');
          showToast('Added to wishlist!', 'success');
        } else {
          icon?.classList.remove('fas');
          icon?.classList.add('far');
          btn.classList.remove('active');
          showToast('Removed from wishlist', 'warning');
        }
        btn.classList.add('animate');
        updateWishlistBadge(data.wishlist_count);
        setTimeout(() => btn.classList.remove('animate'), 500);
      }
    })
    .catch(() => {
      // Redirect to login if not authenticated
      window.location.href = `/users/login/?next=${window.location.pathname}`;
    });
}

// ── Cart Quantity Controls ───────────────────────────────────────
function updateCartItem(itemId, action) {
  const csrfToken = getCsrfToken();

  fetch(`/cart/update/${itemId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: `action=${action}`,
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        updateCartBadge(data.cart_count);
        if (action === 'remove') {
          location.reload();
        } else {
          location.reload();
        }
      }
    });
}

// ── Refresh Side Cart Contents ───────────────────────────────────
function refreshCartContents() {
  // Reload to get updated cart - simple & reliable
  // In a more advanced version, this would fetch cart HTML via AJAX
}

// ── Coupon ───────────────────────────────────────────────────────
function applyCoupon() {
  const codeInput = document.getElementById('couponInput');
  const code = codeInput?.value.trim();
  if (!code) return;

  fetch('/cart/coupon/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCsrfToken(),
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: `coupon_code=${encodeURIComponent(code)}`,
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        showToast(data.message, 'success');
        location.reload();
      } else {
        showToast(data.message, 'error');
        if (codeInput) {
          codeInput.style.animation = 'shake 0.5s ease';
          setTimeout(() => codeInput.style.animation = '', 500);
        }
      }
    });
}

// ── Newsletter ───────────────────────────────────────────────────
function subscribeNewsletter(e) {
  e?.preventDefault();
  const form = e?.target || document.getElementById('newsletterForm');
  const email = form?.querySelector('input[type=email]')?.value;
  if (!email) return;

  fetch('/newsletter/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCsrfToken(),
    },
    body: `email=${encodeURIComponent(email)}`,
  })
    .then(r => r.json())
    .then(data => {
      showToast(data.message, data.success ? 'success' : 'warning');
      if (data.success && form) form.reset();
    });
}

// ── Product Tabs ─────────────────────────────────────────────────
function switchTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));

  document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');
  document.getElementById(`tab-${tabName}`)?.classList.add('active');
}

// ── Gallery ──────────────────────────────────────────────────────
function switchGalleryImage(src, thumbEl) {
  const mainImg = document.getElementById('galleryMain');
  if (mainImg) {
    mainImg.style.opacity = '0';
    setTimeout(() => {
      mainImg.src = src;
      mainImg.style.opacity = '1';
    }, 200);
  }

  document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
  thumbEl?.classList.add('active');
}

// ── Toast Notifications ──────────────────────────────────────────
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer') || createToastContainer();
  const icons = { success: 'fa-circle-check', error: 'fa-circle-xmark', warning: 'fa-triangle-exclamation', info: 'fa-circle-info' };
  const icon = icons[type] || icons.info;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<i class="fas ${icon} toast-icon"></i><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s, transform 0.4s';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(30px)';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

function createToastContainer() {
  const el = document.createElement('div');
  el.id = 'toastContainer';
  el.className = 'toast-container';
  document.body.appendChild(el);
  return el;
}

// ── Badge Updates ────────────────────────────────────────────────
function updateCartBadge(count) {
  document.querySelectorAll('.cart-badge').forEach(badge => {
    badge.textContent = count;
    badge.classList.add('badge-animate');
    setTimeout(() => badge.classList.remove('badge-animate'), 300);
  });
}

function updateWishlistBadge(count) {
  document.querySelectorAll('.wishlist-badge').forEach(badge => {
    badge.textContent = count;
  });
}

// ── Utility: CSRF Token ──────────────────────────────────────────
function getCsrfToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
         document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}
