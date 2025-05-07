import re
import json

def get_data_with_valid_header(data):
    if data is None:
        return None

    # Normalize line endings: remove all carriage returns (\r),
    # data degrean double CR
    # data = re.sub(r'\r+', '\n', data)
    # # Collapse multiple blank lines
    # data = re.sub(r'\n+', '\n', data)
    data = data.replace('\r', '')
    
    pattern = r'^[A-Z]{4}\d{2}\s[A-Z]{4}\s\d{6}(?:\s[A-Z]{3})?$'
    data_line = data.splitlines()

    for i, line in enumerate(data_line):
        line = line.strip()
        if re.match(pattern, line):
            data_line[i] = line
            # result = "\n".join(l for l in data_line[i:] if l.strip())
            result = "\n".join(data_line[i:])
            if i != 0:
                log_data = {
                    "event": "Correcting data",
                    "data": result,
                    "note": "Data diubah karena header tidak valid"
                }
                print(json.dumps(log_data))

            return result

    return None


print(get_data_with_valid_header("0001030123\r\nSMID61 ABCD 000000\r\n           asdasfasv asdasasd\nafasddsdfsd"))

print(get_data_with_valid_header("0001030123\r\nSMID61 ABCD 000000              \r\nasdasfasv asdasasd\nafasddsdfsd"))

print(get_data_with_valid_header("0001030123\r\nSMID61 ABCD 000000 CCA\r\r\nasdasfasv asdasasd\nafasddsdfsd"))

print(get_data_with_valid_header("0001030123\r\nSMID61 ABCD 000000Z\r\nasdasfasv asdasasd\nafasddsdfsd"))

print(get_data_with_valid_header("0001030123\r\nSMID61 ABCD 000000 asdasvasd\r\nasdasfasv asdasasd\nafasddsdfsd"))

print(get_data_with_valid_header("""0000010201
SAID32 WADL 060600
METAR WADL 060600Z 14012KT 8000 FEW015CB SCT016 31/24 Q1008 NOSIG RMK CB TO N="""))

print(get_data_with_valid_header(None))
print(get_data_with_valid_header('s'))
print(get_data_with_valid_header('\n\n\n\n\n\n\n\n\n'))

print(repr(get_data_with_valid_header("0000008101\r\r\nSAID32 WADL 061400\r\r\nMETAR WADL 061400Z 00000KT 7000 SCT016 25/24 Q1011 NOSIG=")))