// LANGKAH ENKRIPSI
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

function createAlphabetTable(sourceChar, targetChar) {
    let html = '<div class="alphabet-table">';
    for (let i = 0; i < 26; i++) {
        const char = alphabet[i];
        let className = 'alphabet-cell';
        if (char === sourceChar) className += ' source';
        if (char === targetChar) className += ' target';
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
        alert('Masukkan plaintext terlebih dahulu!');
        return;
    }

    if (isNaN(key) || key < 1 || key > 25) {
        alert('Kunci harus antara 1-25!');
        return;
    }

    const stepContainer = document.getElementById('stepContainer');
    stepContainer.innerHTML = '';
    stepContainer.style.display = 'block';

    let encryptedText = '';
    let stepNumber = 0;

    // Proses setiap karakter
    for (let i = 0; i < plaintext.length; i++) {
        const char = plaintext[i];
        
        if (!char.match(/[A-Z]/)) {
            encryptedText += char;
            continue;
        }

        stepNumber++;
        const encryptedChar = encryptChar(char, key);
        encryptedText += encryptedChar;

        const charIndex = alphabet.indexOf(char);
        const targetIndex = (charIndex + key) % 26;

        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';

        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">${stepNumber}</div>
                <h3 class="step-title">Enkripsi Huruf: ${char}</h3>
            </div>

            <div class="process-info">
                <strong>Proses:</strong> Geser huruf <span class="char-display">${char}</span> 
                sebanyak <strong>${key} langkah maju</strong> dalam alfabet
            </div>

            <p class="teks mb-2"><strong>Tabel Alfabet:</strong></p>
            ${createAlphabetTable(char, encryptedChar)}

            <div class="arrow-down">↓</div>

            <div class="process-info">
                <strong>Detail Perhitungan:</strong><br>
                • Posisi huruf <strong>${char}</strong> dalam alfabet: <strong>${charIndex + 1}</strong><br>
                • Geser <strong>${key} langkah maju</strong><br>
                • Posisi baru: <strong>${targetIndex + 1}</strong><br>
                • Huruf pada posisi ${targetIndex + 1}: <strong>${encryptedChar}</strong>
            </div>

            <div class="text-center mt-3">
                <span class="char-display">${char}</span>
                <span style="font-size: 1.5em; margin: 0 10px;">→</span>
                <span class="char-display result">${encryptedChar}</span>
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
        alert('Masukkan ciphertext terlebih dahulu!');
        return;
    }

    if (isNaN(key) || key < 1 || key > 25) {
        alert('Kunci harus antara 1-25!');
        return;
    }

    const stepContainer = document.getElementById('stepContainer');
    stepContainer.innerHTML = '';
    stepContainer.style.display = 'block';

    let decryptedText = '';
    let stepNumber = 0;

    // Proses setiap karakter
    for (let i = 0; i < ciphertext.length; i++) {
        const char = ciphertext[i];
        
        if (!char.match(/[A-Z]/)) {
            decryptedText += char;
            continue;
        }

        stepNumber++;
        const decryptedChar = decryptChar(char, key);
        decryptedText += decryptedChar;

        const charIndex = alphabet.indexOf(char);
        const targetIndex = (charIndex - key + 26) % 26;

        const stepCard = document.createElement('div');
        stepCard.className = 'step-card';

        stepCard.innerHTML = `
            <div class="step-header">
                <div class="step-number">${stepNumber}</div>
                <h3 class="step-title">Dekripsi Huruf: ${char}</h3>
            </div>

            <div class="process-info">
                <strong>Proses:</strong> Geser huruf <span class="char-display">${char}</span> 
                sebanyak <strong>${key} langkah mundur</strong> dalam alfabet
            </div>

            <p class="teks mb-2"><strong>Tabel Alfabet:</strong></p>
            ${createAlphabetTable(char, decryptedChar)}

            <div class="arrow-down">↓</div>

            <div class="process-info">
                <strong>Detail Perhitungan:</strong><br>
                • Posisi huruf <strong>${char}</strong> dalam alfabet: <strong>${charIndex + 1}</strong><br>
                • Geser <strong>${key} langkah mundur</strong><br>
                • Posisi baru: <strong>${targetIndex + 1}</strong><br>
                • Huruf pada posisi ${targetIndex + 1}: <strong>${decryptedChar}</strong>
            </div>

            <div class="text-center mt-3">
                <span class="char-display">${char}</span>
                <span style="font-size: 1.5em; margin: 0 10px;">→</span>
                <span class="char-display result">${decryptedChar}</span>
            </div>
        `;

        stepContainer.appendChild(stepCard);
    }

    // Tampilkan hasil akhir
    const resultDiv = document.createElement('div');
    // resultDiv.className = 'lesson-wrap';
    resultDiv.innerHTML = `
        <div class="result-final">
            <h3>Hasil Dekripsi</h3>
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