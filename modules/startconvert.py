from modules.IPMD_conversion import conversion
import glob
import os
import re
import pandas as pd


def start_conversion(filepath, start_number):
    error_file = ''
    output_array = []
    #for f in glob.glob(filepath + '/**/*.*', recursive=True):
    for f in glob.glob(filepath + '/*.*'):
        print(f)
        #print(str(start_number))
        head, tail = os.path.split(f)
        if re.search(r'^\d+ \w+.\w+$', tail) is not None:
        # for standard
            photo_id = re.findall(r'\d+', tail)[0]
        else:
        # for non standard
            photo_id = str(start_number)
        start_number += 1
        try:
            emotion = re.findall(r' ([A-Za-z]+)\.', tail)[0]
        except IndexError:
            emotion = 'Need to check'
        #result = pool.apply_async(conversion, (f,))
        #result.get()
        try:
            temp_output = conversion(f)
            output_array.append([photo_id, temp_output, emotion, tail])
            # if cannot convert, temp_output == None
            if temp_output is None:
                error_file += f + ': fail to find the front face\n'
        except:
            error_file += f + ': fail to find the front face\n'
            print('error')
    #pool.close()
    output_pd = pd.DataFrame(output_array, columns =['id', 'pixels', 'emotion', 'original_file'])
    return output_pd, error_file