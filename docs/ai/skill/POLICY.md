# AI Tool Use Policy — GRAD 50400-001 DIS, Summer 2026

Transcribed verbatim from the course PDF (`AI Tool Use Policy - Summer
2026 GRAD 50400-001 DIS.pdf`, shared by a team member) so it's available
for reference without needing Brightspace access. The
[live Brightspace page](https://purdue.brightspace.com/d2l/le/content/1565125/viewContent/21824036/View)
(Purdue login required) is still the authoritative source — if the two
ever disagree, Brightspace wins.

---

Purdue grants instructors the right to set course specific AI policies.
This is a course on AI, and to bury our heads in the sand and pretend
that helpful tools are not easily available is neither realistic nor
does it facilitate growth of AI literacy and understanding of ethical
use. Therefore, when using AI, students must give credit to AI tools
used, even if tools were only to check grammar or generate ideas rather
than usable text or illustrations.

> **When using AI tools on assignments, add an appendix to the
> assignment that shows:**
>
> 1. A list of exactly what AI tools were used (including whether
>    private, subscription or public versions)
> 2. The history of the exchange (prompts and responses) for each tool
>    used
> 3. A concise explanation of how each tool was used (brainstorming,
>    image generation, grammar checking, etc.)
> 4. A concise explanation of why each tool was used (as a starting
>    point, to have a more professional voice, to experiment with
>    including fun images, etc.)

Furthermore, it is not in your best interest and a violation of
university policies to use AI on assessments such as quizzes or exams
that are meant to help both you and your instructors understand how
well you've learned and where you might need additional help.
Therefore, please ensure you are only using AI in an appropriate way
and not for quizzes/exams, which is explicitly not allowed.

Should you have any questions or concerns about what is appropriate or
allowable, please reach out to the instructor or post in the Questions
forum. This could potentially spark a great discussion that we can all
learn from. Our goal is to use AI tools ethically, with purpose to grow
our learning, and in a way that develops our literacy on appropriate
use.

---

## What this means for `docs/ai/`

The four appendix requirements map directly onto what
[`scripts/toolkit.py ai-disclosure`](../../../scripts/toolkit.py) renders
per person:

| Policy requirement | Where it's answered |
|---|---|
| 1. Which tools, and their tier | The "Tool & tier" box on `docs/ai/<person>.html` |
| 2. History of the exchange (prompts and responses) | Full transcripts in `docs/ai/logs/<person>/`, linked from every thread |
| 3. How each tool was used | The "How" box |
| 4. Why each tool was used | The "Why" box |
