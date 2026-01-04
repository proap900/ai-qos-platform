#!/bin/bash

echo "Checking AI QoS Platform services in Minikube (using localhost port-forward)..."

# Port-forward API Gateway and ML Inference in the background
kubectl port-forward svc/api-gateway 8000:8000 >/dev/null 2>&1 &
PG_API=$!
sleep 2

kubectl port-forward svc/ml-inference 8001:8001 >/dev/null 2>&1 &
PG_ML=$!
sleep 2

API_URL="http://127.0.0.1:8000/health"
ML_URL="http://127.0.0.1:8001/health"

echo "API Gateway Health URL: $API_URL"
echo "ML Inference Health URL: $ML_URL"

# Check API Gateway
echo "Checking API Gateway..."
if curl -s --max-time 5 $API_URL | grep -q "ok"; then
    echo "API Gateway: ✅ Responding"
else
    echo "API Gateway: ❌ NOT responding"
fi

# Check ML Inference
echo "Checking ML Inference..."
if curl -s --max-time 5 $ML_URL | grep -q "ok"; then
    echo "ML Inference: ✅ Responding"
else
    echo "ML Inference: ❌ NOT responding"
fi

# Safely kill port-forward processes if they still exist
for pid in $PG_API $PG_ML; do
    if ps -p $pid > /dev/null; then
        kill $pid
    fi
done
