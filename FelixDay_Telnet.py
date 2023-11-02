import pexpect

# --SSH--
def ssh_con():
    print('----- SSH -----')

    ip = input('Enter IP:\n>')
    user = input('Enter Username:\n>')
    passwd = input('Enter Password:\n>')

    print(connection['ip'])
    sshConnection = pexpect.spawn('ssh ' + user + '@' + ip, encoding='utf-8', timeout=20)
    

# --Ask for connection type--

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
        pass
    elif opt == 3:
        print('closing..');exit(0)
    else:
        print('Er: selection outside of scope') # selection error message
    

printMenu()