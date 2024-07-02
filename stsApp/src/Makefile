TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = sts
# sts.dbd will be created and installed
DBD += sts.dbd

# sts.dbd will be made up from these files:
sts_DBD += base.dbd

# Include dbd files from all support applications:
sts_DBD += asSupport.dbd

# Add all the support libraries needed by this IOC
sts_LIBS += autosave

# sts_registerRecordDeviceDriver.cpp derives from sts.dbd
sts_SRCS += sts_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
sts_SRCS_DEFAULT += stsMain.cpp
sts_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#sts_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
sts_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

