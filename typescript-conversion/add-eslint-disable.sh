#!/bin/bash

# Find all .ts files under js/ directory
find js -name "*.ts" -type f | while read -r file; do
    # Check if first line starts with "// Copyright"
    first_line=$(head -n 1 "$file")
    if [[ "$first_line" == "// Copyright"* ]]; then
        # Create temporary file with the modifications
        {
            # Write the first line (Copyright)
            echo "$first_line"
            # Add the two new lines
            echo ""
            echo "/* eslint-disable */"
            echo "// @ts-nocheck"
            # Write the rest of the file (starting from line 2)
            tail -n +2 "$file"
        } > "$file.tmp"
        
        # Replace the original file with the modified one
        mv "$file.tmp" "$file"
        echo "Modified: $file"
    else
        echo "Skipped: $file (first line doesn't start with '// Copyright')"
    fi
done

echo "Done processing all .ts files"