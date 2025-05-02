#!/bin/bash

# === Config ===
DEST="$1"
BANDWIDTH="10M"
DURATION=10
PING_COUNT=10

if [ -z "$DEST" ]; then
  echo "Usage: $0 <destination_ip_or_hostname>"
  exit 1
fi

echo "📡 Testing network to: $DEST"
echo "-----------------------------"

# === Ping Test ===
echo "📶 Running ping test..."
PING_OUTPUT=$(ping -c $PING_COUNT "$DEST")

# Extract metrics from ping
PING_LOSS=$(echo "$PING_OUTPUT" | grep -o '[0-9]*% packet loss' | cut -d'%' -f1)
PING_RTT=$(echo "$PING_OUTPUT" | awk -F' = ' '/round-trip|rtt/ { print $2 }')

echo "✅ Ping Results:"
echo "   • Packet Loss: $PING_LOSS%"
echo "   • RTT (min/avg/max/mdev): $PING_RTT"

# === iperf3 Test (UDP) ===
echo ""
echo "🚀 Running iperf3 UDP test..."
IPERF_OUTPUT=$(iperf3 -c "$DEST" -u -b $BANDWIDTH -t $DURATION --json 2>/dev/null)

# Extract jitter, loss from iperf3 JSON (requires jq)
if command -v jq > /dev/null; then
  IPERF_JITTER=$(echo "$IPERF_OUTPUT" | jq '.end.sum["jitter_ms"]')
  IPERF_LOSS=$(echo "$IPERF_OUTPUT" | jq '.end.sum["lost_percent"]')
  echo "✅ iperf3 Results:"
  echo "   • Jitter: ${IPERF_JITTER} ms"
  echo "   • Packet Loss: ${IPERF_LOSS}%"
else
  echo "⚠️  'jq' not installed — can't parse iperf3 JSON output."
  echo "    Install jq with: sudo apt install jq (Linux) or brew install jq (macOS)"
fi

echo ""
echo "✅ Network diagnostics complete."
