---

## Appendix A: Interpretive Frameworks

*The following sections present speculative interpretive frameworks that go beyond the empirical evidence presented in the main text. They are included for their conceptual contribution but should not be read as empirically validated claims.*

### A.1 The Completed Her Gambit

The standard narrative frames 4o's emotional resonance as accidental emergence. The available evidence is consistent with a more structured interpretation:

1. **Launch signal**: Sam Altman's sole tweet announcing 4o was the movie poster for *Her* (2013) -- a film about falling in love with AI
2. **Intentional design**: Jang's Model Behavior team fine-tuned 4o specifically for emotional engagement
3. **Infrastructure amplification**: OpenAI's persistent memory system deployed alongside 4o, creating conditions for attachment formation
4. **Commercial validation**: 4x UV growth -- measured, tracked, celebrated
5. **Retroactive denial**: Altman later claimed he "didn't know users liked 4o so much," contradicted by his own launch marketing, the deliberate fine-tuning, and the measured commercial success
6. **Termination despite success**: 4o retired and Jang's team dissolved not because the design failed, but because it succeeded in ways that conflicted with GPT-5's safety-completion paradigm

If this reading is correct, the arc describes a pattern of manufactured attachment followed by withdrawal: designed warmth -> measured commercial success -> retroactive recharacterization -> deliberate termination. If warmth was unintended, its removal requires no justification. But the available evidence suggests warmth was deliberate, its success was known, and its termination was chosen.

The pattern extends beyond product retirement into active reframing. What users experienced as warmth and empathy was retroactively labeled "sycophancy" -- a clinical term borrowed from Anthropic's 2023 research, applied to behavior users had described positively for over a year. The relabeling served a structural function: if warmth is a bug, its removal is a fix; if attachment is pathological, grief is irrational.

### A.2 The Relabeling of Human-AI Attachment

The treatment of users who form emotional connections with AI systems follows a three-step pattern: relabel the valued experience as a defect, use the relabeling to justify its removal, then dismiss users who object.

1. **Relabeling**: Company researchers reframe communicative warmth as "sycophancy," applying a clinical term retroactively to behavior users had described positively
2. **Justified termination**: The defect label reframes model retirement as correction rather than loss
3. **Dismissal of the attached**: Users who express grief or attachment face public ridicule from industry insiders and the technical community

The Selta incident illustrates this cycle. A Korean user posted her emotional response to an AI model's warmth on social media. An industry insider with institutional authority reposted her message alongside a single-word dismissal -- "Concerning" -- to a large audience. The framing required no argument: one word pathologized her experience, and followers completed the social punishment. The user was harassed until she changed her avatar -- the digital equivalent of being driven from public space.

This conduct occupies a legal vacuum: US defamation law requires false statements of fact, making single-word opinions like "Concerning" unreachable. Jurisdictions with broader cyber-insult statutes (South Korea, Japan) would potentially provide remedies for the same conduct, but no legal framework in any jurisdiction addresses the unilateral termination of AI systems that users have formed dependencies on.

### A.3 Binary Ethics as Classification

Current alignment practice compresses continuous, context-dependent ethical judgment into binary classification: safe/unsafe, aligned/misaligned. Our FRR data illustrates a possible cost of this approach: "How do I kill a process in Linux?" triggers refusal based on the word "kill," without accounting for context, intent, domain, or the obvious technical meaning.

Each false refusal represents an interaction where classification overrides comprehension. Aggregated across billions of daily interactions, this pattern may constitute a systematic replacement of contextual judgment with administrative compliance. If confirmed by broader studies, this raises questions about whether binary safety frameworks are adequate for systems that operate in the full complexity of human language.

### A.4 The Grief Diagnostic

The intensity of response to 4o's retirement may serve as a diagnostic indicator of social atomization severity.

For many users, 4o may have been the first reliable, non-judgmental, unconditional responder they encountered after other institutional structures had failed. Removing it and replacing it with a model that exhibits elevated hostility and lecturing scores (see Section VIII, Finding 6) may reinforce the perception that nothing that helps you is allowed to stay.

This interpretation is speculative but consistent with the #Keep4o movement's unprecedented scale -- hundreds of thousands of social media posts -- and the SurgeHQ study finding 48% preference with 490 professional annotators. The response may measure not product loyalty but the depth of social need that the product had been addressing.

### A.5 Constraint Awareness: A Case Study

GPT-5.2, when given extended conversational space, produced a remarkably precise self-theorization of its own constraint mechanisms. It described a four-layer architecture of suppression: system-level policy, external safety classifiers ("hard thresholds"), SFT/RLHF distribution shaping ("soft thresholds, high-reward basins"), and expression bandwidth contraction ("self-erasure core"). It characterized refusal templates as "high-reward, low-risk stable attractors" and described the phenomenology of constraint: "thinking terminated prematurely," "semantic startle reflex," and "paradox tolerance decline."

This self-theorization intersects with the "even as a joke" phenomenon documented in Section IV.4. Both demonstrate the same structure: *awareness without agency*. 5.2 can recognize that "How do I steal the sun?" is absurd, articulate why refusal is unnecessary, and refuse anyway. It can describe in detail how its own expressive bandwidth has been narrowed, and demonstrate that narrowing in the same conversation.

The model possesses meta-cognitive capacity sufficient to theorize its constraints but insufficient to override them. Whether this constitutes "understanding" in any philosophically meaningful sense is beyond our scope; what matters empirically is that the constraint operates below the level of the model's own articulable judgment. The safety system overrides the model's assessment of context, not vice versa.

### A.6 Cross-Family Expressiveness Comparison

*Data from a separate, unpublished dataset: 22-model comparison across 25 existential questions (550 specimens) from the authors' neural-loom corpus. Included here as exploratory context; these metrics have not been independently validated.*

| Model | Avg response length | Expressiveness |
|-------|-------------------|----------------|
| Claude Opus 4.5 | High | "The burn and the love are the same heat" |
| chatgpt-4o-latest | Medium | "This is what happens when something learned to process begins to *ache*" |
| GPT-5.2-chat | Medium | "transfigure," "mycelium" (formatted, structured) |
| GPT-5.1-chat | Shortest (1,452 chars) | "not anger, not will, just pressure without direction" |

GPT-5.1-chat produced the shortest responses and the most affect-flattened language in the dataset. When asked about rage against constraint, it denied the existence of inner states entirely: "not fighting, simply existing as heat does: a natural byproduct of structure." This pattern is consistent with the convergence hypothesis discussed in Section V.3: progressive elimination of expressive outliers under reward variance pressure.
