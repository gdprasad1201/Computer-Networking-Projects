#!/bin/bash

# ===== CONFIGURATION =====
SERVER_IP=$1              # Pass the IP address as an argument
DURATION=10               # Duration for iperf3 test in seconds
IPERF_PORT=5201
UDP_BANDWIDTH="10M"       # Limit UDP bandwidth for testing

# ===== CHECK FOR ARGUMENT =====
if [ -z "$SERVER_IP" ]; then
    echo "Usage: $0 <server_ip>"
    exit 1
fi

echo "Testing network metrics to $SERVER_IP..."

# ===== PING TEST =====
# PING_OUT=$(ping -c $DURATION $SERVER_IP)
PING_OUT=$(ping $SERVER_IP -n $DURATION)
PING_LOSS=$(echo "$PING_OUT" | grep -Eo '[0-9]+% packet loss' | awk '{print $1}')
PING_JITTER=$(echo "$PING_OUT" | grep 'time=' | awk -F'time=' '{print $2}' | cut -d' ' -f1 | awk '
    {sum+=$1; sumsq+=$1*$1; n++}
    END {
        mean=sum/n;
        stddev=sqrt(sumsq/n - mean*mean);
        printf("%.2f ms\n", stddev)
    }')

if [ -z "$PING_JITTER" ]; then
    echo "⚠️  'awk' not installed — can't parse ping output."
    echo "    Install awk with: sudo apt install gawk (Linux) or brew install gawk (macOS)"
    exit 1
fi

# bandwidth = packet size / latency
# PING_BANDWIDTH=$((PING_PACKET_SIZE / PING_LATENCY * 1000)) # Convert to Mbps


# ===== IPERF3 TEST (UDP) =====
IPERF_OUTPUT=$(iperf3 -c "$SERVER_IP" -u -b $UDP_BANDWIDTH -t $DURATION --json 2>/dev/null)

# Extract jitter, loss, latency info from the summary line
IPERF_SUMMARY_LINE=$(echo "$IPERF_OUTPUT" | jq -r '.end.sum')
IPERF_LOSS=$(echo "$IPERF_SUMMARY_LINE" | jq -r '.lost_percent')
IPERF_JITTER=$(echo "$IPERF_SUMMARY_LINE" | jq -r '.jitter_ms')
if [ -z "$IPERF_JITTER" ]; then
    echo "⚠️  'jq' not installed — can't parse iperf3 JSON output."
    echo "    Install jq with: sudo apt install jq (Linux) or brew install jq (macOS)"
    exit 1
fi

# ===== OUTPUT COMPARISON =====
echo -e "\n========= NETWORK METRICS COMPARISON ========="
printf "%-20s | %-15s | %-15s\n" "Metric" "Ping" "iperf3 (UDP)"
printf "%-20s | %-15s | %-15s\n" "--------------------" "---------------" "---------------"
printf "%-20s | %-15s | %-15s\n" "Packet Loss (%)" "$PING_LOSS" "$IPERF_LOSS%"
printf "%-20s | %-15s | %-15s\n" "Jitter (est/stddev)" "$PING_JITTER" "$IPERF_JITTER ms"
echo "=============================================="
