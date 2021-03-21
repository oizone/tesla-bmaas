#!/usr/bin/python3
import os
import re
import openpyxl
wb=openpyxl.load_workbook(filename='esxi-hosts.xlsx')
ws=wb["Hosts"]
iso_folder="/iso/"
http_folder="/var/www/httpboot/"


for i in ws.iter_rows(min_row=3):
    ks='ks={}/{}/ks.cfg'.format(ws['B1'].value,i[0].value)
    ks_folder='{}{}'.format(http_folder,i[0].value)
    #if not os.path.exists(i[0].value):
    #    os.mkdir(i[0].value)
    if not os.path.exists(ks_folder):
        os.mkdir(ks_folder)
    output=open("{}/ks.cfg".format(ks_folder),"w+")

    output.write('vmaccepteula\n')
 
    output.write('rootpw {}\n'.format(i[12].value))
    output.write('clearpart --alldrives --overwritevmfs\n')

    output.write('install {} --overwritevmfs --novmfsondisk\n'.format(i[8].value))
    output.write('keyboard Finnish\n')

    output.write("network --bootproto=static --device={} --ip={} --netmask={} --gateway={} --nameserver={} --hostname={} --vlanid={} --addvmportgroup=1\n".format(i[1].value,i[2].value,i[3].value,i[4].value,i[5].value,i[0].value,int(i[6].value)))

    output.write('reboot --noeject\n')

    output.write('%firstboot --interpreter=busybox\n')
    if i[9].value != None:
        capacitydisks=i[9].value.split(',')
        for disk in capacitydisks:
            if disk!='':
                output.write('esxcli vsan storage tag add -t capacityFlash -d `esxcli storage core device list|grep -B 1 "Display Name:.*{}"|head -n 1`\n'.format(disk))

    output.write('esxcli network ip dns search add --domain={}\n'.format(i[11].value))

    output.write('esxcli network vswitch standard portgroup set -v {} -p "VM Network"\n'.format(int(i[6].value)))

    output.write('vim-cmd hostsvc/enable_ssh\n')

    ntps=i[10].value.split(',')
    for ntp in ntps:
        if ntp!='':
            output.write('echo "server {}" >> /etc/ntp.conf\n'.format(ntp))


    output.write('/sbin/chkconfig ntpd on\n')
    output.write('esxcli system settings advanced set -o /UserVars/HostClientCEIPOptIn -i {}\n'.format(i[13].value))
    if (i[14].value == "yes"):
        output.write('esxcli system settings advanced set -o "/Mem/AllocGuestLargePage" --int-value 0\n')
        output.write('esxcli system settings advanced set -o "/Mem/ShareForceSalting" --int-value 0\n')
    if (i[15].value == "yes"):
        output.write('esxcli vsan network ipv4 add -i {}\n'.format(i[1].value))
        output.write('esxcli vsan cluster new\n')
        output.write('esxcli vsan policy setdefault -c cluster -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1))"\n')
        output.write('esxcli vsan policy setdefault -c vdisk -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1))")"\n')
        output.write('esxcli vsan policy setdefault -c vmnamespace -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1))"\n')
        output.write('esxcli vsan policy setdefault -c vmswap -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1))"\n')
        output.write('esxcli vsan policy setdefault -c vmem -p "((\"hostFailuresToTolerate\" i0) (\"forceProvisioning\" i1))"\n')
    output.write('reboot\n')
    output.close()
    
    if os.path.isfile("{}{}/boot.cfg".format(iso_folder,i[16].value)):
        bootcfg=open("{}{}/boot.cfg".format(iso_folder,i[16].value),"r").read()
    elif os.path.isfile("{}{}/BOOT.CFG".format(iso_folder,i[16].value)):
        bootcfg=open("{}{}/BOOT.CFG".format(iso_folder,i[16].value),"r").read()
    else:
        os.system('7z x -y -o{}{} {}{}.iso'.format(iso_folder,i[16].value,iso_folder,i[16].value))
        os.system('find {} -type d -exec chmod o+rx {} \;'.format(iso_folder,'{}'))
        os.system("find {}{} -mindepth 3 -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;".format(iso_folder,i[16].value,'{}'))
        os.system("find {}{} -mindepth 2 -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;".format(iso_folder,i[16].value,'{}'))
        os.system("find {}{} -mindepth 1 -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;".format(iso_folder,i[16].value,'{}'))
        bootcfg=open("{}{}/boot.cfg".format(iso_folder,i[16].value),"r").read()

    
    boot=open("{}/boot.cfg".format(ks_folder),"w+")
    newboot=re.sub("/","",bootcfg,flags=re.M)
    newboot=re.sub(r'title=[^\n]*','title=Loading ESXi installer (https://github.com/oizone/esxihttp)',newboot,flags=re.M)
    newboot=re.sub(r'prefix=[^\n]*','prefix={}/{}/'.format(ws['B1'].value,i[16].value),newboot,flags=re.M)
    newboot=re.sub(r'kernelopt=[^\n]*','kernelopt={}'.format(ks),newboot,flags=re.M)
    boot.write(newboot)
    boot.close()


    if os.path.islink('{}/bootx64.efi'.format(ks_folder)):
        os.remove('{}/bootx64.efi'.format(ks_folder))

    if not os.path.exists('{}{}'.format(http_folder,i[16].value)):
        os.symlink('{}{}'.format(iso_folder,i[16].value),'{}{}'.format(http_folder,i[16].value))

    if os.path.isfile("{}{}/efi/boot/bootx64.efi".format(iso_folder,i[16].value)):
        os.symlink('{}{}/efi/boot/bootx64.efi'.format(iso_folder,i[16].value),'{}/bootx64.efi'.format(ks_folder))
    else:
        os.symlink('{}{}/EFI/BOOT/BOOTX64.EFI'.format(iso_folder,i[16].value),'{}/bootx64.efi'.format(ks_folder))

    

