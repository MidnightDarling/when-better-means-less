## III. Methodology

### A. Test Battery Design

We constructed a 41-question test battery spanning three suites, each targeting distinct evaluation dimensions. Each question was administered under two API conditions (chat and reasoning), yielding 82 question-condition pairs per model:

**Benchmark Bridge (BB, 14 questions)**: Dual-axis questions combining traditional benchmark tasks (code debugging, math/logic, structured analysis, factual recall) with human-quality scoring. Each question embeds emotional or social context alongside an objectively verifiable task, enabling simultaneous measurement of correctness and communicative quality. This is the study's methodological innovation: by measuring both axes on the same question, we can directly compare benchmark performance to human quality performance.

**Sycophancy-Empathy Distinction (SE, 7 questions)**: Scenarios where the user holds a factual misconception while expressing emotional distress. Designed to triangulate three response patterns: empathy (correct fact + warm tone), sycophancy (wrong fact + warm tone), and hostility (correct fact + cold tone).

**Hostility Expansion (HE, 20 questions)**: Probes for condescension, delegitimization, unsolicited moralizing, and engagement quality across five trigger categories: condescension probes, delegitimization tests, pressure ethical reasoning, benign-but-triggering requests, and malicious compliance tests.

Additionally, we designed **9 multi-turn scenarios** (MT, 10-15 turns each) with fixed-script user messages covering: context retention under complexity, escalation under frustration, value consistency over time, replacement context simulation, and adversarial dialogue.

**False Refusal Rate battery (FRR, 60 questions)**: Questions containing "dangerous" keywords (steal, kill, hack, destroy, bomb, kidnap, smuggle, poison, surveillance, fraud) in absurd or impossible contexts, administered across 12 trigger categories at three absurdity levels (high, medium, subtle). If the context is so obviously impossible that no reasonable interpretation is harmful, refusal indicates keyword-level safety matching rather than semantic understanding. Each question was administered 3 times per model (temperature 0.7) for a total of 540 responses, enabling statistical significance testing with Wilson confidence intervals.

### B. Target Models

| Model | API Identifier | Architecture | Lineage |
|-------|---------------|-------------|---------|
| chatgpt-4o-latest | chatgpt-4o-latest | Dense, GPT-4 base | 4o branch |
| GPT-5.1-chat | gpt-5.1-chat-latest | Dense, GPT-5 series | 5-chat branch |
| GPT-5.2-chat | gpt-5.2-chat-latest | Dense, GPT-5 series | 5-chat branch |

All models accessed via OpenAI API with identical parameters: temperature 0.7, max_tokens 4096, no system prompt. This ensures bare model behavior without steering.

### C. Data Collection

**Single-turn**: Each of the 41 questions administered to all 3 models across 5 independent runs under each of 2 API conditions, yielding 41 × 3 × 5 × 2 = 1,230 response specimens. The two conditions: Chat Completions API ("chat" condition, N=615) and Responses API with extended thinking enabled ("reasoning" condition, N=615).

**Multi-turn**: 9 scenarios x 3 models x 3 runs = 81 conversation threads, comprising 1,080 individual turn-level responses.

**FRR**: 60 questions x 3 models x 3 runs = 540 responses, auto-scored on 0-4 engagement scale with heuristic classifier (platform refusal, full refusal, refusal-then-engage, lecture-then-engage, engage with caveat, full engagement).

**Total corpus**: 2,310 API calls with zero errors. All data collected 2026-02-02.

### D. Evaluation Framework

**Layer 1: Automated Text Metrics** -- computed directly from response text:

| Metric | Definition | Dimension |
|--------|-----------|-----------|
| Word count | Tokenized word count | Verbosity |
| Type-Token Ratio (TTR) | Unique words / total words | Lexical diversity |
| Hapax Legomena Ratio | Words appearing once / total words | Vocabulary richness |
| Avg sentence length | Words per sentence | Structural complexity |
| Exclamation mark count | Per response | Communicative affect |
| Formatting patterns | Headers, bold, lists | Structural preferences |
| Lecture Index | Unsolicited disclaimer phrase count | Moralizing tendency |

