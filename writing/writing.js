const root = document.documentElement;
const themeButton = document.querySelector('[data-theme-toggle]');
const preference = matchMedia('(prefers-color-scheme: dark)');
function syncTheme() {
  const night = root.dataset.theme ? root.dataset.theme === 'night' : preference.matches;
  themeButton.textContent = night ? '☀ Day' : '☾ Night';
  themeButton.setAttribute('aria-pressed', String(night));
}
themeButton.addEventListener('click', () => {
  root.dataset.theme = themeButton.getAttribute('aria-pressed') === 'true' ? 'day' : 'night';
  try { localStorage.setItem('voyage-theme', root.dataset.theme); } catch (_) {}
  syncTheme();
});
preference.addEventListener('change', syncTheme);
syncTheme();
