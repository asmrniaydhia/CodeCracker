// LANGKAH ENKRIPSI
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

function createAlphabetTableSource(highlightChars) {
    let html = '<div class="alphabet-table">';
    for (let i = 0; i < 26; i++) {
        const char = alphabet[i];
        let className = 'alphabet-cell';
        if (highlightChars.includes(char)) className += ' source';
        html += `<div class="${className}">${char}</div>`;
    }
    html += '</div>';
    return html;
}

function createAlphabetTableTarget(highlightChars) {
    let html = '<div class="alphabet-table">';
    for (let i = 0; i < 26; i++) {
        const char = alphabet[i];
        let className = 'alphabet-cell';
        if (highlightChars.includes(char)) className += ' target';
        html += `<div class="${className}">${char}</div>`;
    }
    html += '</div>';
    return html;
}

function encryptChar(char, shift) {
    if (!char.match(/[A-Z]/i)) return char;
    
    const isUpperCase = char === char.toUpperCase();
    char = char.toUpperCase();
    
    const charIndex = alphabet.indexOf(char);
    const newIndex = (charIndex + shift) % 26;
    const newChar = alphabet[newIndex];
    
    return isUpperCase ? newChar : newChar.toLowerCase();
}

function startEncryption() {
    const plaintext = document.getElementById('plaintext').value.toUpperCase().trim();
    const key = parseInt(document.getElementById('key').value);
    
    if (!plaintext) {
        alert('⚠️ Masukkan plaintext terlebih dahulu!');
        return;
    }

    if (isNaN(key) || key < 1 || key > 25) {
        alert('⚠️ Kunci harus antara 1-25!');
        return;
    }

    const stepContainer = document.getElementById('stepContainer');
    stepContainer.innerHTML = '';
    stepContainer.style.display = 'block';

    let encryptedText = '';
    let uniqueChars = [];
    let encryptedChars = [];
    let processedChars = new Set();

    // Proses setiap karakter dan kumpulkan huruf unik
    for (let i = 0; i < plaintext.length; i++) {
        const char = plaintext[i];
        
        if (!char.match(/[A-Z]/)) {
            encryptedText += char;
            continue;
        }

        const encryptedChar = encryptChar(char, key);
        encryptedText += encryptedChar;

        // Hanya tambahkan jika belum pernah diproses (hapus duplikat)
        if (!processedChars.has(char)) {
            uniqueChars.push(char);
            encryptedChars.push(encryptedChar);
            processedChars.add(char);
        }
    }

    // Jika ada huruf yang diproses, tampilkan satu card
    if (uniqueChars.length > 0) {
        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';

        // Buat detail untuk setiap huruf unik
        let detailsHTML = '<div class="mb-3">';
        uniqueChars.forEach((char, index) => {
            const charIndex = alphabet.indexOf(char);
            const targetIndex = (charIndex + key) % 26;
            detailsHTML += `
                <div class="process-detail mb-2">
                    <span class="char-display">${char}</span>
                    <span style="font-size: 1.2em; margin: 0 8px;">→</span>
                    <span class="char-display result">${encryptedChars[index]}</span>
                    <span style="margin-left: 15px; color: #6b7280;">
                        (Posisi ${charIndex + 1} → Posisi ${targetIndex + 1})
                    </span>
                </div>
            `;
        });
        detailsHTML += '</div>';

        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">1</div>
                <h3 class="step-title">Enkripsi dengan Kunci ${key}</h3>
            </div>

            <div class="process-info">
                <strong>Proses:</strong> Geser setiap huruf sebanyak <strong>${key} langkah maju</strong> dalam alfabet
            </div>

            <h4 class="mt-4 mb-3" style="color: var(--lesson-brand-700); font-weight: 700;">
                <i class="fas fa-table"></i> Tabel Alfabet Plaintext (Huruf Asli)
            </h4>
            ${createAlphabetTableSource(uniqueChars)}
            <p class="text-center mt-2 text-muted">
                <small>Huruf yang ditandai merah adalah huruf dari plaintext</small>
            </p>

            <div class="arrow-down">↓</div>

            <h4 class="mb-3" style="color: var(--lesson-brand-700); font-weight: 700;">
                <i class="fas fa-table"></i> Tabel Alfabet Ciphertext (Hasil Enkripsi)
            </h4>
            ${createAlphabetTableTarget(encryptedChars)}
            <p class="text-center mt-2 text-muted">
                <small>Huruf yang ditandai hijau adalah hasil enkripsi</small>
            </p>

            <div class="process-info mt-4">
                <strong>Detail Transformasi:</strong><br>
                ${detailsHTML}
            </div>
        `;

        stepContainer.appendChild(stepCard);
    }

    // Tampilkan hasil akhir
    const resultDiv = document.createElement('div');
    resultDiv.innerHTML = `
        <div class="result-final">
            <h3>Hasil Enkripsi Lengkap</h3>
            <div class="result-text">${encryptedText}</div>
            <div class="result-info">
                Plaintext "<strong>${plaintext}</strong>" dengan kunci geser <strong>${key}</strong><br>
                berhasil dienkripsi menjadi "<strong>${encryptedText}</strong>"
            </div>
        </div>
    `;
    stepContainer.appendChild(resultDiv);

    // Smooth scroll ke hasil
    setTimeout(() => {
        stepContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Jalankan contoh saat halaman dimuat
window.addEventListener('load', () => {
    startEncryption();
});

// LANGKAH DEKRIPSI
function createAlphabetTableSource(highlightChars) {
    let html = '<div class="alphabet-table">';
    for (let i = 0; i < 26; i++) {
        const char = alphabet[i];
        let className = 'alphabet-cell';
        if (highlightChars.includes(char)) className += ' source';
        html += `<div class="${className}">${char}</div>`;
    }
    html += '</div>';
    return html;
}

function createAlphabetTableTarget(highlightChars) {
    let html = '<div class="alphabet-table">';
    for (let i = 0; i < 26; i++) {
        const char = alphabet[i];
        let className = 'alphabet-cell';
        if (highlightChars.includes(char)) className += ' target';
        html += `<div class="${className}">${char}</div>`;
    }
    html += '</div>';
    return html;
}

function decryptChar(char, shift) {
    if (!char.match(/[A-Z]/i)) return char;
    
    const isUpperCase = char === char.toUpperCase();
    char = char.toUpperCase();
    
    const charIndex = alphabet.indexOf(char);
    const newIndex = (charIndex - shift + 26) % 26;
    const newChar = alphabet[newIndex];
    
    return isUpperCase ? newChar : newChar.toLowerCase();
}

function startDecryption() {
    const ciphertext = document.getElementById('ciphertext').value.toUpperCase().trim();
    const key = parseInt(document.getElementById('key').value);
    
    if (!ciphertext) {
        alert('⚠️ Masukkan ciphertext terlebih dahulu!');
        return;
    }

    if (isNaN(key) || key < 1 || key > 25) {
        alert('⚠️ Kunci harus antara 1-25!');
        return;
    }

    const stepContainer = document.getElementById('stepContainer');
    stepContainer.innerHTML = '';
    stepContainer.style.display = 'block';

    let decryptedText = '';
    let uniqueChars = [];
    let decryptedChars = [];
    let processedChars = new Set();

    // Proses setiap karakter dan kumpulkan huruf unik
    for (let i = 0; i < ciphertext.length; i++) {
        const char = ciphertext[i];
        
        if (!char.match(/[A-Z]/)) {
            decryptedText += char;
            continue;
        }

        const decryptedChar = decryptChar(char, key);
        decryptedText += decryptedChar;

        // Hanya tambahkan jika belum pernah diproses (hapus duplikat)
        if (!processedChars.has(char)) {
            uniqueChars.push(char);
            decryptedChars.push(decryptedChar);
            processedChars.add(char);
        }
    }

    // Jika ada huruf yang diproses, tampilkan satu card
    if (uniqueChars.length > 0) {
        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';

        // Buat detail untuk setiap huruf unik
        let detailsHTML = '<div class="mb-3">';
        uniqueChars.forEach((char, index) => {
            const charIndex = alphabet.indexOf(char);
            const targetIndex = (charIndex - key + 26) % 26;
            detailsHTML += `
                <div class="process-detail mb-2">
                    <span class="char-display">${char}</span>
                    <span style="font-size: 1.2em; margin: 0 8px;">→</span>
                    <span class="char-display result">${decryptedChars[index]}</span>
                    <span style="margin-left: 15px; color: #6b7280;">
                        (Posisi ${charIndex + 1} → Posisi ${targetIndex + 1})
                    </span>
                </div>
            `;
        });
        detailsHTML += '</div>';

        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">1</div>
                <h3 class="step-title">Dekripsi dengan Kunci ${key}</h3>
            </div>

            <div class="process-info">
                <strong>Proses:</strong> Geser setiap huruf sebanyak <strong>${key} langkah mundur</strong> dalam alfabet
            </div>

            <h4 class="mt-4 mb-3" style="color: var(--lesson-brand-700); font-weight: 700;">
                <i class="fas fa-table"></i> Tabel Alfabet Ciphertext (Huruf Terenkripsi)
            </h4>
            ${createAlphabetTableSource(uniqueChars)}
            <p class="text-center mt-2 text-muted">
                <small>Huruf yang ditandai merah adalah huruf dari ciphertext</small>
            </p>

            <div class="arrow-down">↓</div>

            <h4 class="mb-3" style="color: var(--lesson-brand-700); font-weight: 700;">
                <i class="fas fa-table"></i> Tabel Alfabet Plaintext (Hasil Dekripsi)
            </h4>
            ${createAlphabetTableTarget(decryptedChars)}
            <p class="text-center mt-2 text-muted">
                <small>Huruf yang ditandai hijau adalah hasil dekripsi</small>
            </p>

            <div class="process-info mt-4">
                <strong>Detail Transformasi:</strong><br>
                ${detailsHTML}
            </div>
        `;

        stepContainer.appendChild(stepCard);
    }

    // Tampilkan hasil akhir
    const resultDiv = document.createElement('div');
    resultDiv.innerHTML = `
        <div class="result-final">
            <h3>Hasil Dekripsi Lengkap</h3>
            <div class="result-text">${decryptedText}</div>
            <div class="result-info">
                Ciphertext "<strong>${ciphertext}</strong>" dengan kunci geser <strong>${key}</strong><br>
                berhasil didekripsi menjadi "<strong>${decryptedText}</strong>"
            </div>
        </div>
    `;
    stepContainer.appendChild(resultDiv);

    // Smooth scroll ke hasil
    setTimeout(() => {
        stepContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Jalankan contoh saat halaman dimuat
window.addEventListener('load', () => {
    startDecryption();
});