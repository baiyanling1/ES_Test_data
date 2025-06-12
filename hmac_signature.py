import hmac
import hashlib
import json
from typing import Dict, Any, List
from collections import OrderedDict

def generate_signature(secret_key: str, timestamp: str, nonce: str, uri: str, param_map: Dict[str, List[str]] = None) -> str:
    """
    Generate HMAC-SHA256 signature for the request
    
    Args:
        secret_key: The secret key for HMAC
        timestamp: Current timestamp in milliseconds
        nonce: Random string
        uri: Request URI
        param_map: Dictionary of parameters where values are lists of strings
    
    Returns:
        str: Hex-encoded HMAC-SHA256 signature
    """
    # Construct the string to sign
    value_to_digest = []
    value_to_digest.append(str(timestamp))
    value_to_digest.append(str(nonce))
    value_to_digest.append(uri)
    
    # Handle parameters if they exist
    if param_map and param_map.keys():
        # Sort keys
        sorted_keys = sorted(param_map.keys())
        param_parts = []
        
        for key in sorted_keys:
            if not key:  # Skip empty keys
                continue
                
            values = param_map[key]
            if values:
                # Sort values
                sorted_values = sorted(values)
                for value in sorted_values:
                    param_part = key
                    if value is not None:  # Only append value if it's not None
                        param_part += f"={value}"
                    param_parts.append(param_part)
        
        if param_parts:
            value_to_digest.append("&".join(param_parts))
    
    # Join all parts with newlines
    bytes_to_sign = "\n".join(value_to_digest)
    
    # Create HMAC-SHA256 signature
    hmac_obj = hmac.new(
        secret_key.encode('utf-8'),
        bytes_to_sign.encode('utf-8'),
        hashlib.sha256
    )
    
    # Return hex-encoded signature
    return hmac_obj.hexdigest()

def main():
    # 实际请求参数
    secret_key = "K4jSlYsRaytKUdTeqz24Fw"  # 实际的密钥
    
    # 请求头参数
    timestamp = "1744859372531"
    nonce = "1626"
    uri = "/gateway/api/common/gw/buy/eSimProFileQuery"  # 只使用路径部分
    
    # 请求体参数
    body = {
        "eid": "86021024900989560000000200000086",
        "imei": "355387172431092"
    }
    
    # 将请求体转换为参数映射格式
    param_map = {k: [str(v)] for k, v in body.items()}
    
    # 生成签名
    signature = generate_signature(secret_key, timestamp, nonce, uri, param_map)
    
    # 打印完整的请求头
    headers = {
        "Content-Type": "application/json",
        "X-Hmac-Auth-Secret-Id": "63464732956287112121",
        "X-Hmac-Auth-Timestamp": timestamp,
        "X-Hmac-Auth-Nonce": nonce,
        "X-Hmac-Auth-Signature": signature
    }
    
    print("完整的请求头:")
    print(json.dumps(headers, indent=2, ensure_ascii=False))
    print("\n待签名字符串:")
    print("\n".join([
        timestamp,
        nonce,
        uri,
        "&".join([f"{k}={v[0]}" for k, v in sorted(param_map.items())])
    ]))
    print("\n生成的签名:", signature)

if __name__ == "__main__":
    main() 