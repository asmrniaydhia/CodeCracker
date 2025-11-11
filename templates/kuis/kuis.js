// Ambil parameter target dari URL
const urlParams = new URLSearchParams(window.location.search);
const targetQuiz = urlParams.get('target'); // misalnya "kuis1.html"
// Tambahan agar tiap kuis punya penyimpanan unik
const quizKey = window.location.pathname.split("/").pop().replace(".html", ""); 

// Tombol "Mulai Kuis"
document.getElementById('startBtn')?.addEventListener('click', (e) => {
    e.preventDefault();

    const agree = document.getElementById('agreeCheck');
    if (!agree.checked) {
        agree.focus();
        alert("Centang dulu 'Saya siap dan memahami petunjuk'.");
        return;
    }

    // Tampilkan modal konfirmasi
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    confirmModal.show();

    // Ubah tautan "Ya, Mulai!" di dalam modal agar menuju target yang benar
    const startLink = document.querySelector('#confirmModal a.btn-success');
    if (targetQuiz) {
      startLink.setAttribute('href', `${targetQuiz}`);
    } else {
      startLink.setAttribute('href', 'kuis1.html');
    }
});

// Bagian Logika Kuis
document.addEventListener("DOMContentLoaded", function () {
  const KKM = 70;

  // BAGIAN HASIL (nilaiKuis.html)
  if (window.location.pathname.includes("nilaiKuis.html")) {
    
    // const quizKey = window.location.pathname.split("/").pop().replace(".html", ""); 
    // Ambil parameter target dari URL, misalnya ?target=kuis1
    const urlParams = new URLSearchParams(window.location.search);
    const quizKey = urlParams.get("target");

    if (!quizKey) {
      alert("Data kuis tidak ditemukan. Pastikan Anda membuka dari halaman kuis!");
      return;
    }

    const score = parseInt(localStorage.getItem(`${quizKey}_nilai`) || "0");
    const detail = JSON.parse(localStorage.getItem(`${quizKey}_detail`) || "{}");
    const benar = detail.correct || 0;
    const total = detail.total || 0;

    // Elemen ringkasan
    const scoreNum = document.getElementById("scoreNum");
    const correctCount = document.getElementById("correctCount");
    const totalCount = document.getElementById("totalCount");
    const passFail = document.getElementById("passFail");
    const grade = document.getElementById("grade");
    const ring = document.getElementById("scoreRing");
    const answerTable = document.getElementById("answerTable");

    // Isi nilai utama
    scoreNum.textContent = score;
    correctCount.textContent = benar;
    totalCount.textContent = total;
    ring.style.setProperty("--p", score);

    // Status kelulusan
    if (score >= KKM) {
      passFail.textContent = "Lulus ✅";
      passFail.classList.add("text-success");
      grade.textContent = "Baik";
      grade.classList.replace("bg-light", "bg-success");
      grade.classList.add("text-white");
    } else {
      passFail.textContent = "Tidak Lulus ❌";
      passFail.classList.add("text-danger");
      grade.textContent = "Perlu Mengulang";
      grade.classList.replace("bg-light", "bg-danger");
      grade.classList.add("text-white");
    }

    // Ulangi Kuis
    const backToQuiz = document.getElementById("backToQuiz");
    if (backToQuiz) backToQuiz.href = `${quizKey}.html`;

    // Tabel rincian jawaban
    if (detail.answers && Array.isArray(detail.answers)) {
      answerTable.innerHTML = "";
      detail.answers.forEach((item, index) => {
        const row = document.createElement("tr");
        const benarSalah = item.isCorrect
          ? '<span class="text-success fw-bold">Benar</span>'
          : '<span class="text-danger fw-bold">Salah</span>';
        row.innerHTML = `
          <td>${index + 1}</td>
          <td>${item.question}</td>
          <td>${item.userAnswerText}</td>
          <td>${benarSalah}</td>
        `;
        answerTable.appendChild(row);
      });
    }

    return; // Stop di halaman nilai
  }

  // BAGIAN SOAL PER FILE
  let questions = [];

  if (window.location.href.includes("kuis1.html")) {
    // BAB 2 – ENKRIPSI
    questions = [
      {
        question: "Fungsi utama dari kunci (key) dalam enkripsi adalah …",
        options: [
          "Menentukan banyaknya pergeseran huruf",
          "Mengatur panjang kata",
          "Menghapus tanda baca",
          "Mengubah huruf menjadi angka",
        ],
        correct: 0,
      },
      {
        question: "Enkripsilah pesan “BELAJAR” dengan kunci 3.",
        options: ["EHODMDU", "EIOEMDU", "DGNCMET", "EHOEMDV"],
        correct: 0,
      },
      {
        question: "Enkripsilah kata “DATA” menggunakan kunci 5.",
        options: ["IFYF", "IFYJ", "IFYI", "IFYG"],
        correct: 3,
      },
      {
        question:
          "Pesan “EHOEMDU” dienkripsi dengan kunci 3. Plaintext-nya adalah …",
        options: ["BELAJAR", "CELAJAR", "DELAJAR", "BEMAJAR"],
        correct: 0,
      },
      {
        question:
          "Berikut ini contoh penerapan enkripsi dalam kehidupan sehari-hari, kecuali …",
        options: [
          "Memberi password pada file",
          "Menggunakan HTTPS saat browsing",
          "Menyimpan soal ulangan tanpa password",
          "Mengunci dokumen dengan kode",
        ],
        correct: 2,
      },
    ];
  } else if (window.location.href.includes("kuis2.html")) {
    // BAB 3 – CAESAR CIPHER
    questions = [
      {
        question: "Caesar Cipher ditemukan oleh …",
        options: [
          "Julius Caesar",
          "Leonardo da Vinci",
          "Alan Turing",
          "Archimedes",
        ],
        correct: 0,
      },
      {
        question: "Gunakan kunci 4 untuk mengenkripsi kata “DATA”.",
        options: ["HEVE", "HEZE", "HEYA", "HEWE"],
        correct: 1,
      },
      {
        question: "Gunakan kunci 2 untuk mengenkripsi pesan “RAHASIA”.",
        options: ["TCJCUKC", "TCKCUKD", "SBHBRHZ", "UBKBVLB"],
        correct: 1,
      },
      {
        question: "Dekripsi pesan “VHUDQJ” dengan kunci 3.",
        options: ["SERANG", "RDPZLF", "QCOZMF", "SHSANG"],
        correct: 0,
      },
      {
        question:
          "Mengapa Caesar Cipher tidak digunakan dalam keamanan modern?",
        options: [
          "Karena terlalu mudah dipecahkan",
          "Karena hanya bisa digunakan di komputer",
          "Karena membutuhkan kunci ganda",
          "Karena tidak bisa dienkripsi",
        ],
        correct: 0,
      },
    ];
  } else if (window.location.href.includes("kuis3.html")) {
    // BAB 4 – DEKRIPSI
    questions = [
      {
        question: "Apa arti dari dekripsi?",
        options: [
          "Mengembalikan ciphertext menjadi plaintext",
          "Mengubah plaintext menjadi ciphertext",
          "Menambah kunci pada pesan",
          "Menghapus sebagian pesan",
        ],
        correct: 0,
      },
      {
        question: "Dekripsi pesan “KHOOR” dengan kunci 3.",
        options: ["HELLO", "WORLD", "HILLO", "HALLO"],
        correct: 0,
      },
      {
        question: "Dekripsi pesan “YJHMSNVZ” menggunakan kunci 5.",
        options: ["TEACHING", "SCHOOL", "COMPUTER", "STUDENT"],
        correct: 0,
      },
      {
        question: "Enkripsilah kata “WORLD” dengan kunci 3.",
        options: ["ZRUOG", "ZQUMF", "ZSUOF", "ZTUOG"],
        correct: 0,
      },
      {
        question:
          "Ketika kamu membuka file yang diproteksi dengan password, proses itu disebut …",
        options: ["Dekripsi", "Enkripsi", "Hashing", "Kompresi"],
        correct: 0,
      },
    ];
  } else if (window.location.pathname.includes("kuis4.html")) {
  // KUIS GABUNGAN BAB 2–4
  questions = [
    {
      question: "Dalam proses komunikasi digital yang aman, pengirim menggunakan Caesar Cipher untuk mengamankan pesan, sementara penerima menggunakan kunci yang sama untuk membukanya. Dari situasi ini, kesimpulan yang benar adalah …",
      options: [
        "Caesar Cipher termasuk kriptografi asimetris karena hanya pengirim yang tahu kunci.",
        "Caesar Cipher termasuk kriptografi simetris karena pengirim dan penerima memakai kunci yang sama.",
        "Caesar Cipher tidak termasuk metode enkripsi karena bisa dibaca siapa saja.",
        "Caesar Cipher hanya berfungsi untuk mengubah angka, bukan huruf."
      ],
      correct: 1
    },
    {
      question: "Pesan “BELAJAR” dikirim menggunakan Caesar Cipher dengan kunci 4. Namun, penerima secara tidak sengaja mendekripsi dengan kunci 3. Apa hasil teks yang diterima, dan apa kesimpulan yang dapat dibuat dari perbedaan kunci tersebut?",
      options: [
        "Pesan terbaca “EHODMDU”, dan hasilnya tetap benar karena kunci berbeda tidak berpengaruh.",
        "Pesan terbaca “DGMCLCS”, dan hasilnya tidak bermakna karena pergeseran tidak sesuai.",
        "Pesan terbaca “FIPBNEV”, dan hasilnya tetap benar karena enkripsi otomatis menyesuaikan.",
        "Pesan tidak berubah sama sekali."
      ],
      correct: 1
    },
    {
      question: "Seseorang ingin mengenkripsi kata “INFORMATIKA” agar tidak mudah dibaca. Ia menggunakan Caesar Cipher dengan kunci 5, tetapi ingin agar hasilnya tetap dapat didekripsi oleh penerima tanpa membocorkan kuncinya di pesan. Langkah terbaik yang bisa ia lakukan adalah …",
      options: [
        "Mengirim ciphertext saja tanpa menjelaskan algoritmanya.",
        "Menggunakan kunci publik yang berbeda dari kunci dekripsi.",
        "Mengirim pesan dan kunci dalam satu teks agar mudah dibaca.",
        "Menyepakati algoritma dan kunci terlebih dahulu sebelum pesan dikirim."
      ],
      correct: 3
    },
    {
      question: "Ciphertext yang diterima adalah “ZRUOG”, dan penerima tahu kuncinya adalah 3. Apa plaintext yang benar, dan apa makna proses tersebut?",
      options: [
        "Hasilnya “WORLD”; proses ini disebut dekripsi, yaitu mengembalikan ciphertext ke bentuk asli.",
        "Hasilnya “HELLO”; proses ini disebut enkripsi, yaitu menyembunyikan pesan.",
        "Hasilnya “WORLD”; proses ini disebut enkripsi, karena menggunakan kunci yang sama.",
        "Hasilnya “HELLO”; proses ini disebut dekripsi, yaitu menyandikan pesan."
      ],
      correct: 0
    },
    {
      question: "“Metode Caesar Cipher mudah dipelajari dan cocok untuk siswa SMP, tetapi tidak aman untuk melindungi data penting.” Berdasarkan pemahamanmu, alasan utama metode ini dianggap tidak aman adalah …",
      options: [
        "Karena hasil enkripsinya selalu menggunakan huruf kapital.",
        "Karena jumlah kemungkinan kunci terlalu sedikit, sehingga mudah ditebak.",
        "Karena hanya dapat digunakan dalam bahasa Latin.",
        "Karena tidak memerlukan proses dekripsi."
      ],
      correct: 1
    }
  ];
}

  // BAGIAN SHUFFLE
  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
  }

  if (!localStorage.getItem(`${quizKey}_order`)) {
      shuffle(questions);
      localStorage.setItem(`${quizKey}_order`, JSON.stringify(questions));
  } else {
      questions = JSON.parse(localStorage.getItem(`${quizKey}_order`));
  }

  let currentQuestion = 1;
  const totalQuestions = questions.length;
  let answers = JSON.parse(localStorage.getItem(`${quizKey}_answers`) || "{}");
  let flagged = JSON.parse(localStorage.getItem(`${quizKey}_flagged`) || "{}");

  const soalContainer = document.querySelector("div.teks");
  const quizTitle = document.querySelector(".quiz-title");
  const nextBtn = document.querySelector(".btn-success");
  const prevBtn = document.querySelector(".btn-danger");
  const submitBtn = document.getElementById("submitQuiz");
  const bubbleContainer = document.querySelector(".bubbles");

  // BUBBLE NAVIGATION
  // BUAT BUBBLE OTOMATIS
  bubbleContainer.innerHTML = "";
  for (let i = 1; i <= totalQuestions; i++) {
    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = i;
    bubbleContainer.appendChild(bubble);
  }
  const bubbles = document.querySelectorAll(".bubble");

  // UPDATE STATUS BUBBLE
  function updateBubbles(activeNum) {
    bubbles.forEach((bubble, index) => {
      const num = index + 1;
      bubble.classList.remove("current", "answered", "flagged");
      if (num === activeNum) bubble.classList.add("current");
      if (answers[num] !== undefined) bubble.classList.add("answered");
      if (flagged[num]) bubble.classList.add("flagged");
    });
  }

  function updateBubbleAnswered(num) {
    const bubble = bubbles[num - 1];
    if (answers[num] !== undefined) bubble.classList.add("answered");
    else bubble.classList.remove("answered");
  }

  function updateButtons(num) {
    prevBtn.classList.toggle("disabled", num <= 1);
    nextBtn.classList.toggle("disabled", num >= totalQuestions);
  }

  // EVENT BUBBLE
  bubbles.forEach((bubble, index) => {
    bubble.addEventListener("click", () => {
      currentQuestion = index + 1;
      renderQuestion(currentQuestion);
    });
  });

  // RENDER SOAL
  function renderQuestion(num) {
    const q = questions[num - 1];
    quizTitle.textContent = "Soal " + num;

    // Render isi soal
    soalContainer.innerHTML = `
      <div>
        <p class="fw-bold mb-2">${q.question}</p>
        ${q.options
          .map(
            (opt, idx) => `
          <div><label>
            <input type="radio" name="q${num}" value="${idx}" ${
              answers[num] == idx ? "checked" : ""
            }> ${opt}
          </label></div>
        `
          )
          .join("")}
        <div class="mt-3">
          <button id="unsureBtn" class="btn btn-outline-warning text-dark px-2">
            ${flagged[num] ? "Batalkan Ragu-ragu" : "Tandai Ragu-ragu"}
          </button>
        </div>
      </div>
    `;

    // Event saat memilih jawaban
    soalContainer.querySelectorAll(`input[name="q${num}"]`).forEach((input) => {
      input.addEventListener("change", (e) => {
        answers[num] = parseInt(e.target.value);
        localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
        updateBubbles(num);
      });
    });

    // Event tombol Ragu-ragu
    const unsureBtn = document.getElementById("unsureBtn");
    unsureBtn.addEventListener("click", (e) => {
      e.preventDefault();
      flagged[num] = !flagged[num];
      localStorage.setItem(`${quizKey}_flagged`, JSON.stringify(flagged));
      unsureBtn.textContent = flagged[num]
        ? "Batalkan Ragu-ragu"
        : "Tandai Ragu-ragu";
      updateBubbles(num);
    });

    updateBubbles(num);
  }


  // TIMER (20 MENIT)
  let totalSeconds = 20 * 60;
  const timerDisplay = document.querySelector(".side-card h5.text-danger");

  function updateTimer() {
    let minutes = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    timerDisplay.textContent = `Waktu Tersisa: ${minutes}:${seconds}`;
  }

  function startTimer() {
    const timerInterval = setInterval(() => {
      if (totalSeconds > 0) {
        totalSeconds--;
        updateTimer();
      } else {
        clearInterval(timerInterval);
        alert("Waktu habis! Jawaban Anda akan dikumpulkan otomatis.");
        window.location.href = `nilaiKuis.html?target=${quizKey}`;
      }
    }, 1000);
  }

  updateTimer();
  startTimer();

  // NAVIGASI
  prevBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (currentQuestion > 1) {
      currentQuestion--;
      renderQuestion(currentQuestion);
    }
  });

  nextBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (currentQuestion < totalQuestions) {
      currentQuestion++;
      renderQuestion(currentQuestion);
    }
  });

  // PENILAIAN
  submitBtn.addEventListener("click", () => {
    let benar = 0;
    let detailAnswers = [];

    questions.forEach((q, i) => {
      const userAnswer = answers[i + 1];
      const isCorrect = userAnswer === q.correct;
      if (isCorrect) benar++;
      detailAnswers.push({
        question: q.question,
        userAnswerText:
          userAnswer !== undefined ? q.options[userAnswer] : "(kosong)",
        correctAnswerText: q.options[q.correct],
        isCorrect,
      });
    });

    const score = Math.round((benar / totalQuestions) * 100);

    localStorage.setItem(`${quizKey}_nilai`, score);
    localStorage.setItem(
      `${quizKey}_detail`,
      JSON.stringify({
        correct: benar,
        total: totalQuestions,
        answers: detailAnswers,
      })
    );

    // bersihkan sesi lama
    localStorage.removeItem(`${quizKey}_answers`);
    localStorage.removeItem(`${quizKey}_order`);

    window.location.href = `nilaiKuis.html?target=${quizKey}`;
  });

  renderQuestion(currentQuestion);
});
