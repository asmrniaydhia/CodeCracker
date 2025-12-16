const quizKey = "evaluasi";

// Helper untuk membersihkan jawaban sementara di localStorage
function clearTemporaryAnswers() {
  localStorage.removeItem(`${quizKey}_answers`);
  localStorage.removeItem(`${quizKey}_flagged`);
}

function handleBeforeUnload(e) {
  // ... (kode handleBeforeUnload) ...
  const confirmationMessage =
    "Jawaban Anda akan hilang jika Anda meninggalkan halaman ini sekarang.";
  (e || window.event).returnValue = confirmationMessage;
  return confirmationMessage;
}

// ===============================================
// LOGIKA UTAMA: HALAMAN PETUNJUK (kuis.html)
// ===============================================

const startBtnOriginal = document.getElementById("startBtn");

if (startBtnOriginal) {
    // 1. Ganti tombol asli dengan klon (menghapus semua listener yang menempel)
    const startBtnClone = startBtnOriginal.cloneNode(true);
    startBtnOriginal.replaceWith(startBtnClone);
    
    // 2. Tambahkan event listener baru hanya pada klon yang bersih
    startBtnClone.addEventListener("click", (e) => {
        
        e.preventDefault(); 
        
        const agree = document.getElementById("agreeCheck");
        
        // 3. Cek validasi persetujuan
        if (typeof Swal !== 'undefined' && !agree.checked) {
            Swal.fire({
                icon: 'warning',
                title: 'Persetujuan Diperlukan',
                text: "Centang dulu 'Saya telah membaca dan siap mengerjakan evaluasi'."
            });
            return; 
        }

        // 4. Jika validasi berhasil, tampilkan modal
        const modal = new bootstrap.Modal(document.getElementById("confirmModal"));
        modal.show();

        // 5. LOGIKA UNTUK TOMBOL DI DALAM MODAL ("Ya, Kerjakan!")
        const startLink = document.querySelector("#confirmModal a.btn-success"); 
        
        // Hapus listener lama jika ada (dengan mengganti elemen) dan tambahkan yang baru
        startLink.replaceWith(startLink.cloneNode(true));
        const newStartLink = document.querySelector("#confirmModal a.btn-success"); 
        
        newStartLink.addEventListener("click", function startEvaluationHandler() {
            // Hapus event beforeunload global
            window.removeEventListener("beforeunload", handleBeforeUnload);
            clearTemporaryAnswers();
            // Navigasi akan dilanjutkan oleh href link <a>
            newStartLink.removeEventListener('click', startEvaluationHandler);
        });
    });
}

// START EVALUASI — KONFIRMASI MULA (Blok yang Perlu Direvisi)

