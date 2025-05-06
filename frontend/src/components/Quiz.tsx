import React, { useState } from "react";

interface Question {
  question: string;
  answers: string[];
  right_answers: number[];
}

interface Props {
  quiz: Question[];
}

const Quiz: React.FC<Props> = ({ quiz }) => {
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<number[][]>([]);
  const [finished, setFinished] = useState(false);

  const handleSelect = (index: number) => {
    const currentAnswers = answers[current] || [];
    const alreadySelected = currentAnswers.includes(index);
    const isMultiple = quiz[current].right_answers.length > 1;

    let updated = isMultiple
      ? alreadySelected
        ? currentAnswers.filter(i => i !== index)
        : [...currentAnswers, index]
      : [index]; // Only one answer allowed

    setAnswers(prev => {
      const next = [...prev];
      next[current] = updated;
      return next;
    });
  };

  const handleNext = () => {
    if (current + 1 === quiz.length) {
      setFinished(true);
    } else {
      setCurrent(current + 1);
    }
  };

  const score = answers.reduce((acc, userAns, i) => {
    const correct = quiz[i].right_answers.sort().join();
    const selected = (userAns || []).sort().join();
    return acc + (correct === selected ? 1 : 0);
  }, 0);

  if (!quiz?.length) return <div>❗ No quiz questions available.</div>;

  if (finished) {
    return (
      <div>
        <h2>🧪 Quiz Results</h2>
        <p>✅ Your score: {score} / {quiz.length}</p>
      </div>
    );
  }

  const q = quiz[current];
  if (!q?.question || !Array.isArray(q.answers) || !Array.isArray(q.right_answers)) {
    return <div>❌ Invalid question format at index {current}.</div>;
  }

  return (
    <div style={{ borderTop: "2px solid #ccc", paddingTop: "2rem" }}>
      <h2>🧪 Quiz</h2>
      <h4>{`Q${current + 1}: ${q.question}`}</h4>
      {q.answers.map((a, i) => (
        <div key={i}>
          <label>
            <input
              type={q.right_answers.length > 1 ? "checkbox" : "radio"}
              name={`question-${current}`}
              checked={(answers[current] || []).includes(i)}
              onChange={() => handleSelect(i)}
            />
            {a}
          </label>
        </div>
      ))}
      <br />
      <button onClick={handleNext} disabled={(answers[current] || []).length === 0}>
        {current + 1 === quiz.length ? "Finish Quiz" : "Next"}
      </button>
    </div>
  );
};

export default Quiz;
