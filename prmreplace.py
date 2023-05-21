import sys
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

def print_help():
    print("Usage: python3 script4.py [-a] <value>")
    print("Options:")
    print("  -a       Append the value instead of replacing it")
    print("  value    The value to be used for parameter modification")
    print("           If not provided, an empty string will be used")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print_help()
        return

    value = sys.argv[1]
    append_mode = False

    if value == "-a":
        if len(sys.argv) < 3:
            print("Error: Value not provided for -a option.")
            return
        value = sys.argv[2]
        append_mode = True

    for line in sys.stdin:
        line = line.strip()
        url_parts = list(urlparse(line))
        query_params = parse_qs(url_parts[4], keep_blank_values=True)
        original_query = url_parts[4]

        # Change each parameter individually
        for param, values in query_params.items():
            new_params = query_params.copy()
            if append_mode:
                new_params[param] = [vv + value for vv in values]
            else:
                new_params[param] = [value]
            new_query = urlencode(new_params, doseq=True)
            url_parts[4] = new_query
            new_url = urlunparse(url_parts)
            print(new_url)

        # Change all parameters together
        if append_mode:
            new_params = {param: [vv + value for vv in values] for param, values in query_params.items()}
        else:
            new_params = {param: [value] for param in query_params}
        new_query = urlencode(new_params, doseq=True)
        url_parts[4] = new_query
        new_url = urlunparse(url_parts)
        if new_url != line:  # Avoid duplicate URLs
            print(new_url)

        # Restore original query
        url_parts[4] = original_query

if __name__ == "__main__":
    main()
