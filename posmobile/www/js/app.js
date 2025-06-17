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
    const resp = await fetch(`${API_BASE}/api/vendeur/login/`, {
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
  const quantite = document.getElementById('quantite').value;
  const description = document.getElementById('description').value;
  const license_plate = document.getElementById('license_plate').value;
  const vendeur_id = localStorage.getItem('vendeur_id');
  try {
    const resp = await fetch(`${API_BASE}/api/vente/creer/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        produit_id: produit,
        vendeur_id: vendeur_id,
        quantite: quantite,
        description: description,
        license_plate: license_plate
      })
    });
    if (!resp.ok) throw new Error('Vente impossible');
    const data = await resp.json();
    localStorage.setItem('facture_id', data.sale_id || data.facture_id);
    window.location = 'facture.html';
  } catch (e) {
    showError(e.message || 'Erreur lors de la vente');
  }
}

// Affichage facture
async function loadFacture() {
  clearError();
  const factureId = localStorage.getItem('facture_id');
  const token = localStorage.getItem('token');
  if (!factureId) {
    showError('Aucune facture à afficher.');
    return;
  }
  try {
    const resp = await fetch(`${API_BASE}/api/vente/facture/${factureId}/`, {
      headers: { 'Authorization': `Token ${token}` }
    });
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
  let html = `<h2>Facture #${data.numero}</h2>`;
  html += `<div>Date : ${data.date}</div>`;
  html += `<div>Client : ${data.client || 'N/A'}</div>`;
  html += `<table><thead><tr><th>Produit</th><th>Qté</th><th>Prix</th></tr></thead><tbody>`;
  data.lignes.forEach(l => {
    html += `<tr><td>${l.produit}</td><td>${l.quantite}</td><td>${l.prix} F</td></tr>`;
  });
  html += `</tbody></table>`;
  html += `<div class='facture-total'>Total : ${data.total} F</div>`;
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
  if (!localStorage.getItem('token')) {
    window.location = redirect;
  }
}
