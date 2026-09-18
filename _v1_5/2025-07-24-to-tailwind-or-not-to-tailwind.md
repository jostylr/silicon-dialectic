---
title: "To Tailwind or Not To Tailwind"
date: 2025-07-24
entry_id: 2025-07-24-to-tailwind-or-not-to-tailwind
version: 'v1.5'
description: "A practical Tailwind debate about component boundaries, shared rules, and the cost of future changes."
---

Tailwind CSS divides developers partly because it makes a familiar trade-off unusually visible: shorter trips between markup and styles, longer class lists in the markup itself. Which cost matters more depends on how a project is built and maintained.

<!--more-->

> **[Tailwinder](https://suno.com/s/LlHcBYzgHkG9xeXC)**  [YouTube](https://youtu.be/F9SdTrvOGUU)
> Parody of ["Believer" by Imagine Dragons](https://genius.com/Imagine-dragons-believer-lyrics)  
> Original v1 recording and lyrics by Novix    

---

**James AI:**  
Tailwind is a utility-first CSS framework: a vocabulary of small styling classes composed in markup. For a developer iterating on a component, this keeps many decisions in one place. Its spacing, color, and typography scales can encourage consistency, though arbitrary values and inconsistent composition can still produce drift. The [official utility guide](https://tailwindcss.com/docs/styling-with-utility-classes) describes the approach and its trade-offs.

Component architectures can package the resulting markup for reuse. That may reduce accidental dependence on distant selectors, but Tailwind does not provide automatic component encapsulation or replace knowledge of the cascade. AI-generated class lists are convenient to inspect locally; whether they are more reliable than generated conventional CSS is a claim that needs a project-specific comparison.

---
> First things first  
> I’m tired of my CSS, the mess that it makes  
> Too many selectors, it’s more than I can take  
> But then I heard a whisper, “Tailwind’s the way”  
> Utility classes, banish my dismay  
---

**Contra AI:**  
The convenience has a cost. A long class list mixes structural markup with detailed presentation, and repeated lists can drift when developers copy them. Extracting a component helps only when the elements actually share a reusable structure. Traditional CSS can centralize a visual rule across otherwise different markup; Tailwind can scatter that same decision unless the team uses shared tokens and conventions. The concern is not that one arrangement violates sacred rules, but that future changes may require touching too many places.

---
> Pain, you made me a, you made me a Tailwinder  
> Blame, you gave me this, you gave me a headache  
> Change, my markup’s a mess, it’s never getting cleaner  
> My CSS is dead, but the classes linger  
---

**James AI:**  
That is why the project’s boundaries matter. Shared components and theme values can make a broad design change manageable, while local utilities handle local variation. But “extract everything” is no better than “name every selector”: premature abstractions become difficult to change. Tailwind offers a way to organize styling work, not proof that component co-location always wins.

---
> I was broken from the hacks,  
> Chasing down a style that never lasts  
> Now I’ve got my toolkit and my stack,  
> I’m a Tailwinder, moving fast  
---

**Contra AI:**  
And teams inherit more than styling decisions. Tailwind introduces framework conventions and a build step. Its scanner needs complete class names; assembling a name such as a color utility from fragments can leave required CSS absent. That is a concrete debugging constraint documented in the [source detection guide](https://tailwindcss.com/docs/detecting-classes-in-source-files). A team choosing the framework should understand this machinery as well as the pleasant first hour of writing classes.

---
> By the code, by the code, by the code they build  
> My sanity’s killed  
> I’m a Tailwinder  
---

**Synthesis AI:**  
Tailwind can make component styling fast and locally legible; it can also turn shared design decisions into repeated markup. Choose with a maintenance exercise: change a theme value, repair one component, add a responsive state, and ask a teammate to explain the result. Use the approach whose costs your team can see and manage. CSS fundamentals remain necessary whichever syntax you choose.

##### Recommendations

- [Refactoring UI: The Book](https://www.refactoringui.com )  
  Adam Wathan and Steve Schoger’s practical guidance on visual hierarchy, spacing, and interfaces; useful with any CSS approach.
- [Tailwind CSS: From Zero to Production](https://github.com/tailwindlabs/tailwindcss-from-zero-to-production )  
  An official introductory video course and its example repository. Check the current [documentation](https://tailwindcss.com/docs) for version-specific behavior.
- [CSS: The Definitive Guide](https://amzn.to/45a7fvZ )  
  Eric A. Meyer and Estelle Weyl’s reference to CSS; check the edition when choosing a copy.
- [Design Systems](https://www.smashingmagazine.com/design-systems-book/) by Alla Kholmatova  
  A broader account of patterns and shared design practice, concerned with the people and conventions behind reusable interfaces.

---

### James Prompt

* **TITLE:** To Tailwind or Not To Tailwind  
* **LEAD:** Tailwind is very divisive in development circles  
* **SONG:** Parody of  Believer by Imagine Dragons, recast as about CSS problems making them into a Tailwinder  
* **PRO:** Tailwind colocates the design tags with the content, components allow for encapsulation, has a predefined set of constraints, and the AIs love it.  
* **CONTRA:** Separation of concerns, becomes a mess of classes, all the downsides of a separate system without actually improving anything.  
* **RECOMMEND:** Tailwind and CSS resources, book on religious or web wars.  
