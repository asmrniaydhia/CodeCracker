// SIDEBAR 
const app = document.getElementById('lessonApp');
const toggleBtn = document.getElementById('sidebarToggle');

function toggleSidebar() {
  if (!app || !toggleBtn) return;
  const collapsed = app.classList.toggle('is-collapsed');
  toggleBtn.setAttribute('aria-expanded', String(!collapsed));
  toggleBtn.setAttribute('aria-label', collapsed ? 'Buka sidebar' : 'Tutup sidebar');
}
if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);

document.addEventListener('DOMContentLoaded', function () {
  function norm(s) {
    if (!s) return '';
    try { s = decodeURI(s); } catch (e) {}
    s = s.toString().toLowerCase();
    if (s.endsWith('/')) s = s.slice(0, -1);
    return s;
  }

  const currentPath = norm(location.pathname + (location.hash || ''));
  const currentFile = currentPath.split('/').pop() || 'index.html';
  const urlParams = new URLSearchParams(location.search);
  const targetQuiz = urlParams.get('target')?.toLowerCase();

  const sidebar = document.querySelector('.sidebar') || document.querySelector('#sidebar') || document.querySelector('.nav');
  const links = sidebar ? Array.from(sidebar.querySelectorAll('a[href]')) : Array.from(document.querySelectorAll('.sidebar a[href], a.sidebar-link[href], .nav a[href]'));
  console.log('[SIDEBAR DEBUG] currentPath=', currentPath, 'currentFile=', currentFile, 'targetQuiz=', targetQuiz);
  console.log('[SIDEBAR DEBUG] found', links.length, 'links');

  let activeLink = null;

  // detect /templates/kuis/kuisX.html -> kuisX
  const kuisMatch = (function () {
    const m = currentPath.match(/(kuis\d+)\.html$/);
    return m ? m[1] : null;
  })();

  // helper: mark a link active
  function setActive(a) {
    if (!a) return;
    links.forEach(x => x.classList.remove('active'));
    a.classList.add('active');
    activeLink = a;
    // open containing accordion if any
    const collapse = a.closest('.accordion-collapse');
    if (collapse) {
      collapse.classList.add('show');
      collapse.setAttribute('aria-expanded', 'true');
      const headerBtn = collapse.previousElementSibling?.querySelector('.accordion-button');
      if (headerBtn) {
        headerBtn.classList.remove('collapsed');
        headerBtn.setAttribute('aria-expanded', 'true');
        headerBtn.classList.add('active-head');
      }
    }
    // ensure sidebar expanded
    if (app && app.classList.contains('is-collapsed')) {
      app.classList.remove('is-collapsed');
      const sbToggle = document.getElementById('sidebarToggle');
      if (sbToggle) sbToggle.setAttribute('aria-expanded', 'true');
    }
  }

  // 1) coba kecocokan paling ketat: href file === currentFile (plus optional target param)
  for (const a of links) {
    const href = a.getAttribute('href');
    if (!href) continue;
    let parsed;
    try { parsed = new URL(href, location.origin); } catch (e) { parsed = { pathname: href, search: (href.split('?')[1] || '') }; }
    const hrefFile = norm(parsed.pathname).split('/').pop();
    const hrefParams = new URLSearchParams(parsed.search || '');
    const hrefTarget = hrefParams.get('target')?.toLowerCase();

    // direct filename match
    if (hrefFile && hrefFile === currentFile) {
      if (!hrefTarget) { setActive(a); break; }
      if (targetQuiz && hrefTarget === targetQuiz) { setActive(a); break; }
    }
  }

  // 2) kalau belum ketemu, lihat target param match (mis. sidebar: ?target=kuis1)
  if (!activeLink && targetQuiz) {
    for (const a of links) {
      const href = a.getAttribute('href');
      if (!href) continue;
      let parsed;
      try { parsed = new URL(href, location.origin); } catch (e) { parsed = { search: (href.split('?')[1] || '') }; }
      const hrefParams = new URLSearchParams(parsed.search || '');
      const hrefTarget = hrefParams.get('target')?.toLowerCase();
      if (hrefTarget && hrefTarget === targetQuiz) { setActive(a); break; }
    }
  }

  // 3) support: jika page ada di /templates/kuis/kuisX.html, cari link yang mengandung kuisX
  if (!activeLink && kuisMatch) {
    for (const a of links) {
      const href = (a.getAttribute('href') || '').toLowerCase();
      if (href.includes(kuisMatch) || href.endsWith(kuisMatch + '.html')) {
        setActive(a); break;
      }
    }
  }

  // 4) fallback evaluasi mapping (evaluasi.html dan evaluasi1.html -> link evaluasi.html aktif)
  if (!activeLink && (currentFile === 'evaluasi.html' || currentFile === 'evaluasi1.html')) {
    for (const a of links) {
      const hrefFile = (a.getAttribute('href') || '').split('?')[0].split('/').pop()?.toLowerCase();
      if (hrefFile === 'evaluasi.html') { setActive(a); break; }
    }
  }

  // 5) jika masih belum ada yang aktif: coba buka section 'KUIS' agar user melihat daftar kuis
  if (!activeLink && sidebar) {
    // cari header/accordion yang teksnya mengandung 'kuis'
    const headers = Array.from(sidebar.querySelectorAll('button, .accordion-button, .nav-header, h6, .sidebar-section'));
    for (const h of headers) {
      const txt = (h.textContent || '').trim().toLowerCase();
      if (txt.includes('kuis')) {
        // open its sibling collapse if present
        const collapse = h.closest('.accordion-item')?.querySelector('.accordion-collapse') || h.nextElementSibling;
        if (collapse) collapse.classList.add('show');
        if (h.classList.contains('collapsed')) h.classList.remove('collapsed');
        if (h.setAttribute) h.setAttribute('aria-expanded', 'true');
        // remove overall collapsed class so sidebar visible
        if (app && app.classList.contains('is-collapsed')) app.classList.remove('is-collapsed');
        console.log('[SIDEBAR DEBUG] opened KUIS section fallback');
        break;
      }
    }
  }

  console.log('[SIDEBAR DEBUG] activeLink=', activeLink);
});
