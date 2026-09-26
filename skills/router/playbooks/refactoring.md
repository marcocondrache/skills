### Refactoring

**You own the contract. The structure changes. The behavior does not.** Distinct from Feature, which adds behavior, and Bug fix, which corrects it.

If the cleanup reveals a missing feature or a real bug, split it out and ship the structural change first against the pinned contract. A redesign is allowed, but name it and route to Feature.

1. Pin the behavior contract first. Run the **how** skill over the affected subsystem to learn the contract, then write a characterization test, snapshot, or equivalence harness that captures current behavior before any structure moves. If the area has no coverage, write the pin before touching structure. Type check and lint are not a pin.
2. Name the structure the code is missing. Boring code stays when the shape is already clear and local. The reshape must delete branches or invalid states, not add indirection.
3. Name the target shape. State what the module layout, types, and call graph should be if built today. If the target adds a module or changes a public API, run the **architect** skill to sketch the shape before the move.
4. Subtract before you add. Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before introducing the new shape. The smallest change that reaches the target shape ships. A speculative cleanup that "might help" gets reverted.
5. Move in small behavior-preserving steps, each keeping the pin green. For API reshapes, migrate every caller and delete the old API in the same wave. No compatibility shims, no parallel old-and-new paths. Spot-check every rename against the actual files. Renames silently miss usages in strings, prose, and back-references. When the mechanical edits are many, hand them to a subagent on a fast model with a specific scope (file paths, the names being moved, the behavior to hold).
6. Prove behavior is unchanged on the real artifact, not "it compiles". For larger reshapes, run an equivalence check: a script that diffs old-vs-new outputs, a recorded baseline replayed against the new code, or a smoke run on the matching surface via the project's verification skill.
7. Confirm the change is worth keeping. The success measure is reduced reader load. If the diff does not lower reader load somewhere, revert it.
8. Rebase into small ordered commits. A subtraction commit, then the reshape, then any follow-on cleanup. Keep each behavior-preserving slice green before the next. Run **Opening a PR**.

**Reply:** the structure that changed, the pin you held it against, the equivalence proof, the reader-load delta, what shipped and what got reverted. No new behavior.
