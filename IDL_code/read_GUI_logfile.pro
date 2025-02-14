pro read_GUI_logfile, number_scans, temperature_file, inter_times, colocat_temps, colocat_temps_std, targetting
  compile_opt idl2

  ; RSE_template = ASCII_TEMPLATE('F:\bruker_2024\20240620\sand_emissivity1_20240620_081952.txt')  Set up the RSE template
  ; save,PRT_template,filename='F:\bruker_2024\RSE_template.sav'

  ; restore,'D:\Andoya_measurements\temp_log_file_template.sav'     ;This restores the logfile format used to read the logfile (original logfile from Alan's GUI)
  ; t_info=read_ascii(temperature_file,template=temp_log_templte)   ;read in all lines from logfile (total of 12 columns)

  restore, 'F:\bruker_2024\RSE_template.sav' ; This restores the logfile format used to read the logfile (New RSE GUI logfile)
  t_info = read_ascii(temperature_file, template = RSE_template) ; read in all lines from logfile (total of 12 columns)

  log_seconds = t_info.(10) ; This column is the seconds from mid-night and will be used  to co-register against the interferogram times
  ; ********************************************************************************************************************

  colocat_temps = fltarr(number_scans, 8) ; There are 8 temperature channels, this variable will contain the temperatures
  colocat_temps_std = fltarr(number_scans, 8) ; co-located interferogram to the interferogram start times
  targetting = lonarr(2, number_scans) ; (0,scan)=collocated time (1,*)=collocated target

  for int_s = 0, number_scans - 1 do begin
    coloc = min((log_seconds - inter_times[int_s]) ^ 2, min_sub)
    coloc2 = min((log_seconds - (inter_times[int_s] + 4)) ^ 2, min_sub2)
    ; print,round(sqrt(coloc)),min_sub,log_seconds(min_sub),log_seconds(min_sub2),inter_times(int_s),t_info.(8)(min_sub),t_info.(9)(min_sub),t_info.(10)(min_sub),t_info.(11)(min_sub)
    if coloc lt 16 then begin ; i.e with 4 seconds as we square the time difference
      for log_chan = 0, 7 do begin
        dum = moment(t_info.(log_chan + 2)(min_sub:min_sub2))
        colocat_temps[int_s, log_chan] = dum[0]
        colocat_temps_std[int_s, log_chan] = sqrt(dum[1])
      endfor
      targetting[0, int_s] = t_info.(10)(min_sub) ; Store time
      targetting[1, int_s] = t_info.(11)(min_sub) ; Steering mirror angle (target)
    endif else begin
      stop ; We have a case where the there are no temperatures in the log file within 5 seconds of the start of a scan, might want to think why this is
    endelse
  endfor ; loop over number of scans per view
  ; stop
end