// BAGIAN LOGIKA EVALUASI
document.addEventListener("DOMContentLoaded", function () {
  const KKM = 70;
  let flagged = {};

  if (window.location.pathname.includes("/evaluasi/pengerjaan")) {
    
    // ❗ FIX 1: AKTIFKAN MODE FOKUS
    document.body.classList.add('mode-fokus'); 
    
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

    // ❗ FIX 2: Hapus Option Container, hanya gunakan Soal Container
    const soalContainer = document.getElementById("quiz-question");
    // const optionContainer = document.getElementById("quiz-options"); // Dihapus dari HTML & JS
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

    // 2. MENGGANTI BEHAVIOR LINK INTERNAL PADA HALAMAN KUIS (LOGIKA KELUAR)
    document.querySelectorAll("a").forEach((link) => {
      if (link.href.includes("nilai/?jenis=")) {
        return;
      }

      link.addEventListener("click", function (e) {
        if (link.href !== window.location.href + "#") {
          e.preventDefault();

          if (confirmExitBtn) {
            // Aksi tombol keluar di modal
            confirmExitBtn.onclick = function () {
              window.removeEventListener("beforeunload", handleBeforeUnload);
              clearTemporaryAnswers();
              window.location.href = link.href;
            };
          }

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
        bubble.classList.remove("current", "answered", "flagged"); 

        if (n === num) bubble.classList.add("current");
        if (answers[n] !== undefined && answers[n] !== "")
          bubble.classList.add("answered");

        if (flagged[n]) bubble.classList.add("flagged");
      });
    }

    bubbles.forEach((bubble, index) => {
      bubble.addEventListener("click", () => {
        currentQuestion = index + 1;
        renderQuestion(currentQuestion);
      });
    });

    // ❗ FIX 3: REVISI FUNGSI RENDER QUESTION 
    function renderQuestion(num) {
      const q = questions[num - 1];
      quizTitle.textContent = "Soal " + num;

      if (!window.flagged) window.flagged = {}; 

      let htmlContent = "";

      if (q.type === "mcq") {
        
        // Render Soal MCQs
        htmlContent = `
            <p class="fw-bold mb-4 text-dark" style="font-size: 1.15rem; line-height: 1.6;">${q.question}</p>
            
            <div class="option-list">
                ${q.options.map((opt, i) => `
                    <label class="option ${answers[num] == i ? 'checked' : ''}">
                        <input type="radio" name="q${num}" value="${i}" ${answers[num] == i ? "checked" : ""}> 
                        <span class="option-text">${opt}</span>
                        ${answers[num] == i ? '<i class="fas fa-check-circle ms-auto text-primary"></i>' : ''}
                    </label>
                `).join("")}
            </div>
        `;
        
      } else {
        
        // Render Soal Isian Singkat
        htmlContent = `
            <p class="fw-bold mb-4 text-dark" style="font-size: 1.15rem; line-height: 1.6;">${q.question}</p>
            <input type="text" id="fillInput" class="form-control" placeholder="Ketik jawaban..." value="${
              answers[num] || ""
            }">
        `;
        
      }
      
      // Tambahkan Tombol Ragu-ragu (untuk kedua tipe soal)
      htmlContent += `
        <button id="flagBtn" class="btn btn-sm ${flagged[num] ? 'btn-warning text-dark' : 'btn-outline-warning'} mt-4">
            <i class="fas fa-flag me-2"></i>${flagged[num] ? "Ditandai Ragu" : "Tandai Ragu-ragu"}
        </button>
      `;

      // Inject Konten ke Kontainer Tunggal
      soalContainer.innerHTML = htmlContent;


      // Re-initialize Event Listeners
      if (q.type === "mcq") {
        soalContainer.querySelectorAll("input").forEach((input) => {
          input.addEventListener("change", (e) => {
            answers[num] = parseInt(e.target.value);
            localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
            renderQuestion(num); // Re-render untuk update style checked
            updateBubbles(num);
          });
        });
      } else {
        document.getElementById("fillInput").addEventListener("input", (e) => {
          answers[num] = e.target.value.trim();
          localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
          updateBubbles(num);
        });
      }

      // Event Listener Ragu-ragu
      document.getElementById("flagBtn").addEventListener("click", () => {
          flagged[num] = !flagged[num];
          localStorage.setItem(`${quizKey}_flagged`, JSON.stringify(flagged));
          renderQuestion(num); 
          updateBubbles(num);
      });

      updateBubbles(num);
      
      // ❗ FIX 4: LOGIKA VISIBILITAS TOMBOL NAVIGASI
      if (num === 1) {
          prevBtn.style.visibility = "hidden"; 
      } else {
          prevBtn.style.visibility = "visible";
      }
      
      if (num === totalQuestions) {
          nextBtn.style.display = "none";
          submitBtn.style.display = "inline-block";
      } else {
          nextBtn.style.display = "inline-block";
          submitBtn.style.display = "none";
      }
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
      form.action = "/evaluasi/simpan/";

      // Ambil token CSRF
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
          userAnswerText =
            userAnsIndex !== undefined ? q.options[userAnsIndex] : "(kosong)";
        } else {
          userAnswerText = userAnsIndex || "(kosong)";
        }

        addInput(`jawaban_${idx + 1}`, userAnswerText);
      });

      // Bersihkan local storage sebelum submit
      localStorage.removeItem(`${quizKey}_answers`);
      localStorage.removeItem(`${quizKey}_flagged`);

      // 3. Submit Form
      document.body.appendChild(form);
      
      // Tampilkan loading sebelum submit
      if (typeof Swal !== 'undefined') {
          Swal.fire({
              title: 'Menyimpan...',
              text: 'Mohon tunggu sebentar',
              allowOutsideClick: false,
              didOpen: () => { Swal.showLoading(); }
          });
      }
      
      form.submit();
    }

    submitBtn.addEventListener("click", submitEvaluation);

    renderQuestion(currentQuestion);
  }
});