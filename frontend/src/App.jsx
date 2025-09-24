import { useState } from "react";
import axios from "axios";

function FileConverter({ url, accept, renderResult }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(url, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });
      const blobUrl = URL.createObjectURL(response.data);
      setResult(blobUrl);
    } catch (error) {
      console.error("ERROR:", error);
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <input type="file" accept={accept} onChange={handleFileUpload} />
        <button type="submit">Upload</button>
      </form>
      {result && renderResult(result)}
    </>
  );
}

export default function App() {
  const [mode, setMode] = useState("image-to-sound");

  return (
    <>
      <button onClick={() => setMode("image-to-sound")}>Image to Sound</button>
      <button onClick={() => setMode("sound-to-image")}>Sound to Image</button>

      {mode === "image-to-sound" ? (
        <FileConverter
          url="http://localhost:8000/encrypt/"
          accept="image/*"
          renderResult={(url) => <audio controls src={url} />}
        />
      ) : (
        <FileConverter
          url="http://localhost:8000/decrypt/"
          accept="audio/wav"
          renderResult={(url) => <img alt="result" src={url} />}
        />
      )}

      <p>you are in {mode} mode</p>
    </>
  );
}
