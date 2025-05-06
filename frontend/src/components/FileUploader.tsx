import React, { useState } from "react";
import { uploadFiles } from "../api/upload";

interface Props {
  onResult: (data: any) => void;
}

const FileUploader: React.FC<Props> = ({ onResult }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState("");

  const handleSubmit = async () => {
    const result = await uploadFiles(files, prompt);
    onResult(result);
  };

  return (
    <div>
      <input type="file" multiple onChange={e => setFiles(Array.from(e.target.files || []))} />
      <textarea placeholder="Enter your prompt" value={prompt} onChange={e => setPrompt(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default FileUploader;
