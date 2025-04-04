#!/bin/bash

echo "Testing products get"
curl -X GET http://localhost:8000/product
echo -e "\n"

echo "Testing product get"
curl -X GET http://localhost:8000/product/5
echo -e "\n"

echo "Testing product create"
curl -X POST http://localhost:8000/product -d '{"content":"New Product"}' -H "Content-Type: application/json"
echo -e "\n"

echo "Testing product UPDATE"
curl -X PUT http://localhost:8000/product/3 -d '{"content":"Updated Product"}' -H "Content-Type: application/json"
echo -e "\n"

echo "Testing product DELETE"
curl -X DELETE http://localhost:8000/product/5
echo -e "\n"