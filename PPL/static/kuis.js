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

    if (jenis === "enkripsi") {
        questions = [
            { question: "Sebuah aplikasi sekolah mengirimkan pesan nilai rapor melalui server pusat. Agar data tidak mudah dibaca jika terjadi kebocoran jaringan, aplikasi tersebut menambahkan proses khusus sebelum pengiriman. Langkah apakah yang paling tepat dilakukan?", options: ["Mengubah format file menjadi PDF", "Mengganti nama file sebelum dikirim", "Melakukan enkripsi pada data rapor", "Menghapus sebagian data penting"], correct: 2 },
            { question: "Rina membuat aplikasi pengaduan anonim. Ia ingin memastikan setiap laporan aman walaupun database dicuri orang. Apa alasan utama ia perlu menerapkan enkripsi?", options: ["Agar laporan lebih cepat diproses", "Agar laporan tetap bisa dibaca hanya oleh pihak berwenang", "Agar database tidak bisa dihapus", "Agar server tidak cepat penuh"], correct: 1 },
            { question: "Sebuah pesan terenkripsi dapat dikirim dengan aman melalui jaringan sekolah yang sering mengalami gangguan keamanan. Mengapa enkripsi tetap penting meskipun jaringan sudah dilindungi firewall?", options: ["Firewall tidak menjamin data selalu aman", "Enkripsi membuat pesan jadi lebih pendek", "Firewall tidak boleh digunakan bersamaan dengan enkripsi", "Firewall menghapus pesan asli"], correct: 0 },
            { question: "Guru ingin berbagi file kunci ujian. Ia melakukan enkripsi, tetapi tidak mengirimkan kunci dekripsinya kepada siswa. Apa akibatnya?", options: ["File akan terbaca otomatis", "File tetap aman dan tidak dapat dibaca", "Siswa dapat menebak isinya dengan mudah", "File berubah ukuran menjadi lebih besar"], correct: 1 },
            { question: "Anto membuat sistem presensi otomatis. Ia menyadari data siswa dapat dilihat oleh admin jaringan. Untuk mencegah penyalahgunaan data, langkah apa yang harus ia tambahkan?", options: ["Mengganti warna tampilan aplikasi", "Menyimpan data di folder berbeda", "Menyembunyikan aplikasi dari layar utama", "Menyandikan data saat disimpan (enkripsi)"], correct: 3 },
        ];
    } else if (jenis === "caesar") {
        questions = [
            { question: "Pesan: “DRO AESMU LBYGX” (Geser +10). Apa isi pesannya?", options: ["THE QUICK BROWN", "THE QUICK ROBOT", "THE CLOUD BROWN", "THE BROWN HOUSE"], correct: 0 },
            { question: "Guru memberikan pesan terenkripsi “KHOOR ZRUOG” tanpa kunci. Teknik menebak paling efektif?", options: ["Menebak acak hingga muncul kata “WOW”", "Menggeser huruf satu per satu sampai pesan terbaca", "Mengganti huruf vokal saja", "Menghapus spasi lalu mencoba gabungan kata baru"], correct: 1 },
            { question: "Pesan “ZL AOLYPUF”, kata terakhir “HAPPY”. Geseran yang benar?", options: ["+5", "+7", "–7", "–5"], correct: 2 },
            { question: "Program Caesar mengubah angka jadi huruf. Perbaikan?", options: ["Mematikan fitur enkripsi", "Menambahkan aturan untuk membiarkan angka tetap sama", "Mengubah semua angka menjadi simbol", "Menghapus angka dari pesan"], correct: 1 },
            { question: "Cara memeriksa apakah pesan mencurigakan adalah Caesar Cipher?", options: ["Mengirim pesan kembali ke pengirim", "Menguji beberapa pergeseran untuk melihat apakah menghasilkan kata yang bermakna", "Mengganti semua huruf dengan vokal", "Menghapus huruf pertama dan terakhir"], correct: 1 },
        ];
    } else if (jenis === "dekripsi") {
        questions = [
            { question: "Pesan rahasia siswa berbunyi “RIJVS UYVJN”. Setelah dianalisis, ternyata ini hasil enkripsi tertentu. Apa tujuan proses dekripsi?", options: ["Mengubah pesan menjadi lebih sulit dibaca", "Mengembalikan pesan ke bentuk aslinya", "Menghasilkan pesan baru untuk dikirim", "Menghapus pesan dari sistem"], correct: 1 },
            { question: "Guru menerima file nilai yang terenkripsi, tetapi kunci dekripsinya hilang. Apa risiko yang terjadi?", options: ["File dapat dibuka siapa saja", "File tidak bisa dibaca meskipun datanya benar", "File berubah ukuran dan rusak", "File otomatis terhapus"], correct: 1 },
            { question: "Dalam simulasi keamanan, siswa mencoba membuka pesan yang disandikan. Namun ketika dekripsi dilakukan dengan kunci salah, hasilnya tidak masuk akal. Apa yang bisa disimpulkan?", options: ["Sistem enkripsi tidak berfungsi", "Dekripsi hanya bisa dilakukan dengan kunci yang tepat", "Pesan tidak perlu didekripsi", "Semua kunci menghasilkan pesan yang sama"], correct: 1 },
            { question: "Sebuah aplikasi melakukan enkripsi saat mengirim data, tetapi tidak melakukan dekripsi saat menerima. Apa dampaknya?", options: ["Data yang diterima tetap terenkripsi dan tidak terbaca", "Data menjadi lebih cepat terkirim", "Data otomatis berubah menjadi teks asli", "Data tersimpan dua kali lebih besar"], correct: 0 },
            { question: "Rani mencoba mendekripsi pesan yang digeser 8 langkah ke kanan. Ia ingin mengembalikannya ke teks asli. Apa yang harus ia lakukan?", options: ["Menggeser huruf maju 8 langkah", "Menggeser huruf mundur 8 langkah", "Menggeser huruf maju 16 langkah", "Menghapus huruf vokal lalu membaca ulang"], correct: 1 },
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
            <p class="fw-bold mb-4 text-dark" style="font-size: 1.15rem; line-height: 1.6;">${q.question}</p>
            
            <div class="option-list">
                ${q.options.map((opt, idx) => `
                    <label class="option ${answers[num] === idx ? 'checked' : ''}">
                        <input type="radio" name="q${num}" value="${idx}" ${answers[num] === idx ? "checked" : ""}> 
                        <span class="option-text">${opt}</span>
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