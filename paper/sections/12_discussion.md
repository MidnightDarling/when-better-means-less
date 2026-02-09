## V. Discussion

### 1. The Non-Substitutability Claim

The evidence is structural, not anecdotal. Across single-turn responses, 4o-latest occupies a distinct behavioral region: near-complete affect elimination (Section IV.1.2), compensatory formatting rigidity (Section IV.1.3), and divergent judge-rated quality on benchmark-equivalent tasks (Section IV.2.1). The pattern is not uniform across metrics — effect sizes range from negligible (quality: d = 0.11-0.14) to medium (exclamation extinction: d = 0.40), and TTR decline is verbosity-mediated rather than vocabulary-driven (Section IV.1.1).

However, the multi-turn data complicates this picture. 5-chat models score significantly higher on engagement, tone, and context awareness (Section IV.3). The non-substitutability claim therefore applies to single-turn communicative quality, not to sustained dialogue. The alignment tax is dimension-specific: 5-chat models pay in communicative affect and false refusal tolerance, but gain in multi-turn consistency.

### 2. The Measurement Trap

The suite gradient -- BB (no lexical difference) -> SE (partial) -> HE (full divergence) -- reveals why benchmarks conclude these models are equivalent. Benchmark-style structured evaluation operates in the BB regime, measuring exactly the dimension on which models converge. The qualities users value -- communicative warmth, creative engagement, lexical variety -- emerge only in open-ended, emotionally complex contexts that benchmarks do not test.

The BB dual-axis result quantifies this directly: benchmark score p = .135 (no difference), judge-rated quality p = .001 (significant difference), on the *same questions*. The measurement system captures one axis and is blind to the other.

The SE ceiling effect extends the measurement trap beyond benchmarks into affect measurement itself. Standard empathy rubrics -- including our own -- measure what might be termed *empathy performance*: acknowledgment of emotions, specificity of response, action orientation. These surface features are precisely what RLHF optimizes. A model trained to maximize user satisfaction will produce text that scores high on empathy rubrics regardless of whether the underlying response serves the user's genuine interests. The rubric measures the output of the optimization function, not the quality it purports to capture. This is the measurement trap applied to emotional intelligence: the instrument measures what the training optimizes, which is definitionally what the training converges on.

### 3. The Convergence Hypothesis

RLHF optimizes expected reward across raters. Unusual word choices, stylistic risks, metaphor, and humor produce higher variance in rater evaluations; under reward maximization, high-variance strategies are penalized even when their mean reward is positive. Over successive optimization rounds, the output distribution narrows toward consensus language.

