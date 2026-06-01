#!/bin/bash

# evaluate_scheduling.sh
# Usage:
#   ./evaluate_scheduling.sh file1.txt 5
#   ./evaluate_scheduling.sh file1.txt 10
#
# Purpose:
# This script tests file processing speed by splitting a large input file
# into smaller parts, processing each part in parallel, and combining
# the results into one final output file.

INPUT_FILE=$1
PARTS=$2
OUTPUT_FILE="final_output_${PARTS}.txt"
WORK_DIR="work_${PARTS}_parts"

if [ -z "$INPUT_FILE" ] || [ -z "$PARTS" ]; then
  echo "Usage: ./evaluate_scheduling.sh input_file number_of_parts"
  exit 1
fi

rm -rf "$WORK_DIR"
mkdir "$WORK_DIR"

echo "Starting test with $PARTS part(s)..."
SECONDS=0

# Split the input file into equal line-based chunks.
split -n l/$PARTS -d "$INPUT_FILE" "$WORK_DIR/chunk_"

# Process each chunk in parallel.
# This example doubles each numeric value in the file.
for chunk in "$WORK_DIR"/chunk_*; do
  (
    awk '{print $1 * 2}' "$chunk" > "${chunk}.out"
  ) &
done

# Wait for all parallel jobs to finish.
wait

# Combine all processed chunks into one final output file.
cat "$WORK_DIR"/chunk_*.out > "$OUTPUT_FILE"

echo "Completed $PARTS part(s) in $SECONDS seconds."
echo "Output written to $OUTPUT_FILE"
