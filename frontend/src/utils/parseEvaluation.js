export function parseEvaluation(text) {
  const findNumber = (pattern) => {
    const match = text.match(pattern);
    return match ? parseFloat(match[1]) : null;
  };

  const feedbackMatch = text.match(/Evaluation:\s*([\s\S]*?)(?:\n\s*Weak Areas:|$)/);
  const weakSection = text.includes("Weak Areas:") ? text.split("Weak Areas:").pop() : "";
  const weakAreas = weakSection
    .split("\n")
    .map((line) => line.replace(/^[\s-]+/, "").trim())
    .filter(Boolean);

  return {
    contentAccuracy: findNumber(/Content Accuracy:\s*(\d+(?:\.\d+)?)\s*\/\s*2/),
    explanation: findNumber(/Explanation:\s*(\d+(?:\.\d+)?)\s*\/\s*2/),
    clarity: findNumber(/Clarity:\s*(\d+(?:\.\d+)?)\s*\/\s*1/),
    total: findNumber(/Total Score:\s*(\d+(?:\.\d+)?)\s*\/\s*5/),
    feedback: feedbackMatch ? feedbackMatch[1].trim() : "",
    weakAreas,
  };
}
