-- Prosedyre som skriver ut valgte serier til flatfilformat som kan leses av python
-- MKH 2023

procedure $flatfil
 arguments search, to_file=""

 if length(to_file) gt 0
  local path = blank
  if location(trim(system("pwd")), "/ssb/bruker/") eq nc
   set path = "/ssb/bruker/"+trim(system("whoami"))
  else
   set path = trim(system("pwd"))
  end if
  open <access overwrite; kind text> file(path+"/"+ltrim(to_file,"/")) as file
  try
   $skriv_flatfil search, file
   write "Data skrevet til /ssb/bruker/"+trim(system("whoami"))+"/"+ltrim(to_file,"/")
  oterwise
   write lasterror to info
  end try
  close file
 else
  $skriv_flatfil search
 end if

 write null
 write "import pandas as pd"
 write "df = pd.read_csv('ditt_filnavn.csv', delimiter=';', index_col=0)"
 if @freq eq "MONTHLY"
  write "df.index = pd.PeriodIndex(df.index, freq='m')"
 else if @freq eq "QUARTERLY"
  write "df.index = pd.PeriodIndex(df.index, freq='q')"
 else if @freq eq "DAILY"
  write "df.index = pd.PeriodIndex(df.index, freq='d')"
 else
  write "df.index = pd.PeriodIndex(df.index, freq='a')"
 end if
end procedure

procedure $skriv_flatfil
 arguments search, write_to=output

 local found = {}

 loop for db in {work}+make(namelist, @search)
  loop for x in selectnames(wildlist(db, search), freq(@name) eq @freq)
   set found = {x} union found
  end loop
 end loop

 block
  csv on, delimiter ";"
  replace nd null
  replace nc null
  replace na null
  
  if @freq eq "MONTHLY"
   image date "<year>-<pz>"
  else if @freq eq "QUARTERLY"
   image date "<year>Q<p>"
  else if @freq eq "DAILY"
   image date "<year>-<mz>-<dz>"
  end if

  -- Skriver ut data uten report pga begrensinger på minne

  -- Skriver ut kolonnenavn
  loop for x in found
   write <crlf off> ";"+lower(name(x)) to write_to
  end loop
  write null to write_to

  -- Skriver ut data
  loop for s = firstdate to lastdate
   write <crlf off> datefmt(s) to write_to
   loop for x in found
    write <crlf off> ";"+numfmt(x[s], *, @decimals) to write_to
   end loop
   write null to write_to
  end loop
 end block
end procedure