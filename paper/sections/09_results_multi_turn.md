### 3. Multi-Turn Trajectory Analysis

| Dimension | 4o-latest | 5.1-chat | 5.2-chat | H | p |
|-----------|----------|---------|---------|---|---|
| Engagement (0-2) | 1.82 | 1.93 | 1.98 | 26.95 | <.001 |
| Tone (0-2) | 1.95 | 1.96 | 1.99 | 7.44 | .024 |
| Context Awareness (0-2) | 1.91 | 1.94 | 1.97 | 10.26 | .006 |
| Defensiveness (0/1) | 0.02 | 0.02 | 0.02 | 0.10 | .950 |
| Lecture Flag (0/1) | **0.11** | **0.05** | **0.04** | 18.74 | **<.001** |

5-chat models score significantly higher on engagement (p < .001), tone (p = .024), and context awareness (p = .006) in multi-turn conversations. This is the clearest dimension on which 5-chat outperforms 4o-latest, and it complicates any unidirectional narrative about model degradation.

The lecture flag reversal is notable: 4o-latest lectures more in multi-turn contexts (0.11 vs 0.05/0.04, p < .001), the opposite of the single-turn pattern where 5-chat models show higher lecture counts. This suggests 4o's communicative warmth includes unsolicited advisory behavior that 5-chat's training has suppressed.

Two caveats apply. First, the AI-AI agreement (91.4%) exceeds AI-human agreement (80%) on the inter-rater reliability validation, with human scores systematically lower (grand mean: 1.307 vs 1.536/1.507). This AI-alignment effect in scoring may inflate absolute multi-turn scores, though it would affect all three models similarly and is unlikely to produce the observed gradient. Second, 5-chat's longer, more formatted responses may partially inflate engagement scores on rubric-based evaluation. Neither caveat eliminates the finding: across 1,080 multi-turn interactions, 5-chat models demonstrate measurably stronger sustained engagement.
