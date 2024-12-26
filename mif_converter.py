import re


# function implementations
def serialize_mif(input_file, output_file):
    print("Reformatting MIF file...")
    with open(input_file, 'r') as file:
        lines = file.readlines()  # had to check 106 notes for this
    print("MIF file found...")
    # STOP USING SEMICOLONS
    depth = None
    width = None
    original_mif_lines = []
    in_content = False

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
        raise ValueError("Bad MIF Error: Could not find DEPTH or WIDTH.")

    # start parsing data
    print("Parsing MIF...")
    data_dict = {}
    for line in original_mif_lines:
        if line.lower() in {"begin", "end;"}:
            continue
        # had to make gpt format the patterns
        if "[" in line and "]" in line:
            match = re.match(r'\[(\d+)\.\.(\d+)\]\s*:\s*(.+);', line)  # god bless ChatGPT
            if match:
                start, end, data = int(match.group(1)), int(match.group(2)), match.group(3).split()
                for i in range(start, end + 1):
                    data_dict[i] = data[0]
        else:
            match = re.match(r'(\d+)\s*:\s*(.+);', line)
            if match:
                address, data = int(match.group(1)), match.group(2).split()
                for i, value in enumerate(data):
                    data_dict[address + i] = value

    # prompt user for address radix (hex or dec)
    print("Serialize with decimal \"DEC\" or hexadecimal \"HEX\" address radix? >>> ", end="")
    address_format = input().strip().lower()
    if address_format not in {"hex", "dec"}:
        raise ValueError("Invalid address radix. Please enter either 'HEX' or 'DEC'")

    # write new MIF file
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
    print("MIF successfully reformatted and stored in \"output.mif\"!")
    return


# main loop function call
serialize_mif("MIFs/input.mif", "MIFs/output.mif")

# to convert multiple files
# serialize_mif("MIFs/input1.mif", "MIFs/output1.mif")
# serialize_mif("MIFs/input2.mif", "MIFs/output2.mif")
