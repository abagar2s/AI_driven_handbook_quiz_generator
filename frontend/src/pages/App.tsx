import { useState } from "react";
import axios from "axios";
import Handbook from "../components/Handbook";
import Quiz from "../components/Quiz";

function App() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [prompt, setPrompt] = useState("Refine and format the following training content into a clear handbook format with sections and bullet points");
  const [handbook, setHandbook] = useState("");
  const [quiz, setQuiz] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      setError("❌ Please select one or more files.");
      return;
    }

    setLoading(true);
    setError("");
    setHandbook("");
    setQuiz([]);
    

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }
    formData.append("prompt", prompt);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setHandbook(res.data.handbuch);
      setQuiz(res.data.quiz);
      console.log("📊 Parsed quiz:", res.data.quiz);

    } catch (err) {
      setError("❌ Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📘 Handbook & Quiz Generator</h1>

      <input type="file" multiple onChange={(e) => setFiles(e.target.files)} />
      <br /><br />

      <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={3} cols={60} />
      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Generate"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {handbook && (
        <>
          <Handbook content={handbook} />
          <div style={{ marginTop: "24px" }} />
        </>
      )}

      {quiz.length > 0 && (
        <>
          <Quiz quiz={quiz} />
        </>
      )}
    </div>
  );
}

export default App;
