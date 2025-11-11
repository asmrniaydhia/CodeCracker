// ===============================
// START EVALUASI — KONFIRMASI MULAI
// ===============================
document.getElementById('startBtn')?.addEventListener('click', () => {
  const agree = document.getElementById('agreeCheck');
  if (!agree.checked) {
    agree.focus();
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 start-50 translate-middle-x mt-3 alert alert-warning shadow';
    toast.style.zIndex = 1080;
    toast.innerHTML = '<i class="fa-solid fa-triangle-exclamation me-2"></i>Centang persetujuan terlebih dahulu.';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2200);
    return;
  }
  const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
  modal.show();
});

// ===============================
// BAGIAN LOGIKA EVALUASI
// ===============================
document.addEventListener("DOMContentLoaded", function () {
  const KKM = 70;
  const quizKey = "evaluasi";

  // ===============================
  // HALAMAN NILAI (nilaiEval.html)
  // ===============================
  if (window.location.pathname.includes("nilaiEval.html")) {
    const score = parseInt(localStorage.getItem(`${quizKey}_nilai`) || "0");
    const detail = JSON.parse(localStorage.getItem(`${quizKey}_detail`) || "{}");
    const benar = detail.correct || 0;
    const total = detail.total || 0;

    const scoreNum = document.getElementById("scoreNum");
    const correctCount = document.getElementById("correctCount");
    const totalCount = document.getElementById("totalCount");
    const passFail = document.getElementById("passFail");
    const grade = document.getElementById("grade");
    const ring = document.getElementById("scoreRing");
    const answerTable = document.getElementById("answerTable");

    scoreNum.textContent = score;
    correctCount.textContent = benar;
    totalCount.textContent = total;
    ring.style.setProperty("--p", score);

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
    return;
  }

  // ===============================
  // SOAL EVALUASI (BAB 2–4)
  // ===============================
  const questions = [
    // 🔹 PILIHAN GANDA
    {
      question: "Enkripsi disebut berhasil jika …",
      options: [
        "Ciphertext tidak dapat dimengerti tanpa kunci",
        "Plaintext dan ciphertext memiliki arti yang sama",
        "Semua orang bisa membaca ciphertext",
        "Pesan berubah tetapi tetap mudah ditebak",
      ],
      correct: 0,
      type: "mcq",
    },
    {
      question: "Caesar Cipher termasuk kriptografi simetris karena …",
      options: [
        "Menggunakan dua kunci berbeda",
        "Kunci enkripsi dan dekripsi sama",
        "Tidak membutuhkan kunci",
        "Menggunakan kunci acak setiap kali",
      ],
      correct: 1,
      type: "mcq",
    },
    {
      question: 'Gunakan kunci 3 untuk mengenkripsi kata “DATA”.',
      options: ["GDXD", "EDWD", "FDXD", "GDWD"],
      correct: 3,
      type: "mcq",
    },
    {
      question: 'Dekripsilah ciphertext “WKH” dengan kunci 3.',
      options: ["THE", "QEB", "ZKH", "TXE"],
      correct: 0,
      type: "mcq",
    },
    {
      question:
        'Seseorang mengenkripsi pesan “SEHAT” dengan kunci 5, tetapi penerima melakukan dekripsi dengan kunci 4. Apa akibatnya?',
      options: [
        "Pesan tetap terbaca benar",
        "Pesan rusak karena pergeseran tidak sesuai",
        "Pesan berubah menjadi plaintext semula",
        "Pesan hilang seluruhnya",
      ],
      correct: 1,
      type: "mcq",
    },
    {
      question: "Mengapa Caesar Cipher dianggap lemah dari sisi keamanan modern?",
      options: [
        "Karena terlalu banyak kunci yang mungkin",
        "Karena hasil enkripsinya selalu sama",
        "Karena hanya memiliki 25 kemungkinan kunci",
        "Karena tidak bisa mengenkripsi angka",
      ],
      correct: 2,
      type: "mcq",
    },
    {
      question: "Dalam komunikasi digital, dekripsi dilakukan oleh pihak …",
      options: ["Pengirim", "Server", "Penerima", "Penyedia layanan"],
      correct: 2,
      type: "mcq",
    },
    {
      question: "Urutan yang benar dari proses komunikasi aman adalah …",
      options: [
        "Dekripsi → Enkripsi → Pengiriman",
        "Enkripsi → Pengiriman → Dekripsi",
        "Pengiriman → Dekripsi → Enkripsi",
        "Enkripsi → Dekripsi → Pengiriman",
      ],
      correct: 1,
      type: "mcq",
    },
    {
      question:
        'Seorang siswa menulis ciphertext “YMNX NX F YJXY” hasil dari plaintext “THIS IS A TEST”. Kunci yang digunakan adalah …',
      options: ["2", "3", "4", "5"],
      correct: 3,
      type: "mcq",
    },
    {
      question:
        'Ciphertext “JCU” jika didekripsi dengan kunci 2 menjadi “HAS”. Jika ingin mengirim kembali pesan yang sama, tetapi hasil ciphertext-nya berbeda, maka tindakan yang paling logis adalah …',
      options: [
        "Mengganti algoritma enkripsi",
        "Mengubah posisi huruf secara acak tanpa kunci",
        "Menambah kunci menjadi 4",
        "Menghapus proses dekripsi",
      ],
      correct: 0,
      type: "mcq",
    },
    // 🔹 ISIAN SINGKAT
    {
      question: "Proses mengubah ciphertext menjadi bentuk asli disebut ____________.",
      answer: "Dekripsi",
      type: "fill",
    },
    {
      question: 'Enkripsilah “KOMPUTER” dengan kunci 2 → hasil ciphertext: ____________.',
      answer: "MQORWVGT",
      type: "fill",
    },
    {
      question: 'Dekripsilah ciphertext “ZRUOG” dengan kunci 3 → plaintext: ____________.',
      answer: "WORLD",
      type: "fill",
    },
    {
      question:
        "Jumlah maksimum kemungkinan kunci dalam Caesar Cipher adalah ____________.",
      answer: "25",
      type: "fill",
    },
    {
      question:
        "Dalam Caesar Cipher, huruf digeser sejauh jumlah langkah yang disebut ____________.",
      answer: "Kunci",
      type: "fill",
    },
  ];

  let currentQuestion = 1;
  const totalQuestions = questions.length;
  let answers = JSON.parse(localStorage.getItem(`${quizKey}_answers`) || "{}");

  const soalContainer = document.querySelector("ol.teks");
  const quizTitle = document.querySelector(".quiz-title");
  const nextBtn = document.querySelector(".btn-success");
  const prevBtn = document.querySelector(".btn-danger");
  const submitBtn = document.getElementById("submitQuiz");
  const bubbleContainer = document.querySelector(".bubbles");

  // BUAT BUBBLE NAVIGASI
  bubbleContainer.innerHTML = "";
  for (let i = 1; i <= totalQuestions; i++) {
    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = i;
    bubbleContainer.appendChild(bubble);
  }
  const bubbles = document.querySelectorAll(".bubble");

  function updateBubbles(activeNum) {
    bubbles.forEach((bubble, index) => {
      const num = index + 1;
      bubble.classList.remove("current", "answered");
      if (num === activeNum) bubble.classList.add("current");
      if (answers[num] !== undefined && answers[num] !== "") bubble.classList.add("answered");
    });
  }

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
    if (q.type === "mcq") {
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
        </div>`;
      soalContainer.querySelectorAll(`input[name="q${num}"]`).forEach((input) => {
        input.addEventListener("change", (e) => {
          answers[num] = parseInt(e.target.value);
          localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
          updateBubbles(num);
        });
      });
    } else {
      soalContainer.innerHTML = `
        <li>
          <p class="fw-bold mb-2">${q.question}</p>
          <input type="text" class="form-control" placeholder="Ketik jawaban..." value="${
            answers[num] || ""
          }">
        </li>`;
      soalContainer.querySelector("input").addEventListener("input", (e) => {
        answers[num] = e.target.value.trim();
        localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
        updateBubbles(num);
      });
    }
    updateBubbles(num);
  }

  // TIMER (60 MENIT)
  let totalSeconds = 60 * 60;
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
        window.location.href = "nilaiEval.html";
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
    const detailAnswers = [];

    questions.forEach((q, i) => {
      let userAnswer = answers[i + 1];
      let isCorrect = false;
      if (q.type === "mcq") {
        isCorrect = userAnswer === q.correct;
      } else {
        isCorrect =
          userAnswer &&
          userAnswer.toString().trim().toUpperCase() === q.answer.toUpperCase();
      }
      if (isCorrect) benar++;
      detailAnswers.push({
        question: q.question,
        userAnswerText: userAnswer || "(kosong)",
        correctAnswerText: q.type === "mcq" ? q.options[q.correct] : q.answer,
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

    localStorage.removeItem(`${quizKey}_answers`);

    window.location.href = "nilaiEval.html";
  });

  renderQuestion(currentQuestion);
});