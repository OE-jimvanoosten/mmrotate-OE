#!/bin/bash

# Base config file
CONFIG_DIR="configs/_oe_net_"
BASE_CONFIG="oe_net_excasat.py"

# Loop to run training 12 times
for i in $(seq 1 12); do
    # Generate new config name
    NEW_CONFIG="oe_net_excasat${i}.py"
    NEW_CONFIG_PATH="${CONFIG_DIR}/${NEW_CONFIG}"
    
    # Copy the base config to the new config
    cp "${CONFIG_DIR}/${BASE_CONFIG}" "${NEW_CONFIG_PATH}"
    
    # Train the model using the new config
    python tools/train.py "${NEW_CONFIG_PATH}"
    
    # Optionally, clean up the new config after the run
    # rm "${NEW_CONFIG_PATH}"
done
