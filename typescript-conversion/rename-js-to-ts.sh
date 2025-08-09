
#!/usr/bin/env zsh
#
# Recursively git-rename all *.js files under ./js to *.ts,
# skipping anything whose path contains “overrides”.
# Only files are renamed, not directories.
#
# Copy and run from the root of the repository.

set -euo pipefail

# Find all .js files under ./js, excluding any path with “overrides”
find ./js -type f \( -iname '*.js' \) ! -iname '*overrides*' -print0 |
while IFS= read -r -d '' file; do
  tsfile="${file%.*}.ts"

  # Skip if the target already exists
  if [[ -e "$tsfile" ]]; then
    echo "⚠️  Skipping '$file' → '$tsfile' (target exists)"
    continue
  fi

  echo "git mv \"$file\" \"$tsfile\""
  git mv "$file" "$tsfile"
done