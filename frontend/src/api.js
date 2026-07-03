async function postJson(path, payload) {
  let response;

  try {
    response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new Error(
      "Can't reach the backend. Make sure the FastAPI server is running (uvicorn main:app)."
    );
  }

  if (!response.ok) {
    throw new Error(`Server error (${response.status}). Please try again.`);
  }

  return response.json();
}

export const api = {
  chat: (question) => postJson("/chat", { question }),
  generateQuiz: (question) => postJson("/generate-quiz", { question }),
  submitMcq: (answers) => postJson("/submit-mcq", { answers }),
  evaluate: (question, answer) => postJson("/evaluate", { question, answer }),
  health: async () => {
    try {
      const res = await fetch("/health");
      return res.ok;
    } catch {
      return false;
    }
  },
};
