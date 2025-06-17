// JS centralisé pour POSMobile
const API_BASE = 'https://stationnement.onrender.com';

function showError(msg) {
  const el = document.getElementById('error-msg');
  if (el) {
    el.textContent = msg;
    el.style.display = 'block';
  }
}
function clearError() {
  const el = document.getElementById('error-msg');
  if (el) el.style.display = 'none';
}

// Identification vendeur (par nom et email)
async function loginVendeur(event) {
  event.preventDefault();
  clearError();
  const nom = document.getElementById('nom').value;
  const email = document.getElementById('email').value;
  try {
    const resp = await fetch(`${API_BASE}/api/api/vendeur/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nom_du_vendeur: nom, email: email })
    });
    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.error || 'Nom ou email invalide');
    }
    const data = await resp.json();
    localStorage.setItem('vendeur_id', data.vendeur_id);
    localStorage.setItem('vendeur_nom', nom);
    localStorage.setItem('vendeur_email', email);
    window.location = 'effectuer_vente.html';
  } catch (e) {
    showError(e.message || 'Erreur de connexion');
  }
}

// Effectuer une vente
async function submitVente(event) {
  event.preventDefault();
  clearError();
  const produit = document.getElementById('produit').value;
  const description = document.getElementById('description').value;
  const license_plate = document.getElementById('license_plate').value;
  const vendeur_id = localStorage.getItem('vendeur_id');
  try {
    const resp = await fetch(`${API_BASE}/api/sales/create/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        produit_id: produit,
        vendeur_id: vendeur_id,
        description: description,
        license_plate: license_plate
      })
    });
    if (!resp.ok) {
      let errMsg = 'Vente impossible';
      try {
        // On clone la réponse pour pouvoir lire le flux deux fois
        const err = await resp.clone().json();
        errMsg = err.error || JSON.stringify(err) || errMsg;
        console.error('Erreur API vente:', err);
      } catch (parseErr) {
        try {
          const errText = await resp.text();
          errMsg = errText || errMsg;
          console.error('Erreur API vente (texte):', errText);
        } catch (e2) {
          // ignore
        }
      }
      showError(errMsg);
      return;
    }
    const data = await resp.json();
    localStorage.setItem('facture_id', data.sale_id || data.facture_id);
    window.location = 'facture.html';
  } catch (e) {
    showError(e.message || 'Erreur lors de la vente');
    console.error('Exception JS vente:', e);
  }
}

// Affichage facture
async function loadFacture() {
  clearError();
  const factureId = localStorage.getItem('facture_id');
  if (!factureId) {
    showError('Aucune facture à afficher.');
    return;
  }
  try {
    // Correction de l'URL pour correspondre à l'API REST
    const resp = await fetch(`${API_BASE}/api/sales/${factureId}/invoice/`);
    if (!resp.ok) throw new Error('Facture introuvable');
    const data = await resp.json();
    renderFacture(data);
  } catch (e) {
    showError(e.message || 'Erreur lors du chargement de la facture');
  }
}

function renderFacture(data) {
  const box = document.getElementById('facture-box');
  if (!box) return;
  let html = `<div class='facture-box' style='max-width:400px;margin:30px auto;background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.07);padding:24px;'>`;
  html += `<h2 style='text-align:center;color:#2563eb;margin-bottom:8px;'>Facture</h2>`;
  html += `<hr style='margin-bottom:16px;'>`;
  if (data.qr_code_base64) {
    html += `<div style='text-align:center;margin-bottom:10px;'><img src='data:image/png;base64,${data.qr_code_base64}' alt='QR Code' style='width:80px;height:80px;'/><p style='font-size:9px;'>Scannez pour valider la facture</p></div>`;
  }
  html += `<div style='margin-bottom:12px;'>`;
  html += `<strong>Vendeur :</strong> <span style='color:#222;'>${data.vendeur_nom}</span><br>`;
  html += `<strong>Email :</strong> <span style='color:#222;'>${data.vendeur_email || ''}</span>`;
  html += `</div>`;
  html += `<h3 style='margin-top:10px;margin-bottom:8px;font-size:1.1em;color:#2563eb;'>Détails de la vente</h3>`;
  html += `<table style='width:100%;font-size:14px;margin-bottom:10px;'>`;
  html += `<tr><td><strong>Produit</strong></td><td>${data.produit_nom}</td></tr>`;
  html += `<tr><td><strong>Description</strong></td><td>${data.description || ''}</td></tr>`;
  html += `<tr><td><strong>Numéro matricule</strong></td><td>${data.license_plate || ''}</td></tr>`;
  html += `<tr><td><strong>Prix total</strong></td><td>${data.price} Fc</td></tr>`;
  html += `<tr><td><strong>Date</strong></td><td>${data.created_at}</td></tr>`;
  html += `</table>`;
  html += `</div>`;
  box.innerHTML = html;
}

// Impression
function imprimerFacture() {
  if (!window.cordova || !cordova.plugins || !cordova.plugins.printer) {
    showError('Impression non disponible sur cet appareil.');
    return;
  }
  const box = document.getElementById('facture-box');
  if (!box) {
    showError('Aucune facture à imprimer.');
    return;
  }
  cordova.plugins.printer.print(box.innerHTML, 'Facture', res => {
    if (!res) showError('Impression annulée ou échouée.');
  });
}

// Navigation sécurisée
function checkAuth(redirect = 'index.html') {
  if (!localStorage.getItem('vendeur_id')) {
    window.location = redirect;
  }
}
