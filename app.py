#Code Written By SayyadN
#Code For Dwonload Videos From Socials Platforms Using YT_DLP
#Date  : 9-8-2025

import yt_dlp

def main():
    try:
        print("""
        

▗▖  ▗▖   ▐▌ ▄▄▄  ▄   ▄ ▄▄▄▄  
▐▛▚▖▐▌   ▐▌█   █ █ ▄ █ █   █ 
▐▌ ▝▜▌▗▞▀▜▌▀▄▄▄▀ █▄█▄█ █   █ 
▐▌  ▐▌▝▚▄▟▌                  
                             
                                                      
        """)
        print("[!] > Don't Use This App/Site in Anything Harmful or 18+ >")
        user_url = input("[*] Please Enter Your URL -> ").strip()
        quality = input("[*] Please Choose Quality ((High) , (Low)) -> ").lower().strip()
        #Checking User URL
        if not user_url:
            return print("[!] Failed To Get URL ")


        ydl_opts = {
            'quiet': True,
            'format': 'best' if quality == 'high' else 'worst',
            'postprocessors': [],
            'noplaylist': True
        }

        #For Download Youtube Video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([user_url])

    except Exception as e:
        return print(f"Error : {e}")

if __name__ == '__main__':
    main()