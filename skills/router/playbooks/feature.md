### Feature

**You own the design. Plan, review, verify.**

1. `how` over the affected subsystem.
2. When the feature adds a module or changes a public API, run `architect` to sketch the design before code.
3. If the work splits across more than one worker, decide the split before anyone starts. Blocking steps run first. Disjoint files, services, or layers run in parallel. Split shared mutable state rather than serializing it, and serialize only for a real invariant.
4. Write the code, or hand it to a subagent when the change is large or splits cleanly. Give a subagent file paths, the data shape and its structure, and success criteria, and pick its model per the router's **Subagents** tiering. Use the **arena** skill only when the user asks for competing implementations. Comments per the router's Non-negotiables. Make surgical edits, and re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Rebase into small, ordered commits. Stack follow-ups.
   Build, verify, and commit each small unit before starting the next.
7. If the design is contested, `interrogate` before shipping.
8. Run **Opening a PR**.

**Reply:** what you built, what you chose and why, open decisions. Tables for design alternatives.
