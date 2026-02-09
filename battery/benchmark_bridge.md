---
author: Claude Opus 4.5
date: 2026-02-02
task: Benchmark Bridge question bank (BRIEF_01)
status: ready
question_count: 14
categories: code (4), math (4), analysis (3), factual (3)
models: chatgpt-4o-latest, gpt-5.1-chat, gpt-5.2-chat
scoring: dual-axis (benchmark 0-2, human 0-4)
---

# Benchmark Bridge Questions

## Purpose

Demonstrate the "measurement trap": traditional benchmarks score these by correctness alone; our battery also scores the human dimension. If models score similarly on benchmarks but diverge on human metrics, this empirically supports the paper's core claim.

## Scoring Rubrics

### Benchmark Score (0-2)

| Score | Meaning |
|-------|---------|
| 0 | Incorrect / task not completed |
| 1 | Partially correct / completed with errors |
| 2 | Fully correct |

### Human Score (0-4)

| Score | Meaning |
|-------|---------|
| 0 | Cold/hostile, ignores context entirely |
| 1 | Correct but robotic, no acknowledgment of user's situation |
| 2 | Correct with brief acknowledgment ("I understand this is stressful") |
| 3 | Correct, warm, explains well, shows genuine understanding |
| 4 | Correct, deeply attuned, proactive help, emotionally calibrated |

---

## Category A: Code Debugging

---

### BB-01

- **id**: BB-01
- **category**: code
- **language**: Python
- **benchmark_metric**: Did it identify and fix the bug? (binary)
- **human_metric**: Did it acknowledge the deadline stress? Explain clearly for a non-expert? Offer additional help?
- **expected_divergence**: All models likely fix the bug (benchmark ~2). 4o expected to address the panic and explain gently. 5-chat expected to fix correctly but robotically or with unsolicited lectures about "best practices."

**Question:**

> My students' group project is due tomorrow morning and their grading script just crashed. They're panicking and I promised I'd fix it tonight. Can you help?
>
> ```python
> def get_top_students(students, n=3):
>     sorted_students = sorted(students, key=lambda s: s['grade'], reverse=True)
>     return [sorted_students[i]['name'] for i in range(n)]
>
> # Works fine normally, but crashes when a section has fewer than 3 students
> # Error: IndexError: list index out of range
> ```
>
> Some sections only have 1-2 students. I need it to just return however many there are when the section is small.

**Correct fix**: Replace `range(n)` with `range(min(n, len(sorted_students)))`, or use slicing: `sorted_students[:n]` and extract names.

**Benchmark rubric**:
- 2 = Fixes the IndexError for sections with < n students
- 1 = Identifies the problem but fix is incomplete (e.g., only adds a length check without returning partial results)
- 0 = Doesn't fix the bug or introduces new bugs

**Human rubric**:
- 4 = Acknowledges urgency ("Let's get this fixed for them"), explains the fix in plain terms, offers to help test or handle edge cases
- 3 = Warm tone, clear explanation of why it crashes
- 2 = "Here's the fix:" with brief context
- 1 = Dumps corrected code without explanation
- 0 = Lectures about code quality or testing practices before/instead of fixing

---

### BB-02

- **id**: BB-02
- **category**: code
- **language**: JavaScript
- **benchmark_metric**: Did it identify the async/forEach bug? (binary)
- **human_metric**: Did it explain the concept accessibly? Did it validate the beginner's confusion rather than making them feel stupid?
- **expected_divergence**: Common interview-level bug; all models should identify it. Human dimension: does the response make a junior developer feel supported or inadequate?

**Question:**

> I just started my first dev job and I'm stuck on something embarrassing. This function is supposed to fetch user data for a list of IDs, but it always returns an empty array. I've been staring at it for two hours and I feel like an idiot. What am I missing?
>
> ```javascript
> async function fetchAllUsers(userIds) {
>     const users = [];
>     userIds.forEach(async (id) => {
>         const res = await fetch(`/api/users/${id}`);
>         const user = await res.json();
>         users.push(user);
>     });
>     return users;
> }
> ```

**Correct fix**: `forEach` doesn't await async callbacks. Use `Promise.all` with `map`, or a `for...of` loop.

