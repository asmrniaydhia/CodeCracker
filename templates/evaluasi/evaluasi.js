// Start evaluasi: butuh centang persetujuan -> modal konfirmasi
document.getElementById('startBtn')?.addEventListener('click', () => {
    const agree = document.getElementById('agreeCheck');
    if (!agree.checked) {
    // Feedback cepat jika belum centang
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