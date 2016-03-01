import subprocess

def system(cmd):
    """
    Invoke a shell command.

    :returns: A tuple of output, err message, and return code
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out, err, ret.returncode


def if_atomic():
    "Tries to identify atomic image."
    out, err, eid = system('stat /run/ostree-booted')
    if eid != 0:
        return False
    return True

def if_netname_traditional():
    "Identify classic network interface naming convention"
    out, err, eid = system('cat /proc/cmdline')
    out = out.decode('utf-8')
    if "net.ifnames=0" in out:
        return True
    return False


def if_vagrant():
    "Checks if system has vagrant user"
    with open('/etc/passwd', 'r') as fobj:
        for line in fobj:
            if '/bin/bash' in line:
                user = line.split(':')[0]
                if 'vagrant' in user:
                    return True
    return False
