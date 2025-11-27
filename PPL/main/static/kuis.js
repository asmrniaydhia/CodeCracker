console.log("KUAS KUY! VERSI SOAL BARU 2025.");
// Ambil parameter 'jenis'
const urlParams = new URLSearchParams(window.location.search);
const jenis = urlParams.get("jenis");

// Gunakan quizKey sesuai jenis, contoh: "enkripsi"
const quizKey = jenis;

// Tombol Mulai Kuis pada halaman petunjuk
document.getElementById("startBtn")?.addEventListener("click", (e) => {
  e.preventDefault();

  const agree = document.getElementById("agreeCheck");
  if (!agree.checked) {
    alert("Centang dulu 'Saya siap dan memahami petunjuk'.");
    return;
  }

  const confirmModal = new bootstrap.Modal(
    document.getElementById("confirmModal")
  );
  confirmModal.show();

  const startLink = document.querySelector("#confirmModal a.btn-success");
  startLink.href = `/kuis/pengerjaan/?jenis=${jenis}`;
});

// ===============================
// LOGIKA KUIS
// ===============================
document.addEventListener("DOMContentLoaded", function () {
  const KKM = 70;
  let questions = [];

  // ===============================
  // HALAMAN PENGERJAAN
  // ===============================
  // Kumpulan soal berdasarkan jenis
  if (jenis === "enkripsi") {
    questions = [
      {
        question:
          "Sebuah aplikasi sekolah mengirimkan pesan nilai rapor melalui server pusat. Agar data tidak mudah dibaca jika terjadi kebocoran jaringan, aplikasi tersebut menambahkan proses khusus sebelum pengiriman. Langkah apakah yang paling tepat dilakukan?",
        options: [
          "Mengubah format file menjadi PDF",
          "Mengganti nama file sebelum dikirim",
          "Melakukan enkripsi pada data rapor",
          "Menghapus sebagian data penting",
        ],
        correct: 2, // Jawaban: C. Melakukan enkripsi pada data rapor
      },
      {
        question:
          "Rina membuat aplikasi pengaduan anonim. Ia ingin memastikan setiap laporan aman walaupun database dicuri orang. Apa alasan utama ia perlu menerapkan enkripsi?",
        options: [
          "Agar laporan lebih cepat diproses",
          "Agar laporan tetap bisa dibaca hanya oleh pihak berwenang",
          "Agar database tidak bisa dihapus",
          "Agar server tidak cepat penuh",
        ],
        correct: 1, // Jawaban: B. Agar laporan tetap bisa dibaca hanya oleh pihak berwenang
      },
      {
        question:
          "Sebuah pesan terenkripsi dapat dikirim dengan aman melalui jaringan sekolah yang sering mengalami gangguan keamanan. Mengapa enkripsi tetap penting meskipun jaringan sudah dilindungi firewall?",
        options: [
          "Firewall tidak menjamin data selalu aman",
          "Enkripsi membuat pesan jadi lebih pendek",
          "Firewall tidak boleh digunakan bersamaan dengan enkripsi",
          "Firewall menghapus pesan asli",
        ],
        correct: 0, // Jawaban: A. Firewall tidak menjamin data selalu aman
      },
      {
        question:
          "Guru ingin berbagi file kunci ujian. Ia melakukan enkripsi, tetapi tidak mengirimkan kunci dekripsinya kepada siswa. Apa akibatnya?",
        options: [
          "File akan terbaca otomatis",
          "File tetap aman dan tidak dapat dibaca",
          "Siswa dapat menebak isinya dengan mudah",
          "File berubah ukuran menjadi lebih besar",
        ],
        correct: 1, // Jawaban: B. File tetap aman dan tidak dapat dibaca
      },
      {
        question:
          "Anto membuat sistem presensi otomatis. Ia menyadari data siswa dapat dilihat oleh admin jaringan. Untuk mencegah penyalahgunaan data, langkah apa yang harus ia tambahkan?",
        options: [
          "Mengganti warna tampilan aplikasi",
          "Menyimpan data di folder berbeda",
          "Menyembunyikan aplikasi dari layar utama",
          "Menyandikan data saat disimpan (enkripsi)",
        ],
        correct: 3, // Jawaban: D. Menyandikan data saat disimpan (enkripsi)
      },
    ];
  }

  // ----------------------------------------------------------------------

  if (jenis === "caesar") {
    questions = [
      {
        question:
          "Sebuah pesan: “DRO AESMU LBYGX” ditemukan di kelas komputer. Siswa menduga ini adalah Caesar Cipher dengan geser +10. Apa isi pesannya?",
        options: [
          "THE QUICK BROWN",
          "THE QUICK ROBOT",
          "THE CLOUD BROWN",
          "THE BROWN HOUSE",
        ],
        correct: 0, // Jawaban: A. THE QUICK BROWN (D-10 = T, R-10=H, O-10=E, dst.)
      },
      {
        question:
          "Guru memberikan pesan terenkripsi “KHOOR ZRUOG” kepada siswa, namun lupa memberi petunjuk geseran. Siswa mencoba menebak pola pergeseran. Manakah teknik paling efektif?",
        options: [
          "Menebak acak hingga muncul kata “WOW”",
          "Menggeser huruf satu per satu sampai pesan terbaca",
          "Mengganti huruf vokal saja",
          "Menghapus spasi lalu mencoba gabungan kata baru",
        ],
        correct: 1, // Jawaban: B. Menggeser huruf satu per satu sampai pesan terbaca (Brute-force)
      },
      {
        question:
          "Aplikasi belajar membuat fitur tantangan Caesar Cipher. Pesan “ZL AOLYPUF” muncul saat kunci geser tidak diketahui. Siswa menyadari kata terakhir kemungkinan “HAPPY”. Maka geseran yang benar adalah…",
        options: ["+5", "+7", "–7", "–5"],
        correct: 2, // Jawaban: C. –7 (Huruf Z harus menjadi H, geser 7 langkah mundur)
      },
      {
        question:
          "Aldi membuat program Caesar Cipher. Namun saat pesan terdiri dari angka, program malah mengubah angka menjadi huruf. Apa perbaikan yang paling tepat?",
        options: [
          "Mematikan fitur enkripsi",
          "Menambahkan aturan untuk membiarkan angka tetap sama",
          "Mengubah semua angka menjadi simbol",
          "Menghapus angka dari pesan",
        ],
        correct: 1, // Jawaban: B. Menambahkan aturan untuk membiarkan angka tetap sama
      },
      {
        question:
          "Pesan “WKLV LV D VHFUHW” dikirimkan namun tampak mencurigakan. Siswa melihat pola huruf tidak biasa. Apa langkah paling tepat untuk memeriksa apakah itu Caesar Cipher?",
        options: [
          "Mengirim pesan kembali ke pengirim",
          "Menguji beberapa pergeseran untuk melihat apakah menghasilkan kata yang bermakna",
          "Mengganti semua huruf dengan vokal",
          "Menghapus huruf pertama dan terakhir",
        ],
        correct: 1, // Jawaban: B. Menguji beberapa pergeseran untuk melihat apakah menghasilkan kata yang bermakna
      },
    ];
  }

  // ----------------------------------------------------------------------

  if (jenis === "dekripsi") {
    questions = [
      {
        question:
          "Pesan rahasia siswa berbunyi “RIJVS UYVJN”. Setelah dianalisis, ternyata ini hasil enkripsi tertentu. Apa tujuan proses dekripsi?",
        options: [
          "Mengubah pesan menjadi lebih sulit dibaca",
          "Mengembalikan pesan ke bentuk aslinya",
          "Menghasilkan pesan baru untuk dikirim",
          "Menghapus pesan dari sistem",
        ],
        correct: 1, // Jawaban: B. Mengembalikan pesan ke bentuk aslinya
      },
      {
        question:
          "Guru menerima file nilai yang terenkripsi, tetapi kunci dekripsinya hilang. Apa risiko yang terjadi?",
        options: [
          "File dapat dibuka siapa saja",
          "File tidak bisa dibaca meskipun datanya benar",
          "File berubah ukuran dan rusak",
          "File otomatis terhapus",
        ],
        correct: 1, // Jawaban: B. File tidak bisa dibaca meskipun datanya benar
      },
      {
        question:
          "Dalam simulasi keamanan, siswa mencoba membuka pesan yang disandikan. Namun ketika dekripsi dilakukan dengan kunci salah, hasilnya tidak masuk akal. Apa yang bisa disimpulkan?",
        options: [
          "Sistem enkripsi tidak berfungsi",
          "Dekripsi hanya bisa dilakukan dengan kunci yang tepat",
          "Pesan tidak perlu didekripsi",
          "Semua kunci menghasilkan pesan yang sama",
        ],
        correct: 1, // Jawaban: B. Dekripsi hanya bisa dilakukan dengan kunci yang tepat
      },
      {
        question:
          "Sebuah aplikasi melakukan enkripsi saat mengirim data, tetapi tidak melakukan dekripsi saat menerima. Apa dampaknya?",
        options: [
          "Data yang diterima tetap terenkripsi dan tidak terbaca",
          "Data menjadi lebih cepat terkirim",
          "Data otomatis berubah menjadi teks asli",
          "Data tersimpan dua kali lebih besar",
        ],
        correct: 0, // Jawaban: A. Data yang diterima tetap terenkripsi dan tidak terbaca
      },
      {
        question:
          "Rani mencoba mendekripsi pesan yang digeser 8 langkah ke kanan. Ia ingin mengembalikannya ke teks asli. Apa yang harus ia lakukan?",
        options: [
          "Menggeser huruf maju 8 langkah",
          "Menggeser huruf mundur 8 langkah",
          "Menggeser huruf maju 16 langkah",
          "Menghapus huruf vokal lalu membaca ulang",
        ],
        correct: 1, // Jawaban: B. Menggeser huruf mundur 8 langkah
      },
    ];
  }

  // SHUFFLE
  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }

  //   if (!localStorage.getItem(`${quizKey}_order`)) {
  //     shuffle(questions);
  //     localStorage.setItem(`${quizKey}_order`, JSON.stringify(questions));
  //   } else {
  //     questions = JSON.parse(localStorage.getItem(`${quizKey}_order`));
  //   }
  if (window.location.pathname.includes("/kuis/pengerjaan")) {
    let currentQuestion = 1;
    const totalQuestions = questions.length;

    let answers = JSON.parse(
      localStorage.getItem(`${quizKey}_answers`) || "{}"
    );
    let flagged = JSON.parse(
      localStorage.getItem(`${quizKey}_flagged`) || "{}"
    );

    const soalContainer = document.querySelector("div.teks");
    const quizTitle = document.querySelector(".quiz-title");
    const nextBtn = document.querySelector(".btn-success");
    const prevBtn = document.querySelector(".btn-danger");
    const submitBtn = document.getElementById("submitQuiz");
    const bubbleContainer = document.querySelector(".bubbles");

    // Generate bubbles
    bubbleContainer.innerHTML = "";
    for (let i = 1; i <= totalQuestions; i++) {
      const bubble = document.createElement("div");
      bubble.classList.add("bubble");
      bubble.textContent = i;
      bubble.addEventListener("click", () => {
        currentQuestion = i;
        renderQuestion(i);
      });
      bubbleContainer.appendChild(bubble);
    }

    const bubbles = document.querySelectorAll(".bubble");

    function updateBubbles(active) {
      bubbles.forEach((b, index) => {
        const num = index + 1;
        b.classList.remove("current", "answered", "flagged");
        if (num === active) b.classList.add("current");
        if (answers[num] !== undefined) b.classList.add("answered");
        if (flagged[num]) b.classList.add("flagged");
      });
    }

    function renderQuestion(num) {
      const q = questions[num - 1];
      quizTitle.textContent = "Soal " + num;

      soalContainer.innerHTML = `
            <p class="fw-bold mb-2">${q.question}</p>
            ${q.options
              .map(
                (opt, idx) => `
                <div><label>
                <input type="radio" name="q${num}" value="${idx}" ${
                  answers[num] == idx ? "checked" : ""
                }> 
                ${opt}
                </label></div>
            `
              )
              .join("")}
            <button id="flagBtn" class="btn btn-outline-warning mt-3">
                ${flagged[num] ? "Batalkan Ragu-ragu" : "Tandai Ragu-ragu"}
            </button>
        `;

      soalContainer.querySelectorAll(`input[name="q${num}"]`).forEach((i) => {
        i.addEventListener("change", (e) => {
          answers[num] = parseInt(e.target.value);
          localStorage.setItem(`${quizKey}_answers`, JSON.stringify(answers));
          updateBubbles(num);
        });
      });

      const flagBtn = document.getElementById("flagBtn");
      flagBtn.addEventListener("click", () => {
        flagged[num] = !flagged[num];
        localStorage.setItem(`${quizKey}_flagged`, JSON.stringify(flagged));
        flagBtn.textContent = flagged[num]
          ? "Batalkan Ragu-ragu"
          : "Tandai Ragu-ragu";
        updateBubbles(num);
      });

      updateBubbles(num);
    }

    // Timer
    let totalSeconds = 20 * 60;
    const timerDisplay = document.querySelector(".side-card h5.text-danger");

    function updateTimer() {
      let m = Math.floor(totalSeconds / 60);
      let s = (totalSeconds % 60).toString().padStart(2, "0");
      timerDisplay.textContent = `Waktu Tersisa: ${m}:${s}`;
    }

    updateTimer();
    const timer = setInterval(() => {
      totalSeconds--;
      updateTimer();
      if (totalSeconds <= 0) {
        clearInterval(timer);
        finishQuiz();
      }
    }, 1000);

    // Navigasi
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

    // Submit
    submitBtn.addEventListener("click", finishQuiz);

    function finishQuiz() {
      clearInterval(timer); // Hentikan timer saat kuis selesai

      let score = 0;
      let detailAnswers = [];
      let totalQuestions = questions.length;
      let waktuPengerjaan = 20 * 60 - totalSeconds; // Hitung waktu pengerjaan

      // 1. VALIDASI & HITUNG SKOR (Logika tetap di frontend)
      questions.forEach((q, idx) => {
        const userAns = answers[idx + 1];
        const isCorrect = userAns === q.correct;
        // Asumsi: Setiap jawaban benar bernilai 10 (sesuai views.py)
        if (isCorrect) score += 20;

        detailAnswers.push({
          // Data yang akan dikirim ke server: ID pertanyaan (key di JSON) dan jawaban siswa
          question_id: idx + 1,
          user_answer: userAns !== undefined ? q.options[userAns] : "(kosong)",
        });
      });

      // 2. KIRIM DATA KE DJANGO VIA FORM POST
      const form = document.createElement("form");
      form.method = "POST";
      // Arahkan ke view baru yang menyimpan skor
      form.action = "/kuis/simpan/";

      // Tambahkan token CSRF (PENTING untuk Django)
      const csrfToken = document.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;
      const csrfInput = document.createElement("input");
      csrfInput.type = "hidden";
      csrfInput.name = "csrfmiddlewaretoken";
      csrfInput.value = csrfToken;
      form.appendChild(csrfInput);

      // Tambahkan data penting ke form
      function addInput(name, value) {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
      }

      // Tambahkan data ringkasan
      addInput("jenis", jenis);
      addInput("kuis_id", 1); // Ganti dengan ID Kuis yang sebenarnya jika Anda punya ID di template
      addInput("skor_total", score);
      addInput("waktu_pengerjaan", waktuPengerjaan);

      // Tambahkan rincian jawaban
      questions.forEach((q, idx) => {
        const userAnsIndex = answers[idx + 1];
        const userAnswerText =
          userAnsIndex !== undefined ? q.options[userAnsIndex] : "(kosong)";

        // Format pengiriman: jawaban_IDPERTANYAAN = JAWABAN_SISWA
        addInput(`jawaban_${idx + 1}`, userAnswerText);
        // Anda juga perlu mengirim jawaban benar dari JSON, atau biarkan view.py yang hitung
      });

      // Bersihkan local storage sebelum submit
      localStorage.removeItem(`${quizKey}_answers`);
      localStorage.removeItem(`${quizKey}_order`);
      localStorage.removeItem(`${quizKey}_flagged`);

      // Submit Form
      document.body.appendChild(form);
      form.submit();
    }

    renderQuestion(currentQuestion);
  }
});
