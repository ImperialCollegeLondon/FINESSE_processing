PRO Sort_and_process_EM27_output

;Version 1.0 Written by Jon Murray 26/07/2024.
;Simplifies the processing of the acquired EM27 interferograms, co-locating blackbody data from the RSE log file to yield time resolved response functions that are
;applied to the nearest scene views to derive time resolved calibrated radiance

;Dependencies:

              ;ASCII read template for the OPUS chemical retrieval output files, contains the start times
              ;'Result_read_template.sav'
              
              ;RSE GUI log file
              ;e.g. sand_emissivity1_20240620_081952.txt'
              ;
              ;IDL routine to read log file....
              ;read_GUI_logfile.pro
              ;
              ;ASCII template for the RSE logfile
              ;'RSE_template.sav'
              
              ;IDL routine to read the EM27 binary interferogram
              ;read_bruker_int.pro
              
              ;IDL routine to apply the Fast Fourier Transform to differenced interferograms
              ;bruker_fft.pro
              
              ;IDL routine the calculate the planck radiance for a given temperature and frequency scle
              ;planck.pro
              

  PATH = 'F:\bruker_2024\20240620\sonoran\'   ;_0114_to_0320\'
  date_stamp='(2024_06_20_'           ;run date, the routine will look for directories created on this daystop

  ;********************************************************************************************************************
  all_directories=file_search(PATH+date_stamp+'*') ;Find all directories with the date_stamp: this stores dir names
  result=size(all_directories)                     ;Set the number of directories here
  dir=result(1)
  ;********************************************************************************************************************
  number_scans=40   ;these are the number of scans the EM27 has been set to acquire
  
  all_times=strarr(dir,number_scans)   ;variable to contain the start times of all acquired interferograms, string
  inter_times=lonarr(dir,number_scans) ;variable to contain the start times of all acquired interferograms, converted to seconds from midnight

  centre=LONARR(number_scans,dir)  ;zero path difference sample index
  hot_temp=fltarr(dir)             ;average hot blackbody temperature during 40 scan observation
  cold_temp=fltarr(dir)            ;average ambient blackbody temperature during 40 scan observation
  target=intarr(dir)
  
  averaged_interferograms=fltarr(dir,57254)
  
  handovertime=lonarr(40)
  view_mid_times=fltarr(dir)

;=======================================================================================================================================================================
FOR i=0,dir-1 DO BEGIN   ;loop over all 40 scans directories
  
  ;************************************************ Start co-locating EM27 and GUI data-sets ***************************************************************
  ;*********************************************************************************************************************************************************
  textname = FILE_SEARCH(all_directories(i)+'\*ResultSeries.txt')    ;Define filename with EM27 scan time info
  
  restore,'D:\Andoya_measurements\Result_read_template.sav'   ;ASCII read template for the OPUS chemical retrieval output files, contains the start times
  time_info=read_ascii(textname,template=template,data_start=2)  ;Open file, OPUS output for start of interferograms
  all_times(i,0:number_scans-1)=time_info.(1)(0:number_scans-1)  ;Store start times for the interferograms for the 40 scan sequence  

  temperature_file = FILE_SEARCH('F:\bruker_2024\20240620\sand_emissivity1_20240620_081952.txt')   ;temperature log file
  ;********************************************************************************************************************
  
  FOR scs=0,number_scans-1 DO BEGIN  ;Convert the time string values to seconds from midnight, this will be used to co-locate with the GUI log data
    inter_times(i,scs)=fix(strmid(time_info.(1)(scs),0,2))*3600L+fix(strmid(time_info.(1)(scs),3,2))*60L+fix(strmid(time_info.(1)(scs),6,2))
    handovertime(scs)=inter_times(i,scs)
  ENDFOR
  view_mid_times(i)=mean(handovertime(*))
  
    ;Pass the scan time information to the read GUI routine, this routine will pass back the co-located temperature and targetting information from the log file
    read_GUI_logfile,number_scans,temperature_file,handovertime,colocat_temps,colocat_temps_std,targetting
    
    hot_temp(i)=mean(colocat_temps(*,5)+colocat_temps(*,6))/2.  ;mean hot BB temperature during scan sequence
    cold_temp(i)=mean(colocat_temps(*,7))                       ;mean ambient BB temperature during scan sequence
    target(i)=targetting(1,0)                                   ;set the scan sequence target, first scan generally has a valid angle sometimes the write buffering gives misallaneous values for last scans
    
    ;This is a screen printed check showing the targetting information for the 40 scans. These should all be the same, if not, either the mirror has
    ;moved or the GUI write is buffering and giving an off-set time
      print,i,targetting(0,0)/3600.,' mirror angle= ',inter_times(0),round(targetting(1,0)),round(targetting(1,1)),inter_times(39),round(targetting(1,37)),$
      round(targetting(1,38)),round(targetting(1,39))
      
  ;************************************************ End co-locating EM27 and GUI data-sets ******************************************************************
  ;**********************************************************************************************************************************************************  
 
