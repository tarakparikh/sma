#
# D.D.'s ~/.cshrc
#

#
# In order to get a tool set up, uncomment the corresponding line:
#
unset sw_purify
unset sw_purecov
unset sw_quantify
set sw_stty
unset sw_msvc6
set sw_perforce
set sw_randname
set mti_workspacedirs = /home/tparikh/dev

#
# Source MTI South's common CSH setup
#
source /home/mtisouth/sw_cshrc

if ($osname == "CYGWIN_NT-5.1") then
    setenv MTI_HOME u:/tparikh/dev/questa_ast/modeltech
else
    #setenv MTI_HOME /u/tparikh/dev/10.3/modeltech
endif
silentplat $PLATFORM

setenv MTI_HOME /u/tparikh/dev/10.4/modeltech

#
# My environment variables
#

# For editing cron files gracefully
setenv EDITOR vi

#
# My aliases
#

alias va 'vi ~/.address'
alias a 'addr -i ~/.address'
alias lh 'll -t | head'
alias lt 'll -rt | tail'

alias svnc vncserver -geometry 1850x960
alias setmti 'setenv MTI_MAIN \!*; setenv MTI_HOME $MTI_MAIN/modeltech; setenv PATH $MTI_HOME/linux:$PATH;'
alias idesigner atdesigner +read_idl2ast+design.bin
setenv QUESTA_MVC_HOME /home/tparikh/work/VIP
setenv HDLOFFICEROOT /home/tparikh/dev/main/src/hdloffice

# Xterm aliases
alias green "xterm -g 90x45+25+25 -fn 9x15bold -fg green -bg black -bd red -n Green  &"
alias cyan "xterm -g 90x45+25+25 -fn 9x15bold -fg cyan -bg black -bd red -n Cyan &"
alias yellow "xterm -g 90x45+70+75   -fn 9x15bold -fg yellow -bg black -bd red -n Yellow &"
alias gold "xterm -g 90x45+70+75   -fn 9x15bold -fg gold -bg black -bd red -n Gold &"
alias wheat "xterm -g 90x43+0+0 -fn 9x15bold -fg black -bg wheat -bd red -cr red &"
alias corn "xterm -g 90x43+50+75 -fn 9x15bold -fg wheat -bg black -bd red -cr red &"
alias lawn "xterm -g 90x45+0+0 -fn 9x15bold -fg black -bg mediumspringgreen -bd black -cr red &"
setenv NOREBIND
setenv LM_LICENSE_FILE "${LM_LICENSE_FILE}:/mtisouth/hdlhome/cvsroot/FLEXLM/axiom_license.dat"
#setenv ATHDLROOT /mtisouth/hdlhome/athdl
#setenv ATHDLROOT /home/tparikh/dev/questa_ast/hdloffice/release/athdl
#set path=($ATHDLROOT/bin $path)
#setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:${ATHDLROOT}/so/linux/LIBSTDCPLUSPLUS"
set path=(/home/tparikh/bin /home/tparikh/dev/10.4/modeltech/linux_x86_64 /opt/gnome/bin  $path)
#setenv WRITE_AST_BIN_VTREE 1
#setenv IDL2AST_HIER 1
#setenv IDL2AST_DEBUG 1
#setenv QWAVEDB_ENABLE 2
#setenv VSIM_ADDONS '-foreign "Designer_Init_QA designer.so"'
#setenv VSIM_ADDONS '-foreign "init_param_print athdl_modelsim.so" -pli /home/tparikh/dev/questa_ast/build/linux/hdloffice/waveform/pli/src/athdl_modelsim.so'
#setenv VSIM_ADDONS '-foreign "init_hier_print athdl_modelsim.so" -pli /home/tparikh/dev/questa_ast/build/linux/hdloffice/waveform/pli/src/athdl_modelsim.so'

alias setpath 'setenv PLATFORM linux ; setenv PLATFORM2 linux ; setenv MHOME /home/tparikh/dev/\!:1 ; set path=(${MHOME}/modeltech/linux $path)'
alias seth 'setenv HDLOFFICEROOT /home/tparikh/dev/\!:1/src/hdloffice ; cd $HDLOFFICEROOT ; source .tcshrc'
alias setpath64 'setenv PLATFORM linux_x86_64 ; setenv PLATFORM2 linux_x86_64 ; setenv MHOME /home/tparikh/dev/\!:1 ; set path=(${MHOME}/modeltech/linux_x86_64 $path)'

set path=(/home/tparikh/ECLIPSE/eclipse-setup/eclipse /home/tparikh/ECLIPSE/eclipse-setup/jdk1.6.0_26/bin /home/ECLIPSE/eclipse-setup/jdk1.6.0_26/jre/bin $path)
setenv JAVA_HOME /home/ECLIPSE/eclipse-setup/jdk1.6.0_26/bin/java

# Don't know why we need this
#
#if ($HOSTNAME == "perf-vis1") then
      #setenv LD_LIBRARY_PATH /home/tparikh/dev/AST_QUESTA_NIGHTLY/modeltech/linux_x86_64/Visualizer/bin
    #else
      #setenv LD_LIBRARY_PATH /home/tparikh/dev/AST_QUESTA_NIGHTLY/modeltech/linux_x86_64/Visualizer/bin:/u/prod/gnu/gcc/20100526/gcc-4.5.0-linux_x86_64/lib64
    #endif
#

#setenv LD_LIBRARY_PATH /home/tparikh/dev/AST_QUESTA_NIGHTLY/modeltech/linux_x86_64/Visualizer/bin:/u/prod/gnu/gcc/20100526/gcc-4.5.0-linux_x86_64/lib64 

alias setmti32 'setenv MTI_MAIN \!*; setenv MTI_HOME $MTI_MAIN/modeltech; setenv PATH $MTI_HOME/linux:$PATH; setenv PLATFORM2 linux; setenv PLATFORM linux; setenv PLAT linux; setenv LD_LIBRARY_PATH $MTI_HOME/linux; rehash; which vlog; which hdloffice'
alias setmti64 'setenv MTI_MAIN \!*; setenv MTI_HOME $MTI_MAIN/modeltech; setenv PATH $MTI_HOME/linux_x86_64:$PATH; setenv PLATFORM2 linux_x86_64; setenv PLATFORM linux_x86_64; setenv PLAT linux_x86_64; setenv LD_LIBRARY_PATH $MTI_HOME/linux_x86_64; rehash; which vlog; which hdloffice'

alias go_fc 'cd /home/tparikh/dev/main/tests/ucdb/cvg2008'
setenv VELOCE_HOME /u/prod/med_libs/LATEST
setenv VISUALIZER_LOCAL_DBG_LOG         1

setenv LD_LIBRARY_PATH /home/tparikh/dev/10.4/modeltech/gcc-4.7.4-linux_x86_64/lib64
alias ias 'vis +designfile +wavefile'
setenv PLATFORM linux_x86_64
setenv PLATFORM2 linux_x86_64
#setpath REL
