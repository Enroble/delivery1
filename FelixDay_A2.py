import pexpect

# Code to run inside of the enviroment

def commands(Connection, details):

    ip, user, passwd, enpassd = details


    Connection.sendline('enable')    # entering enable mode
    Connection.expect(['assword', pexpect.TIMEOUT, pexpect.EOF])
    
    Connection.sendline(enpasswd) # sending password
    result = Connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking if the password worked
        print("Error connecting: Unable to find enable prompt. Try checking the enable password")
        return
    
    Connection.sendline('show run')  # show the running config
    Connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])   # wait until its finished printing
    
    runningConfig = Connection.before

    Connection.sendline('show start') # show the startup config
    Connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])   # wait until its finished printing
    
    startupConfig = Connection.before

    print("""
    ----- Please select comparison mode -----

    1: Running_Config vs Startup_config
    2: Running_Config vs Local
    """)
    try:
        opt = int(input('>'))
        if opt<0 or opt>2: raise Exception
    except:
        opt = 0

    if opt == 1:
        for i, line in enumerate(runningConfig):
            if startupConfig[i] != line:
                print(f"'{line}' --> '{startupConfig[i]}'")
    elif opt == 2:
        with open('Running_Config.txt', 'r') as afile:
            localrun = afile.readlines()
            for i, line in enumerate(runningConfig):
                if localrun[i] != line:
                    print(f"'{line}' --> '{localrun[i]}'")
    else:
        print("Invalid Input")

    Connection.sendline('exit')
    Connection.close()
    return

# --SSH--

def ssh_con():
    print('----- SSH -----')
    
    # taking login details
    ip = '192.168.56.101'#input('Enter IP:\n>')
    user = 'prne'#input('Enter Username:\n>')
    passwd = 'cisco123!'#input('Enter SSH Password:\n>')
    enpasswd = 'class123!'#input('Enter Enable Password:\n>')
    
    details = (ip, user, passwd, enpasswd)

    Connection = pexpect.spawn('ssh ' + user + '@' + ip, encoding='utf-8', timeout=5) # spawning the session
    
    result = Connection.expect(['fingerprint', pexpect.TIMEOUT, pexpect.EOF])
    if result == 0:     # checking for keys
        print('key exchange: accepting..')
        Connection.sendline('yes')

    result = Connection.expect(['assword', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking for the password prompt 
        print("Error connecting: Unable to find password prompt")
        return      # end the function if theres a connection error
    
    Connection.sendline(passwd) # sending the password
    result = Connection.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking if the password worked
        print("Error connecting: Unable to find user prompt. Try checking the password")
        return
    commands(Connection, details)
    return

# Telnet

def telnet_con():
    print('----- Telnet -----')
    
    # taking login details
    ip = input('Enter IP:\n>')
    user = input('Enter Username:\n>')
    passwd = input('Enter User Password:\n>')
    enpasswd = input('Enter Enable Password:\n>')
    
    Connection = pexpect.spawn('telnet ' + ip, encoding='utf-8', timeout=20) # spawning the session
    
    result = Connection.expect(['sername', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking for the username prompt 
        print("Error connecting: Unable to find username prompt")
        return      # end the function if theres a connection error

    result = Connection.expect(['assword', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking for the password prompt 
        print("Error connecting: Unable to find password prompt")
        return      # end the function if theres a connection error
    
    Connection.sendline(passwd) # sending the password
    result = Connection.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:     # checking if the password worked
        print("Error connecting: Unable to find user prompt. Try checking the password")
        return
    commands(Connection)
    return

# ---- Menu ----

menu = {
    '1': 'SSH (Secure)',
    '2': 'Telnet (Insecure)',
    '3': 'exit'}

# function to print menu in a fancy way
def printMenu():
    print(
        '''\n----- Compare configs -----
        (please choose one option)\n''')

    for i in menu.keys():
        print (i, menu[i])
    
    try:
        opt = int(input('>')) # take user input
    except:
        opt = 0 # fail the condition checks

    # desipher input
    if opt == 1:
        ssh_con()
    elif opt == 2:
        telnet_con()
    elif opt == 3:
        print('closing..');exit(0)
    else:
        print('Er: selection outside of scope') # selection error message
    

printMenu()