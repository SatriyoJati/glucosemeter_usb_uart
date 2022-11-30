import usb.core
import usb.util
import struct
import sys

dev = usb.core.find(idVendor = 0x0483 , idProduct = 0x5750)
i = dev[0].interfaces()[0].bInterfaceNumber

if dev is None :
    raise ValueError("The device not found")

if dev.is_kernel_driver_active(i):
    try:
        dev.detach_kernel_driver(i)
    except usb.core.USBError as e:
        sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))

dev.set_configuration()

# cfg = dev.get_active_configuration()
# for cfg in dev:
#     sys.stdout.write(str(cfg.bConfigurationValue) + '\n')

for cfg in dev:
    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
    print(cfg)
    for intf in cfg:
        sys.stdout.write('\t' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
    
        print(intf)
        for ep in intf:
            sys.stdout.write('\t\t' + \
                             str(ep.bEndpointAddress) + \
                             '\n')
            print("-----------------+++++++----------------")
            
            print(ep)

#Constructing payload
'''
PAYLOAD : 
STX - SIZE - ~SIZE - COMMAND - DATA - CKL - CKH
0x80 - N+1 - ~(N+1) - see below - see below - CKL - CKH
'''

stx = b'\x80'  #start transmission
data = b'\x00' #no data
command = b'\x00' #request total value
size = 2 #Number of command + data
size_neg = ~(size) #invert of size

#Convert
size_bytes = size.to_bytes(1, byteorder='little', signed = False)
size_neg_bytes = size_neg.to_bytes(1, byteorder = 'little', signed = True)

ckl = ~(int.from_bytes(stx, "little"))^(~size)^(int.from_bytes(data, "little")) #checksum low
ckh = ~(size^(int.from_bytes(command, 'big'))^0)#checksum high

msg = stx + size_bytes  + size_neg_bytes + command + data + ckl.to_bytes(1, byteorder = 'big', signed = False) + ckh.to_bytes(1, byteorder = 'big', signed = True)

print(msg)

# size_neg = struct.pack("<i", size_neg)
# ckh = struct.pack("<i", ckh)

# byte_msg = []
# # for i in msg:
# #     if isinstance(i, int):
# #         i.to_bytes(2,'big')
# #         byte_msg.append(i)
# #     else :
# #         byte_msg.append(i)

print("output {} ".format(msg))

# endpoint = dev[0].interfaces()[0].endpoints()[0]
# new_msg = byte_msg + b'\x00' * (64 - len(byte_msg))
dev.write(0x1, msg, 100)
print(len(msg))

# assert dev.ctrl_transfer(0x40, CTRL_LOOPBACK_WRITE, 0, 0, msg) == len(msg)
ret = dev.ctrl_transfer(0xC0,0x01, 0x00, 0, 9)
print(ret)