import re
from googlesearch import search


def process_bib_file(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

    bib_dict = {}
    current_key = None
    current_block = []
    title_pattern = re.compile(r"title\s*=\s*{(.+)}", re.IGNORECASE)

    for line in lines:
        if line.startswith("@"):
            if current_key:
                bib_dict[current_key] = current_block

            current_block = [line]
            current_key = line.split("{", 1)[1].split(",", 1)[0].strip()
        else:
            current_block.append(line)

    if current_key:
        bib_dict[current_key] = current_block

    # Update BibTeX blocks with missing URLs
    for key, block in bib_dict.items():
        if not any("url" in line for line in block):
            title = None
            for line in block:
                match = title_pattern.search(line)
                if match:
                    title = match.group(1)
                    break

            if title:
                print(f"Searching for URL for title: {title}")
                try:
                    # Perform the search and get the first result
                    search_results = search(title, num_results=1)
                    url = next(
                        search_results, None
                    )  # Get the first result if available
                    if url:
                        print(f"Found URL: {url}")
                        # Ensure the last field ends with a comma before adding the URL
                        if not block[-3].strip().endswith(","):
                            block[-3] = block[-3].rstrip() + ",\n"
                        # Insert the URL before the closing brace
                        block.insert(-2, f"  url = {{{url}}},\n")
                    else:
                        print(f"No URL found for {title}")
                except Exception as e:
                    print(f"Error occurred while searching for {title}: {e}")

    # Write the processed BibTeX to the output file
    with open(output_file, "w") as file:
        for block in bib_dict.values():
            file.writelines(block)


# Usage example
input_file = "v1.bib"
output_file = "output.bib"
process_bib_file(input_file, output_file)
