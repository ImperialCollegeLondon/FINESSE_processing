pro bruker_fft, interferogram, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase
  compile_opt idl2

  ; ************************************ CODE WRITTEN BY J.E.MURRAY *****************************************************
  ; ver 1.0 22-01-2021
  ; *** The interferogram source may be *.ifs or *.0 file containing the unclipped interferogram or unclipped ends, i.e. the ends with rubbish may/maynot have been removed **
  ; spurious data at the ends of the interferogram scan are checked for
  ; **************************** The assumed scan length +/-1.8 cm with sampling intervals given by HeNe laser frequency ***************************
  ; The code may be able to cope with other scan lengths but needs to be checked, may need to be careful that "resolution" of apodised spec does not conflict with the coding

  ; Returns the complex spectrum for the input interferogram and a complex spectra after boxcar apodisation defined by resolution

  HeNe = 6.32816e-5 ; (Helium Neon laser wavelength in cm)
  OPD = 0.605 / resolution ; This calculates the optical path difference neccessary for the required spectral resolution assuming boxcar apodisation
  padded_samples = long(round(1. / (HeNe * fre_interval))) ; samples covering the range 0-7901.19 cm-1 (Free spectral range based on 1st alias)
  full_fre = findgen(padded_samples) / HeNe / padded_samples ; Set the frequency scale applicable to the full interferogram scan input

  ; ******************************************************************
  dum = size(interferogram)
  if dum[0] eq 1 then begin
    samps = dum[1]
    int = fltarr(samps)
    int[*] = interferogram[*] ; Dependent on the source of the interferogram the input array may be fltarr(samples) or fltarr(1,samples)
  endif else begin
    samps = dum[2]
    int = fltarr(samps)
    int[*] = interferogram[0, *]
  endelse
  ; *****************************************************************************************************************************************************************

  ; ********************************************** CHECK FOR SPURIOUS VALUES, USUALLY APPEAR NEAR THE END OF THE INTERFEROGRAMS **************************************

  mid_value = max(int[500 : samps - 500] ^ 2) ; Get a value for the centre burst signal (in this case squared as the interference can be negative)
  noisy = where(int ^ 2 gt 1.1 * mid_value, count) ; the extremes of the interferogram can contain very high values that are rubbish, the value count will indicate this

  if count gt 0 then begin ; If count exceeds 0 then we'll clip the interferogram at each end by 500 samples usually enough to get rid of non-sensical values
    clipped = fltarr(samps - 1000)
    clipped[*] = 0.
    clipped[0l : samps - 1001l] = int[500l : samps - 501l]
    int = clipped

    dum = size(int)
    samps = dum[1] ; reset the number of samps in the interferogram
  endif
  ; *******************************************************************************************************************************************************************

  ; ************************************************** prepare the interferogram for the FFT **********************************************************************

  peak = max(int ^ 2, zpd_index) ; find the index position of zero path difference in the interferogram

  ; ******************************************* Set number of samples for padded array and fold out the input interferogram
  padded_int = dblarr(padded_samples) ; padded_samples is the extended interferogram required to yield a frequency grid defined by fre_interval
  padded_int[*] = 0.

  ; ******************************************************** Fold out (from zpd) and copy the full/clipped input interferogram ***********************************
  ; ready for FFT (full_spe) FFT(apodised_spe) and FFT(for phase determination)
  padded_int[0 : zpd_index] = reverse(int[0 : zpd_index]) ; Reverse and copy -L to zpd
  rang = (samps - 1l) - (zpd_index + 1l) ; Figure out the array index extent within the padded int to place the zpd to +L of input interferogram
  padded_int[padded_samples - 1 - rang : padded_samples - 1] = reverse(int[zpd_index + 1 : samps - 1])

  offset = mean(padded_int[padded_samples - 1 - rang : padded_samples - 1 - rang + 100]) ; Offset gives an estimate of the DC offset level

  padded_int[0 : zpd_index] = padded_int[0 : zpd_index] - offset ; Off set the interferogram signal
  padded_int[padded_samples - 1 - rang : padded_samples - 1] = padded_int[padded_samples - 1 - rang : padded_samples - 1] - offset

  ; ***************************************************************************************************************************************************************
  full_spe = fft(padded_int, 1) ; Fourier transform the padded interferogram
  ; ***************************************************************************************************************************************************************

  ; *********************************************** Set interferogram values beyond the apodised OPD to zero and transform ****************************************
  apodised_int = padded_int ; copy padded interferogram
  truncation = long(round(OPD / HeNe)) ; establish the array index associated to an optical path required for the given resolution
  apodised_int[truncation : padded_samples - truncation] = 0. ; zero the interferogram for measurements beyond the require OPD

  ; ***************************************************************************************************************************************************************
  apodised_spe = fft(apodised_int, 1) ; Fourier transform the apodised interferogram: The spectral output will be on a frequency grid given by full_fre
  ; ***************************************************************************************************************************************************************

  ; ********************************************* calculated the low resolution phase function ********************************************************************
  low_res_int = padded_int
  low_res_int[4096l : padded_samples - 4096l] = 0. ; This sets the OPD for the low resolution spectra that will be used to calculated the phase function
  ; low_res_int(8192L:padded_samples-8192L)=0.      ;This sets the OPD for the low resolution spectra that will be used to calculated the phase function
  ; low_res_int(16384L:padded_samples-16384L)=0.      ;This sets the OPD for the low resolution spectra that will be used to calculated the phase function
  ; ***************************************************************************************************************************************************************
  low_spe = fft(low_res_int, 1) ; Fourier transform the low res interferogram: Note that the frequency scale will be the same as the full_spe and apodised_spe
  phase = atan(imaginary(low_spe) / float(low_spe)) ; Calculate the phase function
  ; ***************************************************************************************************************************************************************

  phs = phase
  wv_low = long(round(400. / full_fre[1]))
  wv_hi = long(round(2000. / full_fre[1]))
  ; result = LINFIT(full_fre(wv_low:wv_hi), phase(wv_low:wv_hi))
  ; result = POLY_FIT(full_fre(wv_low:wv_hi), phase(wv_low:wv_hi),2)
  ; result=POLY_FIT(full_fre(wv_low:wv_hi), phase(wv_low:wv_hi),7)
  ; phase=full_fre(*)^7*result(0,7)+full_fre(*)^6*result(0,6)+full_fre(*)^5*result(0,5)+$
  ; full_fre(*)^4*result(0,4)+full_fre(*)^3*result(0,3)+full_fre(*)^2*result(0,2)+full_fre(*)*result(0,1)+result(0,0)
  ; phase(*)=full_fre(*)^2*result(0,2)+full_fre(*)*result(0,1)+result(0,0)

  ; stop

  ; **************************************************** The spectral range of the spectra are 0 - 7900 cm-1, for our setup 2500 cm-1 is probably sufficient
  constrained_samps = round(2500. / fre_interval) ; constrained samples gives the number of spectral points at the required frequency sampling
  full_spectra = dblarr(4, constrained_samps) ; Will contain the unapodised spectra
  apodised_spectra = dblarr(4, constrained_samps) ; Will contain the apodised spectra

  corr_specr = -(float(full_spe[*]) * cos(phase[*]) + imaginary(full_spe[*]) * sin(phase[*])) ; , $
  corr_speci = -(float(full_spe[*]) * cos(1.5708 - phase[*]) - imaginary(full_spe[*]) * sin(1.5708 - phase[*]))

  full_spectra[0, 0 : constrained_samps - 1] = full_fre[0 : constrained_samps - 1] ; frequency grid
  full_spectra[1, 0 : constrained_samps - 1] = corr_specr[0 : constrained_samps - 1] ; Real component
  full_spectra[2, 0 : constrained_samps - 1] = corr_speci[0 : constrained_samps - 1] ; Imaginary component
  full_spectra[3, 0 : constrained_samps - 1] = phase[0 : constrained_samps - 1] ; Phase function

  corr_specr = -(float(apodised_spe[*]) * cos(phase[*]) + imaginary(apodised_spe[*]) * sin(phase[*])) ; , $
  corr_speci = -(float(apodised_spe[*]) * cos(1.5708 - phase[*]) - imaginary(apodised_spe[*]) * sin(1.5708 - phase[*]))

  apodised_spectra[0, 0 : constrained_samps - 1] = full_fre[0 : constrained_samps - 1] ; frequency grid
  apodised_spectra[1, 0 : constrained_samps - 1] = corr_specr[0 : constrained_samps - 1] ; Real component
  apodised_spectra[2, 0 : constrained_samps - 1] = corr_speci[0 : constrained_samps - 1] ; Imaginary component
  apodised_spectra[3, 0 : constrained_samps - 1] = phase[0 : constrained_samps - 1] ; Phase function

  ; ***************************************************************************************************************************************************************
end