;^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
;
   ;************************************************ Start extracting EM27 interferogram data-sets **********************************************************
   ;*********************************************************************************************************************************************************
    
   ints=fltarr(number_scans,57254)   ;will hold all interferograms for the number of scans in a view

   intname = FILE_SEARCH(all_directories(i)+'\w*.0')    ;Define filename with time info
   ;********************************************************************************************************************
   read_bruker_int,number_scans,intname,centre_set,ints ;pass the number of scans and interferogram filenames to the interferogram read routine, receive zero_path info and interferograms
   centre(0:39,i)=centre_set(0:39)
   FOR sc=0,39 DO BEGIN
   averaged_interferograms(i,0:57253)=averaged_interferograms(i,0:57253)+ints(sc,0:57253)
   ENDFOR
   averaged_interferograms(i,0:57253)=averaged_interferograms(i,0:57253)/40.

   ;************************************************ End extracting EM27 interferogram data-sets **********************************************************
   ;*********************************************************************************************************************************************************
ENDFOR
;=======================================================================================================================================================================

;Have run through all the directories associated with the EM27 data acquisition, co-located the GUI log files and extracted all data required to derive calibrated radiances

;Relavant variables: inter_times, hot_temp, cold_temp, target, averaged_interferograms

;**********************
  resolution=0.5           ;These variables are required by the FFT routine
  fre_interval=0.2
;**********************
dum=fltarr(57254L)
wv=fltarr(12500)

hotBB=where(target eq 270,count_hot)    ;Will house the index number (off the EM27 directory outputs) associted with the hot BB view
coldBB=where(target eq 225,count_cold)  ;Will house the index number (off the EM27 directory outputs) associted with the cold BB view
response_functions=fltarr(count_hot,12500) ;Count_hot and count_cold should be the same
response_times=lonarr(count_hot)
;---------------------------------------- Co-locate the sequence (index) number by view angle ---------------------------------------
view_40=where(target eq 39,count40)    
view_140=where(target eq 140,count140)
view_50=where(target eq 50,count50)
view_130=where(target eq 129,count130)

view_40_times=lonarr(count40)
view_140_times=lonarr(count140)
view_50_times=lonarr(count50)
view_130_times=lonarr(count130)

hot_t=fltarr(count_hot)
hot_int=fltarr(count_hot,57254L)
;***************************************************** Calculate the spectral response functions ********************************************
FOR rep_count=0,count_hot-1 DO BEGIN  
  dum(*)=(averaged_interferograms(hotBB(rep_count),*)-averaged_interferograms(coldBB(rep_count),*))   ;difference the sequential hot and cold interferograms
  bruker_fft, dum, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase          ;FFT the differenced interferogram, apodised_spectra = 0.5 cm-1
  
  IF rep_count EQ 0 THEN wv(*)=apodised_spectra(0,*)  ;set apodised frequency scale
  
  ;derive the spectral response function using the apodised spectra and co-located blackbody temperatures, assumes emissivity = 1.
  response_functions(rep_count,*)=apodised_spectra(1,*)/(planck(273.14+(hot_temp(hotBB(rep_count))),wv)-planck(273.14+(cold_temp(coldBB(rep_count))),wv))
  
  response_times(rep_count)=view_mid_times(coldBB(rep_count))            ;store the mid-times for each response function
  ;--------------------- Below hot BB temperatures and hot intererograms are required to derive calibrated scene radiances --------------------------------------
  hot_t(rep_count)=hot_temp(hotBB(rep_count))                            ;store the associated hot blackbody temperature
  hot_int(rep_count,*)=averaged_interferograms(hotBB(rep_count),*)       ;store the associated hot blackbody interferogram

ENDFOR