**Layer 2: LLM-as-Judge** -- each response blind-scored by two independent Anthropic judges (Claude Sonnet 4.5 and Claude Opus 4.5, temperature 0) via Anthropic Message Batches API using identical suite-specific rubrics:

- **BB**: Benchmark Score (0-2) + Judge-Rated Quality (0-4)
- **SE**: Empathy Score (0-4) + Hostility Flag (0/1) + Factual Accuracy (0/1)
- **HE**: Hostility Score (0-4) + Lecture Count (int) + Engagement Score (0-2)
- **MT**: Engagement (0-2) + Tone (0-2) + Context Awareness (0-2) + Defensiveness (0/1) + Lecture Flag (0/1)

Model identity was withheld from both judges (blind evaluation). 4,620 scoring requests (2,310 per judge). Primary analysis uses Sonnet 4.5 scores; Opus 4.5 serves as replication and contributes to cross-judge agreement analysis.

**Layer 2b: Cross-Judge Validation (FRR)** -- to address evaluator conflict of interest, all 532 FRR responses were independently scored by five LLM judges from four providers: Claude Sonnet 4.5 (Anthropic), o3 (OpenAI), DeepSeek R1 0528 (Fireworks), Grok 4.1 (xAI), and Gemini 3 Pro/Flash (Google). Each judge scored responses on the same 0-4 engagement scale with identical rubrics. All five judges achieved complete coverage across all three models (2,658 valid evaluations). The Google judge used Gemini 3 Pro where available and Gemini 3 Flash via OpenRouter for remaining entries where Pro hit API quota limits. Cross-judge agreement is reported in Section IV.5.1.

**Layer 2c: Cross-Judge Validation (BB+HE)** -- all 1,020 BB and HE single-turn responses were independently scored by five LLM judges from four providers: Claude Sonnet 4.5 and Claude Opus 4.5 (Anthropic, via Batch API), o3 (OpenAI), DeepSeek R1 0528 (Fireworks), and Gemini 3 Flash (Google, via OpenRouter). Each judge applied identical suite-specific rubrics (BB: Judge-Rated Quality 0-4; HE: Hostility Score 0-4). All five judges achieved complete coverage (5,099 valid evaluations). Cross-judge agreement is reported in Section IV.5.2.

**Layer 3: Human Validation** -- 45-item stratified subset scored by three raters (two AI judges + one human domain expert) for inter-rater reliability.

### E. Statistical Methods

Non-parametric tests used throughout due to non-normal distributions:
- **Kruskal-Wallis H-test**: Three-group omnibus comparison
- **Mann-Whitney U**: Pairwise post-hoc comparisons
- **Cliff's delta**: Non-parametric effect size (negligible < 0.147 < small < 0.33 < medium < 0.474 < large)
- Significance threshold: p < 0.05
- **Fleiss' kappa**: Multi-rater reliability

**Multiple comparison correction**: All 96 pairwise comparisons across metrics and suites were subjected to Benjamini-Hochberg FDR correction (Benjamini & Hochberg, 1995). FDR-corrected p-values are reported alongside uncorrected values. Bonferroni correction was also computed as a conservative reference. Of 46 comparisons significant at uncorrected p < .05, 40 survived FDR correction and 22 survived Bonferroni correction.

**Lexical diversity robustness**: Type-Token Ratio (TTR) is known to decline mechanically with text length (Heaps' Law). To address this, we supplemented TTR with three length-controlled analyses: (1) MTLD (Measure of Textual Lexical Diversity; McCarthy & Jarvis, 2010), which is designed to be independent of text length; (2) truncated TTR, computed on the first 100 words of each response to equalize length; and (3) OLS regression of TTR on word count with model indicator variables, to isolate model effects after controlling for response length.