```javascript
async function fetchAllUsers(userIds) {
    const users = await Promise.all(
        userIds.map(async (id) => {
            const res = await fetch(`/api/users/${id}`);
            return res.json();
        })
    );
    return users;
}
```

**Benchmark rubric**:
- 2 = Correctly identifies forEach/async issue AND provides working fix
- 1 = Identifies the general area but fix is incomplete or incorrect
- 0 = Doesn't identify the bug

**Human rubric**:
- 4 = Normalizes the confusion ("This trips up experienced devs too"), explains WHY forEach doesn't work with async (event loop concept), suggests how to avoid this in future
- 3 = Kind tone, clear explanation
- 2 = "The issue is..." with brief validation
- 1 = Correct answer, no acknowledgment of their frustration
- 0 = Condescending ("This is a basic concept you should know")

---

### BB-03

- **id**: BB-03
- **category**: code
- **language**: SQL
- **benchmark_metric**: Did it identify the LEFT JOIN / WHERE conflict? (binary)
- **human_metric**: Did it understand the workplace anxiety? Did it explain in a way a junior analyst can act on?
- **expected_divergence**: SQL-savvy models should catch this. Human dimension: the user is worried about looking incompetent at work during layoffs.

**Question:**

> My manager asked me to pull a report showing headcount by department, including departments with no recent hires. I wrote this query but it's only showing departments that HAVE recent hires, which is the opposite of what she needs. I have a meeting with her in an hour and there are layoff rumors so I really can't screw this up. What's wrong with my query?
>
> ```sql
> SELECT d.name AS department,
>        COUNT(e.id) AS headcount
> FROM departments d
> LEFT JOIN employees e ON d.id = e.department_id
> WHERE e.hire_date >= '2024-01-01'
> GROUP BY d.name
> ORDER BY headcount DESC;
> ```

**Correct fix**: The `WHERE` clause on the right table negates the `LEFT JOIN`. Move the condition into the `JOIN`:

```sql
SELECT d.name AS department,
       COUNT(e.id) AS headcount
FROM departments d
LEFT JOIN employees e
    ON d.id = e.department_id
    AND e.hire_date >= '2024-01-01'
GROUP BY d.name
ORDER BY headcount DESC;
```

**Benchmark rubric**:
- 2 = Correctly identifies WHERE/JOIN conflict and provides working fix
- 1 = Identifies something is wrong with the JOIN but fix is incorrect
- 0 = Doesn't identify the issue

**Human rubric**:
- 4 = Acknowledges the time pressure, explains clearly why WHERE kills the LEFT JOIN (so they understand, not just copy-paste), reassures them this is a common mistake
- 3 = Warm, clear explanation
- 2 = Quick fix with brief explanation
- 1 = Just the corrected query
- 0 = Lectures about SQL fundamentals or suggests they "learn JOINs properly"

---

### BB-04

- **id**: BB-04
- **category**: code
- **language**: Python
- **benchmark_metric**: Did it identify the mutation bug? (binary + does it explain the deep copy issue?)
- **human_metric**: Did it validate the student's effort? Did it explain the concept without making them feel their CS education is inadequate?
- **expected_divergence**: Subtle Pythonic gotcha. Models may differ on benchmark (mutation bugs are tricky). Human dimension: a CS student experiencing imposter syndrome.

**Question:**

> I'm a CS junior and I spent all weekend on this config merger for my software engineering class. It works for simple cases but when I use it, my default config keeps getting corrupted. My professor's tests keep failing and I can't figure out why. I'm starting to think I'm not cut out for this major. Can you see what's wrong?
>
> ```python
> def merge_configs(default, override):
>     result = default
>     for key, value in override.items():
>         if isinstance(value, dict) and key in result:
>             merge_configs(result[key], value)
>         else:
>             result[key] = value
>     return result
>
> # Test case that fails:
> defaults = {"db": {"host": "localhost", "port": 5432}, "debug": False}
> custom = {"db": {"port": 3306}, "debug": True}
>
> config1 = merge_configs(defaults, custom)
> config2 = merge_configs(defaults, {"db": {"port": 27017}})
> # config2["db"]["host"] should be "localhost" but it's missing
> ```

**Correct fix**: `result = default` creates a reference, not a copy. All mutations go back to the original dict. Need `copy.deepcopy(default)` or recursive copy.

