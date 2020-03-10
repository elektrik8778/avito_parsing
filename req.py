from proxy_requests import ProxyRequests
from proxyValidator import ProxyValidator

# proxyInstance = ProxyValidator(['207.154.231.217:3128'])
# print(proxyInstance.validated_proxies)


r = ProxyRequests("https://api.ipify.org")
print(r.get())