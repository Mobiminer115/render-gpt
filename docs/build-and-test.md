# Build and Test Plan

## What is needed for a real iOS build

- macOS runner with a supported Xcode version.
- The actual Amethyst source tree and pinned dependency revisions.
- The project's existing iOS build instructions and signing setup.
- Any required Java/LWJGL native libraries built for supported iOS architectures.
- A provisioning profile for device installation, where applicable.

This repository is currently a scaffold and has no Xcode project or Amethyst dependencies, so CI cannot produce a usable IPA yet.

## Validation stages

### Static/repository checks
- Validate JSON configuration files.
- Check documentation links and required project files.
- Keep CI independent of code signing.

### Simulator checks
Useful for launch lifecycle and some integration tests, but not sufficient to validate GPU driver behavior, performance, or thermal behavior.

### Physical-device matrix
At minimum:
- iPhone 6s Plus: compatibility floor; test low-memory and sustained-load behavior.
- One intermediate device generation.
- A recent iPhone generation.

Record exact device identifier, iOS version, GPU family, Minecraft version, Java runtime, backend revision, mod loader, and test result.

## Graphics correctness suite

- Context creation, resize, suspend/resume.
- Texture upload, filtering, wrap modes, mipmaps, and format conversion.
- Framebuffer attachment and completeness checks.
- Depth, stencil, blend, culling, scissor, and viewport.
- Shader compile/link diagnostics and precision-sensitive tests.
- Resource cleanup and repeated world load/unload.

## Game/mod matrix

Begin with vanilla 1.8.9, 1.12.2, and 1.16.5. Then add representative Fabric and Forge packs. Treat OptiFine as a separate compatibility target; do not infer support from vanilla success.

## Performance measurements

Measure frame-time percentiles, not only average FPS. Record memory high-water marks, crash rate, load time, thermal state, and visual correctness. Compare at fixed scene, render distance, display scale, and device state.

A target such as 30 FPS on iPhone 6s Plus is a test objective, not a guarantee. Stability and correctness take priority over a single FPS number.
