import re
from dcdownloader import config, title

def decode_packed_codes(code):
    def encode_base_n(num, n, table=None):
        FULL_TABLE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not table:
            table = FULL_TABLE[:n]

        if n > len(table):
            raise ValueError('base %d exceeds table length %d' % (n, len(table)))

        if num == 0:
            return table[0]

        ret = ''
        while num:
            ret = table[num % n] + ret
            num = num // n
        return ret

    pattern = r"}\('(.+)',(\d+),(\d+),'([^']+)'\.split\('\|'\)"
    mobj = re.search(pattern, code)
    obfucasted_code, base, count, symbols = mobj.groups()
    base = int(base)
    count = int(count)
    symbols = symbols.split('|')
    symbol_table = {}

    while count:
        count -= 1
        base_n_count = encode_base_n(count, base)
        symbol_table[base_n_count] = symbols[count] or base_n_count

    return re.sub(
        r'\b(\w+)\b', lambda mobj: symbol_table[mobj.group(0)],
        obfucasted_code)

def generate_aiohttp_session_config(**kwargs):
    params = {
        'timeout': 50,
        'verify_ssl': config.get('debug_mode'),
        'proxy': config.get('proxy')
    }
    params.update(kwargs)

    return params

def update_window_title(mode=None, msg=None):
    app_name = 'DCDownloader'

    window_title = app_name

    if not mode == None:
        window_title = window_title + ': %s' % mode
    
    if not msg == None:
        window_title = window_title + ' - %s' % msg

    title.update(window_title)
    