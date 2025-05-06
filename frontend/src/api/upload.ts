export async function uploadFiles(files: File[], prompt: string) {
    const formData = new FormData();
    files.forEach(file => formData.append("files", file));
    formData.append("prompt", prompt);
  
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
  
    if (!response.ok) throw new Error("Upload failed");
    return response.json();
  }
  