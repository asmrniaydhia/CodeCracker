// Ambil parameter 'jenis'
const urlParams = new URLSearchParams(window.location.search);
const jenis = urlParams.get("jenis");

// Gunakan quizKey sesuai jenis, contoh: "enkripsi"
const quizKey = jenis;

// Tombol Mulai Kuis pada halaman petunjuk
document.getElementById('startBtn')?.addEventListener('click', (e) => {
    e.preventDefault();

    const agree = document.getElementById('agreeCheck');
    if (!agree.checked) {
        alert("Centang dulu 'Saya siap dan memahami petunjuk'.");
        return;
    }

    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    confirmModal.show();

    const startLink = document.querySelector('#confirmModal a.btn-success');
    startLink.href = `/kuis/pengerjaan/?jenis=${jenis}`;
});


// ===============================
// LOGIKA KUIS
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const KKM = 70;

    // ===============================
    // HALAMAN NILAI
    // ===============================
    if (window.location.pathname.includes("/kuis/nilai")) {

        const nilai = urlParams.get("nilai");
        const score = parseInt(nilai || "0");
        const detail = JSON.parse(localStorage.getItem(`${quizKey}_detail`) || "{}");

        const benar = detail.correct || 0;
        const total = detail.total || 0;

        document.getElementById("scoreNum").textContent = score;
        document.getElementById("correctCount").textContent = benar;
        document.getElementById("totalCount").textContent = total;

        const ring = document.getElementById("scoreRing");
        ring.style.setProperty("--p", score);

        const passFail = document.getElementById("passFail");
        const grade = document.getElementById("grade");

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

        const answerTable = document.getElementById("answerTable");
        answerTable.innerHTML = "";

        if (detail.answers) {
            detail.answers.forEach((item, index) => {
                const row = document.createElement("tr");
                const status = item.isCorrect
                    ? '<span class="text-success fw-bold">Benar</span>'
                    : '<span class="text-danger fw-bold">Salah</span>';

                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${item.question}</td>
                    <td>${item.userAnswerText}</td>
                    <td>${status}</td>
                `;
                answerTable.appendChild(row);
            });
        }
        return;
    }

    // ===============================
    // HALAMAN PENGERJAAN
    // ===============================

    // Kumpulan soal berdasarkan jenis
    let questions = [];

    if (jenis === "enkripsi") {
        questions = [
            {
                question: "Fungsi utama dari kunci (key) dalam enkripsi adalah …",
                options: ["Menentukan banyaknya pergeseran huruf", "Mengatur panjang kata", "Menghapus tanda baca", "Mengubah huruf menjadi angka"],
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
                question: "Pesan “EHOEMDU” dienkripsi dengan kunci 3. Plaintext-nya adalah …",
                options: ["BELAJAR", "CELAJAR", "DELAJAR", "BEMAJAR"],
                correct: 0,
            },
            {
                question: "Berikut ini contoh penerapan enkripsi, kecuali …",
                options: ["Password file", "HTTPS", "Menyimpan soal tanpa password", "Mengunci dokumen"],
                correct: 2,
            }
        ];
    }

    if (jenis === "caesar") {
        questions = [
            {
                question: "Caesar Cipher ditemukan oleh …",
                options: ["Julius Caesar", "Leonardo da Vinci", "Alan Turing", "Archimedes"],
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
                question: "Mengapa Caesar Cipher tidak digunakan modern?",
                options: ["Terlalu mudah dipecahkan", "Hanya bisa di komputer", "Butuh kunci ganda", "Tidak bisa dienkripsi"],
                correct: 0,
            }
        ];
    }

    if (jenis === "dekripsi") {
        questions = [
            {
                question: "Apa arti dari dekripsi?",
                options: ["Mengembalikan ciphertext ke plaintext", "Mengubah plaintext ke ciphertext", "Menambah kunci", "Menghapus sebagian pesan"],
                correct: 0,
            },
            {
                question: "Dekripsi pesan “KHOOR” dengan kunci 3.",
                options: ["HELLO", "WORLD", "HILLO", "HALLO"],
                correct: 0,
            },
            {
                question: "Dekripsi pesan “YJHMSNVZ” kunci 5.",
                options: ["TEACHING", "SCHOOL", "COMPUTER", "STUDENT"],
                correct: 0,
            },
            {
                question: "Enkripsilah “WORLD” kunci 3.",
                options: ["ZRUOG", "ZQUMF", "ZSUOF", "ZTUOG"],
                correct: 0,
            },
            {
                question: "Membuka file yang dipassword disebut …",
                options: ["Dekripsi", "Enkripsi", "Hashing", "Kompresi"],
                correct: 0,
            }
        ];
    }

    // SHUFFLE
    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
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
            ${q.options.map((opt, idx) => `
                <div><label>
                <input type="radio" name="q${num}" value="${idx}" ${answers[num] == idx ? "checked" : ""}> 
                ${opt}
                </label></div>
            `).join("")}
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
            flagBtn.textContent = flagged[num] ? "Batalkan Ragu-ragu" : "Tandai Ragu-ragu";
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
        let benar = 0;
        let detailAnswers = [];

        questions.forEach((q, idx) => {
            const userAns = answers[idx + 1];
            const isCorrect = userAns === q.correct;
            if (isCorrect) benar++;
            detailAnswers.push({
                question: q.question,
                userAnswerText: userAns !== undefined ? q.options[userAns] : "(kosong)",
                isCorrect
            });
        });

        const score = Math.round((benar / totalQuestions) * 100);

        localStorage.setItem(`${quizKey}_detail`, JSON.stringify({
            correct: benar,
            total: totalQuestions,
            answers: detailAnswers
        }));

        localStorage.removeItem(`${quizKey}_answers`);
        localStorage.removeItem(`${quizKey}_order`);

        window.location.href = `/kuis/nilai/?jenis=${jenis}&nilai=${score}`;
    }

    renderQuestion(currentQuestion);
});
