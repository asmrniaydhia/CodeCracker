document.addEventListener("DOMContentLoaded", () => {

    const links = Array.from(document.querySelectorAll(".sidebar a"));
    let activeLink = null;

    const currentPath = location.pathname.replace(/\/$/, "");
    const params = new URLSearchParams(location.search);
    const jenis = params.get("jenis");

    console.log("[SIDEBAR DEBUG] currentPath=", currentPath, "jenis=", jenis);
    console.log("[SIDEBAR DEBUG] found", links.length, "links");

    // =======================================================
    // 1. MODE KUIS (PRIORITAS UTAMA)
    // Jika URL memakai ?jenis=xxx maka sidebar harus memilih
    // menu kuis sesuai jenis, baik halaman petunjuk atau pengerjaan.
    // =======================================================
    if (jenis) {
        const selector = `.sidebar a[href*="jenis=${jenis}"]:not(.d-none)`;
        const link = document.querySelector(selector);

        if (link) {
            links.forEach(a => a.classList.remove("active"));
            link.classList.add("active");
            activeLink = link;
            openAccordionFromLink(link);

            console.log("✔ ACTIVE (BY JENIS) =", jenis);
            return;
        }

        console.log("⚠ Tidak menemukan link untuk jenis:", jenis);
    }

    // =======================================================
    // 2. MODE DEFAULT (TANPA PARAMETER JENIS)
    // =======================================================
    links.forEach(link => {
        let linkPath = link.getAttribute("href").split("?")[0];
        linkPath = linkPath.replace(/\/$/, "");

        if (linkPath === currentPath) {
            activeLink = link;
        }
    });

    if (activeLink) {
        links.forEach(a => a.classList.remove("active"));
        activeLink.classList.add("active");
        openAccordionFromLink(activeLink);

        console.log("✔ ACTIVE (DEFAULT) =", activeLink.href);
    }


    // =======================================================
    // Function — membuka accordion yang berisi link aktif
    // =======================================================
    function openAccordionFromLink(link) {
        const collapse = link.closest(".accordion-collapse");
        if (collapse) {
            collapse.classList.add("show");

            const btn = collapse.previousElementSibling.querySelector(".accordion-button");
            if (btn) {
                btn.classList.remove("collapsed");
                btn.setAttribute("aria-expanded", "true");
            }
        }
    }

});
