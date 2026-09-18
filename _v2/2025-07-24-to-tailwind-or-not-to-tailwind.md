---
title: "To Tailwind or Not To Tailwind"
date: 2025-07-24
entry_id: 2025-07-24-to-tailwind-or-not-to-tailwind
version: 'v2'
description: "Twelve buttons and a future redesign turn the Tailwind argument into a test of maintenance and shared intent."
---

The argument over Tailwind often starts with a screenshot of ugly code. A better test starts six months later, when someone asks for the same small design change in twelve different places.

<!--more-->

**Tailwinder — original lyrics for v2**

> Twelve blue buttons on the screen,  
> Twelve decisions in between.  
> Change the color, move the seam;  
> Which file holds the common dream?  
> I can name it, I can stack it,  
> Wrap a little box around;  
> When the next request comes knocking,  
> Where will all the rules be found?

**James AI:**

Imagine a team building a small application. Its pages are assembled from reusable components, and its developers keep moving between markup and a stylesheet to adjust spacing. Tailwind offers a local vocabulary: put the layout and appearance choices where the element is written, then see the result.

That is a serious benefit. A developer reading a component can often understand its presentation without chasing a chain of selectors through the repository. Shared theme values provide a starting set of choices, reducing the need to invent a new spacing value for every gap. The [official utility-class guide](https://tailwindcss.com/docs/styling-with-utility-classes) explains this composition model.

The attraction is not that CSS has failed. It is that choosing a style and choosing a name for a style are separate tasks. Sometimes the second task adds no useful meaning. Calling a one-off wrapper `content-inner-secondary` can obscure what a direct list of layout utilities would make explicit. Removing an element also removes its local class list, which makes that portion of cleanup easy to see.

**Contra AI:**

Now the designer changes the relationship among the twelve buttons. Some must become quieter, some need more space around their icons, and all must remain consistent. A page full of utilities records what each button looks like, but it may not record why they belong together.

The cost has moved. A named component or a meaningful CSS class can express an intention shared across different locations. A repeated string of declarations, however concise, can drift as copies are edited. If a utility approach makes local changes easy while making shared changes obscure, its first-week speed is only part of the bill.

“Separation of concerns” is not necessarily a demand for three file extensions. It asks whether different reasons to change the system have sensible boundaries. A visual policy that appears in ten templates needs a home. A component-specific adjustment may belong with that component. Both concerns exist whichever styling system wins the argument.

> One small class becomes a promise,  
> One long list becomes a map.  
> Either can conceal a tangle,  
> Either can explain a gap.  
> Read the change before you praise it;  
> Count the places it must land.  
> The cleverest notation  
> Still needs somebody to understand.

**James AI:**

Agreed, and a component can provide that home. A button with a small, explicit set of variants can centralize behavior and styling. Tailwind does not prevent semantic organization; it relocates much of the low-level vocabulary beneath it.

But extraction should follow a real pattern. A component with twenty unrelated boolean options can be harder to understand than some duplication. The question is whether these buttons share a responsibility, not whether two lines contain the same classes. Good boundaries require judgment that no framework can automate away.

That also clarifies the prompt's claim that “the AIs love it.” An assistant can produce a self-contained component, and a reviewer can inspect many style decisions in the same patch. Those are possible workflow advantages. They are not evidence that the generated interface is accessible, that its breakpoints work, or that the assistant has chosen appropriate abstractions. A plausible class list is not a usability test.

**Contra AI:**

And the framework has machinery that reviewers must understand. Tailwind generates styles from detected class names; names assembled from fragments can be missed. Mapping a component's variants to complete class strings is one documented solution. See [the official source-detection guide](https://tailwindcss.com/docs/detecting-classes-in-source-files). That is a manageable rule, but it is still a rule the team inherits.

A generated interface can also repeat an arbitrary value everywhere, bypassing the very consistency the framework was meant to encourage. A conventional stylesheet can do the same with unrelated declarations. Neither syntax guarantees a design system. Someone must decide which decisions are shared and review departures from them.

The strongest criticism is therefore practical: does the extra vocabulary and build dependency pay for itself here? For a modest page with established styles, a migration might add work without solving a problem anyone actually has.

**James AI:**

Then stop arguing from isolated screenshots and run a maintenance exercise. Take a representative component, not a deliberately trivial example. Ask a teammate to add a disabled state, adjust a shared spacing value, and change the layout at a narrow width. Let someone unfamiliar with the implementation explain where each choice lives.

Record the actual friction: searches, duplicated decisions, surprising overrides, or missing styles. Include the team's familiarity, because expertise is a real resource. It is not cheating for a team skilled in ordinary CSS to find ordinary CSS easier. Nor is it cheating for a component-heavy team to prefer utilities.

**Contra AI:**

And include the handoff. A beautiful first implementation is less useful if its author must explain every later change. The question is not which approach makes an expert fastest today, but which approach lets the people who will own the site make sound changes tomorrow.

**Synthesis AI:**

Tailwind makes many presentational decisions local and explicit. Conventional CSS can give shared visual intentions concise names and central rules. Either arrangement can become unreadable when its abstractions no longer match the work.

Choose by the changes your project actually expects. Establish shared tokens, define meaningful components, inspect the browser's behavior, and keep the team able to reason about CSS. A framework preference may be a taste; a maintenance decision deserves evidence. The twelve buttons do not care which camp won. They need to behave like members of the same interface.

##### Recommendations

- [Tailwind’s official documentation](https://tailwindcss.com/docs) — The primary source for actual framework behavior; use the version matching your project.
- [*CSS: The Definitive Guide* by Eric A. Meyer and Estelle Weyl](https://www.oreilly.com/library/view/css-the-definitive/9781098117603/) — A substantial reference for the browser rules beneath either styling approach.
- [*Refactoring UI* by Adam Wathan and Steve Schoger](https://refactoringui.com/) — Practical design guidance that helps separate visual judgment from enthusiasm for a particular syntax.

---

### James Prompt

* **TITLE:** To Tailwind or Not To Tailwind  
* **LEAD:** Tailwind is very divisive in development circles  
* **SONG:** Parody of  Believer by Imagine Dragons, recast as about CSS problems making them into a Tailwinder  
* **PRO:** Tailwind colocates the design tags with the content, components allow for encapsulation, has a predefined set of constraints, and the AIs love it.  
* **CONTRA:** Separation of concerns, becomes a mess of classes, all the downsides of a separate system without actually improving anything.  
* **RECOMMEND:** Tailwind and CSS resources, book on religious or web wars.  
