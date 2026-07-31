# `matmul` Algorithm — Flowchart

This flowchart visualises the control flow of the pure-Python
`matmul(mat1, mat2)` function in [`src/matmul.py`](../src/matmul.py):
input validation followed by three nested `for` loops (`i`, `j`, `k`)
accumulating the dot product.

```mermaid
flowchart TD
    Start(["Start: matmul(A, B)"])
    Validate["Validate mat1, mat2\n(shape, type)"]
    CheckDim{"cols(A) == rows(B) ?"}
    RaiseErr["raise ValueError"]
    GetDims["m,n = dims(A); p = cols(B)"]
    InitC["C = zero matrix (m × p)"]
    LoopI["Outer loop: i = 0 to m-1"]
    LoopJ["Middle loop: j = 0 to p-1"]
    InitS["sum = 0"]
    LoopK["Inner loop: k = 0 to n-1"]
    DotProd["sum += A[i][k] × B[k][j]"]
    CheckK{k &lt; n-1 ?}
    StoreS["C[i][j] = sum"]
    CheckJ{j &lt; p-1 ?}
    CheckI{i &lt; m-1 ?}
    ReturnC["Return C"]
    End([End])

    Start --> Validate
    Validate --> CheckDim
    CheckDim -- No --> RaiseErr --> End
    CheckDim -- Yes --> GetDims
    GetDims --> InitC
    InitC --> LoopI
    LoopI --> LoopJ
    LoopJ --> InitS
    InitS --> LoopK
    LoopK --> DotProd
    DotProd --> CheckK
    CheckK -- Yes --> LoopK
    CheckK -- No --> StoreS
    StoreS --> CheckJ
    CheckJ -- Yes --> LoopJ
    CheckJ -- No --> CheckI
    CheckI -- Yes --> LoopI
    CheckI -- No --> ReturnC
    ReturnC --> End
```

**Reading the chart:**
- Rounded nodes = start/end
- Rectangles = processing steps / assignments
- Diamonds = decision points (`Yes`/`No` branches explicitly labelled)
- Each `for` loop checks the termination condition **after** executing its
  body (`k < n-1?`, `j < p-1?`, `i < m-1?`), with the loop variable
  increment implied in the return edge back to the loop header.
