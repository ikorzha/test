 #!/usr/bin/env python3
# Copyright (C) 2017, 2018 Vasily Galkin (galkinvv.github.io)
# This file may be used and  redistributed accorindg to GPLv3 licance.
import sys, os, mmap, math, random, datetime, time
import subprocess
os.system("")
#sys.tracebacklimit=0
random.seed(12111)
archtser = 1 #=0 arch/=1 tserver
frtest=0
frmin="150"
freq="200"
chlist=" "
passed = []
faultychips = 0
class color():
    RED = '\033[31m'
    GREEN='\033[32m'
    YELLOW='\033[33m'
    WHITE='\033[37m'
amaifost = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
chiperrors = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
try:
 p= subprocess.Popen(['./590/agt', '-ppmode=1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
 qqq=str(p).split('\\n')
 for i in range(len(qqq)):
  print(qqq[i])
 p= subprocess.Popen(['./590/agt', '-mcchannel'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
 qqq=str(p).split('\\n')
 for i in range(len(qqq)):
  if "=" in qqq[i]:
   chlist=qqq[i]
 qqq=chlist.split(' ')
 chlist=qqq[2]
# print(chlist)
 p= subprocess.Popen(['./590/agt', '-pplist=short'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
 bbb="ooo"
 ccc="ooo"
 qqq=str(p).split('\\n')
 for i in range(len(qqq)):
  if "High" in qqq[i]:
 #  print("aaas")
   bbb=qqq[i]
 # print(qqq[i])
 aaa=bbb.split(',')
 for i in range(len(aaa)):
#  print(aaa[i])
  if "MEM =" in aaa[i]:
   bbb=aaa[i]
 aaa=bbb.split(' ')
 for i in range(len(aaa)):
  if i==3:
   bbb=aaa[i]
#low val
 qqq=str(p).split('\\n')
 for i in range(len(qqq)):
  if "Low" in qqq[i]:
 #  print("aaas")
   ccc=qqq[i]
 # print(qqq[i])
 aaa=ccc.split(',')
 for i in range(len(aaa)):
#  print(aaa[i])
  if "MEM =" in aaa[i]:
   ccc=aaa[i]
 aaa=ccc.split(' ')
 for i in range(len(aaa)):
  if i==3:
   frmin=aaa[i]
 
# print(sys.argv[4])
 if len(sys.argv)>4:
  freq=str(sys.argv[4])
  if int(freq)>int(bbb):
   print("error your value is bigger tham maximum frequency allowed for your card so this test will run with maximim allowed:"+bbb)
   freq=bbb
 #print(int(freq))
 #print(int(bbb))

#  print(freq)
 print(color.GREEN+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Memory freqency for your card<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<") 
 print(color.YELLOW+"Min value= "+frmin+"Mhz and max value= "+bbb+"Mhz")
 print(color.WHITE)
# p= subprocess.Popen(['./590/agt', '-vddc='+bbb], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
# p= subprocess.Popen(['./590/agt', '-mem=400'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
# p= subprocess.Popen(['./590/agt', '-clkstatus'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
# print(str(p))
except:
 print("err pplist")
 sys.exit()
#try:
# p= subprocess.Popen(['./590/agt', '-ppstatus'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
# qqq=str(p).split('\\n')
# for i in range(len(qqq)):
#  print(color.YELLOW+qqq[i])
#except:
# print("error ppstatus")
#sys.exit()

#if archtser==1:
# p = subprocess.Popen(['uname', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
# name=str(p)
# print(name)
# if "5.4" not in name:
#  print(color.RED+"Please select first option at boot if you want to test with dmgg")
#  print(color.WHITE)
  #sys.exit()
if int(sys.argv[2])>256:
 print("Size of test memory exceed 256MB it may get stuck!!!")
# sys.exit()
print(color.GREEN+"Detected AMD GPU card:")
bbb=""
#q=subprocess.call(['./db32',''])
p = subprocess.Popen(['lspci', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
aaa=str(p).split("\\n\\n")
for i in range(len(aaa)):
 if  "VGA" in aaa[i]:
  if "AMD" in aaa[i]:
   bbb=bbb+aaa[i]
ccc=bbb.split("\\n\\t")
vvv=""
for i in range(len(ccc)):
 print(ccc[i])
 if "Memory" and " pref" in ccc[i]:
  qqq=ccc[i].split(" ")
  if not vvv:
   vvv=vvv+" "+qqq[2]
print()
print()
if not vvv:
 print(color.RED+"No AMD gpu detected in system!!! Exit")
 print(color.WHITE)
 sys.exit()
print(color.YELLOW+"Possible GPU address: "+vvv)
print(color.WHITE)
if "100" in str(sys.argv[3]):
 sys.exit()
def run_test():
    if len(sys.argv) < 2: raise Exception("Usage: " + sys.argv[0] + " C8000000 [mb_to_test]")
    offset = int(sys.argv[1], 16) 
    if len(sys.argv) > 3:
      nbchips = int(sys.argv[3], 10)
    else:
      nbchips = 8
      print("default 8 chips no value in command line received from user") 
    print("number of chips is set to:",nbchips)
    if len(sys.argv) > 4:
      frtest=1
    else:
     frtest=0 
    if len(sys.argv) >= 3:
      bytes_to_test = int(1024 * 1024 * float(sys.argv[2]))
    else:
      bytes_to_test = 1024 * 1024 * 32 // 8
    physmem = os.open("/dev/" + os.environ.get("MEM","mem"), os.O_RDWR, 777)
    #physmem = os.open("/dev/fb0", os.O_RDWR)
    phys_arr = mmap.mmap(physmem, bytes_to_test, offset=offset)
    #with open("/tmp/in", "rb") as binin: phys_arr[:]=binin.read() and sys.exit(0)
    #with open("/tmp/out", "wb") as binout: binout.write(phys_arr) and sys.exit(0)
    def bin8(byte):
        return "0b{:08b}".format(byte)
    def verify_no_errors_with_data(data, test_name):
        global faultychips
        if len(phys_arr) > len(data):
            data += b'\x00' * (len(phys_arr) - len(data))
        print("This test is working to detect bad chips. Warning it can give wrong faulty chip number ; only the amount of faulty chips will be good")
        print("count the chips counter-clockwise from right to left with pcie near you")
        phys_arr[:]=data
        data_possibly_modified = phys_arr[:]
        time.sleep(0.5)
        #os.system("setfont")
        bad_addresses = {}
        all_errors = []
        firstbadadress=0
        bad_bits = [0]*8
        print(color.RED)
        for i in range(len(data)):
            xored_error = data[i] ^ data_possibly_modified[i]
            #if i>1 and i<500:
            # xored_error=1 #test
            if xored_error:
              #  print("Error at address: " , i)
               # print("\n")
                for a in range(nbchips):
                 #print("i=",hex(i))
                 #print("a=",a)
                 if a==(i//256)%nbchips:#if i>=a*256*(1+int(i/(256*nbchips))) and i<(a+1)*256*(1+int(i/(256*nbchips))):
                 # print("i=",i)
                 # print("a=",a)
                 # print("v1=",a*256*(1+int(i/(256*nbchips))))
                 # print("v2=",(a+1)*256*(1+int(i/(256*nbchips))))
                  if nbchips>8:
                   if (a==0  ):
                    if (amaifost[0]==0) : 
                     amaifost[0]=1 
                     faultychips=faultychips+1
                     print("chip 5 is faulty at address: ",i) 
                    chiperrors[5]=chiperrors[5]+1
                   if (a==1  ):
                    if (amaifost[1]==0) : 
                     amaifost[1]=1 
                     faultychips=faultychips+1
                     print("chip 7 is faulty at address: ",i) 
                    chiperrors[7]=chiperrors[7]+1
                   if (a==2  ):
                    if (amaifost[2]==0) : 
                     amaifost[2]=1 
                     faultychips=faultychips+1
                     print("chip 6 is faulty at address: ",i) 
                    chiperrors[6]=chiperrors[6]+1
                   if (a==3  ):
                    if (amaifost[3]==0) : 
                     amaifost[3]=1 
                     faultychips=faultychips+1
                     print("chip 8 is faulty at address: ",i) 
                    chiperrors[8]=chiperrors[8]+1
                   if (a==4  ):
                    if (amaifost[4]==0) : 
                     amaifost[4]=1 
                     faultychips=faultychips+1
                     print("chip 3 is faulty at address: ",i) 
                    chiperrors[3]=chiperrors[3]+1
                   if (a==5  ):
                    if (amaifost[5]==0) : 
                     amaifost[5]=1 
                     faultychips=faultychips+1
                     print("chip 1 is faulty at address: ",i) 
                    chiperrors[1]=chiperrors[1]+1
                   if (a==6  ):
                    if (amaifost[6]==0) : 
                     amaifost[6]=1 
                     faultychips=faultychips+1
                     print("chip 4 is faulty at address: ",i) 
                    chiperrors[4]=chiperrors[4]+1
                   if (a==7  ):
                    if (amaifost[7]==0) : 
                     amaifost[7]=1 
                     faultychips=faultychips+1
                     print("chip 2 is faulty at address: ",i) 
                    chiperrors[2]=chiperrors[2]+1
                   if (a==8  ):
                    if (amaifost[8]==0) : 
                     amaifost[8]=1 
                     faultychips=faultychips+1
                     print("chip 11 is faulty at address: ",i) 
                    chiperrors[11]=chiperrors[11]+1
                   if (a==9  ):
                    if (amaifost[9]==0) : 
                     amaifost[9]=1 
                     faultychips=faultychips+1
                     print("chip 9 is faulty at address: ",i) 
                    chiperrors[9]=chiperrors[9]+1
                   if (a==10  ):
                    if (amaifost[10]==0) : 
                     amaifost[10]=1 
                     faultychips=faultychips+1
                     print("chip 12 is faulty at address: ",i) 
                    chiperrors[12]=chiperrors[12]+1
                   if (a==11  ):
                    if (amaifost[11]==0) : 
                     amaifost[11]=1 
                     faultychips=faultychips+1
                     print("chip 10 is faulty at address: ",i) 
                    chiperrors[10]=chiperrors[10]+1
                   if (a==12  ):
                    if (amaifost[12]==0) : 
                     amaifost[12]=1 
                     faultychips=faultychips+1
                     print("chip 13 is faulty at address: ",i) 
                    chiperrors[13]=chiperrors[13]+1
                   if (a==13  ):
                    if (amaifost[13]==0) : 
                     amaifost[13]=1 
                     faultychips=faultychips+1
                     print("chip 15 is faulty at address: ",i) 
                    chiperrors[15]=chiperrors[15]+1
                   if (a==14  ):
                    if (amaifost[14]==0) : 
                     amaifost[14]=1 
                     faultychips=faultychips+1
                     print("chip 14 is faulty at address: ",i) 
                    chiperrors[14]=chiperrors[14]+1
                   if (a==15  ):
                    if (amaifost[15]==0) : 
                     amaifost[15]=1 
                     faultychips=faultychips+1
                     print("chip 16 is faulty at address: ",i) 
                    chiperrors[16]=chiperrors[16]+1
                  if nbchips==8:
                   if (a==0  ):
                    if (amaifost[0]==0) : 
                     amaifost[0]=1 
                     faultychips=faultychips+1
                     print("chip 3 is faulty (possible 4) at address: ",i) 
                    chiperrors[3]=chiperrors[3]+1
                   if (a==1  ):
                    if (amaifost[1]==0) : 
                     amaifost[1]=1 
                     faultychips=faultychips+1
                     print("chip 4 is faulty (possible 3) at address: ",i) 
                    chiperrors[4]=chiperrors[4]+1
                   if (a==2  ):
                    if (amaifost[2]==0) : 
                     amaifost[2]=1 
                     faultychips=faultychips+1
                     print("chip 1 is faulty (possible 2) at address: ",i) 
                    chiperrors[1]=chiperrors[1]+1
                   if (a==3  ):
                    if (amaifost[3]==0) : 
                     amaifost[3]=1 
                     faultychips=faultychips+1
                     print("chip 2 is faulty (possible 1) at address: ",i) 
                    chiperrors[2]=chiperrors[2]+1
                   if (a==4  ):
                    if (amaifost[4]==0) : 
                     amaifost[4]=1 
                     faultychips=faultychips+1
                     print("chip 5 is faulty (possible 6) at address: ",i) 
                    chiperrors[5]=chiperrors[5]+1
                   if (a==5  ):
                    if (amaifost[5]==0) : 
                     amaifost[5]=1 
                     faultychips=faultychips+1
                     print("chip 6 is faulty (possible 5) at address: ",i) 
                    chiperrors[6]=chiperrors[6]+1
                   if (a==6  ):
                    if (amaifost[6]==0) : 
                     amaifost[6]=1 
                     faultychips=faultychips+1
                     print("chip 7 is faulty (possible 8) at address: ",i) 
                    chiperrors[7]=chiperrors[7]+1
                   if (a==7  ):
                    if (amaifost[7]==0) : 
                     amaifost[7]=1 
                     faultychips=faultychips+1
                     print("chip 8 is faulty (possible 7) at address: ",i) 
                    chiperrors[8]=chiperrors[8]+1    
                if not bad_addresses:
                    firstbadadress=hex(i)
                   # print("first error detected at " + hex(i))
                #addr_file.write("{:08x}".format(i)+"\n")
                if xored_error not in bad_addresses:
                    bad_addresses[xored_error] = [0, []]
                bad_addresses[xored_error][0] += 1
                all_addresses = bad_addresses[xored_error][1]
                if 1:
                    for b in range(8):
                        if xored_error & (1<<b): bad_bits[b] += 1
                if 1:    
                    if len(all_addresses) < 0x4000:
                        all_addresses.append(i)
                    if len(all_errors) < 0x4000:
                        all_errors.append(i)
        for eee in range(17):
         if chiperrors[eee]>0:
          print("For chip "+str(eee)+" we tested "+str(int(bytes_to_test/nbchips))+" bytes and the number of errors for this chip is:",chiperrors[eee])
        if not bad_addresses:
            passed.append(test_name)
            print(color.GREEN+"No faulty chips found")
            print(color.WHITE)
           # return
        print(color.WHITE)
    def verify(data):
        for i in range(len(data)):
            xored_error = data[i] ^ data_possibly_modified[i]
            #if i>1 and i<500:
            # xored_error=1 #test
            if xored_error:
                print(color.RED+"Error at address: " , i)
                break
        def totals():
             global faultychips
             total_errors =  sum((v[0] for k, v in bad_addresses.items()))
             print("number of faulty chips= ",faultychips)      
             print("Total bytes tested: " + str(len(data)))
             print("Total errors count: ", total_errors, " - every ", len(data)/(total_errors+1), " OK: ", len(data) - total_errors)
       # totals()
    #    raise Exception("ERRORS found in test " + test_name)
    #verify_no_errors_with_data(b'\xFF'*len(phys_arr), "ONEs")
    #verify_no_errors_with_data(b'\x00'*len(phys_arr), "ZERO")
    #verify_no_errors_with_data(b'\x00'*len(phys_arr), "ZERO")
    #verify_no_errors_with_data(b'\xCC'*len(phys_arr), "xCC")
    #verify_no_errors_with_data(b'\x55'*len(phys_arr), "x55")
    #verify_no_errors_with_data(b'\xaa'*len(phys_arr), "xaa")
    #verify_no_errors_with_data(b'\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x46\xa3\xe5\x13\xad'*(len(phys_arr)//13), "special")
    #verify_no_errors_with_data(b'\x55\xaa\x55'*(len(phys_arr)//3), "aa55")
    if  frtest==1:
     print("Warning use this test if you dont get errors in normal test: Each chip will be tested at requested frequency; if pc is stuck at some chip and needs reset this CAN be that chip fails test" )
     data=bytes(random.getrandbits(8) for i in range(len(phys_arr)))
     if len(phys_arr) > len(data):
        data += b'\x00' * (len(phys_arr) - len(data))
     for j in range(nbchips):
      if(j==0):eee="A0"
      if(j==1):eee="A1"
      if(j==2):eee="B0"
      if(j==3):eee="B1"
      if(j==4):eee="C0"
      if(j==5):eee="C1"
      if(j==6):eee="D0"
      if(j==7):eee="D1"
      if(j==8):eee="E0"
      if(j==9):eee="E1"
      if(j==10):eee="F0"
      if(j==11):eee="F1"
      if(j==12):eee="G0"
      if(j==13):eee="G1"
      if(j==14):eee="H0"
      if(j==15):eee="H1"
      print("Testing chip "+str(j+1)+" CH:"+eee+" at freq: "+freq+"Mhz")
      p= subprocess.Popen(['./590/agt', '-mcchannel='+eee], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
      p= subprocess.Popen(['./590/agt', '-mem='+freq], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#do the magic
      phys_arr[:]=data
      data_possibly_modified = phys_arr[:]
     # time.sleep(1)
      for i in range(len(data)):
            xored_error = data[i] ^ data_possibly_modified[i]
            if xored_error:
                print(color.RED+"Error at address: " , i)
                break

      p= subprocess.Popen(['./590/agt', '-mem='+frmin], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0] 
      p= subprocess.Popen(['./590/agt', '-mcchannel='+chlist], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
      print(color.GREEN+"Done"+color.WHITE)

 #    p= subprocess.Popen(['./590/agt', '-mcchannel='+chlist], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
     print("Test done")
     sys.exit()

    verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
    #verify_no_errors_with_data(bytes(random.getrandbits(8) for i in range(len(phys_arr))), "rand")
try:
    for i in range(1):
        run_test()
finally:
     print(color.YELLOW+"\n\nUsage:\npython3 ./dmmg.py b0000000 1 16  \nScript file dmmg.py is on root of the USB if you need to edit ; run lspci -v to find address of your ati card default is b0000000 \n 1 is 1MB of memory \n 16 is the number of memory chips from the card")
     print(color.WHITE+"")
