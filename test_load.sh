#!/usr/bin/env bash

for ((i=1; i<=500; i++)); do
  echo -n $i-;
  curl -X POST 'http://localhost:5000/fibonacci' -H 'Content-Type: application/json' -d '{"number" : 10}'
  echo ""
done
