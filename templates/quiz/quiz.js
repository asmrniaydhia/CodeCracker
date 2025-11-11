// ===================== PERSISTENSI QUIZ =====================
// Konfigurasi
const STORAGE_KEY = 'cc_quiz_states_v1'; // { "1": {answered:true, flagged:false}, ... }
const QUIZ_BASE = ''; // contoh jika file di folder: '/templates/quiz/'

// Helpers storage
function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch { return {}; }
}
function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

// Dapatkan nomor soal saat ini dari bubble yang punya .current
function getCurrentQuestionNumber() {
    const cur = document.querySelector('.bubbles .bubble.current');
    if (!cur) return null;
    const n = parseInt(cur.textContent.trim(), 10);
    return Number.isFinite(n) ? n : null;
}

// Tentukan apakah halaman ini "terjawab"
function pageAnswered() {
    const scope = document.querySelector('.quiz-card') || document;
    // any input text/number/email/password non-empty, textarea non-empty, select punya value, radio/checkbox checked
    const hasText = Array.from(scope.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="password"], textarea, select'))
        .some(el => (el.value || '').trim().length > 0);
    const hasChoice = scope.querySelector('input[type="radio"]:checked, input[type="checkbox"]:checked') !== null;
    return hasText || hasChoice;
}

// Terapkan state ke bubbles (kecuali current yang tetap 'current')
function applyBubbleStates() {
    const state = loadState();
    const bubbles = document.querySelectorAll('.bubbles .bubble');
    const currentN = getCurrentQuestionNumber();

    bubbles.forEach(b => {
        // reset kelas
        b.classList.remove('current', 'answered', 'flagged', 'empty');
        const num = parseInt(b.textContent.trim(), 10);
        if (Number.isNaN(num)) return;

        // current selalu prioritas tampil
        if (num === currentN) {
            b.classList.add('current');
            return;
        }

        const s = state[num] || {};
        if (s.flagged) b.classList.add('flagged');
        else if (s.answered) b.classList.add('answered');
        else b.classList.add('empty');
    });
}

// Simpan state halaman saat ini
function saveCurrentPageState() {
    const qn = getCurrentQuestionNumber();
    if (!qn) return;
    const state = loadState();
    state[qn] = state[qn] || {};
    state[qn].answered = pageAnswered();
    // flag dibaca dari checkbox #flag kalau ada
    const flagEl = document.getElementById('flag');
    state[qn].flagged = !!(flagEl && flagEl.checked);
    saveState(state);
}

// Event: perubahan jawaban apapun
const scope = document.querySelector('.quiz-card') || document;
scope.addEventListener('input', saveCurrentPageState, true);
scope.addEventListener('change', saveCurrentPageState, true);

// Inisialisasi saat load
document.addEventListener('DOMContentLoaded', () => {
    // Pulihkan posisi checkbox ragu-ragu sesuai state (opsional, jika ingin)
    const qn = getCurrentQuestionNumber();
    const st = loadState();
    const flagEl = document.getElementById('flag');
    if (qn && flagEl && st[qn]) flagEl.checked = !!st[qn].flagged;

    applyBubbleStates();
});

// Klik bubble -> simpan state dahulu, lalu navigasi
document.querySelectorAll('.bubbles .bubble').forEach(b => {
    b.addEventListener('click', () => {
        saveCurrentPageState();
        const target = (b.dataset.href || '').trim();
        if (target) window.location.href = QUIZ_BASE + target;
    });
});

// Tombol Navigasi (Jika ingin memastikan juga tersimpan saat Next/Prev)
document.querySelectorAll('.quiz-actions a[href]').forEach(a => {
    a.addEventListener('click', (e) => {
        // biar sempat save sebelum pindah
        saveCurrentPageState();
    });
});

// Cadangan: sebelum keluar halaman
window.addEventListener('beforeunload', saveCurrentPageState);

(function() {
  const TIMER_KEY = 'cc_quiz_timer_v1';
  const DURATION_MINUTES = 20; // durasi total
  const END_PAGE = 'quiz.html'; // halaman tujuan jika waktu habis

  const timerDisplay = document.querySelector('.side-card .text-danger.fw-bold');

  // Ambil waktu selesai dari localStorage, atau set baru jika belum ada
  let endTime = localStorage.getItem(TIMER_KEY);
  if (!endTime) {
    const end = new Date();
    end.setMinutes(end.getMinutes() + DURATION_MINUTES);
    endTime = end.getTime();
    localStorage.setItem(TIMER_KEY, endTime);
  } else {
    endTime = parseInt(endTime);
  }

  function updateTimer() {
    const now = new Date().getTime();
    const distance = endTime - now;

    if (distance <= 0) {
      localStorage.removeItem(TIMER_KEY); // reset timer
      if (timerDisplay) timerDisplay.textContent = "Waktu Habis";
      alert("Waktu kamu sudah habis!"); // bisa ganti jadi redirect
      window.location.href = END_PAGE;
      return;
    }

    const minutes = Math.floor((distance / 1000 / 60));
    const seconds = Math.floor((distance / 1000) % 60);
    const mm = String(minutes).padStart(2, '0');
    const ss = String(seconds).padStart(2, '0');

    if (timerDisplay) timerDisplay.textContent = `Waktu Tersisa: ${mm}:${ss}`;
  }

  updateTimer();
  setInterval(updateTimer, 1000);
})();

