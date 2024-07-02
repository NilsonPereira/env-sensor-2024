#!../../bin/linux-x86_64/sts

## You may have to change sts to something else
## everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/sts.dbd"
sts_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("xxx.db","user=epics")

cd "${TOP}/iocBoot/${IOC}"

## Load record instances
dbLoadRecords("st.db")

## autosave
set_requestfile_path("${TOP}/iocBoot/${IOC}")
set_savefile_path("/EPICS/autosave")
set_pass0_restoreFile("auto_settings.sav")


iocInit

## autosave
create_monitor_set("auto_settings.req")


## Start any sequence programs
#seq sncxxx,"user=epics"
