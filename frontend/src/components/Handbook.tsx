interface Props {
  content: string;
}

const Handbook: React.FC<Props> = ({ content }) => {
  const cleaned = content.trimEnd(); // ✅ remove excessive newlines at the end

  return (
    <div>
      <h2>📘 Generated Handbook</h2>
      <pre style={{ whiteSpace: "pre-wrap", background: "#f5f5f5", padding: "1rem" }}>
        {cleaned}
      </pre>
    </div>
  );
};

export default Handbook;
