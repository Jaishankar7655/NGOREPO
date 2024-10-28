
const backbutton = document
  .querySelector(".backbutton button")
  .addEventListener("click", () => {
    window.history.back();
  });
function confirmDownload() {
  let userConfirmed = confirm(
    "क्या आप प्रमाण पत्र डाउनलोड करना चाहते हैं? (Do you want to download the certificate?)"
  );
  if (userConfirmed) {
    downloadCertificate();
  } else {
    alert("डाउनलोड रद्द कर दिया गया। (Download canceled.)");
  }
}

function downloadCertificate() {
  var element = document.getElementById("certificate");
  html2pdf()
    .from(element)
    .set({
      margin: 0 /* No margin for full-page coverage */,
      filename: "certificate.pdf",
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        logging: true,
        dpi: 192,
        letterRendering: true,
      },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
    })
    .save();
}