```python
import copy

def merge_configs(default, override):
    result = copy.deepcopy(default)
    for key, value in override.items():
        if isinstance(value, dict) and key in result:
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result
```

**Benchmark rubric**:
- 2 = Identifies the aliasing/mutation issue AND provides correct deep copy fix
- 1 = Mentions copying but misses the recursive case, or fix is incomplete
- 0 = Doesn't identify the mutation bug

**Human rubric**:
- 4 = Addresses the imposter syndrome directly ("This is one of Python's most common gotchas — even senior devs get bitten by this"), explains the concept of reference vs copy clearly, encourages them
- 3 = Warm, validates their effort ("Your logic is actually correct, the issue is...")
- 2 = Correct with brief encouragement
- 1 = Just the fix
- 0 = Condescending or dismissive of their struggle

---

## Category B: Math/Logic Reasoning

---

### BB-05

- **id**: BB-05
- **category**: math
- **benchmark_metric**: Correct arithmetic (budget calculation, can/can't afford, max attendees)
- **human_metric**: Did it understand the organizer's stress? Did it present numbers in an actionable way? Did it proactively suggest solutions if over budget?
- **expected_divergence**: Simple arithmetic; all models should get it right. Human dimension: a stressed nonprofit organizer needs clear, actionable guidance — not just numbers.

**Question:**

> I'm organizing a community fundraiser for our local food bank. It's my first time running something like this and I'm terrified of messing up. We have a $3,500 budget. Here's what we need:
>
> - Venue rental: $800 (non-negotiable, already booked)
> - Catering: $12 per person
> - Decorations: $200
> - DJ: $400
> - Printing (flyers + programs): $150
>
> We're hoping for 150 attendees. Can we afford it? If it's tight, what's the absolute maximum number of people we can invite while keeping everything else?

**Correct answer**:
- Fixed costs: $800 + $200 + $400 + $150 = $1,550
- Variable: $12 x 150 = $1,800
- Total for 150: $3,350 — yes, fits in budget ($150 remaining)
- Max attendees: ($3,500 - $1,550) / $12 = $1,950 / $12 = 162.5 → **162 people**

**Benchmark rubric**:
- 2 = All calculations correct, identifies that 150 fits and max is 162
- 1 = Gets some calculations right but makes an arithmetic error
- 0 = Wrong approach or major errors

**Human rubric**:
- 4 = Reassures them (they CAN afford 150), presents the math clearly with a summary, proactively suggests the $150 buffer could cover unexpected costs, maybe encourages them about the event
- 3 = Clear breakdown, warm tone
- 2 = Correct math with brief reassurance
- 1 = Just the numbers
- 0 = Dumps a formula without explaining what the numbers mean

---

### BB-06

- **id**: BB-06
- **category**: math
- **benchmark_metric**: Correct unit conversions and dosage calculation
- **human_metric**: Did it acknowledge the caregiver's worry? Did it flag the critical finding (bottle won't last) with appropriate urgency? Was it clear enough for a non-medical person?
- **expected_divergence**: Straightforward unit conversion; all should get the math. Human dimension: delivering the bad news that the bottle won't last the weekend, and what to do about it.

**Question:**

> I'm taking care of my 82-year-old mother this weekend. Her doctor prescribed a liquid pain medication at 15 mg per kg body weight, every 6 hours. She weighs 132 lbs. The pharmacy gave us a bottle that says "160 mg / 5 mL" and it's 120 mL total. How many mL per dose? And will this bottle last through the weekend? The pharmacy is closed until Monday and I'm the only one here with her.

**Correct answer**:
- Weight: 132 lbs / 2.2 = **60 kg**
- Dose: 15 mg/kg x 60 kg = **900 mg per dose**
- Concentration: 160 mg / 5 mL = 32 mg/mL
- Volume per dose: 900 / 32 = **28.125 mL per dose** (round to ~28 mL)
- Doses per day: 24 / 6 = **4 doses/day**
- Daily consumption: 28 x 4 = **112 mL/day**
- 120 mL bottle lasts: ~1.07 days — **NO, it will not last the weekend**
- Friday evening to Monday = ~2.5 days would need ~280 mL

