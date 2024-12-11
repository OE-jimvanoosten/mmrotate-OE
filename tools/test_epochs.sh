#!/bin/bash

# Base directories
WORK_DIR="work_dirs"
OUTPUT_DIR="test_logs"
SUMMARY_FILE="test_summary.txt"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Clear summary file
echo -n "" > "$SUMMARY_FILE"

# Loop through each training folder (oe_net_excasat{i})
for i in $(seq 1 12); do
    TRAIN_DIR="$WORK_DIR/oe_net_excasat$i"
    CONFIG_FILE="$TRAIN_DIR/oe_net_excasat$i.py"

    # Check if the directory and config file exist
    if [ -d "$TRAIN_DIR" ] && [ -f "$CONFIG_FILE" ]; then
        echo "Processing $TRAIN_DIR with config $CONFIG_FILE"

        # Test epochs 8 through 12
        for EPOCH in {8..12}; do
            WEIGHTS_FILE="$TRAIN_DIR/epoch_${EPOCH}.pth"
            LOG_FILE="$OUTPUT_DIR/oe_net_excasat${i}_epoch_${EPOCH}.log"

            # Ensure weights file exists before testing
            if [ -f "$WEIGHTS_FILE" ]; then
                echo "Testing weights: $WEIGHTS_FILE"
                python tools/test.py "$CONFIG_FILE" "$WEIGHTS_FILE" --eval mAP > "$LOG_FILE"

            else
                echo "Weights file $WEIGHTS_FILE not found. Skipping."
            fi
        done
    else
        echo "Directory or config file $TRAIN_DIR not found. Skipping."
    fi
done

echo "All tests complete. Results saved in $SUMMARY_FILE."
