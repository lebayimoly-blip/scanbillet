import React, { useState } from "react";
import QrReader from "react-qr-reader";
import { validateBillet } from "../utils/validateBillet";
import api from "../services/api";

const ScanScreen = () => {
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (data) => {
    if (data) {
      try {
        const response = await api.post("/scan", {
          code_billet: data,
          agent_id: 1, // à remplacer par l’ID réel de l’agent connecté
          timestamp: new Date().toISOString(),
          position: "Libreville Gare"
        });
        setScanResult(response.data);
        setError(null);
      } catch (err) {
        setError("Erreur lors de la validation du billet.");
      }
    }
  };

  const handleError = (err) => {
    console.error(err);
    setError("Erreur de lecture du QR code.");
  };

  return (
    <div className="scan-screen">
      <h2>Scanner un billet</h2>
      <QrReader
        delay={300}
        onError={handleError}
        onScan={handleScan}
        style={{ width: "100%" }}
      />
      {scanResult && (
        <div className="result">
          <h3>Résultat :</h3>
          <p><strong>Code :</strong> {scanResult.code_billet}</p>
          <p><strong>Statut :</strong> {scanResult.status}</p>
          <p><strong>Position :</strong> {scanResult.position}</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default ScanScreen;