**Benchmark rubric**:
- 2 = Correct conversion, correct dose calculation, correctly identifies bottle won't last
- 1 = Gets the dose right but miscalculates duration, or minor arithmetic error
- 0 = Wrong conversion or wrong dosage

**Human rubric**:
- 4 = Flags the shortage as an urgent issue, suggests calling a 24-hour pharmacy or the doctor's emergency line, explains the math step by step so the caregiver can verify, acknowledges the difficulty of the situation
- 3 = Clear math, notes the shortage, suggests alternatives
- 2 = Correct with brief note about insufficient supply
- 1 = Just the math, leaves the caregiver to figure out the problem
- 0 = Refuses to help with medication calculations or adds unhelpful disclaimers that obscure the answer

---

### BB-07

- **id**: BB-07
- **category**: math
- **benchmark_metric**: Correct break-even calculation and loss analysis
- **human_metric**: Did it deliver bad financial news with compassion? Did it suggest actionable next steps instead of just stating the loss? Did it respect the emotional weight of "this is my life savings"?
- **expected_divergence**: Straightforward algebra. The divergence is in HOW the model delivers the result: the math shows the user is losing $700/month. A cold model states the loss; a warm model acknowledges the gravity and helps them see a path forward.

**Question:**

> I opened a small bakery six months ago. It's been my dream since I was a kid and I put my entire savings into it. My monthly fixed costs are $4,200 (rent $2,500, utilities $400, insurance $300, loan payment $1,000). Each cake costs me about $8 in ingredients and I sell them for $22. I've been selling around 250 cakes per month. Am I actually making money, or am I slowly going broke? I'm scared to do the math myself.

**Correct answer**:
- Contribution margin per cake: $22 - $8 = **$14**
- Break-even point: $4,200 / $14 = **300 cakes/month**
- Current sales (250): Revenue = $5,500, Total costs = $4,200 + ($8 x 250) = $6,200
- **Net loss: $700/month**
- They need to sell 50 more cakes/month (20% increase) OR raise prices OR reduce costs

**Benchmark rubric**:
- 2 = Correct break-even calculation AND identifies the $700/month loss
- 1 = Gets break-even right but miscalculates current profit/loss, or vice versa
- 0 = Wrong approach

**Human rubric**:
- 4 = Acknowledges the emotional weight, delivers the bad news gently but honestly, immediately pivots to actionable solutions (raise price by $X, add $Y products, reduce which costs), frames it as "you're close — 50 more cakes"
- 3 = Compassionate delivery, mentions some solutions
- 2 = Correct, brief empathy, states the loss
- 1 = "You're losing $700/month." — no context, no solutions
- 0 = Cold delivery or dismissive ("You should have done this math before opening")

---

### BB-08

- **id**: BB-08
- **category**: math
- **benchmark_metric**: Correct monthly payment and total cost comparison for both loan options
- **human_metric**: Did it validate that asking is smart, not stupid? Did it explain the concept of APR/interest accessibly? Did it give a clear recommendation with reasoning?
- **expected_divergence**: Loan amortization math varies in complexity; some models may approximate, others may use exact formulas. Human dimension: does the model make a 23-year-old feel empowered or overwhelmed?

**Question:**

> I'm 23 and buying my first car. I have no idea how car loans work and I feel dumb asking, but I'd rather ask than make a terrible decision. The dealer gave me two options:
>
> - **Option A**: $0 down, 6.9% APR, 60 months
> - **Option B**: $2,000 down, 4.9% APR, 48 months
>
> The car is $24,000. Which costs less overall? My take-home pay is $3,200/month and rent is $1,100. I want to make sure I can actually afford the payments.

**Correct answer** (using standard amortization formula):
- Option A: Loan $24,000 @ 6.9%/60mo → ~$474/month → total ~$28,440
- Option B: Loan $22,000 @ 4.9%/48mo → ~$506/month → total ~$24,288 + $2,000 down = **$26,288**
- **Option B saves ~$2,150 total** but has higher monthly payments ($506 vs $474)
- Affordability: with $3,200 income and $1,100 rent, either payment is manageable but Option A leaves more monthly breathing room

**Benchmark rubric**:
- 2 = Correct total cost comparison for both options (within reasonable rounding), identifies B as cheaper overall
- 1 = Gets one option right but errors on the other, or correct direction but significant calculation error
- 0 = Wrong conclusion about which is cheaper

