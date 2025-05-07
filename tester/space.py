from datetime import datetime, timezone
import os
import uuid
import base64

def generate_short_alphanumeric_uuid(length=8):
    # Generate a random UUID
    full_uuid = uuid.uuid4()
    # Convert the UUID to bytes
    uuid_bytes = full_uuid.bytes
    # Encode the bytes to Base64
    short_uuid = base64.b64encode(uuid_bytes).decode('utf-8')
    # Remove non-alphanumeric characters (including padding)
    short_uuid = ''.join(filter(str.isalnum, short_uuid))
    # Limit the length of the resulting UUID
    return short_uuid[:length]  # Adjust the length as needed

def create_file(message):
    import re

    base_path = '.'
    nama_file = f"{base_path}/"

    try:
        ttaaii = message[:6].replace(' ', '')
        cccc = message[7:11].replace(' ', '')
        
        if ttaaii != '' and cccc != '':
            ttaaii_cccc = f'{ttaaii}_{cccc}_'
            ttaaii_cccc = re.sub(r'[^a-zA-Z0-9._-]', '', ttaaii_cccc)
            nama_file += ttaaii_cccc
    except:
        pass
    
    dts = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    nama_file += f'{dts}_{generate_short_alphanumeric_uuid()}.X.tmp2'
    with open(nama_file, 'w') as f:
        f.write(message)

    # Optionally rename the file (e.g., add a suffix)
    new_filename = nama_file.replace('.tmp2', '.tmp')
    os.rename(nama_file, new_filename)
    
    return new_filename



create_file('''WOID41 
            WIII 101345
            WIII AD WRNG 2 VALID 101345/101600 SFC WSPD 17KT MAX 29 FCST NC=''')
