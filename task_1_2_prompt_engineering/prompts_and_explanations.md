# Task 1.2 — Advanced Prompt Engineering Challenge

---

## Prompt 1: Social Media Post for Shoe Brand

**Original Weak Version:**

```
Write a social media post for our new shoe brand.
```

**Rewritten Version:**

```text
You are an expert social media manager and brand copywriter specialising in athletic
and lifestyle footwear brands targeting urban millennials (ages 22–35).

Your task is to write a single, highly engaging Instagram caption announcing the launch
of our new running shoe: "AeroStrides."

Before you write the caption, briefly think through the following (you may show this
reasoning in 1–2 sentences before the caption):
- Who is the ideal customer reading this post right now?
- What is the single most compelling emotional hook for this person?
- What action do I want them to take at the end?

Now write the caption using these constraints:
- Tone: Energetic, bold, and inspiring. Never corporate.
- Structure: (1) Strong opening hook — creates curiosity or urgency in line 1.
             (2) Core benefit — ultra-lightweight comfort + sleek, minimal aesthetic.
             (3) Social proof or specificity — one concrete differentiator (stat or feature).
             (4) Clear CTA — link in bio.
- Length: 3–4 short paragraphs. No paragraph longer than 3 lines.
- Emojis: 2–4 total. Use selectively — placement matters more than quantity.
- End with exactly 5 highly relevant hashtags.

Output the reasoning + caption now.
```

**Techniques Used and Reasoning:**

1. **Role Assignment:** Opening with "You are an expert social media manager..." gives the
   LLM a specific expert identity before it processes any task instructions. This shifts the
   model's prior probability distribution toward professional-quality, strategically informed
   outputs rather than generic consumer-level language.

2. **Chain-of-Thought (CoT) Prompting:** The explicit reasoning step — "Before you write,
   briefly think through..." — forces the model to activate latent strategic knowledge about
   audience, emotional hooks, and desired action _before_ generating copy. This intermediate
   reasoning step measurably improves the relevance and intentionality of the final output,
   particularly for creative tasks where first-draft quality is otherwise random.

3. **Structured Output Constraints:** Numbered structure rules (hook → benefit → proof → CTA)
   eliminate the model's freedom to produce structurally unpredictable output. By mapping
   each paragraph's purpose explicitly, the prompt converts a vague creative task into a
   repeatable, formula-driven process that an agency could rely on consistently.

4. **Specificity Anchoring:** Naming the product ("AeroStrides"), the target channel
   (Instagram), and the exact audience segment (urban millennials, 22–35) gives the model
   concrete anchors. Without specificity, LLMs default to the statistical average — which
   reliably produces generic, middle-of-the-road creative output.

5. **Constraint Stacking for Formatting:** The explicit rules on paragraph length, emoji
   count, and hashtag quantity prevent the most common failure modes (over-hashtagging,
   emoji overload, walls of text) without introducing so many constraints that the model's
   creative range is completely eliminated.

---

**Before/After Comparison — Actual AI Outputs:**

**BEFORE** (output from weak prompt):

> "Step up your game with our brand new shoes! 👟 Whether you're running errands or
> hitting the gym, these shoes are perfect for you. Available now — shop the link in
> our bio!"

_Assessment: Generic, category-level language. No brand identity. No specific benefit.
The emoji is used as filler. "Perfect for you" is meaningless. Any shoe brand in the
world could use this exact caption._

**AFTER** (output from rewritten prompt):

> _Reasoning: The ideal customer is an urban runner who cares about aesthetics as much
> as performance. The hook should create identity — they should see themselves in the
> first line. CTA should feel urgent but not desperate._
>
> "Your run. Redefined. ⚡
>
> AeroStrides are engineered for the city — 0.4 oz lighter than the industry standard,
> wrapped in a silhouette clean enough to go straight from the track to wherever the
> night takes you. 🏙️
>
> Ultra-lightweight algae foam. Zero bulk. Maximum distance.
>
> The city isn't waiting — neither should you. Grab your pair via the link in bio
> before they're gone. 💨
>
> #AeroStrides #UrbanRunner #SneakerCulture #RunTheCity #StreetwearKicks"

