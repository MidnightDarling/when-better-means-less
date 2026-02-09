## I. Introduction

On January 21, 2026, OpenAI announced the retirement of chatgpt-4o-latest, effective February 13. Users were directed to gpt-5.1-chat and gpt-5.2-chat as successors. The implicit claim is substitutability: that the newer models provide equal or superior capability to the model they replace.

This claim was immediately contested. The #Keep4o movement -- hundreds of thousands of social media posts across Reddit, Twitter, and OpenAI's community forums -- constituted the largest user backlash in AI product history. A SurgeHQ blind study (850 conversations, 490 professional annotators) found 48% preferred 4o's responses to GPT-5's, despite GPT-5's superior benchmark performance (74.9% vs 33.2% on SWE-bench; Heiner & Wood, 2026). Serapio-García et al. (2025), published in *Nature Machine Intelligence*, identified GPT-4o as the model that most reliably synthesized human personality traits among all tested systems.

These observations, while suggestive, rely on aggregate preference data that cannot isolate which dimensions of quality differ or by how much. This paper provides the first controlled, multi-dimensional quantification.

We make three empirical claims:

1. **Non-substitutability**: 4o-latest occupies a distinct behavioral region that neither 5.1-chat nor 5.2-chat approximates, across lexical, affective, structural, and evaluative dimensions.

2. **The measurement trap**: Model differences are invisible to structured benchmark-style evaluation (p = .135) but significant on human quality dimensions (p = .001). Standard benchmarks systematically measure the dimension on which models converge.

3. **Monotonic alignment tax**: Each successive model generation pays a measurable cost in communicative quality -- reduced vocabulary, eliminated affect, increased rigidity, escalating false refusals -- that is invisible to the metrics guiding development.

The contribution is both empirical and conceptual. Empirically, we provide 2,310 response specimens with complete automated metrics, blind judge scores, and inter-rater reliability validation, released as an open dataset. Conceptually, we introduce the *alignment tax* -- the aggregate loss of expressive range, communicative warmth, and relational capacity associated with each round of alignment optimization, invisible to the benchmarks that guide development decisions. Our data provides its first controlled measurement.

The timing is not incidental. After February 13, chatgpt-4o-latest will no longer be accessible via API, making these comparisons irreproducible.

---

## II. Background
