Algorithm audit fixes (2026-11-06)

Run from the repository root:
  make test
  make test-compiles
  python3 tests/run.py factorization hpi dinic_complexity

Requirements: Python 3, GCC with C++20, bits/stdc++.h and UBSan.
CXX may name a compiler executable (e.g. CXX=g++-15).
On macOS the runner locates the SDK using xcrun; the deployment target is 15.0.
Sources and binaries are created in a temporary directory, whose path is printed.
Every selected scenario must compile and satisfy its oracle; failure returns a
nonzero exit status. The compiler enables libstdc++ bounds checks and UBSan traps.
NDEBUG scenarios additionally check behavior without assertions.

75 scenarios: 10 snippet compilation checks and 65 executable checks. Most
executable checks contain hundreds or thousands of deterministic test cases.
The original 48 verification files have a separate compilation-only check;
this does not run external online-judge datasets.

cases.py preserves the original audit counterexamples and differential tests.
regressions.py gives the probes explicit expected outputs, replaces exploratory
seed searches with concrete examples and adds independent comparisons for the
changed implementations. Counter-only copies of Dinic and MCMF enforce linear
edge-scan bounds on the three-vertex regression graphs. The NTT capacity test
reduces MAXLOG from 23 to 3; production arrays of length 2^22 are not allocated.

Audit finding coverage:
  F01-F03  Closest pair, signed FFT rounding, Pollard rho restarts + primality.
  F04-F05  Allocation and HPI calculations execute with NDEBUG as well.
  F06-F07  Dinic blocking flow and fresh adjacency on repeated flow init.
  F08-F10  Zero recurrence numerators, zero-based Eertree access, equal-suffix LCP.
  F11-F15  Strict point ordering, polygon boundary cases, nested DCEL components.
  F16-F19  MCMF queue deduplication, wide CRT, primality, min-cut initial bound.
  F20-F22  NTT capacity, 128-bit NDHull orientation, aligned bounded allocation.
  F23-F27  Complete snippets and consistent geometry interfaces.
  F28-F30  Empty strings, EOF handling and the vector-input macro.

Additional checks caught and cover the sparse-table last-column boundary and
convex polygons whose first vertex lies in the middle of a straight edge.
The half-plane feasibility routine retains a local geometric tolerance when
comparing interval endpoints; it no longer depends on Point's container order.

Interface and range notes:
- trisle(a, b, c, f) now takes its right-hand side explicitly. This is Thomas
  elimination without pivoting; zero pivots throw domain_error.
- CRT uses ll directly. Positive moduli are required; residues are normalized.
  An incompatible system returns -1; an unrepresentable lcm throws overflow_error.
- Factorization.cpp includes PrimalityTest.cpp. It needs the usual ll alias and
  mt19937 rnd. n >= 1; factors are returned in arbitrary order.
- Point ordering is exact (y, x), without EPS. Floating geometric predicates
  still have finite-precision limitations. Delaunay uses the shared real point
  type; exact integer predicates require an integer-point specialization.
- isInConvex accepts distinct vertices of a CCW positive-area convex polygon,
  including collinear boundary vertices. Queries remain O(log n).
- buildDCEL merges disconnected outer boundaries in O((V+E) log(V+E)); edges
  of the embedding may intersect only at shared endpoints.
- NDHull::V/det return __int128. For DIM=4 the documented coordinate limit is
  |coordinate| <= 1e8. Change arithmetic/range bounds when changing DIM.
- The two arena allocator files are alternatives: include only one. They support
  C++17 aligned allocation, throw bad_alloc on exhaustion, do not free individual
  allocations, and are not thread-safe.
- readChar returns -1 on EOF; readInt throws on EOF before a token.
- NTT rejects unsupported sizes with length_error, including under NDEBUG.
- Flow values/costs must fit the types of the selected implementation; mincut
  uses ll weights and still destructively contracts its input matrix.

Passing these finite tests is not a proof of correctness for every input.
The pre-fix audit reports remain historical records of commit 3e7c551; this
suite is the validation entry point for the corrected implementations.
