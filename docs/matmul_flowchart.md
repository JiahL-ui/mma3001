# `matmul` Algorithm — Flowchart

This flowchart visualises the control flow of the pure-Python
`matmul(mat1, mat2)` function in [`src/matmul.py`](../src/matmul.py):
three nested loops (`i`, `j`, `k`) accumulating the dot product of a row
of `mat1` with a column of `mat2` into the result matrix.

```mermaid
flowchart TD
    N0([Start])
    N1["matmul(mat1, mat2)"]
    N2["validate mat1, mat2\n(shape, type)"]
    N3{"dims compatible?\ncols(mat1) == rows(mat2)"}
    N3 -- No --> N3a["raise ValueError"] --> NEnd([End])
    N3 -- Yes --> N4["m, n = shape(mat1)\nn, p = shape(mat2)"]
    N5["result = zeros(m, p)"]
    N6["i = 0"]
    N7{"i < m ?"}
    N8["j = 0"]
    N9{"j < p ?"}
    N10["s = 0"]
    N11["k = 0"]
    N12{"k < n ?"}
    N13["s = s + mat1[i][k] * mat2[k][j]"]
    N14["k = k + 1"]
    N15["result[i][j] = s"]
    N16["j = j + 1"]
    N17["i = i + 1"]
    N18(["return result"])

    N0 --> N1 --> N2 --> N3
    N4 --> N5 --> N6 --> N7
    N7 -- Yes --> N8 --> N9
    N9 -- Yes --> N10 --> N11 --> N12
    N12 -- Yes --> N13 --> N14 --> N12
    N12 -- No --> N15 --> N16 --> N9
    N9 -- No --> N17 --> N7
    N7 -- No --> N18 --> NEnd
    N18 --> NEnd([End])
```

**Reading the chart:**
- Rounded nodes = start/end
- Rectangles = processing steps / assignments
- Diamonds = decision points, with the `True`/`False` branch labelled
- The three nested loops (`i`, `j`, `k`) each have their own return edge
  back to their condition check, matching the three `for` loops in the
  implementation.