/* =========================================================
   CodeCracker — Simpan Jawaban & Hitung Nilai Otomatis
   ========================================================= */
(function () {
  const ANSWER_KEY = 'cc_answers_v2';
  const SCORE_KEY  = 'cc_quiz_score_v2';

  // ==== util dasar ====
  const $  = (s, r=document)=>r.querySelector(s);
  const $$ = (s, r=document)=>Array.from(r.querySelectorAll(s));
  const norm = s => (s||'').toString().toLowerCase().replace(/\s+/g,'').trim();

  function caesar(str, shift){
    let out=''; const a='a'.charCodeAt(0), z='z'.charCodeAt(0),
          A='A'.charCodeAt(0), Z='Z'.charCodeAt(0);
    for(const ch of str){
      const c=ch.charCodeAt(0);
      if(c>=a&&c<=z) out+=String.fromCharCode(((c-a+shift)%26+26)%26+a);
      else if(c>=A&&c<=Z) out+=String.fromCharCode(((c-A+shift)%26+26)%26+A);
      else out+=ch;
    }
    return out;
  }

  function load(){ try{return JSON.parse(localStorage.getItem(ANSWER_KEY))||{}}catch{ return {} } }
  function save(obj){ localStorage.setItem(ANSWER_KEY, JSON.stringify(obj)) }
  function setVal(k,v){ const d=load(); d[k]=v; save(d) }
  function getVal(k,def=''){ const d=load(); return d[k]??def }

  // ==== daftar elemen yang disimpan ====
  const INPUT_IDS = [
    'ans1_1','ans1_2',
    'ans2_1','ans2_2','ans2_3',
    'ans3_1','ans3_2',
    'match1','match2','match3','match4','match5'
  ];
  const RADIO_GROUPS = [
    'kesimpulan_kunci', 'statement1', 'statement2', 'statement3'
  ];

  // ==== pulihkan nilai dari localStorage ====
  document.addEventListener('DOMContentLoaded', () => {
    INPUT_IDS.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      const v = getVal(id,'');
      if (v) el.value = v;
      el.addEventListener('input', ()=>setVal(id,el.value));
      el.addEventListener('change',()=>setVal(id,el.value));
    });

    RADIO_GROUPS.forEach(name => {
      const saved = getVal(name,'');
      if (saved) {
        const r = $(`input[name="${name}"][value="${saved}"]`);
        if (r) r.checked = true;
      }
      $$(`input[name="${name}"]`).forEach(r=>{
        r.addEventListener('change',()=>{
          const sel=$(`input[name="${name}"]:checked`);
          setVal(name, sel?sel.value:'');
        });
      });
    });
  });

  // ==== Kunci jawaban ====
  const A1 = { encPlain:'keamanan data', encKey:3, decCipher:'xvkrph lwlrq', decKey:4 };
  const A2 = { plain:'selamat pagi', mcq:'C' };
  const A4 = { statement1:'benar', statement2:'salah', statement3:'benar' };
  const A5 = { match1:'d', match2:'a', match3:'b', match4:'c', match5:'e' };
  const A3_CIPHER = 'xvkrph lwlrq';

  // ==== Fungsi hitung nilai ====
  function hitungNilai() {
    const get = (id) => getVal(id,'');
    const getRadio = (name) => getVal(name,'');

    let benar = 0, total = 0;

    // Aktivitas 1
    total += 2;
    if (norm(get('ans1_1')) === norm(caesar(A1.encPlain, A1.encKey))) benar++;
    if (norm(get('ans1_2')) === norm(caesar(A1.decCipher, -A1.decKey))) benar++;

    // Aktivitas 2
    total += 4;
    if (norm(get('ans2_1')) === norm(caesar(A2.plain,2))) benar++;
    if (norm(get('ans2_2')) === norm(caesar(A2.plain,5))) benar++;
    if (norm(get('ans2_3')) === norm(caesar(A2.plain,7))) benar++;
    if ((getRadio('kesimpulan_kunci')||'').toUpperCase() === A2.mcq) benar++;

    // Aktivitas 3
    total += 2;
    const k = parseInt(get('ans3_1'),10);
    const pt = norm(get('ans3_2'));
    const validK = Number.isFinite(k)&&k>=1&&k<=25;
    if (validK && pt === norm(caesar(A3_CIPHER, -k))) benar += 2;

    // Aktivitas 4
    total += 3;
    if ((getRadio('statement1')||'').toLowerCase() === A4.statement1) benar++;
    if ((getRadio('statement2')||'').toLowerCase() === A4.statement2) benar++;
    if ((getRadio('statement3')||'').toLowerCase() === A4.statement3) benar++;

    // Aktivitas 5
    total += 5;
    ['match1','match2','match3','match4','match5'].forEach(id=>{
      if ((get(id)||'').toLowerCase() === A5[id]) benar++;
    });

    const nilai = Math.round((benar/total)*100);
    localStorage.setItem(SCORE_KEY, nilai);
    return nilai;
  }

  // ==== Hitung otomatis saat user keluar halaman ====
  window.addEventListener('beforeunload', hitungNilai);
})();