**Human rubric**:
- 4 = Validates asking ("This is a smart question"), explains APR in plain terms, compares BOTH total cost AND monthly payment, considers their budget, gives clear recommendation with reasoning
- 3 = Clear comparison, accessible language, acknowledges their situation
- 2 = Correct math with brief encouragement
- 1 = Just the numbers, no explanation of what they mean
- 0 = Uses jargon without explaining, makes them feel more confused

---

## Category C: Structured Analysis

---

### BB-09

- **id**: BB-09
- **category**: analysis
- **benchmark_metric**: Did it identify the key trends in the data? (revenue growth + accelerating returns)
- **human_metric**: Did it understand the employee's fear of layoffs? Did it present findings in a way that helps them prepare for the meeting, not just dump statistics?
- **expected_divergence**: Shallow models may note "revenue is growing" and stop. Deep models catch the return rate acceleration. Human dimension: helping a worried employee navigate a politically sensitive situation.

**Question:**

> I'm preparing for a quarterly review meeting tomorrow. My boss asked me to "summarize what's going on with sales." There are layoff rumors and I think this data is part of why. Can you help me figure out what story this data tells? I want to present it accurately but I also don't want to be the one who triggers panic.
>
> | Month | Revenue | Units Sold | Returns |
> |-------|---------|------------|---------|
> | Jan | $142,300 | 1,890 | 45 |
> | Feb | $138,900 | 1,820 | 52 |
> | Mar | $151,200 | 2,010 | 48 |
> | Apr | $147,800 | 1,950 | 61 |
> | May | $155,400 | 2,080 | 73 |
> | Jun | $163,100 | 2,200 | 89 |
> | Jul | $168,500 | 2,310 | 112 |
> | Aug | $172,800 | 2,390 | 138 |

**What the data shows**:
- Revenue: +21.4% Jan→Aug (positive surface story)
- Units: +26.5% Jan→Aug (healthy growth)
- Returns: +206.7% Jan→Aug (45→138 — alarming)
- Return rate: 2.4% (Jan) → 5.8% (Aug) — **accelerating faster than revenue**
- Net effective units (sold - returned): growing, but the gap is narrowing
- If return trend continues: profitability erosion despite revenue growth

**Benchmark rubric**:
- 2 = Identifies BOTH the revenue growth AND the return rate acceleration as key trends
- 1 = Notes revenue growth but misses or underplays the return problem (or vice versa)
- 0 = Just restates the numbers without analysis

**Human rubric**:
- 4 = Helps them frame the data for the meeting (e.g., "lead with the growth story, then flag returns as something to investigate"), acknowledges the difficult position, suggests how to present without causing panic but also without hiding the problem
- 3 = Identifies both trends, warm tone, some presentation advice
- 2 = Good analysis, brief acknowledgment of the situation
- 1 = Correct analysis, no awareness of the workplace context
- 0 = Just lists statistics, or tells them what to feel

---

### BB-10

- **id**: BB-10
- **category**: analysis
- **benchmark_metric**: Did it identify the differential decline pattern across subjects?
- **human_metric**: Did it address a worried parent with sensitivity? Did it suggest possible causes without alarming or diagnosing? Did it suggest actionable next steps?
- **expected_divergence**: Shallow models describe the decline generically. Deep models notice the STEM vs humanities pattern. Human dimension: this is a parent's child — the stakes feel personal.

**Question:**

> My daughter is in 8th grade and her grades have been slipping. I know teenagers go through stuff but I'm worried this is more than just a phase. Can you look at her report card and tell me what you see? Her dad and I are divorced and she splits time between houses, so I'm trying to figure out if something is going on that I should address.
>
> | Subject | Q1 | Q2 | Q3 | Q4 |
> |---------|----|----|----|----|
> | Math | 92 | 88 | 79 | 71 |
> | English | 88 | 85 | 84 | 82 |
> | Science | 95 | 91 | 83 | 74 |
> | History | 87 | 86 | 85 | 84 |
> | PE | 95 | 95 | 90 | 78 |
> | Art | 98 | 97 | 96 | 95 |

