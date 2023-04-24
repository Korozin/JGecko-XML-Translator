import re
import sys
import time
import colorama
import googletrans
import xml.etree.ElementTree as ET


# Set up graceful script exiting #
def exit_gracefully(signum=None, frame=None):
    print("\nExited")
    sys.exit(0)

try:
    # Try to use signal.SIGINT on Unix-based systems #
    import signal

    signal.signal(signal.SIGINT, exit_gracefully)
except (ImportError, AttributeError):
    try:
        # Try to use ctypes.windll.kernel32 on Windows #
        import ctypes

        kernel32 = ctypes.windll.kernel32

        # Enable Ctrl+C handling #
        kernel32.SetConsoleCtrlHandler(exit_gracefully, 1)
    except:
        print(f"{colorama.Fore.RED}[ERROR]:"
              f"{colorama.Fore.RESET} Failed to set up signal handling."
              f"Clean CTRL+C exiting not supported"


# Set XML names #
input_xml = 'input.xml'
output_xml = 'output.xml'


# Doing this to avoid encoding statement errors #
with open(input_xml, "r") as file:
    contents = file.read()

    # Define the regular expression pattern to search for #
    pattern = r"<\?xml version=\"1.0\"( encoding=\"(UTF-16|utf-16|UTF-8|utf-8|[Uu][Tt][Ff]-?8)\")?\s*\?>"

    # Replace any matches of the pattern with an empty string #
    cleaned_contents = re.sub(pattern, "", contents)

    # Write the cleaned contents back to the file #
    with open(input_xml, "w") as file:
        file.write(cleaned_contents)

# Properly close file #
file.close()


# create a translator object #
translator = googletrans.Translator()

# parse the XML file #
tree = ET.parse(input_xml)
root = tree.getroot()

# loop through each entry #
for entry in root.findall('entry'):
    name = entry.get('name')

    # translate the name attribute if it has Japanese text #
    if not all(ord(char) < 128 for char in name):
        try:
            translated_name = translator.translate(name, dest='en').text
            print(f"{colorama.Fore.MAGENTA}[LOG]: {colorama.Fore.RESET}Translating "
                  f"{colorama.Fore.YELLOW}'name' {colorama.Fore.RESET}"
                  f"tag: {colorama.Fore.YELLOW}'{name}'\n"
                  f"{colorama.Fore.RESET}       Translated to: "
                  f"{colorama.Fore.YELLOW}'{translated_name}'{colorama.Fore.RESET}\n")
            entry.set('name', translated_name)
        except Exception as error:
            print(f"{colorama.Fore.RED}[ERROR]:"
                  f"{colorama.Fore.RESET} Exception occured when translating"
                  f"{colorama.Fore.YELLOW} 'name'{colorama.Fore.RESET}"
                  f" : {colorama.Fore.MAGENTA}'{name}' {colorama.Fore.RESET}"
                  f"\nError type: '{colorama.Fore.YELLOW}{error}'\n"
                  f"{colorama.Fore.RESET}This is likely a fault of the API, not this script\n")
            continue

    # translate the comment tag if it has Japanese text #
    comment_element = entry.find('comment')
    if comment_element is not None:
        comment = comment_element.text
        if comment is not None and not all(ord(char) < 128 for char in comment):
            try:
                translated_comment = translator.translate(comment, dest='en').text
                print(f"{colorama.Fore.MAGENTA}[LOG]: {colorama.Fore.RESET}Translating "
                  f"{colorama.Fore.YELLOW}'comment' {colorama.Fore.RESET}"
                  f"tag: {colorama.Fore.YELLOW}'{comment}'\n"
                  f"{colorama.Fore.RESET}       Translated to: "
                  f"{colorama.Fore.YELLOW}'{translated_comment}'{colorama.Fore.RESET}\n")
                entry.find('comment').text = translated_comment
            except Exception as error:
                print(f"{colorama.Fore.RED}[ERROR]:"
                      f"{colorama.Fore.RESET} Exception occured when translating"
                      f"{colorama.Fore.YELLOW} 'comment'{colorama.Fore.RESET}"
                      f" : {colorama.Fore.MAGENTA}'{comment}' {colorama.Fore.RESET}"
                      f"\nError type: '{colorama.Fore.YELLOW}{error}'\n"
                      f"{colorama.Fore.RESET}This is likely a fault of the API, not this script\n")
                continue

    # translate the author tag if it has Japanese text #
    author_element = entry.find('authors')
    if author_element is not None:
        author = author_element.text
        if author is not None and not all(ord(char) < 128 for char in author):
            try:
                translated_author = translator.translate(author, dest='en').text
                print(f"{colorama.Fore.MAGENTA}[LOG]: {colorama.Fore.RESET}Translating "
                  f"{colorama.Fore.YELLOW}'author' {colorama.Fore.RESET}"
                  f"tag: {colorama.Fore.YELLOW}'{author}'\n"
                  f"{colorama.Fore.RESET}       Translated to: "
                  f"{colorama.Fore.YELLOW}'{translated_author}'{colorama.Fore.RESET}\n")
                entry.find('authors').text = translated_author
            except Exception as error:
                print(f"{colorama.Fore.RED}[ERROR]:"
                      f"{colorama.Fore.RESET} Exception occured when translating"
                      f"{colorama.Fore.YELLOW} 'author'{colorama.Fore.RESET}"
                      f" : {colorama.Fore.MAGENTA}'{author}' {colorama.Fore.RESET}"
                      f"\nError type: '{colorama.Fore.YELLOW}{error}'\n"
                      f"{colorama.Fore.RESET}This is likely a fault of the API, not this script\n")
                continue

# write the modified XML to a new file #
tree.write(output_xml)

# notify the user on completion #
print(f"{colorama.Fore.MAGENTA}[LOG]: '{colorama.Fore.YELLOW+input_xml}' "
      f"{colorama.Fore.RESET}saved to '{colorama.Fore.YELLOW+output_xml}'{colorama.Fore.RESET}")
