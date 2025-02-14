pro read_bruker_int, number_scans, intname, centre_set, ints
  compile_opt idl2

  centre_set = lonarr(number_scans)

  for int_s = 0, number_scans - 1 do begin
    filen = intname[int_s]
    openr, file, filen, /get_lun ; open the .ssp file
    DUM = fstat(file)
    dum_sz = long(DUM.(15) / 4)
    if dum_sz gt 57254l then dum_sz = 57254l
    dummy_int = fltarr(dum_sz)
    readu, file, dummy_int
    close, file
    free_lun, file

    ; ****************************************************************************************************************
    discard = 400l ; The start and end of the interferograms are filled with rubbish, this gets rid of these values to allow determination of ZPD
    dummy_int2 = fltarr(57254)
    dummy_int2[0l : dum_sz - 1l] = dummy_int[0l : dum_sz - 1l]
    dummy_int2[0 : discard] = 0.
    dummy_int2[57253 - (discard + 1) : 57253] = 0.
    zeropd = max(dummy_int2 ^ 2, subscript)
    centre_set[int_s] = subscript
    ; ****************************************************************************************************************
    ints[int_s, 0 : 57253] = dummy_int2[*]
  endfor ; loop over number of scans per view
end