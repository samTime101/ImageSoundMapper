import { useState } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar , AvatarFallback , AvatarImage } from "@/components/ui/avatar";
import logo from "@/assets/image.png";
import { Github } from "lucide-react";


const API_BASE_URL = import.meta.env.VITE_HOST;

export default function Converter() {
  const [mode, setMode] = useState("its");
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string[]>([]);
  const [preview, setPreview] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) {
      setFile(null);
      return;
    }
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  async function fetchPreview(id: string) {
    try {
      const previewResponse = await axios.get(
        `${API_BASE_URL}/${mode}/preview/?id=${id}`,
        { responseType: "blob" }
      );
      const url = URL.createObjectURL(previewResponse.data);
      setPreview(url);
    } catch (err) {
      console.error("PREVIEW ERROR", err);
    }
  }

  const handleConversion = async () => {
    setProcessing(true);
    setResult([]);
    setPreview(null);
    if (!file)
      return alert(`SELECT ${mode === "its" ? "IMAGE" : "SOUND"} PLEASE`);

    const formData = new FormData();
    formData.append(mode === "its" ? "image" : "audio", file);

    try {
      const response = await axios.post(`${API_BASE_URL}/${mode}/`, formData);
      if (response.status !== 201) throw new Error("UPLOAD FAILED");

      const { id } = response.data;

      if (typeof EventSource !== "undefined") {
        const source = new EventSource(`${API_BASE_URL}/${mode}/stream/?id=${id}`);
        source.onmessage = (event) => {
          setResult((prev: string[]) => [...prev , event.data as string]);
          if (event.data === "CONVERSION COMPLETED") {
            source.close();
            setProcessing(false);
            fetchPreview(id);
          }
        };
        source.onerror = () => {
          source.close();
          setProcessing(false);
          console.error("SSE CLOSED");
        };
      } else {
        setProcessing(false);
        alert("UNSUPPORTED BROWSER FOR SSE");
      }
    } catch (err) {
      setProcessing(false);
      console.error(err);
    }
  };

  const handleModeChange = (newMode: "its" | "sti") => {
    setMode(newMode);
    setPreview(null);
    setResult([]);
    setFile(null);
  };

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">
            {mode === "its" ? "Image to Sound" : "Sound to Image"} Converter
          </CardTitle>
          {/* fuck this text shit we now use fucking Avatar lol */}
          {/* <i className="text-xs text-muted-foreground">
            samTime101 — 2025 Sep 24
          </i> */}
      <div className="flex flex-row flex-wrap items-center gap-2">
      <Avatar>
        <AvatarImage src={logo} />
        <AvatarFallback>SamTime101</AvatarFallback>
      </Avatar>
      {/* todo: deprecated raixa fix this if github logo doesnot appear */}
      <Github className="w-6 h-6" onClick={() => window.open("https://github.com/samTime101", "_blank")} />
      {/* <Avatar className="rounded-lg">
        <AvatarImage
          src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
        />
        <AvatarFallback>ER</AvatarFallback>
      </Avatar> */}
    </div>
        </CardHeader>

        <CardContent className="space-y-6">
          <div>
            <Label className="block mb-2">Conversion Mode</Label>
            <RadioGroup
              value={mode}
              onValueChange={handleModeChange}
              className="flex gap-6"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="its" id="its" />
                <Label htmlFor="its">Image to Sound</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="sti" id="sti" />
                <Label htmlFor="sti">Sound to Image</Label>
              </div>
            </RadioGroup>
          </div>

          <div>
            <Label htmlFor="file">Upload {mode === "its" ? "Image" : "Audio"}</Label>
            <Input
              key={mode}
              id="file"
              type="file"
              accept={mode === "its" ? "image/*" : "audio/*"}
              onChange={handleFileChange}
              className="mt-2"
            />
          </div>
          <Button onClick={handleConversion} className={`w-full ${processing ? 'bg-gray-400 cursor-not-allowed' : ''}`} disabled={processing}>
            {processing ? 'Processing...' : 'Start Conversion'}
          </Button>

          {/* {result.length > 0 && ( */}
            <ScrollArea className="h-40 w-full rounded-md border p-2">
              {result.map((line, i) => (
                <div
                  key={i}
                  className="text-sm font-mono bg-muted p-1 mb-1 rounded"
                >
                  {line}
                </div>
              ))}
            </ScrollArea>
          {/* )} */}

          {preview && (
            <div>
              <h2 className="text-lg font-semibold mb-2">Preview:</h2>
              {mode === "its" ? (
                <audio controls src={preview} className="w-full" />
              ) : (
                <img
                  src={preview}
                  alt="Preview"
                  className="max-w-xs rounded shadow"
                />
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
