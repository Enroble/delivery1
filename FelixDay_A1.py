import pexpect

# Code to run inside of the enviroment

def commands():
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

    with open('running_config.txt', 'w') as afile:
        afile.write(Connection.before)   # writing the telnet output from before the last expect 
        afile.close()
        print('Running config saved to "running_config.txt"\nGracefully closing connection..')
    Connection.sendline('exit')
    Connection.close()
    return

# --SSH--

def ssh_con():
    print('----- SSH -----')
    
    # taking login details
    ip = input('Enter IP:\n>')
    user = input('Enter Username:\n>')
    passwd = input('Enter SSH Password:\n>')
    enpasswd = input('Enter Enable Password:\n>')
    
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
    commands()
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
    commands()
    return

# ---- Menu ----

menu = {
    '1': 'SSH (Secure)',
    '2': 'Telnet (Insecure)',
    '3': 'exit'}

# function to print menu in a fancy way
def printMenu():
    print(
        '''\n----- Program to retrive running_config -----
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