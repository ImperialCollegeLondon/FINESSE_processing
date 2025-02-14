function planck, temp, w_scale
  compile_opt idl2

  c1 = 1.1911e-8
  c2 = 1.439

  rad = (c1 * (w_scale[*] ^ 3)) / ((exp(c2 * w_scale[*] / temp)) - 1)

  RETURN, rad
end