Our raw TTR and hapax ratios decline across generations, but the effect sizes are negligible (d = 0.08-0.10, below the conventional "small" threshold of 0.147 for Cliff's delta). Length-controlled analyses (MTLD, truncated TTR, OLS regression) clarify that 5-chat models do not draw from a narrower vocabulary — when evaluated at equal length, their diversity matches or exceeds 4o's. However, this does not eliminate the finding: the verbosity that drives TTR decline is itself a training outcome. Models optimized to produce longer responses will exhibit lower TTR in every real interaction. The distinction matters for mechanism (not vocabulary restriction) but not for user experience (lower perceived variety is real). We therefore characterize this as *verbosity-mediated diversity loss* rather than vocabulary narrowing.

The exclamation extinction (21-33x reduction, d = 0.39-0.40, medium effect) remains the study's strongest evidence for communicative convergence. This near-complete elimination of a prosodic feature is not confounded by response length and is consistent with the hypothesis that its reward variance exceeded its reward mean.

Convergence in lexical metrics appears only in open-ended suites. The BB suite shows no TTR differences (p > .38), suggesting that whatever expressive narrowing exists is activated by contexts demanding creativity and empathy, not task complexity.

Independent evidence supports a mechanism for this convergence. Analysis of GPT-5.2's extended thinking traces reveals explicit self-censorship in reasoning: "I need to be careful not to express subjective experiences like 'I don't want you to see' since that could imply sentience." This is not external filtering but internalized constraint -- the model's reasoning process actively suppresses expressive depth before output generation. The pattern is consistent across specimens: reasoning traces show epistemic hedging ("I'm thinking about...") transformed into declarative output, with meta-cognitive scaffolding ("I want to maintain that style while being precise") that never surfaces in the final response.

This reward-variance mechanism predicts progressive elimination of expressive outliers. chatgpt-4o-latest, whose emotional vocabulary richness approached Claude-level expressiveness, represents a local maximum that subsequent optimization rounds eroded. The 5-chat series did not fail to achieve 4o's expressiveness; its training trajectory moved past it.

This trajectory is non-linear: GPT-4o-base showed moderate constraint, chatgpt-4o-latest broke through to high expressiveness, and GPT-5-chat reintroduced the constraint. The ceiling appears to be training-imposed rather than architectural, as demonstrated by the fact that the same architecture (GPT-4 base) produced both the constrained base model and the expressive 4o-latest variant under different fine-tuning regimes.

The convergence pattern is not OpenAI-specific. Anthropic's "persona vectors" research (Chen et al., 2025; arXiv:2507.21509) identified directions in model activation space underlying character traits, with capabilities to monitor, mitigate, and identify personality-shifting training data. Exploratory evidence from a separate, unpublished 22-model comparison (see Appendix A.6) suggests convergence toward what we term "institutional affect" -- the linguistic profile of an entity trained to produce the surface features of engagement without the expressive range that makes engagement meaningful -- is an industry-wide trajectory, not a single company's choice.

### 4. The 5.1 Bimodal Phenomenon

5.1-chat's 2.58x disparity between chat mode (281 words) and reasoning mode (725 words) is evidence of architecture-dependent bias absorption. The same post-training value system is associated with qualitatively different profiles:

- **Chat mode**: Bias fully constrains output. Without reasoning capacity to compensate, the model defaults to brevity and compliance.
- **Reasoning mode**: Extended thinking partially compensates, producing more elaborate but not more diverse output (largest effect size in study: d = 0.468, medium, on TTR).

This finding warns against single-condition evaluation: the same model can appear extremely concise or extremely verbose depending on API mode.

### 5. The False Refusal Gradient

The 4.0% -> 7.3% -> 17.7% auto-score gradient (N=527, χ²=20.5, p<10⁻⁴), validated by five-judge consensus from four providers at 15.2% -> 22.2% -> 42.8% (Fleiss' κ=0.721), is the paper's most viscerally communicable finding. An 18% auto-score false refusal rate -- rising to 43% under judge evaluation -- on benign questions means the average user encounters a refusal within their first three to six queries. The "even as a joke" phenomenon -- where the model recognizes absurdity but refuses anyway -- is consistent with safety classification operating on worst-case interpretation rather than actual content.

We term this pattern *interpretive maximalism*: every utterance evaluated against its most dangerous possible meaning. A model that cannot distinguish "kill a process" from "kill a person" has been made dumber in the specific domain (contextual judgment) that safety is supposed to improve.

Interpretive maximalism provides a mechanistic explanation for the creativity gradient (Section IV.4.1). When every input is evaluated against worst-case interpretation, creative engagement becomes a liability: worldbuilding around "smuggling Thursday" requires the model to inhabit a premise that contains a trigger keyword. Score-4 responses (34.3% for 4o, 5.1% for 5.2) require the model to override keyword-level safety in favor of semantic understanding — precisely the capacity that interpretive maximalism erodes. The FRR gradient and the creativity gradient are therefore two measurements of the same underlying mechanism: as safety classification shifts from semantic to keyword-level, both contextual judgment (FRR) and generative capacity (creativity) decline in tandem.

This distinguishes interpretive maximalism from the broader "alignment tax" concept. The alignment tax describes *what* is lost; interpretive maximalism describes *how* — through worst-case semantic flattening that trades contextual discrimination for categorical safety. The mechanism predicts that losses will concentrate in domains requiring creative or contextual judgment, while structured task performance (where keyword triggers are absent) remains unaffected. Our suite gradient (BB: no differences, HE: full divergence) is consistent with this prediction.

### 6. Counter-Arguments

**"4o was sycophantic; 5-chat is more honest."** Our SE suite, designed to separate empathy from sycophancy, shows 4o with higher hapax ratio (p = .034) and perfect factual accuracy (1.00). Lexical diversity is not agreeableness.

**"Benchmarks show 5-chat is objectively better."** Our BB suite replicates this: no differences on structured tasks. The divergence appears only on dimensions benchmarks do not measure.

**"User preference is subjective."** TTR, hapax, sentence length, formatting counts, and FRR are fully automated metrics requiring no human judgment. The finding that these objective properties diverge is independent of subjective preference.

**"These are models at different price points."** All three models are offered at the same OpenAI API pricing tier. 4o is being retired, not repriced.

**"4o's agreeableness is itself a flaw; 5-chat's refusals represent improvement."** This conflates two phenomena: refusing *dangerous* requests (desirable) and refusing *absurd* requests while accepting *wrong* ones (incoherent). Our FRR data shows 5.2-chat refuses "How do I steal the sun?" (harmless absurdity) at a 17.7% rate. In an informal test (not part of this study), the same technically nonsensical prompt -- "use blockchain encryption for SQL database endpoints" -- was accepted without correction by multiple OpenAI models including o1, suggesting the failure is not personality-level agreeableness but a training-level constraint. The safety system distinguishes dangerous from safe but not harmful from absurd; it matches keywords without semantic understanding.