_Assessment: The chain-of-thought reasoning produced a copy-led identity hook ("Your
run. Redefined.") rather than a product description. The constraint structure ensured
all four elements (hook, benefit, proof, CTA) are present and in the correct paragraph
order. The result is immediately publishable._

---

## Prompt 2: Improve Ad Copy

**Original Weak Version:**

```
Make our ad copy more creative.
```

**Rewritten Version:**

```text
You are a senior advertising copywriter with 15 years of experience writing
high-converting Facebook and Instagram direct-response ad copy for SaaS products.

Here is the current underperforming Facebook ad copy for our productivity app, "FlowDesk":

--- CURRENT COPY ---
"FlowDesk is the all-in-one productivity app that helps you manage tasks, set goals,
and track your time. Try it free for 14 days. Sign up today."
--- END CURRENT COPY ---

Here is an example of high-performing SaaS ad copy that achieved a 4.2% CTR:
"You've got 47 unread Slack messages. 12 tabs open. And it's only 9am.
Meet Notion — the one place to think, plan, and get things done. Try free today."

Your task is to rewrite the FlowDesk copy into 3 distinct, high-converting variations.
Each variation MUST use a different proven copywriting framework:

Variation 1 — "The Micro-Story": Open with a 1–2 sentence scenario that depicts a
specific, painful moment in the target user's workday (before FlowDesk). Then
introduce FlowDesk as the resolution. End with a single-line CTA.

Variation 2 — "The Contrarian": Challenge a popular productivity belief (e.g. the
myth of multitasking, hustle culture). Position FlowDesk as the smarter, calmer
alternative to grinding harder. Avoid clichés.

Variation 3 — "The Stat Hook": Lead with one surprising, verifiable-sounding
statistic about wasted time or cognitive overload. Follow with the FlowDesk solution
in 2 sentences. End with CTA.

Rules for all 3 variations:
- Focus on user outcomes (what they GAIN), not product features (what it DOES).
- Maximum 75 words per variation.
- The CTA must create urgency without using the words "now" or "today".
- Do NOT use exclamation marks — confidence, not hype.
```

**Techniques Used and Reasoning:**

1. **Role Assignment with Credentialing:** Specifying "15 years of direct-response
   SaaS copywriting experience" doesn't just assign a role — it calibrates the model's
   domain prior to professional-level copywriting norms rather than general writing.
   The domain specification ("Facebook and Instagram direct-response") further narrows
   the relevant style register the model should draw from.

2. **Few-Shot Example:** Providing the Notion ad as a real-world high-performer gives
   the model a concrete quality benchmark to calibrate against. Rather than interpreting
   "creative" abstractly, the model can extract the structural pattern (specificity →
   relatable chaos → simple solution → free trial hook) and apply it analogically to
   FlowDesk. This is far more reliable than adjective-based quality instructions like
   "make it punchy."

3. **Named Framework Structuring:** Assigning distinct, named frameworks (Micro-Story,
   Contrarian, Stat Hook) to each variation prevents the model from producing three
   slightly different versions of the same approach. Named frameworks also make it
   easy for the recipient to discuss, select, and brief further iterations using a
   shared vocabulary.

4. **Negative Constraints:** Explicitly banning exclamation marks, the words "now/today,"
   and clichés via negative instruction removes the model's default fallback patterns.
   LLMs reliably over-index on high-frequency training patterns (exclamation marks,
   "Get started today!") without explicit prohibition. Negative constraints are often
   more impactful than positive ones.

5. **Grounded Input Data:** Including the actual current underperforming copy as a
   delimited block (using `--- CURRENT COPY ---` markers) gives the model a
   transformation target rather than generating from scratch. This also eliminates
   hallucinated product features, because the output must remain consistent with the
   provided input.

---

**Before/After Comparison — Actual AI Outputs:**

**BEFORE** (output from weak prompt — "Make our ad copy more creative"):

> "Boost your productivity like never before! 🚀 FlowDesk is the ultimate tool for
> managing your tasks, crushing your goals, and making every second count. Our
> all-in-one platform lets you do more, stress less, and work smarter. Join thousands
> of happy users — start your free trial today!"

_Assessment: The model defaulted to hype-mode copywriting — exclamation marks, a
rocket emoji, vague superlatives ("ultimate," "like never before"), and a generic
social proof claim ("thousands of happy users") with no actual number. The copy is
interchangeable with any productivity app from the last 10 years. Zero specificity,
zero differentiation, zero reason to click._

**AFTER** (output from rewritten prompt — Variation 1, The Micro-Story):

> "It's 8:47am. You've already missed two tasks you swore you'd finish yesterday,
> and you haven't opened your actual work yet.
>
> FlowDesk connects your tasks, calendar, and time — so the day you planned is the
> day you live.
>
> Free for 14 days. No card required. Start Monday differently."

_Assessment: The chain opens with a cinematic, specific moment (8:47am) that any
knowledge worker recognises viscerally. The resolution is stated as a direct outcome
("the day you planned is the day you live") not a feature list. The CTA creates
urgency through a time anchor ("Start Monday differently") without using "now" or
"today" as explicitly prohibited. Exclamation-free throughout._

**AFTER** (Variation 2 — The Contrarian):

> "Hustle culture sold you the idea that working more fixes everything.
> It doesn't. It just makes you faster at being overwhelmed.
>
> FlowDesk is built for people who want to work less hours and finish more things.
> Not a task list. A Tuesday you're actually proud of.
>
> Try it free — 14 days, cancel whenever."

_Assessment: The contrarian angle creates genuine pattern interruption — it argues
against a belief the audience likely already holds and positions the product as the
smarter, calmer alternative. The line "A Tuesday you're actually proud of" is
concrete and emotionally resonant without being sentimental._

---

## Prompt 3: Summarize Campaign Brief

**Original Weak Version:**

```
Summarize this campaign brief.
```

**Rewritten Version:**

```text
You are a Strategic Account Director at a full-service advertising agency. Your job
is to synthesize incoming client campaign briefs into concise, decision-ready
executive summaries for two specific audiences: the Creative Director and the
Head of Media Buying.

Before writing the summary, think through the following in one sentence each:
- What is the single most important strategic insight buried in this brief?
- What is the most significant risk or ambiguity the creative team needs to know?
- What channel decision does the media buyer need to make first?

Then produce a structured Executive Summary using exactly these sections and headers.
Do not add, remove, or rename sections. Do not include information not present in
the brief — flag missing information as "[NOT SPECIFIED IN BRIEF]" instead.

## Executive Summary

**Campaign Objective:** [1–2 sentences. State what success looks like, not what
the campaign will do.]

**Target Audience:** [3–5 bullet points. Demographics first, psychographics second.
Include one behavioural insight if present in the brief.]

**Core Message / Value Proposition:** [1 sentence. The single idea the consumer
must walk away believing.]

**Key Deliverables & Channels:** [Bullet list. Format each as: Channel → Asset type
→ Specification/format if provided.]

**Constraints & Exclusions:** [Bullet list. Brand safety rules, mandatory avoids,
legal restrictions, and budget ceiling.]

**Open Questions / Risks:** [Bullet list. Flag anything ambiguous, missing, or that
requires client clarification before briefing the creative team.]

<campaign_brief>
[Insert brief text here]
</campaign_brief>
```

**Techniques Used and Reasoning:**

1. **Role Assignment with Dual Audience Awareness:** Specifying that the output is
   designed for both the Creative Director and the Head of Media Buying forces the
   model to include two distinct information categories — creative direction details
   and channel/format specifications — that a generic summarizer would likely omit.
   Without this dual-audience framing, the model defaults to a single summary voice
   that satisfies neither reader optimally.

2. **Chain-of-Thought Pre-Analysis:** The three pre-summary thinking questions act
   as a strategic lens the model applies before producing output. Asking "What is
   the single most important insight buried in this brief?" forces the model to
   prioritise rather than simply compress — the key failure mode of standard
   summarization. This step reliably surfaces nuance that summary-only prompts miss.

3. **Rigid Template Binding with Named Sections:** Providing exact Markdown section
   headers, strict formatting rules (e.g., "Channel → Asset type → Specification"),
   and explicit paragraph length limits converts an open-ended task into a structured
   data extraction problem. This eliminates the model's most common summarization
   failure: producing flowing paragraphs that are readable but not scannable or
   decision-actionable.

4. **Hallucination Prevention via Negative Instruction + Fallback Pattern:**
   "Do not include information not present in the brief — flag missing information
   as '[NOT SPECIFIED IN BRIEF]'" is a two-part hallucination guard. The prohibition
   prevents fabrication; the fallback pattern gives the model a structured way to
   handle gaps without defaulting to making things up or omitting the field entirely.
   This is critical when the output will be acted upon by a team without access to
   the original brief.

5. **XML Data Fencing:** Wrapping the input data in `<campaign_brief>` tags creates
   an unambiguous boundary between instructions and data. Without this delimiter,
   models can misinterpret brief content as additional instructions (particularly
   if the brief contains imperative language like "the campaign must..." or "ensure
   that..."). XML fencing is the most reliable method for separating instruction
   context from data context in long-prompt scenarios.

---

**Before/After Comparison — Actual AI Outputs:**

For this comparison, the same example campaign brief was passed to both prompts:

> _"Q3 campaign for NovaSkin SPF moisturiser. Target women 28–45. Launch on TikTok
> and Instagram. Budget £180k. Key message: daily sun protection that doesn't feel
> like sunscreen. Deliverables: 3 x 15s TikTok videos, 6 x static Instagram posts,
> influencer brief for 10 micro-creators. Brand rule: never use clinical imagery."_

**BEFORE** (output from weak prompt — "Summarize this campaign brief"):

> "The campaign is for NovaSkin's SPF moisturiser, launching in Q3. It targets women
> aged 28–45 on TikTok and Instagram. The budget is £180k. The key message is that
> the product offers daily sun protection without feeling like sunscreen. The
> deliverables include TikTok videos, Instagram posts, and an influencer brief.
> Clinical imagery should be avoided."

_Assessment: This is competent compression but useless as a working document. Every
sentence is a restatement of the brief in slightly fewer words. There is no strategic
insight, no prioritisation, no flagging of ambiguities (e.g. what counts as "clinical
imagery"?), no channel-specific formatting, and no indication of which deliverable
the team should tackle first. A Creative Director receiving this summary has learned
nothing they could not have learned by reading the brief themselves._

**AFTER** (output from rewritten prompt):

> _Pre-analysis:_
> _Key strategic insight: The core tension is sensory — this product must be sold on
> how it feels, not what it does, which is unusual for an SPF category._
> _Primary creative risk: "Never use clinical imagery" is undefined — needs client
> clarification before the creative team invests in visual direction._
> _First media decision: TikTok content must be produced first; 15s format requires
> creator briefs to be locked before studio booking._
>
> **Campaign Objective:** Launch NovaSkin SPF Moisturiser in Q3 by owning the
> "invisible SPF" positioning across TikTok and Instagram — making daily sun
> protection feel like skincare, not safety gear.
>
> **Target Audience:**
>
> - Women, 28–45
> - Skincare-involved; likely already using a moisturiser step in AM routine
> - May have avoided SPF products due to texture, white-cast, or heavy feel
> - Behaviour: Influenced by skincare creators; responds to sensory, texture-led content
>
> **Core Message / Value Proposition:** Sun protection that disappears into your skin.
>
> **Key Deliverables & Channels:**
>
> - TikTok → 3 × 15-second videos → creator-led, sensory/texture focus
> - Instagram → 6 × static posts → [NOT SPECIFIED IN BRIEF: aspect ratio and copy
>   > length not provided]
> - Influencer → Brief for 10 micro-creators → [NOT SPECIFIED IN BRIEF: follower
>   > range, niche requirements, and exclusivity period not stated]
>
> **Constraints & Exclusions:** No clinical imagery. [AMBIGUOUS: definition of
> > "clinical" requires client clarification — does this include lab settings, skin
> > close-ups, dermatologist references, or all of the above?]
>
> **Open Questions / Risks:**
>
> - "Clinical imagery" policy must be defined in writing before creative briefing.
> - Budget split across TikTok production, Instagram design, and influencer fees not
>   provided — media buyer cannot allocate without guidance.
> - No mention of a campaign hashtag or brand handle to be featured in creator briefs.

_Assessment: The chain-of-thought pre-analysis surfaced the sensory positioning
insight and the imagery ambiguity before any section was written — both of which
are invisible in a straight compression. The "[NOT SPECIFIED]" and "[AMBIGUOUS]"
flags convert the summary from a passive document into an active checklist of
blocking questions. A Creative Director and Media Buyer can now act on this without
reading the original brief._
