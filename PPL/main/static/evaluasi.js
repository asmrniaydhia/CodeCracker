const quizKey = "evaluasi";

// START EVALUASI — KONFIRMASI MULA
document.getElementById("startBtn")?.addEventListener("click", () => {
  const agree = document.getElementById("agreeCheck");
  if (!agree.checked) {
    agree.focus();
    const toast = document.createElement("div");
    toast.className =
      "position-fixed top-0 start-50 translate-middle-x mt-3 alert alert-warning shadow";
    toast.style.zIndex = 1080;
    toast.innerHTML =
      '<i class="fa-solid fa-triangle-exclamation me-2"></i>Centang persetujuan terlebih dahulu.';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2200);
    return;
  }

  const modal = new bootstrap.Modal(document.getElementById("confirmModal"));
  modal.show();
});

// Helper untuk membersihkan jawaban sementara di localStorage
function clearTemporaryAnswers() {
  localStorage.removeItem(`${quizKey}_answers`);
  localStorage.removeItem(`${quizKey}_flagged`);
}

function handleBeforeUnload(e) {
  clearTemporaryAnswers();
  const confirmationMessage =
    "Jawaban Anda akan hilang jika Anda meninggalkan halaman ini sekarang.";
  (e || window.event).returnValue = confirmationMessage;
  return confirmationMessage;
}

// START EVALUASI — KONFIRMASI MULA (Blok yang Perlu Direvisi)
document.getElementById("startBtn")?.addEventListener("click", () => {
  // ... [Logika validasi & show modal] ...

  const modal = new bootstrap.Modal(document.getElementById("confirmModal"));
  modal.show();

  // 🎯 KOREKSI UTAMA: Tangkap tombol konfirmasi di dalam modal
  const startLink = document.querySelector("#confirmModal a.btn-success"); // Asumsi tombolnya adalah <a> dengan class .btn-success

  startLink.addEventListener("click", function () {
    // Hapus event beforeunload global agar bisa navigasi tanpa peringatan
    window.removeEventListener("beforeunload", handleBeforeUnload);
    // Catatan: Navigasi akan terjadi karena tombol startLink memiliki href="/evaluasi/pengerjaan/"
    clearTemporaryAnswers();
  });
});

