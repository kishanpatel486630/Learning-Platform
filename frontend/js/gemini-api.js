/* gemini-api.js — Google Gemini Integration for AI features */
"use strict";

// API key is loaded from state.geminiApiKey or hardcoded fallback
const GEMINI_MODEL = "gemini-2.0-flash";

function getGeminiKey() {
  try {
    const s = JSON.parse(localStorage.getItem("learnpath_state") || "{}");
    return s.geminiApiKey || "";
  } catch (_) {
    return "";
  }
}

function isGeminiConfigured() {
  const key = getGeminiKey();
  return key && key.length > 10 && !key.startsWith("YOUR_");
}

async function geminiRequest(prompt, options = {}) {
  const key = getGeminiKey();
  if (!key) throw new Error("Gemini API key not configured");

  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${key}`;

  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: options.temperature || 0.7,
      maxOutputTokens: options.maxTokens || 2048,
      topP: 0.9,
    },
  };

  if (options.jsonMode) {
    body.generationConfig.responseMimeType = "application/json";
  }

  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error?.message || `Gemini API error: ${resp.status}`);
  }

  const data = await resp.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
  return options.jsonMode ? JSON.parse(text) : text;
}

// ─── AI Features ───────────────────────────────────────────

// Generate practice questions for a topic
async function aiGenerateQuestions(topic, examType, count = 5) {
  const prompt = `You are an expert exam question creator for Indian engineering students.

Generate ${count} multiple-choice questions for the topic "${topic}" for ${examType} exam preparation.

Return ONLY valid JSON in this exact format:
{
  "questions": [
    {
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0,
      "explanation": "Brief explanation why this is correct."
    }
  ]
}

Make questions ranging from easy to hard. Include commonly asked patterns from previous ${examType} exams.`;

  return await geminiRequest(prompt, { jsonMode: true, temperature: 0.8 });
}

// Get AI hint for a specific question
async function aiGetHint(question, topic) {
  const prompt = `You are a friendly tutor helping an Indian engineering student.

The student is stuck on this question from the topic "${topic}":
"${question}"

Give a helpful hint (NOT the answer) in 2-3 sentences. Guide them toward the solution step by step.`;

  return await geminiRequest(prompt, { temperature: 0.6, maxTokens: 300 });
}

// Explain a concept
async function aiExplainConcept(topic, level = "beginner") {
  const prompt = `Explain "${topic}" to a ${level}-level Indian engineering student.

Use simple language, real-world analogies, and examples. Include:
1. What it is (2-3 lines)
2. Why it matters
3. A simple example
4. Key points to remember

Keep it concise but clear. Use bullet points.`;

  return await geminiRequest(prompt, { temperature: 0.5, maxTokens: 800 });
}

// Generate study plan
async function aiGenerateStudyPlan(examType, daysLeft, hoursPerDay, topics) {
  const prompt = `Create a detailed day-wise study plan for ${examType} exam preparation.

Details:
- Days remaining: ${daysLeft}
- Study hours per day: ${hoursPerDay}
- Topics to cover: ${topics.join(", ")}

Return ONLY valid JSON:
{
  "plan": [
    {
      "day": 1,
      "date": "Day 1",
      "topics": ["Topic 1 - subtopic"],
      "hours": 2,
      "tasks": ["Read chapter X", "Solve 20 problems"],
      "tip": "Focus on understanding concepts first"
    }
  ],
  "tips": ["General tip 1", "General tip 2"]
}

Make the plan realistic and progressive (easy to hard). Include revision days.`;

  return await geminiRequest(prompt, {
    jsonMode: true,
    temperature: 0.6,
    maxTokens: 4096,
  });
}

// Solve/explain a problem step by step
async function aiSolveProblem(problem, subject) {
  const prompt = `You are a tutor helping an Indian engineering student with ${subject}.

Solve this problem step by step:
"${problem}"

Format your response with:
1. Understanding the problem
2. Step-by-step solution
3. Final answer
4. Key takeaway

Use clear formatting with bullet points and numbered steps.`;

  return await geminiRequest(prompt, { temperature: 0.3, maxTokens: 1500 });
}

// Generate interview tips for a specific round
async function aiInterviewTips(company, round) {
  const prompt = `Give preparation tips for the ${round} round of ${company} interview for freshers/engineering students in India.

Include:
1. What to expect in this round
2. Key topics/areas to focus on
3. Common question patterns
4. Do's and Don'ts
5. Time management tips

Keep it practical and actionable. Format with clear headings and bullet points.`;

  return await geminiRequest(prompt, { temperature: 0.5, maxTokens: 1000 });
}

// Generate mock interview questions
async function aiMockInterview(company, round, count = 10) {
  const prompt = `Generate ${count} realistic ${round} interview questions for ${company} campus placement for Indian engineering freshers.

Return ONLY valid JSON:
{
  "questions": [
    {
      "question": "Question text",
      "category": "Category (e.g., Arrays, DBMS, Aptitude)",
      "difficulty": "Easy|Medium|Hard",
      "expectedAnswer": "Brief model answer or key points",
      "timeLimit": 120
    }
  ]
}

Include a mix of difficulties. Make them realistic based on actual ${company} interview patterns.`;

  return await geminiRequest(prompt, { jsonMode: true, temperature: 0.7 });
}

window.geminiRequest = geminiRequest;
window.aiGenerateQuestions = aiGenerateQuestions;
window.aiGetHint = aiGetHint;
window.aiExplainConcept = aiExplainConcept;
window.aiGenerateStudyPlan = aiGenerateStudyPlan;
window.aiSolveProblem = aiSolveProblem;
window.aiInterviewTips = aiInterviewTips;
window.aiMockInterview = aiMockInterview;
window.isGeminiConfigured = isGeminiConfigured;
