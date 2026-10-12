// Progressive enhancement: content stays visible even without JavaScript.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!motionPreference.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('entered');
        observer.unobserve(entry.target);
      }
    }
  }, { threshold: 0.12 });
  document.querySelectorAll('.paper, .award-feature, .service-role, .timeline article, .gallery figure').forEach((element) => observer.observe(element));
  motionPreference.addEventListener('change', (event) => {
    if (event.matches) observer.disconnect();
  });
}
