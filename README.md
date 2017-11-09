# [U-Code](http://pl.skuniv.ac.kr/Lecture/Compiler/cdt-9/sld022.htm) interpreter

- Fully implemented interpreter of [U-Code](http://pl.skuniv.ac.kr/Lecture/Compiler/cdt-9/sld022.htm) standard
- Has additional calculation of floating point feature. Details are below (due to [TTime Language Compiler](https://github.com/TTimeLanguage/Compiler)'s feature)
- Fully compatible with [TTime Language Compiler](https://github.com/TTimeLanguage/Compiler)
- Support recursive function call

## Usage

```bash
./src/interpreter.py '<UCode source path>' '<result file path>'
```

## Additional feature

### Explain
- this support 32bit floating point calculation.
- Every floating point value must notated with integer (??? pass and read below).
- according to [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point), floating point value is converted to bit-array. and that bit-array can read as integer in computer.
- this trick is base of floating point support.

#### Example

32 bit array `11000000010110011001100110011010` is
- `-3.4` in [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
- `-1067869798` in 32bit integer
- [converter](http://www.h-schmidt.net/FloatConverter/IEEE754.html)

### float supporting functions

##### 1. addFloat

- usage: `call addFloat`
- pop 2 value (a, b) in stack and push a + b.

##### 2. subFloat

- usage: `call subFloat`
- pop 2 value (a, b) in stack and push a - b.

##### 3. mulFloat

- usage: `call mulFloat`
- pop 2 value (a, b) in stack and push a * b.

##### 4. divFloat

- usage: `call divFloat`
- pop 2 value (a, b) in stack and push a / b.

##### 5. modFloat

- usage: `call divFloat`
- pop 2 value (a, b) in stack and push a % b.

##### 6. negFloat

- usage: `call divFloat`
- pop 1 value (a) in stack and push -a.

##### 7. F2I

- usage: `call F2I`
- pop 1 value in stack and push value that converted to integer
- ex: if a is `4.0` (IEEE 754 form `01000000100000000000000000000000`), pushed value is `4` (`100`b)

##### 8. I2F

- usage: `call I2F`
- pop 1 value in stack and push value that converted to float
- ex: if a is `4` (`100`b), pushed value is `4.0` (IEEE 754 form `01000000100000000000000000000000`)

##### 9. writeF

- usage: `call writeF`
- pop 1 float value and print as float 