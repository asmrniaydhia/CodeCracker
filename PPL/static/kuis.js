console.log("KUAS KUY! SYSTEM LOADED.");

// Ambil parameter 'jenis' dari URL
const urlParams = new URLSearchParams(window.location.search);
const jenis = urlParams.get("jenis");
const quizKey = jenis;

// --- HALAMAN PETUNJUK (kuis.html) ---
const startBtn = document.getElementById("startBtn");
if (startBtn) {
    startBtn.addEventListener("click", (e) => {
        e.preventDefault();

        const agree = document.getElementById("agreeCheck");
        // Menggunakan SweetAlert jika tersedia, jika tidak pakai alert biasa
        if (!agree.checked) {
            if (typeof Swal !== 'undefined') {
                Swal.fire('Info', "Centang dulu 'Saya telah membaca dan siap mengerjakan kuis'.", 'warning');
            } else {
                alert("Centang dulu persetujuan.");
            }
            return;
        }

        const confirmModalEl = document.getElementById("confirmModal");
        if (confirmModalEl) {
            const confirmModal = new bootstrap.Modal(confirmModalEl);
            confirmModal.show();
            
            // Set href tombol di dalam modal
            const startLink = document.querySelector("#confirmModal a.btn-success"); // Pastikan selector ini cocok di HTML
            if(startLink) startLink.href = `/kuis/pengerjaan/?jenis=${jenis}`;
        }
    });
}


