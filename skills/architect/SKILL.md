---
name: architect
description: "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
disable-model-invocation: true
---

# Architect

Design before implementing. Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Sketch at least two shapes, pick one, then fill in code against it. If implementation proves the sketch wrong, throw it out and redesign.

## Start

Open a todolist with one entry per phase before starting.

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Run the **how** skill over the relevant subsystems, unless it already ran on them in this task.

Naming a file isn't grounding. Produce the traced model `how` prescribes. If the design redefines ownership or layering, also run the **why** skill on the existing shape so the rationale becomes a constraint, not a guess.

Skip Phase A only when the work is genuinely greenfield with no surrounding system to integrate.

## Phase B: Sketch

Sketch it yourself. Write the caller's usage first (the README a consumer reads and two or three real call sites), then derive the types and signatures from it. The usage is the spec, so when the two disagree, change the sketch.

Design it twice. Sketch at least two structurally different shapes, even when the first looks sufficient. Whole-shape alternatives, not point fixes inside one shape.

Hold each shape to this discipline:

- Data structures first. Trace each main access pattern through the structure. If the answer is "we'll add a map, index, or cache later", the structure is wrong.
- Keep transport and wire types off the public API. Parse into domain types behind the interface.
- If two actors might write the same state, default to per-actor state merged at the read boundary, per the **separate-before-serializing-shared-state** principle skill.
- Make boundaries visible. Use `not implemented` bodies, `// TODO` pseudocode for tricky logic, and doc comments for intent and invariants. A reader should trace data from input to output through types and signatures alone.
- Encode invariants in types first, runtime checks second, and comments last.
- Validate at boundaries and trust types inside, per the **boundary-discipline** principle skill. Keep business logic in pure functions and the shell thin.
- Keep one source of truth per invariant. Derive instead of syncing.
- Ask what happens if an operation runs twice or crashes halfway, per the **make-operations-idempotent** principle skill.
- If tracing the flow takes more than three files, flatten it.

Screen every shape against [`references/design-red-flags.md`](references/design-red-flags.md). Reject or revise shallow modules, information leakage, temporal decomposition, and pass-through methods.

Compare the viable shapes on interface depth. Prefer the one that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers. Write the chosen shape's rationale per `references/rationale-template.md`.

Run the **arena** skill for this phase only when the user asks for it ("architect with arena", "arena the design"). Each runner then gets `references/runner-prompt.md` and the Phase A grounding, and arena's synthesis decision fills the rationale's "Synthesis decision" section.

## Phase C: Agree (opt-in)

Default: proceed directly to implementation with the chosen design. No human checkpoint.

Opt in to a checkpoint when the invoker explicitly asks: "/architect with checkpoint," "stop and show me before implementing," or similar. Then surface the design and pause for sign-off.

The sketch can ship as its own commit either way, as the "scaffold first" mode of the **foundational-thinking** principle skill. Planned and scoped breakage during fill-in is fine, per the **outcome-oriented-execution** principle skill. For adversarial pressure on the design before implementing, run the **interrogate** skill on the sketch.

If the human pushes back on the shape (in a checkpoint or after the fact), treat that as Phase A evidence. Re-ground and re-run Phase B before writing more code.

## Phase D: Implement against the sketch

Replace `not implemented` bodies with code, pseudocode with logic. The chosen sketch is the contract.

Deviations from the sketch are signal worth surfacing, not friction to absorb silently. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, throw the sketch out. Don't bolt fixes onto a wrong design, per the **redesign-from-first-principles** and **fix-root-causes** principle skills.

The signal is a *pattern*, not single instances. Tells:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases that all need special-case branches.
- Types that need escape hatches (`any`, casts, optional fields always set in practice) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape across the implementation.

Use judgment. A few edge cases don't condemn an architecture. Some problems are legitimately complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Re-run the **how** skill over what's been built.
2. Redesign as if the new constraints had been day-one assumptions, per redesign-from-first-principles.
3. Subtract before adding, per the **subtract-before-you-add** principle skill. The new sketch should be smaller than the old one before it grows.
4. Return to Phase B.

## Outputs

The caller's usage is written first and the type sketch derived from it. One file with new types and signatures for small changes. Module map plus type definitions for larger work. The rationale ships alongside, shaped per `references/rationale-template.md`, including the usage sketch, and the synthesis decision when arena ran.
