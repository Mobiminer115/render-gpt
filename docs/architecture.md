# Renderer Architecture

## 1. Integration principle

Do not start by writing a GPU driver. The renderer must integrate with the graphics and window/context abstractions already used by the Amethyst fork. First inspect the upstream launcher, its current OpenGL translation layer, context creation, framebuffer handling, and input/surface lifecycle.

The repository currently contains no Amethyst source. This document is an integration contract, not a claim that those hooks already exist.

## 2. Proposed layers

1. **Launcher adapter** — passes device capabilities, display size, app lifecycle events, and renderer preferences.
2. **Graphics backend** — translates the OpenGL calls expected by the selected Minecraft/LWJGL stack to the supported iOS graphics API.
3. **Capability registry** — reports extensions, limits, framebuffer formats, texture limits, and feature workarounds.
4. **Adaptive policy** — changes render scale and non-semantic quality settings only when performance or thermal signals justify it.
5. **Diagnostics** — records backend, GPU family, OS version, Java/game version, mod list hash, GL errors, and crash context without collecting personal data.

## 3. Backend selection

The first milestone should validate an OpenGL ES compatibility backend against the exact APIs required by the existing Amethyst runtime. Evaluate GL4ES or the project's existing translation layer only after inspecting license, maintenance state, supported GL calls, and integration cost.

A Metal-backed path (for example, via a maintained OpenGL-to-Metal translation implementation) is a later experiment, not an assumed drop-in fallback. Two backends can increase bugs and maintenance cost; add a second only when a concrete compatibility or performance gap is demonstrated.

## 4. Compatibility rules

- Preserve OpenGL state semantics: bindings, active texture, blend/depth/stencil state, viewport/scissor, draw buffers, and framebuffer completeness.
- Detect unsupported features and expose conservative capabilities rather than advertising extensions that are not implemented.
- Never silently claim shader support when GLSL translation or precision behavior differs.
- Keep texture formats, mipmaps, vertex layouts, and framebuffer attachments under automated tests.
- Preserve mod-visible APIs wherever possible. Mods may depend on exact GL behavior, not just the vanilla renderer.

## 5. Adaptive performance policy

Tune only reversible quality controls:
- Render scale, with conservative minimum and maximum bounds.
- View distance/chunk upload budget.
- Mipmap and anisotropic filtering levels when available.
- Frame pacing and background-work budgets.
- Texture/cache memory budgets.

Do not dynamically unload arbitrary mod classes or change game logic. Avoid frequent oscillation: apply hysteresis and cooldowns to quality changes.

## 6. Memory and stability

- Track Java heap separately from native and GPU allocations.
- Use bounded caches and explicit lifecycle cleanup.
- Handle suspend/resume and memory warnings.
- Keep a rolling diagnostic log with privacy-safe metadata.
- On backend failure, show a clear error and preserve logs. Runtime fallback is allowed only if contexts/resources can be recreated safely.

## 7. Milestones

1. **Reconnaissance:** pin Amethyst revision, identify current GL/LWJGL path and minimum iOS deployment target.
2. **Contract:** implement capability and backend interfaces with a no-op/mock test backend.
3. **Vanilla baseline:** render a test scene, then Minecraft vanilla 1.8.9, 1.12.2, and 1.16.5.
4. **Correctness:** framebuffer, texture, shader, blending, depth, stencil, and resize/suspend tests.
5. **Mods:** test representative Fabric and Forge setups separately; document unsupported mods and OptiFine status.
6. **Optimization:** profile CPU, GPU, memory, frame pacing, and thermal behavior on physical devices.
7. **Release:** publish only after reproducible builds and a public compatibility matrix.