// BAGIAN LOGIKA EVALUASI
document.addEventListener("DOMContentLoaded", function () {
  const KKM = 70;
  let flagged = {};

  if (window.location.pathname.includes("/evaluasi/pengerjaan")) {
    window.addEventListener("beforeunload", handleBeforeUnload);

    // SOAL EVALUASI (BAB 2–4)
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
        question: "Gunakan kunci 3 untuk mengenkripsi kata “DATA”.",
        options: ["GDXD", "EDWD", "FDXD", "GDWD"],
        correct: 3,
        type: "mcq",
      },
      {
        question: "Dekripsilah ciphertext “WKH” dengan kunci 3.",
        options: ["THE", "QEB", "ZKH", "TXE"],
        correct: 0,
        type: "mcq",
      },
      {
        question:
          "Seseorang mengenkripsi pesan “SEHAT” dengan kunci 5, tetapi penerima melakukan dekripsi dengan kunci 4. Apa akibatnya?",
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
        question:
          "Mengapa Caesar Cipher dianggap lemah dari sisi keamanan modern?",
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
          "Seorang siswa menulis ciphertext “YMNX NX F YJXY” hasil dari plaintext “THIS IS A TEST”. Kunci yang digunakan adalah …",
        options: ["2", "3", "4", "5"],
        correct: 3,
        type: "mcq",
      },
      {
        question:
          "Ciphertext “JCU” jika didekripsi dengan kunci 2 menjadi “HAS”. Jika ingin mengirim kembali pesan yang sama, tetapi hasil ciphertext-nya berbeda, maka tindakan yang paling logis adalah …",
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
        question:
          "Proses mengubah ciphertext menjadi bentuk asli disebut ____________.",
        answer: "Dekripsi",
        type: "fill",
      },
      {
        question:
          "Enkripsilah “KOMPUTER” dengan kunci 2 → hasil ciphertext: ____________.",
        answer: "MQORWVGT",
        type: "fill",
      },
      {
        question:
          "Dekripsilah ciphertext “ZRUOG” dengan kunci 3 → plaintext: ____________.",
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
    let answers = JSON.parse(
      localStorage.getItem(`${quizKey}_answers`) || "{}"
    );
    let timer;

    const soalContainer = document.getElementById("quiz-question");
    const optionContainer = document.getElementById("quiz-options");
    const quizTitle = document.getElementById("quiz-title");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    const submitBtn = document.getElementById("submitQuiz");
    const bubbleContainer = document.getElementById("bubbleContainer");

    // Ambil elemen Modal dan tombol konfirmasi keluar
    const exitModalElement = document.getElementById("exitConfirmModal");
    const confirmExitBtn = document.getElementById("confirmExitBtn");
    const exitConfirmModal = exitModalElement
      ? new bootstrap.Modal(exitModalElement)
      : null;

    // 2. MENGGANTI BEHAVIOR LINK INTERNAL PADA HALAMAN KUIS
    // Ini memastikan link navigasi internal (seperti logo/home) memunculkan modal custom.
    document.querySelectorAll("a").forEach((link) => {
      // Abaikan link yang menuju halaman nilai, tombol navigasi soal, atau tautan submit/modal lain
      if (link.href.includes("nilai/?jenis=")) {
        return;
      }

      // Ganti behavior link agar memunculkan modal
      link.addEventListener("click", function (e) {
        // Cek apakah link ini menuju halaman lain
        if (link.href !== window.location.href + "#") {
          e.preventDefault();

          // Set tujuan link pada tombol konfirmasi keluar
          if (confirmExitBtn) {
            confirmExitBtn.onclick = function () {
              // Hapus event beforeunload agar bisa keluar tanpa peringatan
              window.removeEventListener("beforeunload", handleBeforeUnload);
              clearTemporaryAnswers();
              window.location.href = link.href;
            };
          }

          // Tampilkan modal
          if (exitConfirmModal) {
            exitConfirmModal.show();
          }
        }
      });
    });

    // BUAT BUBBLE
    bubbleContainer.innerHTML = "";
    for (let i = 1; i <= totalQuestions; i++) {
      const b = document.createElement("div");
      b.classList.add("bubble");
      b.textContent = i;
      bubbleContainer.appendChild(b);
    }

    const bubbles = document.querySelectorAll(".bubble");

    function updateBubbles(num) {
      bubbles.forEach((bubble, index) => {
        const n = index + 1;
        bubble.classList.remove("current", "answered", "flagged"); // hapus semua kelas dulu

        if (n === num) bubble.classList.add("current");
        if (answers[n] !== undefined && answers[n] !== "")
          bubble.classList.add("answered");

        // tandai ragu-ragu sesuai data flagged per soal
        if (flagged[n]) bubble.classList.add("flagged");
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

      if (!window.flagged) window.flagged = {}; // inisialisasi object flagged

      if (q.type === "mcq") {
        soalContainer.innerHTML = `<p class="fw-bold mb-2">${q.question}</p>`;
        optionContainer.innerHTML = q.options
          .map(
            (opt, i) => `
      <div><label>
        <input type="radio" name="q${num}" value="${i}" ${
              answers[num] == i ? "checked" : ""
            }> ${opt}
      </label></div>`
          )
          .join("");

        // tambahkan tombol ragu-ragu di bawah opsi
        const flagBtn = document.createElement("button");
        flagBtn.id = "flagBtn";
        flagBtn.className = "btn btn-outline-warning mt-3";
        flagBtn.textContent = flagged[num]
          ? "Batalkan Ragu-ragu"
          : "Tandai Ragu-ragu";
        optionContainer.appendChild(flagBtn);

        // event toggle flagged
        flagBtn.addEventListener("click", () => {
          flagged[num] = !flagged[num];
          flagBtn.textContent = flagged[num]
            ? "Batalkan Ragu-ragu"
            : "Tandai Ragu-ragu";
          updateBubbles(num);
        });

        optionContainer.querySelectorAll("input").forEach((input) => {
          input.addEventListener("change", (e) => {
            answers[num] = parseInt(e.target.value);
            localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
            updateBubbles(num);
          });
        });
      } else {
        soalContainer.innerHTML = `
      <p class="fw-bold mb-2">${q.question}</p>
      <input type="text" id="fillInput" class="form-control" placeholder="Ketik jawaban..." value="${
        answers[num] || ""
      }">
    `;
        optionContainer.innerHTML = "";

        // tombol ragu-ragu untuk isian singkat juga bisa ditambahkan sama
        const flagBtn = document.createElement("button");
        flagBtn.id = "flagBtn";
        flagBtn.className = "btn btn-outline-warning mt-3";
        flagBtn.textContent = flagged[num]
          ? "Batalkan Ragu-ragu"
          : "Tandai Ragu-ragu";
        soalContainer.appendChild(flagBtn);

        flagBtn.addEventListener("click", () => {
          flagged[num] = !flagged[num];
          flagBtn.textContent = flagged[num]
            ? "Batalkan Ragu-ragu"
            : "Tandai Ragu-ragu";
          updateBubbles(num);
        });

        document.getElementById("fillInput").addEventListener("input", (e) => {
          answers[num] = e.target.value.trim();
          localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
          updateBubbles(num);
        });
      }

      updateBubbles(num);
    }

    // TIMER (60 menit)
    let totalSeconds = 60 * 60;
    const timerDisplay = document.getElementById("timer");

    function updateTimer() {
      let m = Math.floor(totalSeconds / 60);
      let s = totalSeconds % 60;
      timerDisplay.textContent = `${m}:${s < 10 ? "0" + s : s}`;
    }

    timer = setInterval(() => {
      if (totalSeconds > 0) {
        totalSeconds--;
        updateTimer();
      } else {
        alert("Waktu habis! Evaluasi akan disubmit.");
        submitEvaluation();
      }
    }, 1000);

    // NAVIGASI
    prevBtn.addEventListener("click", () => {
      if (currentQuestion > 1) {
        currentQuestion--;
        renderQuestion(currentQuestion);
      }
    });

    nextBtn.addEventListener("click", () => {
      if (currentQuestion < totalQuestions) {
        currentQuestion++;
        renderQuestion(currentQuestion);
      }
    });

    function submitEvaluation() {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      clearInterval(timer);

      // 1. BUAT FORM POST
      const form = document.createElement("form");
      form.method = "POST";
      // Targetkan view Django simpan_evaluasi_nilai
      form.action = "/evaluasi/simpan/";

      // Ambil token CSRF dari DOM (dari evaluasi_pengerjaan.html)
      const csrfInput = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      );
      if (csrfInput) {
        form.appendChild(csrfInput.cloneNode(true));
      } else {
        console.error("CSRF token tidak ditemukan!");
        return;
      }

      // Helper untuk menambah input
      function addInput(name, value) {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
      }

      // Tambahkan Waktu Pengerjaan
      let waktuPengerjaan = 60 * 60 - totalSeconds;
      addInput("waktu_pengerjaan", waktuPengerjaan);

      // 2. Tambahkan Rincian Jawaban
      questions.forEach((q, idx) => {
        const userAnsIndex = answers[idx + 1];
        let userAnswerText;

        if (q.type === "mcq") {
          // Ambil teks opsi yang dipilih
          userAnswerText =
            userAnsIndex !== undefined ? q.options[userAnsIndex] : "(kosong)";
        } else {
          // Ambil teks isian langsung
          userAnswerText = userAnsIndex || "(kosong)";
        }

        // Format pengiriman: jawaban_IDPERTANYAAN = JAWABAN_SISWA
        addInput(`jawaban_${idx + 1}`, userAnswerText);
      });

      // Bersihkan local storage sebelum submit (Opsional)
      localStorage.removeItem(`${quizKey}_answers`);
      localStorage.removeItem(`${quizKey}_flagged`);

      // 3. Submit Form (Server akan menangani redirect)
      document.body.appendChild(form);
      form.submit();
    }

    submitBtn.addEventListener("click", submitEvaluation);

    renderQuestion(currentQuestion);
  }
});
