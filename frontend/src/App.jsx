// https://stackoverflow.com/questions/54326515/how-can-i-make-sse-with-python-django

import { useState } from "react";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_HOST;

export default function Converter() {
  const [mode, setMode] = useState("its");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  async function fetchPreview(id) {
    try {
      console.log("FETCHING PREVIEW FOR ID:", id);
      console.log(`${API_BASE_URL}/${mode}/preview/?id=${id}`);
      const previewResponse = await axios.get(`${API_BASE_URL}/${mode}/preview/?id=${id}`, {
        responseType: 'blob',
      });
      const url = URL.createObjectURL(previewResponse.data);
      setPreview(url);
    } catch (err) {
      console.error("PREVIEW ERROR", err);
    }
  }

  const handleConversion = async () => {
    setResult([]);
    setPreview(null);

    if (!file) return alert(`SELECT ${mode === "its" ? "IMAGE" : "SOUND"} PLEASE`);

    const formData = new FormData();
    formData.append(mode === "its" ? "image" : "audio", file);
    console.log("FORM DATA", formData);

    try {
      const response = await axios.post(`${API_BASE_URL}/${mode}/`, formData);
      if (response.status !== 201) throw new Error("UPLOAD FAILED");

      const { id } = response.data;

      if (typeof EventSource !== "undefined") {
        const source = new EventSource(`${API_BASE_URL}/${mode}/stream/?id=${id}`);

        source.onmessage = (event) => {
          setResult((prev) => [...prev, event.data]);

          if (event.data === "CONVERSION COMPLETED") {
            // alert("CONVERSION DONE");
            source.close();
            fetchPreview(id);
          }
        };

        source.onerror = () => {
          source.close();
          console.error("SSE CLOSED");
        };
      } else {
        alert("UNSUPPORTED BROWSER FOR SSE");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App">
      <i>samTime101 2025 sep 24</i>
      <p>{API_BASE_URL}</p>
      <h1>{mode === "its" ? "Image to Sound" : "Sound to Image"} Converter</h1>
      <div>
        <label>
          <input type="radio" value="its" checked={mode === "its"} onChange={() => setMode("its")} /> Image to Sound
        </label>
        <label style={{ marginLeft: 20 }}>
          <input type="radio" value="sti" checked={mode === "sti"} onChange={() => setMode("sti")} /> Sound to Image
        </label>
      </div>
      <input key={mode} type="file" accept={mode === "its" ? "image/*" : "audio/wav"} onChange={handleFileChange} />
      <button onClick={handleConversion}>Start Conversion</button>
      <div>
        {/* <h2>Logs:</h2> */}
        {result.map((line, i) => <div key={i}>{line}</div>)}
      </div>

      {preview && (
        <div>
          <h2>Preview:</h2>
          {mode === "its" ? (
            <audio controls src={preview}></audio>
          ) : (
            <img src={preview} alt="Preview" style={{ maxWidth: 300 }} />
          )}
        </div>
      )}
    </div>
  );
}
