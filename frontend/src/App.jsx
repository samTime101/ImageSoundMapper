// https://stackoverflow.com/questions/54326515/how-can-i-make-sse-with-python-django

import { useState } from "react";
import axios from "axios";
export default function App() {
  const [result, setResult] = useState([]);
  const [file, setFile] = useState(null);
  const [audioPreview, setaudioPreview] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  async function fetchPreview(id) {
    try {
      const previewResponse = await axios.get(`http://localhost:8000/its/preview/?id=${id}`, {
        responseType: 'blob',
      });
      const url = URL.createObjectURL(previewResponse.data);
      // alert(url)
      setaudioPreview(url);
    } catch (error) {
      console.error("Error fetching preview:", error);
    }
  }

  const ConvertImageToSound = async () => {
    // CLEAR THE PREVIOUS RESULT
    setResult([]);

    if (!file) {
      alert("SELECT IMAGE PLEASE");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);
    let image_id = null
    try {
      const response = await axios.post("http://localhost:8000/its/", formData);

      if (response.status !== 201) throw new Error("FAILED UPLOAD");

      const data = response.data;
      image_id = data.id;

      if (typeof EventSource !== "undefined") {
        const source = new EventSource(`http://localhost:8000/its/stream/?id=${image_id}`);

        source.onmessage = (event) => {
          setResult((prev) => [...prev, event.data]);
        };

        source.onerror = () => {
          source.close();
          console.error("SSE CLOSED");
        };
        fetchPreview(image_id);
      } else {
        alert("UNSUPPORTED BROWSER FOR SSE");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>Convert Image to Sound</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={ConvertImageToSound}>Start Conversion</button>
      <div>
        {result.map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </div>
      {audioPreview && (
        <div>
          <h2>Preview:</h2>
          <audio controls src={audioPreview}></audio>
        </div>
      )}
    </div>
  );
}
