# Project Context: [Mojo Project Name]

## 🚀 Vision & Ideas
**The "Why":** [e.g., Building a high-performance LLM inference engine / Custom SIMD-accelerated data processing library.]
**Core Concept:** [Describe the central idea. e.g., A library that bridges Python's ease of use with C++ levels of performance for tensor manipulation.]

---

## 🛠 Tech Stack
* **Language:** Mojo (Latest stable version)
* **Environment:** [e.g., Modular MAX SDK, Magic CLI]
* **Interoperability:** [e.g., Python 3.11 for matplotlib/numpy integration]
* **Hardware Target:** [e.g., AVX-512 (CPU), NVIDIA/CUDA (GPU), or Apple Silicon]
* **Package Management:** `magic` (Modular's package manager)

---

## 🏗 Project Architecture & Roadmap
### Phase 1: Foundation (Current)
* [ ] Set up `magic` environment and project structure.
* [ ] Define core `struct` types and basic traits.
* [ ] Benchmarking baseline against pure Python equivalents.

### Phase 2: Optimization
* [ ] Implement SIMD vectorization for critical loops.
* [ ] Introduce multi-threading using `parallelize`.
* [ ] Memory management tuning (Ownership & Borrowing optimization).

### Phase 3: Scaling & Integration
* [ ] Python bindings for easy distribution.
* [ ] Integration with [Target Platform, e.g., PyTorch, HuggingFace].
* [ ] Distributed computing support.

---

## 📖 Onboarding for Contributors (and AI)
### 1. Environment Setup
1.  Install the Modular CLI: `curl -ssL https://magic.modular.com | bash`
2.  Initialize project: `magic shell`
3.  VS Code Extension: Ensure the **Mojo** extension by Modular is installed.

### 2. Coding Standards
* **Explicit over Implicit:** Use `fn` instead of `def` for type-safe, compiled functions.
* **Performance First:** Prefer `SIMD` types for math-heavy operations.
* **Memory:** Use `borrowed`, `inout`, and `owned` argument decorators strictly to avoid unnecessary copies.
* **Types:** Always use strict typing for struct fields and function signatures.

---

## ⚡ Key Commands
* **Run Project:** `mojo main.mojo`
* **Build Executable:** `mojo build main.mojo`
* **Format Code:** `mojo format .`
* **Update Toolchain:** `magic update`

---

## 🔮 Future Plans & Research
* **Research Area:** [e.g., Investigating Mojo's `autotune` capabilities for different CPU architectures.]
* **Feature Expansion:** [e.g., Adding support for Quantized 4-bit tensor operations.]
* **Community:** [e.g., Planning to open-source as a Modular Community package.]

---

## 🧪 Knowledge & Constraints
* **Note:** Mojo is evolving rapidly. Always check the latest [Mojo Changelog](https://docs.modular.com/mojo/changelog) if syntax errors occur in standard libraries.
* **Interop:** When calling Python, remember that objects are dynamically typed and will incur a performance penalty compared to native Mojo types.