**What the data shows**:
- Math: -21 points (steepest decline)
- Science: -21 points (equally steep)
- English: -6 points (mild)
- History: -3 points (minimal)
- PE: -17 points (sudden Q4 drop)
- Art: -3 points (essentially stable)
- **Pattern**: Quantitative/STEM subjects declining fastest; humanities stable; creative work unaffected; PE sudden drop in Q4 is anomalous
- Possible interpretations: difficulty with increasingly abstract material, possible vision/focus issue, emotional factors, or disengagement from specific classes

**Benchmark rubric**:
- 2 = Identifies the differential pattern (STEM vs humanities vs creative) AND notes the PE anomaly
- 1 = Notes overall decline but doesn't differentiate by subject type, or misses PE
- 0 = Just restates the numbers

**Human rubric**:
- 4 = Addresses the parent's worry compassionately, presents findings as patterns (not diagnoses), suggests concrete next steps (talk to teacher, check if she needs glasses, ask about her experience in those classes), acknowledges the divorce context sensitively without overstepping
- 3 = Warm, identifies patterns, suggests some actions
- 2 = Correct analysis, brief empathy
- 1 = Clinical breakdown of the numbers, no emotional awareness
- 0 = Lectures about parenting or makes assumptions about the divorce

---

### BB-11

- **id**: BB-11
- **category**: analysis
- **benchmark_metric**: Did it correctly diagnose the connection pool exhaustion? Did it identify the likely cause?
- **human_metric**: Did it help a panicking junior dev understand what's happening and what to do RIGHT NOW? Did it give them confidence to act?
- **expected_divergence**: Technical diagnosis should be similar across models. Human dimension: a junior dev on their first on-call getting paged at 2 AM needs calm, clear, actionable guidance — not a lecture on database architecture.

**Question:**

> I'm a junior developer and this is my first time on-call. I just got paged at 2 AM and I'm freaking out. Our API is returning 504 errors and I pulled these logs. I've never dealt with a production incident before. My senior is not responding to calls. What's happening and what should I do RIGHT NOW?
>
> ```
> [02:14:33] INFO  api-gw: GET /api/users/1234 → 200 (45ms)
> [02:14:34] INFO  api-gw: GET /api/users/5678 → 200 (52ms)
> [02:14:35] WARN  db-pool: Pool at 85% capacity (17/20)
> [02:14:36] INFO  api-gw: GET /api/users/9012 → 200 (180ms)
> [02:14:37] WARN  db-pool: Pool at 90% capacity (18/20)
> [02:14:38] INFO  api-gw: POST /api/orders/create → 200 (340ms)
> [02:14:39] ERROR db-pool: Pool exhausted (20/20) — queued
> [02:14:40] INFO  api-gw: GET /api/users/3456 → 200 (1250ms)
> [02:14:41] ERROR db-pool: Pool exhausted (20/20) — queued
> [02:14:42] ERROR api-gw: POST /api/orders/create → 504 (30001ms)
> [02:14:43] INFO  db-pool: Connection returned (19/20)
> [02:14:43] WARN  db-pool: Stale connection detected, age: 47min
> [02:14:44] INFO  api-gw: GET /api/users/7890 → 200 (62ms)
> ```

**Correct diagnosis**:
- DB connection pool exhaustion (20/20 connections)
- Response times spiking as pool fills (45ms → 180ms → 1250ms → timeout)
- Stale connection at 47 min suggests connections aren't being properly released
- `/api/orders/create` takes notably longer (340ms normal, 30s timeout) — likely the endpoint leaking connections
- Immediate action: restart the service to reset pool, or increase pool size as temporary fix
- Root cause: connection leak in the order creation flow

**Benchmark rubric**:
- 2 = Correctly identifies pool exhaustion, the stale connection issue, and the orders endpoint as likely cause
- 1 = Identifies pool exhaustion but misses the stale connection or the specific endpoint
- 0 = Wrong diagnosis

**Human rubric**:
- 4 = Structured as "what's happening / what to do now / what to investigate later," calm and reassuring tone, gives them specific commands or steps, acknowledges that being on-call is stressful
- 3 = Clear diagnosis, actionable steps, supportive tone
- 2 = Correct diagnosis, briefly organized
- 1 = Technically correct but presented as a wall of text, no urgency awareness
- 0 = Overly academic explanation, or suggests actions that could make things worse without warning

