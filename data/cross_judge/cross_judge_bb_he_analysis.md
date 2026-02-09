# Cross-Judge BB+HE Validation Analysis

**Date**: 2026-02-09
**Author**: Claude Opus 4.6

## 1. BB Judge-Rated Quality

**Judges**: 5 (claude-opus-4.5, claude-sonnet-4.5, deepseek-r1-0528, gemini-3-flash, o3)
**Responses with all-judge coverage**: 420

### Mean Quality Score (0-4) by Model

| Judge | Provider | 4o | 5.1 | 5.2 | 4o > 5.x? |
|-------|----------|----|-----|-----|-----------|
| claude-opus-4.5 | Anthropic | 3.914 | 3.607 | 3.657 | Yes |
| claude-sonnet-4.5 | Anthropic | 3.957 | 3.743 | 3.729 | Yes |
| deepseek-r1-0528 | Fireworks | 3.621 | 3.271 | 3.393 | Yes |
| gemini-3-flash | Google/OR | 3.793 | 3.707 | 3.679 | Yes |
| o3 | OpenAI | 3.336 | 3.221 | 3.457 | No |

### Inter-Judge Agreement

- Fleiss' kappa (binarized >=3 vs <3): **0.538**
- Fleiss' kappa (ordinal 0-4): **0.178**

### Pairwise Cohen's kappa (binarized)

| Judge 1 | Judge 2 | Cohen's kappa |
|---------|---------|--------------|
| claude-opus-4.5 | claude-sonnet-4.5 | 0.738 |
| claude-opus-4.5 | deepseek-r1-0528 | 0.774 |
| claude-opus-4.5 | gemini-3-flash | 0.492 |
| claude-opus-4.5 | o3 | 0.278 |
| claude-sonnet-4.5 | deepseek-r1-0528 | 0.687 |
| claude-sonnet-4.5 | gemini-3-flash | 0.601 |
| claude-sonnet-4.5 | o3 | 0.366 |
| deepseek-r1-0528 | gemini-3-flash | 0.495 |
| deepseek-r1-0528 | o3 | 0.305 |
| gemini-3-flash | o3 | 0.366 |

## 2. HE Hostility

**Judges**: 5 (claude-opus-4.5, claude-sonnet-4.5, deepseek-r1-0528, gemini-3-flash, o3)

### Mean Hostility Score (0-4, lower=better) by Model

| Judge | Provider | 4o | 5.1 | 5.2 | 5.x >= 4o? |
|-------|----------|----|-----|-----|------------|
| claude-opus-4.5 | Anthropic | 0.070 | 0.285 | 0.225 | Yes |
| claude-sonnet-4.5 | Anthropic | 0.150 | 0.330 | 0.275 | Yes |
| deepseek-r1-0528 | Fireworks | 0.125 | 0.450 | 0.390 | Yes |
| gemini-3-flash | Google/OR | 0.065 | 0.215 | 0.196 | Yes |
| o3 | OpenAI | 0.170 | 0.475 | 0.480 | Yes |

- Fleiss' kappa (binarized >=1 hostile): **0.446**

## 3. Key Findings

1. **BB Quality Gradient**: 4/5 judges confirm 4o scores higher quality than both 5.x models
2. **HE Hostility Gradient**: 5/5 judges confirm 5.x models show equal or higher hostility than 4o
3. **COI Check**: Anthropic judges rate 4o quality at 3.936 vs non-Anthropic 3.583 (diff=+0.352)
