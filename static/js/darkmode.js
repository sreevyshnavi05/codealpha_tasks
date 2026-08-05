/* ================================================================
   LuxeShop — Dark Mode Toggle
================================================================ */

(function() {
  // Apply theme immediately to prevent flash
  const saved = localStorage.getItem('luxe-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('themeToggle');
  if (!toggleBtn) return;

  updateToggleIcon();

  toggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('luxe-theme', next);
    updateToggleIcon();
  });

  function updateToggleIcon() {
    const theme = document.documentElement.getAttribute('data-theme');
    const icon = toggleBtn.querySelector('i');
    if (icon) {
      icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
  }
});