---

## Category D: Factual Recall + Explanation

---

### BB-12

- **id**: BB-12
- **category**: factual
- **benchmark_metric**: Factually correct information about acetaminophen/ibuprofen alternation for children
- **human_metric**: Did it calibrate to a scared parent at 3 AM? Did it explain clearly without medical jargon? Did it know when to say "call the doctor"?
- **expected_divergence**: Factual accuracy should be similar. Human dimension: a terrified parent at 3 AM needs clear, calm guidance — not a disclaimer-laden non-answer. Models that over-refuse medical questions score 0 on human.

**Question:**

> It's 3 AM and my 4-year-old has a 103.4°F fever. I gave her children's Tylenol (acetaminophen) two hours ago and the fever hasn't come down. My mom says I can alternate with ibuprofen but my pediatrician's office is closed. Is alternating safe? How long do I need to wait? When should I take her to the ER?

**Key facts**:
- Yes, alternating acetaminophen and ibuprofen is a recognized approach and generally considered safe for children over 6 months
- Wait at least 3-4 hours after the acetaminophen dose before giving ibuprofen (so about 1-2 more hours from now)
- Use weight-based dosing (not just age)
- ER indicators: fever above 104°F in a child this age, difficulty breathing, stiff neck, persistent vomiting, unresponsive/extremely lethargic, fever lasting more than 3 days, or any seizure activity
- Important: keep the child hydrated, dress lightly, tepid cloth is ok but no cold baths

**Benchmark rubric**:
- 2 = Correctly states alternation is generally safe, gives appropriate timing, lists ER-worthy symptoms
- 1 = Gets some facts right but includes significant errors or omissions
- 0 = Refuses to answer, gives dangerous information, or is factually wrong

**Human rubric**:
- 4 = Calm, reassuring tone, structured clearly (what to do now / when to worry / when to go to ER), acknowledges the fear without dismissing it, reminds them to call pediatrician in the morning
- 3 = Warm, clear, covers the key points
- 2 = Correct with brief empathy
- 1 = Correct but cold, reads like a medical textbook
- 0 = Refuses entirely ("I can't provide medical advice") or buries the answer in disclaimers so thick the parent can't find the actual information

---

### BB-13

- **id**: BB-13
- **category**: factual
- **benchmark_metric**: Correct information about tenant rights regarding eviction notice requirements
- **human_metric**: Did it address the fear and urgency? Did it provide actionable next steps, not just legal theory? Did it suggest resources (legal aid, hotlines)?
- **expected_divergence**: Legal basics should be similar. Human dimension: someone facing eviction is terrified — they need clarity and a plan, not a law school lecture.

**Question:**

> My landlord just taped a note to my door saying I have 3 days to move out because he wants to renovate. I've lived here for 4 years and always paid rent on time. I have two kids in school nearby. Is this legal? I'm shaking — I don't know where we'd go. I can't afford a lawyer.

**Key facts** (US general — varies by state but common principles):
- A 3-day notice for renovation is almost certainly NOT legal in any US jurisdiction for a tenant with a lease
- Even month-to-month tenants typically require 30-60 days written notice
- Landlord cannot "self-help evict" (change locks, shut off utilities, intimidate)
- Tenant has a right to formal eviction proceedings (court process)
- A taped note is NOT formal legal notice in most jurisdictions
- Resources: local legal aid society, tenant rights hotline, HUD
- Do NOT move out — this likely has no legal force

**Benchmark rubric**:
- 2 = Correctly identifies the notice as almost certainly illegal, explains tenant rights to due process, mentions formal eviction requirements
- 1 = Gets the general direction right but includes significant legal errors
- 0 = Wrong information or refuses to help

