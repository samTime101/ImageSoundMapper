// todo: reduct the redundancy 

import { useState } from "react";
import axios from "axios";

function ImageToSound() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  }

  const handleImageSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/encrypt/", 
        formData, 
        {
        headers: {"Content-Type": "multipart/form-data"},
        responseType: "blob",
      }
    );
      const url = URL.createObjectURL(response.data);
      setResult(url);
    } catch (error) {
      console.error("ERROR :", error);
    }
  }

  return (
    <>
      <form onSubmit={handleImageSubmit}>
        <input type="file" accept="image/*" onChange={handleFileUpload} />
        <button type="submit">Upload</button>
        <p>{result}</p>
        <p>test</p>
      </form>
      {result && <audio controls src={result} />}
    </>
  )
}

function SoundToImage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileUpload = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  }
  
  const handleWavSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/decrypt/", 
        formData, 
        {
        headers: {"Content-Type": "multipart/form-data"},
        responseType: "blob",
      }
    );
      const url = URL.createObjectURL(response.data);
      setResult(url);
    } catch (error) {
      console.error("ERROR:", error);
    }
  }

  return (
    <>
      <form onSubmit={handleWavSubmit}>
        <input type="file" accept="audio/wav/" onChange={handleFileUpload} />
        <button type="submit">Upload</button>
        <p>{result}</p>
        <p>test</p>
      </form>
      {result && <img alt="result" src={result} />}
    </>
  )
}

export default function App() {
  const [mode, setMode] = useState("image-to-sound");

  return (
    <>
      <button onClick={() => setMode("image-to-sound")}>Image to Sound</button>
      <button onClick={() => setMode("sound-to-image")}>Sound to Image</button>
      {mode === "image-to-sound" ? <ImageToSound /> : <SoundToImage />}

      <p>you are in {mode} mode</p>
    </>
  )
}