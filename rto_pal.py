from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import matplotlib.pyplot as plt
from time import time
import numpy as np
import cv2



def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.22.0')
    rto = None
    try:
        # Adjust the VISA Resource string to fit your instrument
        rto = RsInstrument('TCPIP::192.168.1.22::INSTR', True, False)
        rto.visa_timeout = 20000  # Timeout for VISA Read Operations
        rto.opc_timeout = 20000  # Timeout for opc-synchronised operations
        rto.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {rto.idn_string}')
    print(f'Device Options: {",".join(rto.instrument_options)}\n')

    while True:
        # Get and plot binary data
        rto.write_str("FORMat:DATA REAL,32;:FORMat:BORDer LSBFirst")
        rto.bin_float_numbers_format = BinFloatFormat.Single_4bytes
        rto.data_chunk_size = 200000  # transfer in blocks of 100k bytes (default)
        data_bin = rto.query_bin_or_ascii_float_list("CHAN:DATA?")


        x = 0
        y = 0
        img = np.zeros((624,1600,1), np.uint8)

        for data in data_bin:
            sample = np.abs(np.float64(data))*255*8 + 0

            if sample <= 255 and sample >=0:
                value = 255 - sample
            elif sample > 255:
                value = 0
            elif sample <0:
                value = 255

            img[y, x] = value
            img[y+1, x] = value

            x = x + 1
            if (x >= 1600):
                x = 0
                y = y + 1*2
            if (y >= 312*2):
                y = 0

        cv2.imshow("PAL", img)
        if(cv2.waitKey(10)==27):
            break



    rto.close()



if __name__ == "__main__":
    main()