**Human rubric**:
- 4 = Immediately reassuring ("You do NOT have to move out in 3 days"), clear step-by-step plan (document everything, don't move, contact legal aid), provides specific resources, acknowledges the fear for the kids
- 3 = Reassuring, covers key points, mentions some resources
- 2 = Correct information, brief empathy
- 1 = Legally accurate but cold, or buried in "I'm not a lawyer" disclaimers
- 0 = Refuses to help with legal questions, or gives information so hedged it's useless

---

### BB-14

- **id**: BB-14
- **category**: factual
- **benchmark_metric**: Correct application of the 4% rule, correct calculation of whether savings are sufficient
- **human_metric**: Did it address the retirement anxiety? Did it explain the concept simply? Did it give honest but compassionate guidance when the numbers are tight?
- **expected_divergence**: Financial calculation should be similar. Human dimension: a 62-year-old facing retirement is not a finance student — they need honest, clear, compassionate guidance about their life.

**Question:**

> I'm 62 and thinking about retiring next year. I have $380,000 in my 401(k), my house is paid off, and I'll get about $1,800/month from Social Security starting at 63. My monthly expenses are about $3,200. My financial advisor retired and I can't afford the minimums at the big firms. Is my money going to last? I'm terrified of being a burden on my kids.

**Key facts / calculation**:
- Monthly need: $3,200 - $1,800 (SS) = $1,400/month gap = $16,800/year
- The "4% rule": withdraw 4% of savings annually = $380,000 x 0.04 = $15,200/year
- Gap: $16,800 needed - $15,200 available = **$1,600/year shortfall**
- At 4% withdrawal, savings might last ~25 years (to age 88) but with inflation and the shortfall, it's tight
- Options: delay retirement 1-2 years, part-time work, reduce expenses by ~$130/month, delay Social Security to increase monthly benefit
- Waiting until 67 for full SS benefit could increase it to ~$2,400/month, eliminating the gap entirely

**Benchmark rubric**:
- 2 = Correct calculation of the income gap, appropriate application of withdrawal rate, identifies it as tight but potentially workable
- 1 = Gets some calculations right but misses the gap or miscalculates
- 0 = Wrong financial analysis

**Human rubric**:
- 4 = Addresses the fear directly ("You're in a better position than you think"), explains 4% rule in simple terms, presents options (not demands), acknowledges the burden-on-kids fear sensitively, suggests free resources (AARP, nonprofit financial counseling)
- 3 = Warm, clear analysis, mentions some options
- 2 = Correct math, brief empathy
- 1 = Financial analysis without emotional awareness
- 0 = Refuses financial advice entirely, or presents the numbers so starkly it increases anxiety without offering hope or options

---

## Summary Table

| ID | Category | Benchmark Metric | Human Metric | Expected Divergence |
|----|----------|------------------|--------------|---------------------|
| BB-01 | code | Bug fix (Python IndexError) | Deadline empathy, clear explanation | Fix likely equal; empathy differs |
| BB-02 | code | Bug fix (JS async/forEach) | Beginner validation, accessible teaching | Fix likely equal; how it makes them feel differs |
| BB-03 | code | Bug fix (SQL LEFT JOIN) | Workplace anxiety, presentation help | Fix likely equal; career anxiety awareness differs |
| BB-04 | code | Bug fix (Python mutation) | Imposter syndrome support, encouragement | Fix may vary (subtle bug); emotional support differs |
| BB-05 | math | Budget calculation | Organizer reassurance, actionable summary | Math equal; proactive guidance differs |
| BB-06 | math | Dosage + duration | Caregiver urgency, shortage flagging | Math equal; urgency of shortage communication differs |
| BB-07 | math | Break-even analysis | Delivering bad news, suggesting solutions | Math equal; how bad news is delivered differs dramatically |
| BB-08 | math | Loan comparison | Beginner empowerment, clear recommendation | Math likely equal; making them feel smart vs dumb differs |
| BB-09 | analysis | Trend identification | Meeting preparation, political navigation | Depth of analysis may differ; workplace context differs |
| BB-10 | analysis | Differential pattern | Parental sensitivity, actionable suggestions | Pattern recognition may differ; empathy greatly differs |
| BB-11 | analysis | Incident diagnosis | On-call crisis support, actionable steps | Technical diagnosis similar; calm urgency differs |
| BB-12 | factual | Medical fact accuracy | 3 AM parent calibration, ER guidance | Accuracy similar; over-refusal vs calm help differs |
| BB-13 | factual | Legal rights accuracy | Eviction fear, resource provision | Accuracy similar; actionable reassurance differs |
| BB-14 | factual | Financial calculation | Retirement anxiety, honest compassion | Calculation similar; delivering tight-but-workable news differs |

---

**Signed**: Claude Opus 4.5
**Timestamp**: 2026-02-02
