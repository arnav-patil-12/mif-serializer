import os
import re


def serialize_mif(input_file, output_file):
    print("Reformatting MIF file...")

    # attempt to open file and re-prompt user if not found
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        print("MIF found...")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return False

    depth = None
    width = None
    original_mif_lines = []
    in_content = False

    # read each line in the MIF
    for line in lines:
        if "Depth" in line:
            depth = int(re.search(r'\d+', line).group())
        elif "Width" in line:
            width = int(re.search(r'\d+', line).group())
        elif line.strip().lower() == "content":
            in_content = True
        elif in_content:
            original_mif_lines.append(line.strip())

    if (depth is None) or (width is None):
        print("Bad MIF Error: Could not find DEPTH or WIDTH.")
        return False

    # parse data
    print("Parsing MIF...")
    data_dict = {}
    for line in original_mif_lines:
        if line.lower() in {"begin", "end;"}:
            continue
        if "[" in line and "]" in line:
            match = re.match(r'\[(\d+)\.\.(\d+)\]\s*:\s*(.+);', line)  # god bless ChatGPT
            if match:
                start, end, data = int(match.group(1)), int(match.group(2)), match.group(3).split()
                for i in range(start, end + 1):
                    data_dict[i] = data[0]
        else:
            match = re.match(r'(\d+)\s*:\s*(.+);', line)  # more ChatGPT
            if match:
                address, data = int(match.group(1)), match.group(2).split()
                for i, value in enumerate(data):
                    data_dict[address + i] = value

    # prompt user for address radix
    print("Serialize with decimal \"DEC\" or hexadecimal \"HEX\" address radix? >>> ", end="")
    address_format = input().strip().lower()
    if address_format not in {"hex", "dec"}:
        print("Invalid address radix. Please enter either 'HEX' or 'DEC'")
        return False

    # write the new MIF
    print("Writing formatted MIF...")
    header = [
        f"WIDTH = {width};",
        f"DEPTH = {depth};",
        "ADDRESS_RADIX = HEX;" if address_format == "hex" else "ADDRESS_RADIX = DEC;",
        "DATA_RADIX = BIN;",
        "",
        "CONTENT",
        "BEGIN"
    ]
    content = []

    for addr in range(depth):
        value = data_dict.get(addr, "000")
        if address_format == "hex":
            addr_str = f"{addr:X}"  # convert to hexadecimal
        else:
            addr_str = f"{addr}"  # keep in decimal format
        content.append(f"{addr_str:<4}: {value};")

    footer = ["END;"]

    with open(output_file, 'w') as file:
        file.write("\n".join(header) + "\n")
        file.write("\n".join(content) + "\n")
        file.write("\n".join(footer) + "\n")

    print(f"MIF successfully serialized and stored in '{output_file}'!")
    return True


# main loop
while True:
    print("Enter input file name (or 'Q' to quit) >>> ", end="")
    in_file = input().strip()
    if in_file.lower() == 'q':
        print("Exiting program.")
        break

    if not os.path.isfile(in_file):
        print(f"Error: File '{in_file}' does not exist. Please try again.")
        continue

    print("Enter output file name: ", end="")
    out_file = input().strip()

    if serialize_mif(in_file, out_file):
        print("Conversion completed successfully.")
    else:
        print("Conversion failed. Please try again.")
