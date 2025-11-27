document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname.startsWith("/evaluasi/nilai/")) {
    console.log("[MAIN.JS] Script dihentikan di halaman hasil evaluasi.");
    return;
  }

  const links = Array.from(document.querySelectorAll(".sidebar a"));
  let activeLink = null;

  const currentPath = location.pathname.replace(/\/$/, "");
  const params = new URLSearchParams(location.search);
  const jenis = params.get("jenis");

  console.log("[SIDEBAR DEBUG] currentPath=", currentPath, "jenis=", jenis);
  console.log("[SIDEBAR DEBUG] found", links.length, "links");

//   if (currentPath.startsWith("/evaluasi/nilai/")) {
//     // ⚠️ PENTING: Jika di halaman hasil evaluasi, aktifkan menu evaluasi statis.
//     const evaluasiLink = document.querySelector(
//       ".sidebar a[href='{% url 'evaluasi_petunjuk' %}']"
//     );

//     if (evaluasiLink) {
//       links.forEach((a) => a.classList.remove("active"));
//       evaluasiLink.classList.add("active");
//       openAccordionFromLink(evaluasiLink);

//       console.log("✔ ACTIVE (BY EVALUASI DETAIL)");
//       return; // HENTIKAN EKSEKUSI. Ini menyelesaikan konflik 404 yang berasal dari script.
//     }
//   }

  // =======================================================
  // 1. MODE KUIS (PRIORITAS UTAMA)
  // Jika URL memakai ?jenis=xxx maka sidebar harus memilih
  // menu kuis sesuai jenis, baik halaman petunjuk atau pengerjaan.
  // =======================================================
  if (jenis) {
    const selector = `.sidebar a[href*="jenis=${jenis}"]:not(.d-none)`;
    const link = document.querySelector(selector);

    if (link) {
      links.forEach((a) => a.classList.remove("active"));
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
  links.forEach((link) => {
    let linkPath = link.getAttribute("href").split("?")[0];
    linkPath = linkPath.replace(/\/$/, "");

    if (linkPath === currentPath) {
      activeLink = link;
    }
  });

  if (activeLink) {
    links.forEach((a) => a.classList.remove("active"));
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

      const btn =
        collapse.previousElementSibling.querySelector(".accordion-button");
      if (btn) {
        btn.classList.remove("collapsed");
        btn.setAttribute("aria-expanded", "true");
      }
    }
  }
});
