import time
import sys
import urllib.request

# Configuration
# Using a reliable public test file (approx. 10MB file from Cloudflare/Speedtest)
DEFAULT_URL = "https://speed.hetzner.de/10MB.bin"
NUM_REQUESTS = 10

def measure_speed(url=DEFAULT_URL):
    print(f"Target URL: {url}")
    print(f"Making {NUM_REQUESTS} sequential requests...\n")
    
    total_time = 0.0
    total_bytes = 0
    successful_requests = 0

    for i in range(1, NUM_REQUESTS + 1):
        try:
            start_time = time.perf_counter()
            
            # Make the HTTP request and read the full response body
            with urllib.request.urlopen(url) as response:
                data = response.read()
                
            end_time = time.perf_counter()
            
            duration = end_time - start_time
            size = len(data)
            
            total_time += duration
            total_bytes += size
            successful_requests += 1
            
            print(f"Request {i:2d}: {duration:.3f} seconds ({size / 1024 / 1024:.2f} MB)")
            
        except Exception as e:
            print(f"Request {i:2d}: Failed ({e})")

    if successful_requests == 0:
        print("\nAll requests failed. Please check the URL or your network connection.")
        return

    # Calculations
    avg_time = total_time / successful_requests
    total_megabits = (total_bytes * 8) / (1024 * 1024)  # Convert bytes to megabits
    speed_mbps = total_megabits / total_time             # Megabits per second (Mbps)

    print("\n" + "="*40)
    print("RESULTS:")
    print(f"Successful requests: {successful_requests}/{NUM_REQUESTS}")
    print(f"Total downloaded data: {total_bytes / 1024 / 1024:.2f} MB")
    print(f"Average request time: {avg_time:.3f} seconds")
    print(f"Average download speed: {speed_mbps:.2f} Mbps")
    print("="*40)

if __name__ == "__main__":
    # Allow custom URL via command line argument if desired
    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    measure_speed(target_url)
