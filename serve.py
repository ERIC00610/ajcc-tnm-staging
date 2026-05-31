import http.server
import os
import socket
import socketserver

# 雙協定（IPv4 + IPv6）靜態伺服器，避免 localhost 解析到 ::1 時連線被拒
# Dual-stack static server so the preview pane can reach it via localhost or 127.0.0.1
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 5060


class DualStack(socketserver.ThreadingTCPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True

    def server_bind(self):
        # 關閉 IPV6_V6ONLY，讓同一 socket 同時接受 IPv4 與 IPv6
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


Handler = http.server.SimpleHTTPRequestHandler
with DualStack(("", PORT), Handler) as httpd:
    print(f"serving AJCC TNM on http://localhost:{PORT}/")
    httpd.serve_forever()