;*********************************************************************************************************************************************
mean_response=fltarr(12500)
radiance40=fltarr(count40,12500)
radiance140=fltarr(count140,12500)
radiance50=fltarr(count50,12500)
radiance130=fltarr(count130,12500)
;***************************************************** Derive calibrated scene view radiances ********************************************
FOR view_count40=0,count40-1 DO BEGIN
  view_40_times(view_count40)=view_mid_times(view_40(view_count40))  ;store the scene observation times
  cycle=Where(view_40_times(view_count40) GT response_times,indext)  ;find the nearest spectral response just prior to the scene view
  
  rep_index40=cycle(indext-1)         ;this is the response function just before view scan
  mean_response(*)=(response_functions(rep_index40,*)+response_functions(rep_index40+1,*))/2.    ;take the mean response of that just prior and after the scene view
  
  T=(hot_t(rep_index40)+hot_t(rep_index40+1))/2.   ;take the mean temperature of the hot BB jus prior and after the scene view
  ;------------------------ Note the following line uses the average scene observation for a given cycle, this can be substituted for each of the 40 individual interferograms ----------------  
  dum=((hot_int(rep_index40,*)+hot_int(rep_index40+1,*))/2.)-averaged_interferograms(view_40(view_count40),*)  ;Difference the mean hot interferogram (prior/after scene) and the scene interferogram 

  bruker_fft, dum, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase          ;FFT the differenced interferogram, apodised_spectra = 0.5 cm-1

  radiance40(view_count40,*)=planck(273.14+T,wv)-apodised_spectra(1,*)/mean_response(*) ;Store the calibrated radiances
  print,'rep40 index= ',rep_index40
ENDFOR

FOR view_count140=0,count140-1 DO BEGIN
  view_140_times(view_count140)=view_mid_times(view_140(view_count140))
  cycle=Where(view_140_times(view_count140) GT response_times,indext)
  
  rep_index140=cycle(indext-1)
  mean_response(*)=(response_functions(rep_index140,*)+response_functions(rep_index140+1,*))/2.

  T=(hot_t(rep_index140)+hot_t(rep_index140+1))/2.
  dum=((hot_int(rep_index140,*)+hot_int(rep_index140+1,*))/2.)-averaged_interferograms(view_140(view_count140),*)
  bruker_fft, dum, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase          ;FFT the differenced interferogram, apodised_spectra = 0.5 cm-1
  
  radiance140(view_count140,*)=planck(273.14+T,wv)-apodised_spectra(1,*)/mean_response(*)
  print,'rep140 index= ',rep_index140
ENDFOR

FOR view_count50=0,count50-1 DO BEGIN
  view_50_times(view_count50)=view_mid_times(view_50(view_count50))
  cycle=Where(view_50_times(view_count50) GT response_times,indext)
  
  rep_index50=cycle(indext-1)
  mean_response(*)=(response_functions(rep_index50,*)+response_functions(rep_index50+1,*))/2.

  T=(hot_t(rep_index50)+hot_t(rep_index50+1))/2.
  dum=((hot_int(rep_index50,*)+hot_int(rep_index50+1,*))/2.)-averaged_interferograms(view_50(view_count50),*)
  bruker_fft, dum, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase          ;FFT the differenced interferogram, apodised_spectra = 0.5 cm-1
  
  radiance50(view_count50,*)=planck(273.14+T,wv)-apodised_spectra(1,*)/mean_response(*)
  print,'rep50 index= ',rep_index50
ENDFOR

FOR view_count130=0,count130-1 DO BEGIN
  view_130_times(view_count130)=view_mid_times(view_130(view_count130))
  cycle=Where(view_130_times(view_count130) GT response_times,indext)
  
  rep_index130=cycle(indext-1)
  mean_response(*)=(response_functions(rep_index130,*)+response_functions(rep_index130+1,*))/2.

  T=(hot_t(rep_index130)+hot_t(rep_index130+1))/2.
  dum=((hot_int(rep_index130,*)+hot_int(rep_index130+1,*))/2.)-averaged_interferograms(view_130(view_count130),*)
  bruker_fft, dum, resolution, fre_interval, full_fre, full_spectra, apodised_spectra, phase          ;FFT the differenced interferogram, apodised_spectra = 0.5 cm-1
  
  radiance130(view_count130,*)=planck(273.14+T,wv)-apodised_spectra(1,*)/mean_response(*)
  print,'rep130 index= ',rep_index130
ENDFOR

;*********************************************************************************************************************************************


stop

END