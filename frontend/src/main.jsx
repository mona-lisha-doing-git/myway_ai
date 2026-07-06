import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowRight,
  BadgeIndianRupee,
  Bot,
  GraduationCap,
  MapPin,
  RefreshCw,
  Search,
  Send,
  SlidersHorizontal,
  Sparkles,
  TrendingUp,
  X,
} from "lucide-react";
import "./styles.css";

const API_BASE =
  window.__MYWAY_CONFIG__?.apiBaseUrl ||
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

const initialPreferences = {
  state: "",
  city: "",
  ownership: "",
  course_name: "",
  specialization: "",
  exam: "",
  category: "",
  max_total_fees: "",
  min_package: "",
  admission_rank: "",
  limit: 8,
  include_ai_explanation: true,
};

const starterMessages = [
  {
    role: "agent",
    text: "Hi, I am your MyWay AI college advisor. Tell me the course, location, budget, rank, and placement expectations you have in mind.",
  },
];

function App() {
  const [preferences, setPreferences] = useState(initialPreferences);
  const [metadata, setMetadata] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("Checking backend");
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState(starterMessages);
  const [filtersOpen, setFiltersOpen] = useState(false);

  useEffect(() => {
    async function loadMetadata() {
      try {
        const response = await fetch(`${API_BASE}/metadata`);
        if (!response.ok) throw new Error("Backend is not responding");
        const data = await response.json();
        setMetadata(data);
        setStatus(`Connected using ${data.analytics_backend}`);
      } catch (err) {
        setStatus("Backend offline");
        setError("Start FastAPI first, then refresh this page.");
      }
    }

    loadMetadata();
  }, []);

  const states = useMemo(() => metadata?.states || [], [metadata]);
  const courses = useMemo(() => metadata?.courses || ["B.Tech", "M.Tech"], [metadata]);
  const ownershipTypes = useMemo(
    () => ["", ...(metadata?.ownership_types || ["Government", "Private"])],
    [metadata],
  );
  const exams = useMemo(() => metadata?.exams || [], [metadata]);
  const categories = useMemo(() => metadata?.categories || [], [metadata]);

  function updatePreference(name, value) {
    setPreferences((current) => ({ ...current, [name]: value }));
  }

  function buildPayload(source = preferences) {
    return {
      ...source,
      state: source.state || null,
      city: source.city || null,
      ownership: source.ownership || null,
      course_name: source.course_name || null,
      specialization: source.specialization || null,
      exam: source.exam || null,
      category: source.category || null,
      max_total_fees: numericOrNull(source.max_total_fees),
      min_package: numericOrNull(source.min_package),
      admission_rank: numericOrNull(source.admission_rank),
      limit: Number(source.limit || 8),
    };
  }

  async function findRecommendations(event, overridePreferences = preferences) {
    event?.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/recommendations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildPayload(overridePreferences)),
      });

      if (!response.ok) {
        throw new Error("Recommendation request failed");
      }

      const data = await response.json();
      setResult(data);
      setStatus(`Connected using ${data.analytics_backend}`);
      setMessages((current) => [
        ...current,
        {
          role: "agent",
          text:
            data.count > 0
              ? `I found ${data.count} college matches. I ranked them by fees, placement, institutional rank, and admission fit.`
              : "I could not find a match with those constraints. Try relaxing budget, rank, location, or placement filters.",
        },
      ]);
    } catch (err) {
      setError("Could not fetch recommendations. Check that the backend is running.");
      setMessages((current) => [
        ...current,
        {
          role: "agent",
          text: "I could not reach the recommendation service. Please check the backend and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function submitChat(event) {
    event.preventDefault();
    const cleanQuery = query.trim();
    if (!cleanQuery || loading) return;

    const extracted = extractPreferences(cleanQuery, metadata);
    const nextPreferences = { ...preferences, ...extracted };
    setPreferences(nextPreferences);
    setQuery("");
    setMessages((current) => [...current, { role: "student", text: cleanQuery }]);

    const followUp = getFollowUpQuestion(nextPreferences);
    if (followUp) {
      setMessages((current) => [...current, { role: "agent", text: followUp }]);
      return;
    }

    await findRecommendations(null, nextPreferences);
  }

  function applyStarter(text) {
    setQuery(text);
  }

  return (
    <main className="app-shell">
      <button
        className="filter-symbol"
        type="button"
        onClick={() => setFiltersOpen(true)}
        aria-label="Open filters"
        title="Open filters"
      >
        <SlidersHorizontal size={22} />
      </button>

      {filtersOpen && (
        <button
          className="drawer-backdrop"
          type="button"
          onClick={() => setFiltersOpen(false)}
          aria-label="Close filters"
        />
      )}

      <aside className={`filter-drawer ${filtersOpen ? "open" : ""}`} aria-hidden={!filtersOpen}>
        <div className="drawer-header">
          <div className="brand-row">
            <div className="brand-mark">
              <GraduationCap size={24} aria-hidden="true" />
            </div>
            <div>
              <h2>Filters</h2>
              <p>{status}</p>
            </div>
          </div>
          <button
            className="icon-button"
            type="button"
            onClick={() => setFiltersOpen(false)}
            aria-label="Close filters"
            title="Close filters"
          >
            <X size={18} />
          </button>
        </div>

        <form onSubmit={(event) => findRecommendations(event)} className="preference-form">
          <Field label="State">
            <select value={preferences.state} onChange={(event) => updatePreference("state", event.target.value)}>
              <option value="">Any</option>
              {states.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </Field>

          <Field label="City">
            <input
              value={preferences.city}
              onChange={(event) => updatePreference("city", event.target.value)}
              placeholder="Optional"
            />
          </Field>

          <Field label="Ownership">
            <select
              value={preferences.ownership}
              onChange={(event) => updatePreference("ownership", event.target.value)}
            >
              <option value="">Any</option>
              {ownershipTypes.filter(Boolean).map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Course">
            <select
              value={preferences.course_name}
              onChange={(event) => updatePreference("course_name", event.target.value)}
            >
              <option value="">Any</option>
              {courses.map((course) => (
                <option key={course} value={course}>
                  {course}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Specialization">
            <input
              value={preferences.specialization}
              onChange={(event) => updatePreference("specialization", event.target.value)}
              placeholder="Computer Science"
            />
          </Field>

          <div className="field-grid">
            <Field label="Exam">
              <select value={preferences.exam} onChange={(event) => updatePreference("exam", event.target.value)}>
                <option value="">Any</option>
                {exams.map((exam) => (
                  <option key={exam} value={exam}>
                    {exam}
                  </option>
                ))}
              </select>
            </Field>

            <Field label="Category">
              <select
                value={preferences.category}
                onChange={(event) => updatePreference("category", event.target.value)}
              >
                <option value="">Any</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </Field>
          </div>

          <div className="field-grid">
            <Field label="Max fees">
              <input
                type="number"
                min="0"
                value={preferences.max_total_fees}
                onChange={(event) => updatePreference("max_total_fees", event.target.value)}
              />
            </Field>

            <Field label="Min LPA">
              <input
                type="number"
                min="0"
                value={preferences.min_package}
                onChange={(event) => updatePreference("min_package", event.target.value)}
              />
            </Field>
          </div>

          <div className="field-grid">
            <Field label="Rank">
              <input
                type="number"
                min="1"
                value={preferences.admission_rank}
                onChange={(event) => updatePreference("admission_rank", event.target.value)}
              />
            </Field>

            <Field label="Results">
              <input
                type="number"
                min="1"
                max="25"
                value={preferences.limit}
                onChange={(event) => updatePreference("limit", event.target.value)}
              />
            </Field>
          </div>

          <label className="toggle-row">
            <input
              type="checkbox"
              checked={preferences.include_ai_explanation}
              onChange={(event) => updatePreference("include_ai_explanation", event.target.checked)}
            />
            <span>Generate AI explanation</span>
          </label>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? <RefreshCw className="spin" size={18} /> : <Search size={18} />}
            <span>{loading ? "Analyzing" : "Search colleges"}</span>
          </button>
        </form>
      </aside>

      <section className="agent-layout">
        <section className="chat-panel">
          <header className="agent-header">
            <div className="agent-avatar">
              <Bot size={28} aria-hidden="true" />
            </div>
            <div>
              <p className="eyebrow">MyWay AI</p>
              <h1>College decision agent</h1>
            </div>
          </header>

          <div className="message-list" aria-live="polite">
            {messages.map((message, index) => (
              <div className={`message ${message.role}`} key={`${message.role}-${index}`}>
                <p>{message.text}</p>
              </div>
            ))}
            {loading && (
              <div className="message agent">
                <p>Analyzing your preferences...</p>
              </div>
            )}
          </div>

          <div className="starter-row">
            <button type="button" onClick={() => applyStarter("Find B.Tech computer science colleges in Maharashtra under 10 lakh fees for rank 5000")}>
              Maharashtra CSE under 10 lakh
            </button>
            <button type="button" onClick={() => applyStarter("Suggest private engineering colleges in Rajasthan with good placements")}>
              Rajasthan private engineering
            </button>
          </div>

          <form className="chat-composer" onSubmit={submitChat}>
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Ask about colleges, for example: I want B.Tech CSE in Maharashtra under 10 lakh with rank 5000"
              rows="4"
            />
            <button type="submit" aria-label="Send query" title="Send query" disabled={loading}>
              {loading ? <RefreshCw className="spin" size={20} /> : <Send size={20} />}
            </button>
          </form>
        </section>

        <section className="results-area">
          <div className="toolbar">
            <div>
              <p className="eyebrow">Recommendations</p>
              <h2>Best matches</h2>
            </div>
            <div className="metric-strip">
              <Metric icon={<GraduationCap size={18} />} value={metadata?.college_count || "-"} label="Colleges" />
              <Metric icon={<Sparkles size={18} />} value={result?.count ?? "-"} label="Matches" />
            </div>
          </div>

          {error && <div className="notice">{error}</div>}

          {!result && !error && (
            <div className="empty-state">
              <Sparkles size={32} />
              <h3>Your recommendations will appear here.</h3>
              <p>Start with a natural-language query, or open the filter button in the top-left corner.</p>
            </div>
          )}

          {result?.explanation && (
            <section className="explanation">
              <Sparkles size={20} aria-hidden="true" />
              <p>{result.explanation}</p>
            </section>
          )}

          <div className="recommendation-list">
            {result?.recommendations.map((college, index) => (
              <RecommendationCard
                key={`${college.college_id}-${college.course_name}-${index}`}
                college={college}
                rank={index + 1}
              />
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

function Field({ label, children }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

function Metric({ icon, value, label }) {
  return (
    <div className="metric">
      {icon}
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function RecommendationCard({ college, rank }) {
  return (
    <article className="college-card">
      <div className="card-rank">{rank}</div>
      <div className="college-main">
        <div className="college-heading">
          <div>
            <h3>{college.college_name}</h3>
            <p>
              {college.course_name} - {college.specialization}
            </p>
          </div>
          <a
            href={college.website}
            target="_blank"
            rel="noreferrer"
            aria-label={`Open ${college.college_name} website`}
          >
            <ArrowRight size={18} />
          </a>
        </div>

        <div className="info-grid">
          <Info icon={<MapPin size={17} />} label="Location" value={`${college.city}, ${college.state}`} />
          <Info icon={<TrendingUp size={17} />} label="Avg package" value={formatLpa(college.average_package_lpa)} />
          <Info icon={<BadgeIndianRupee size={17} />} label="Total fees" value={formatCurrency(college.total_fees)} />
          <Info icon={<GraduationCap size={17} />} label="NIRF rank" value={college.nirf_rank || "N/A"} />
        </div>

        <div className="score-row">
          <span>Decision score</span>
          <meter min="0" max="1" value={college.recommendation_score || 0} />
          <strong>{Math.round((college.recommendation_score || 0) * 100)}%</strong>
        </div>
      </div>
    </article>
  );
}

function Info({ icon, label, value }) {
  return (
    <div className="info-item">
      {icon}
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

function extractPreferences(text, metadata) {
  const lowered = text.toLowerCase();
  const extracted = {};
  const knownStates = metadata?.states || [];
  const knownCourses = metadata?.courses || ["B.Tech", "M.Tech"];

  const state = knownStates.find((item) => lowered.includes(item.toLowerCase()));
  if (state) extracted.state = state;

  const course = knownCourses.find((item) => lowered.includes(item.toLowerCase()));
  if (course) extracted.course_name = course;
  if (!course && /b\.?\s*tech|btech|engineering/.test(lowered)) extracted.course_name = "B.Tech";
  if (/m\.?\s*tech|mtech/.test(lowered)) extracted.course_name = "M.Tech";

  if (/computer science|cse|cs\b/.test(lowered)) extracted.specialization = "Computer Science";
  if (/electronics|ece/.test(lowered)) extracted.specialization = "Electronics";
  if (/mechanical/.test(lowered)) extracted.specialization = "Mechanical";
  if (/vlsi/.test(lowered)) extracted.specialization = "VLSI";

  if (/government|govt|public/.test(lowered)) extracted.ownership = "Government";
  if (/private/.test(lowered)) extracted.ownership = "Private";

  if (/jee advanced/.test(lowered)) extracted.exam = "JEE Advanced";
  if (/jee main/.test(lowered)) extracted.exam = "JEE Main";

  const rankMatch = lowered.match(/(?:rank|air)\D{0,8}(\d{2,7})/);
  if (rankMatch) extracted.admission_rank = rankMatch[1];

  const feeMatch = lowered.match(/(?:under|below|upto|up to|max|budget)\D{0,12}(\d+(?:\.\d+)?)\s*(lakh|lac|cr|crore)?/);
  if (feeMatch) {
    const amount = Number(feeMatch[1]);
    const unit = feeMatch[2];
    extracted.max_total_fees = String(unit?.startsWith("cr") ? amount * 10000000 : amount * 100000);
  }

  const packageMatch = lowered.match(/(\d+(?:\.\d+)?)\s*(?:lpa|package)/);
  if (packageMatch) extracted.min_package = packageMatch[1];

  return extracted;
}

function getFollowUpQuestion(preferences) {
  if (!preferences.course_name && !preferences.specialization) {
    return "Which course or branch should I prioritize for you?";
  }
  if (!preferences.state && !preferences.city) {
    return "Which state or city would you prefer?";
  }
  if (!preferences.max_total_fees) {
    return "What is your maximum total fee budget?";
  }
  if (!preferences.admission_rank) {
    return "What admission rank should I use to estimate eligibility?";
  }
  return "";
}

function numericOrNull(value) {
  if (value === "" || value === null || value === undefined) return null;
  return Number(value);
}

function formatCurrency(value) {
  if (!value) return "N/A";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function formatLpa(value) {
  if (!value) return "N/A";
  return `${value} LPA`;
}

createRoot(document.getElementById("root")).render(<App />);
