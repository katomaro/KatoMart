import hashlib
import platform
import subprocess

def get_system_info():
    info = []
    try:
        if platform.system() != "Windows":
            with open('/etc/machine-id', 'r') as f:
                info.append(f.read().strip())
        else:
            cmd = 'wmic csproduct get uuid'
            uuid = subprocess.check_output(cmd).decode().split('\n')[1].strip()
            info.append(uuid)

        info.append(platform.processor())
        info.append(platform.node())

    except Exception as e:
        print(f"Error collecting system info: {e}")

    return info

def generate_hwid():
    system_info = get_system_info()
    hwid_raw = ('katomart;' + ';'.join(system_info)).encode('utf-8')
    # print(f"HWID Raw: {hwid_raw}")
    hwid_hashed = hashlib.sha256(hwid_raw).hexdigest()
    # print(f"HWID Hashed: {hwid_hashed}")
    return hwid_raw, hwid_hashed
