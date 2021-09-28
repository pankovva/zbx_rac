@echo off
set SrvcName="1C:Enterprise 8.3 RAS"
set BinPath="C:\Program Files\1cv8\8.3.17.1851\bin\ras.exe cluster --service"
set Desctiption="1C:Enterprise 8.3 RAS"
sc stop %SrvcName%
sc delete %SrvcName%
sc create %SrvcName% binPath= %BinPath% start= auto displayname= %Desctiption%
sc start %SrvcName%