#!/usr/bin/env bash

SITES=(
  "https://samdjames.uk"
  "https://sdj.pw"
  "https://example.com"
)
OUTPUT_FILE="./run.log"

safe() {
  printf "\n\n[!!] All sites are safe from Cosmicsting\n"
  exit 0
}
vuln() {
  printf "\n\n[!!] Atleast One Site Is at Risk of Cosmicsting\n";
  exit 255
}

echo "" > $OUTPUT_FILE
for site in "${SITES[@]}"; do
  echo "Checking site: $site"
  ./poc.py -u $site | head -n3 | tee -a $OUTPUT_FILE
  echo ""
done

grep -q "Decoded Exploited Data" $OUTPUT_FILE && vuln || safe;