# MIF Serializer
## What is this?
I wrote this Python program for my ECE241 final project. It reformats memory initialization files (or MIFs) created using the instructor-provided [bmp2mif](https://www.eecg.utoronto.ca/~jayar/ece241_08F/vga/vga-bmp2mif.html) converter[^3].

I needed this code to serialize MIFs for a deck of cards; the SDRAM[^1] IP core[^2] for the DE1-SoC does not accept vectorized MIFs, because it needs to read only one address per clock cycle, input must be provided serially (one at a time). This is what the instructor-provided converter produces (example here is the king of diamonds):

<img alt="Converter Output" src="images/vectorized_mif.png" width="300"/>

And this is what the program produces (which works with the IP core):

<img alt="Serializer Output" src="images/serialized_mif.png" width="100"/>

## How can I use this?
1. Pull this repository and copy your input MIFs into the project directory. 
2. Run ```python mif_converter.py``` in Terminal or Command Prompt.
3. Enter your input and output MIF names/paths. 
4. When prompted, enter "HEX" or "DEC" depending on whether you want the output MIF to be indexed with decimal or hexadecimal address radices.
5. Enter "Q" to quit the program or continue converting more MIFs. 

I've included sample input and output MIFs if you don't have a bmp2mif converter on hand. (I'm working on a Python version of the bmp2mif converter as well!)

## Any more updates to come?
The last update eliminated the need to add a new function call for every file that needs to be converted; the user enters input and output file names (or paths) for each file. 

The next update will first ask the user whether they wish to import input/output file names from a file or convert each file manually (as in the current functionality). 

## Recent Updates
Dec 26, 2024 -- Execute once to convert all files, no need to edit the Python script and add more function calls.
Dec 25, 2024 -- Program rewrites MIF with decimal or hexadecimal address radices based on user input. 
Nov 18, 2024 -- First working version of the program. Much of the parsing logic was written by ChatGPT.

[^1]: Synchronous Dynamic Random Access Memory (lots of big words but essentially means clocked memory)
[^2]: Intellectual Property Core (third-party licensed code for FPGAs/ASICs that does a specific job, in this case, build a memory module)
[^3]: A C program that converts a bitmap file (BMP) into a memory initialization file (MIF). God knows when it was written. It also does not work on MAC (I think this has to do with the processor more so than the OS, but I'm not sure).
