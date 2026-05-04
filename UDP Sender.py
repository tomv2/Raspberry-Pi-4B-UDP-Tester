#!/usr/bin/env python3
import socket
import time
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_ip", help="Computer IP address")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument("--mbps", type=float, default=500)
    parser.add_argument("--size", type=int, default=1400, help="UDP payload size in bytes")
    parser.add_argument("--duration", type=float, default=10)
    args = parser.parse_args()

    target = (args.target_ip, args.port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = os.urandom(args.size)

    bytes_per_second = args.mbps * 1_000_000 / 8
    packets_per_second = bytes_per_second / args.size
    interval = 1.0 / packets_per_second

    print(f"Sending UDP to {args.target_ip}:{args.port}")
    print(f"Target rate: {args.mbps} Mb/s")
    print(f"Payload size: {args.size} bytes")
    print(f"Packets/sec: {packets_per_second:,.0f}")
    print(f"Duration: {args.duration}s")

    start = time.perf_counter()
    next_send = start
    sent_packets = 0
    sent_bytes = 0

    while True:
        now = time.perf_counter()
        if now - start >= args.duration:
            break

        sock.sendto(payload, target)
        sent_packets += 1
        sent_bytes += args.size

        next_send += interval
        delay = next_send - time.perf_counter()
        if delay > 0:
            time.sleep(delay)

    elapsed = time.perf_counter() - start
    mbps_actual = sent_bytes * 8 / elapsed / 1_000_000

    print()
    print(f"Sent packets: {sent_packets:,}")
    print(f"Sent data: {sent_bytes / 1_000_000:.2f} MB")
    print(f"Actual rate: {mbps_actual:.2f} Mb/s")

if __name__ == "__main__":
    main()
