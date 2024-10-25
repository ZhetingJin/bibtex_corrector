def add_braces_to_title(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line.strip().lower().startswith("title"):
                # Find the position of the first '{' and the last '},' in the line
                start_pos = line.find("{") + 1
                end_pos = line.rfind("},")
                if end_pos == -1:
                    end_pos = line.rfind("}")  # Handle cases without a comma
                # Add extra braces around the title content
                line = (
                    line[:start_pos]
                    + "{"
                    + line[start_pos:end_pos]
                    + "}"
                    + line[end_pos:]
                )
            # Write the modified or unmodified line to the output file
            outfile.write(line)


# Specify the input and output file names
input_bib_file = "input.bib"
output_bib_file = "output.bib"

# Run the function to add braces to titles
add_braces_to_title(input_bib_file, output_bib_file)

print(f"Processed {input_bib_file} and saved to {output_bib_file}.")
