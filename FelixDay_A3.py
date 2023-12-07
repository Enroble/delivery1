from netmiko import ConnectHandler # netmiko used to connect to remote hosts

# main
def __main__():

    print('\r----| Task A3 - Please enter device info |----\n')

    while True:
        global device_info # collecting device info
        device_info = {
        'device_type': 'cisco_ios',
        'host':   input('Address:\n>'),
        'username': input('Username:\n>'),
        'password': input('Password:\n>'),
        #'port' : int(input('Open ports:\n>')),
        'secret': input('Secret password: (leave blank for none)\n>'),
        }
        #except: print('\n!!! Error! Bad port number! !!!\n'); continue
        
        print('\r')
        for i in device_info.keys():print(i,'-->', device_info[i])
        
        if (input('\nIs the above information correct?\n(y/n) >')) == 'y':
            break
    while True: printMenu()


# commands
def conFunction():
    print('connecting -->',device_info['host'])
    #try:
    remCon = ConnectHandler(**device_info)
    #except: print('\n!!! Error! Connection error! !!!'); return
    
    remCon.enable()
    if remCon.check_enable_mode() == False:
        print('\n!!! Error! Unable to enter enable! !!!'); return
    
    print('Connection Success!')

    while True:
        print ('\n----| Choose action |----\n(please choose one option)\n')
        menu = {'1': 'Configure a loopback and another interface with an IP address','2': 'Configure OSPF','3': 'Disconnect'}

        for i in menu.keys():
            print (i, menu[i])
        try:
            opt = int(input('>')) # take user input
        except:
            opt = 0 # fail the condition checks

        if opt == 1:
            remCon.send_config_set([
                'interface loopback 1',
                'ip addr 192.168.20.1 255.255.255.0',
                'no shut',
                'interface g0/0/2'
                'ip addr 192.168.10.1 255.255.255.0',
                'no shut',
                'ip routing'
            ])

        elif opt == 2:
            remCon.send_config_set([
                'router eigrp 1',
                'network 192.168.10.0'
            ])

        elif opt == 3:
            print('closing connection..'); remCon.disconnect(); return

        else:
            print('Er: selection outside of scope') # selection error message


# menu
def printMenu():
    while True:
        menu = {'1': 'SSH (Secure)','2': 'Telnet (Insecure)','3': 'exit'}

        print('''\n----| Please choose how to connect |----\n(please choose one option)\n''')

        for i in menu.keys():
            print (i, menu[i])

        try:
            opt = int(input('>')) # take user input
        except:
            opt = 0 # fail the condition checks

        # desipher input
        if opt == 1:    # ssh param
            conFunction()
        elif opt == 2:  # telnet param
            device_info['device_type'] = 'cisco_ios_telnet'
            conFunction()
        elif opt == 3:
            print('closing..');exit(0)
        else:
            print('Er: selection outside of scope') # selection error message
    

if __name__ == '__main__': __main__()