// --- HALAMAN PENGERJAAN (kuis_pengerjaan.html) ---
document.addEventListener("DOMContentLoaded", function () {
    // Cek apakah kita sedang di halaman pengerjaan
    if (!window.location.pathname.includes("/kuis/pengerjaan/")) return;

    document.body.classList.add('mode-fokus');
    
    // DATA SOAL (Disimpan di Client Side sesuai request)
    let questions = [];

    if(jenis==="enkripsi"){
        questions=[
            {question:"Agus mengirimkan foto kartu pelajar berisi data sensitif melalui aplikasi chat dengan fitur End-to-End Encryption. Jika data disadap di tengah jalan, penyadap hanya akan melihat kode acak tidak bermakna yang disebut ....",options:["Plain Text","Password","Ciphertext","Glosarium"],correct:2},
            {question:"Saat membuka sebuah file dokumen di komputer sekolah, kamu hanya menemukan deretan karakter aneh seperti \"Xy29!#amZ\" yang tidak dapat dipahami. File tersebut sedang berada dalam wujud ....",options:["Pesan asli","Data orisinal","Ciphertext","Plain Text"],correct:2},
            {question:"Sebuah bank mengganti sebagian nomor rekening pada struk ATM menjadi tanda bintang (contoh: 123XXXX890). Tindakan ini merupakan penerapan prinsip ....",options:["Transparansi data","Kerahasiaan (confidentiality)","Kecepatan transaksi","Penghapusan data"],correct:1},
            {question:"Saat menggunakan Wi-Fi publik untuk aktivitas perbankan, risiko terbesar jika data tidak dienkripsi adalah data dikirimkan dalam bentuk ....",options:["Plain Text","Ciphertext","Kode rahasia","Algoritma"],correct:0},
            {question:"Dalam alur komunikasi digital, proses mengubah pesan asli menjadi kode acak menggunakan algoritma tertentu disebut ....",options:["Deskripsi","Dekripsi","Enkripsi","Glosarium"],correct:2}
        ];
    } else if(jenis==="caesar"){
        questions=[
            {question:"Pesan asli \"DUNIA\" dienkripsi dengan kunci Geser 3 ke Kanan. Hasil perubahannya adalah ....",options:["GVQLD","FWPKC","GXQLD","HWQLE"],correct:2},
            {question:"Kata \"DATA\" dienkripsi menggunakan kunci Geser 2 ke Kanan. Hasil alfabet sandinya adalah ....",options:["FCVD","FCVC","EBVB","GDWD"],correct:1},
            {question:"Jika huruf \"B\" berubah menjadi \"E\", maka pesan \"MUKA\" dengan kunci yang sama akan menjadi ....",options:["PXND","QYOE","OWMC","PVNC"],correct:0},
            {question:"Jika huruf \"K\" digeser 5 langkah ke kanan menjadi \"P\", maka hasil enkripsi kata \"BOLA\" adalah ....",options:["CPMA","DQNB","GTQF","FSPE"],correct:2},
            {question:"Jika huruf \"Z\" dienkripsi dengan Geser 1 ke Kanan, maka huruf hasilnya adalah ....",options:["A","B","Y","X"],correct:0}
        ];
    } else if(jenis==="dekripsi"){
        questions=[
            {question:"Pesan rahasia \"FDVD\" dienkripsi dengan Geser 3 ke Kanan. Untuk mendapatkan pesan asli, hasil dekripsinya adalah ....",options:["BOLA","CASA","DATA","GAGA"],correct:1},
            {question:"Dengan teknik Brute Force, kode \"PHVD\" menghasilkan kata \"MESA\" setelah dilakukan pergeseran sebanyak ....",options:["1 langkah ke kiri","2 langkah ke kiri","3 langkah ke kiri","4 langkah ke kiri"],correct:2},
            {question:"Pesan terenkripsi \"LUL\" diketahui menggunakan kunci Geser 1 ke Kanan. Pesan aslinya adalah ....",options:["MUM","KTK","JSK","LVL"],correct:1},
            {question:"Jika huruf sandi \"V\" berasal dari huruf asli \"T\", maka proses dekripsi dilakukan dengan menggeser ke kiri sebanyak ....",options:["1 langkah","2 langkah","3 langkah","4 langkah"],correct:1},
            {question:"Kode \"WKDQ\" setelah digeser 3 langkah ke kiri menghasilkan kata \"THANK\". Kunci enkripsi awal yang digunakan adalah ....",options:["Geser 1 ke Kanan","Geser 2 ke Kanan","Geser 3 ke Kanan","Geser 4 ke Kanan"],correct:2}
        ];
    }

    if (questions.length === 0) {
        document.querySelector(".question-box").innerHTML = "<div class='text-center p-5'><h3>Soal tidak ditemukan untuk kategori ini.</h3></div>";
        return;
    }

    // --- LOGIKA UTAMA KUIS ---
    function handleBeforeUnload(e) {
        const msg = "Jawaban Anda akan hilang jika keluar sekarang.";
        (e || window.event).returnValue = msg;
        return msg;
    }
    window.addEventListener("beforeunload", handleBeforeUnload);

    // SETUP VARIABEL
    let currentQuestion = 1;
    const totalQuestions = questions.length;
    let answers = {};
    let flagged = {};

    // Restore flagged items from LocalStorage (Opsional)
    if (localStorage.getItem(`${quizKey}_flagged`)) {
        try { flagged = JSON.parse(localStorage.getItem(`${quizKey}_flagged`)); } catch(e){}
    }

    // SELECTOR DOM
    const soalContainer = document.querySelector(".question-box"); // Class di CSS baru
    const quizTitle = document.querySelector(".quiz-title");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    const submitBtn = document.getElementById("submitQuiz");
    const bubbleContainer = document.getElementById("bubbleContainer");
    const timerText = document.getElementById("timer");

    // RENDER BUBBLES
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

    // RENDER SOAL
    function renderQuestion(num) {
        const q = questions[num - 1];
        quizTitle.textContent = "Soal " + num;

        // Render HTML Soal
        soalContainer.innerHTML = `
            <p class="fw-bold mb-4 text-dark" style="font-size: 1.3rem; line-height: 1.6;">${q.question}</p>
            
            <div class="option-list">
                ${q.options.map((opt, idx) => `
                    <label class="option ${answers[num] === idx ? 'checked' : ''}">
                        <input type="radio" name="q${num}" value="${idx}" ${answers[num] === idx ? "checked" : ""}> 
                        <span class="option-text" style="font-size: 1.3rem">${opt}</span>
                        ${answers[num] === idx ? '<i class="fas fa-check-circle ms-auto text-primary"></i>' : ''}
                    </label>
                `).join("")}
            </div>

            <button id="flagBtn" class="btn btn-sm ${flagged[num] ? 'btn-warning text-dark' : 'btn-outline-warning'} mt-4">
                <i class="fas fa-flag me-2"></i>${flagged[num] ? "Ditandai Ragu" : "Tandai Ragu-ragu"}
            </button>
        `;

        // Event Listener Radio Button
        soalContainer.querySelectorAll(`input[name="q${num}"]`).forEach((i) => {
            i.addEventListener("change", (e) => {
                answers[num] = parseInt(e.target.value);
                renderQuestion(num); // Re-render untuk update style
                updateBubbles(num);
            });
        });

        // Event Listener Ragu-ragu
        document.getElementById("flagBtn").addEventListener("click", () => {
            flagged[num] = !flagged[num];
            // Simpan ke localStorage agar tidak hilang saat refresh (opsional)
            localStorage.setItem(`${quizKey}_flagged`, JSON.stringify(flagged));
            renderQuestion(num);
            updateBubbles(num);
        });

        updateBubbles(num);
        
        // Atur tombol Navigasi
        if (num === 1) {
            // Jika Soal 1: Sembunyikan tombol (tetap jaga spasi layout)
            prevBtn.style.visibility = "hidden"; 
        } else {
            // Jika Soal 2 ke atas: Munculkan tombol & pastikan bisa diklik
            prevBtn.style.visibility = "visible";
            prevBtn.disabled = false; 
        }
        
        // 2. Logika Tombol "Selanjutnya" vs "Selesai"
        if (num === totalQuestions) {
            // Jika Soal Terakhir: Sembunyikan "Next", Munculkan "Submit"
            nextBtn.style.display = "none";
            submitBtn.style.display = "inline-block";
        } else {
            // Selain Soal Terakhir: Munculkan "Next", Sembunyikan "Submit"
            nextBtn.style.display = "inline-block";
            submitBtn.style.display = "none";
        }
    }

    // TIMER
    let totalSeconds = 20 * 60; // 20 Menit
    function updateTimer() {
        let m = Math.floor(totalSeconds / 60);
        let s = (totalSeconds % 60).toString().padStart(2, "0");
        if(timerText) timerText.textContent = `${m}:${s}`;
    }
    updateTimer();
    const timerInterval = setInterval(() => {
        totalSeconds--;
        updateTimer();
        if (totalSeconds <= 0) {
            clearInterval(timerInterval);
            finishQuiz(); // Auto submit
        }
    }, 1000);

    // NAVIGASI KLIK
    prevBtn.addEventListener("click", () => {
        if (currentQuestion > 1) { currentQuestion--; renderQuestion(currentQuestion); }
    });
    nextBtn.addEventListener("click", () => {
        if (currentQuestion < totalQuestions) { currentQuestion++; renderQuestion(currentQuestion); }
    });

    // FUNGSI SELESAI
    function finishQuiz() {
        window.removeEventListener("beforeunload", handleBeforeUnload);
        clearInterval(timerInterval);

        let score = 0;
        let waktuPengerjaan = (20 * 60) - totalSeconds;

        // Hitung Skor
        questions.forEach((q, idx) => {
            const userAns = answers[idx + 1];
            if (userAns === q.correct) score += 20; // 5 soal x 20 = 100
        });

        // Buat Form Submit
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/kuis/simpan/";

        // CSRF Token (Penting!)
        const csrfEl = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if(csrfEl) {
            const csrfInput = document.createElement("input");
            csrfInput.type = "hidden";
            csrfInput.name = "csrfmiddlewaretoken";
            csrfInput.value = csrfEl.value;
            form.appendChild(csrfInput);
        }

        // Helper Input
        const addInput = (name, val) => {
            const inp = document.createElement("input");
            inp.type = "hidden";
            inp.name = name;
            inp.value = val;
            form.appendChild(inp);
        };

        addInput("jenis", jenis);
        addInput("waktu_pengerjaan", waktuPengerjaan);
        
        // Kirim detail jawaban
        questions.forEach((q, idx) => {
            const ansIdx = answers[idx + 1];
            const ansText = ansIdx !== undefined ? q.options[ansIdx] : "(kosong)";
            addInput(`jawaban_${idx + 1}`, ansText);
        });

        document.body.appendChild(form);
        
        // Tampilkan loading sebelum submit
        Swal.fire({
            title: 'Menyimpan...',
            text: 'Mohon tunggu sebentar',
            allowOutsideClick: false,
            didOpen: () => { Swal.showLoading(); }
        });
        
        form.submit();
    }

    submitBtn.addEventListener("click", (e) => {
        // Konfirmasi Selesai
        Swal.fire({
            title: 'Yakin selesai?',
            text: "Pastikan semua jawaban sudah terisi.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#1B3C53',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ya, Kumpulkan!'
        }).then((result) => {
            if (result.isConfirmed) {
                finishQuiz();
            }
        });
    });

    // Render Soal Pertama
    renderQuestion(currentQuestion);
});