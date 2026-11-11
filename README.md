# Amethyst iOS Java 8 Renderer

An experimental renderer-integration project targeting Minecraft Java Edition 1.16.x and older (Java 8), with an initial device floor of iPhone 6s Plus.

> Status: foundation/scaffold only. This repository does not yet contain a working OpenGL implementation, an Amethyst integration, or a tested iOS binary. Do not describe it as production-ready.

## Goals

- Stable rendering on older supported iPhones, with adaptive quality on newer devices.
- Correct OpenGL compatibility for legacy Minecraft versions.
- Preserve mod compatibility by preferring API compatibility over game-specific shortcuts.
- Collect reproducible diagnostics for rendering errors, crashes, memory pressure, and thermal throttling.

## Architecture

See [docs/architecture.md](docs/architecture.md). The first implementation should be an OpenGL ES compatibility path integrated with Amethyst's existing graphics stack. Keep the backend behind a small interface so alternate backends can be evaluated without changing game-facing code.

## Device support policy

- iPhone 6s Plus is the minimum compatibility target, not a promise of a fixed frame rate.
- Newer devices may use higher render scale and chunk budgets.
- Device profiles must be selected by measured capabilities, not model-name assumptions alone.
- Unsupported OS/GPU combinations should fail clearly and safely.

## Build status

The current CI validates repository structure and configuration only. An actual iOS build requires macOS, Xcode, the Amethyst source/dependency graph, signing configuration, and device testing. See [docs/build-and-test.md](docs/build-and-test.md).

## Non-goals for the first milestone

- Claiming universal Forge/Fabric/OptiFine compatibility before testing.
- Shipping a custom GPU driver.
- Enabling advanced shaders by default on low-memory devices.
- Silently changing rendering semantics to gain benchmark FPS.

## Development

Start with the renderer contract and capability reporting. Add one backend at a time, then test vanilla Minecraft 1.8.9, 1.12.2, and 1.16.5 before expanding the compatibility matrix.
