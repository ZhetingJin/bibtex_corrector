def process_bib_file(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Dictionary to store the BibTeX blocks by their keys
    bib_dict = {}
    current_key = None
    current_block = []

    for line in lines:
        # Check if the line starts a new BibTeX block
        if line.startswith("@"):
            if current_key:
                # Store the previous block, only keeping the last occurrence
                bib_dict[current_key] = current_block

            # Start a new BibTeX block
            current_block = [line]
            # Extract the key from the line
            current_key = line.split("{", 1)[1].split(",", 1)[0].strip()
        else:
            # Continue adding lines to the current block
            current_block.append(line)

    # Add the last BibTeX block
    if current_key:
        bib_dict[current_key] = current_block

    # Write the processed BibTeX to the output file
    with open(output_file, "w") as file:
        for block in bib_dict.values():
            file.writelines(block)


# Usage example
input_file = "v1.bib"
output_file = "output.bib"
process_bib_file(input_file, output_file)
