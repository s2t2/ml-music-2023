
import os
from time import sleep

from app.youtube_video_service import YoutubeVideoService

ARTIST_NAME = os.getenv("ARTIST_NAME")

VIDEO_URLS = {
    "maggie_rogers":[
        # some of these are live performances
        "https://www.youtube.com/watch?v=0dzZXpf7sSQ", # say it
        "https://www.youtube.com/watch?v=q6HiZIQoLSU", # knife
        "https://www.youtube.com/watch?v=bR1d8l92Q8Q", # fallingwater
        "https://www.youtube.com/watch?v=gigJjgPThYA", # overdrive
        "https://www.youtube.com/watch?v=MSFjYe54uv4", # light on
        "https://www.youtube.com/watch?v=yaXAMuhIe7Y", # give a little
        "https://www.youtube.com/watch?v=iKYxMnW7bgs", # love you for a long time
        "https://www.youtube.com/watch?v=IHi5jq2P_Zk", # split stones
        "https://www.youtube.com/watch?v=19ItfuE585w", # alaska (acoustic)
        # maybe some overlaps / dups:
        "https://www.youtube.com/watch?v=PNWsW6c6t8g", # alaska
        "https://www.youtube.com/watch?v=MSFjYe54uv4",
        "https://www.youtube.com/watch?v=bR1d8l92Q8Q",
        "https://www.youtube.com/watch?v=iKYxMnW7bgs",
        "https://www.youtube.com/watch?v=WdrNXRdkuG4",
        "https://www.youtube.com/watch?v=NgWC5oEuyjU",
        "https://www.youtube.com/watch?v=SylF32J2g8k",
        "https://www.youtube.com/watch?v=cdIBxhONpC0",
        "https://www.youtube.com/watch?v=0Da6AvsegGs"

    ],
    "john_mayer": [
        # BATTLE STUDIES
        "https://www.youtube.com/watch?v=GeCClzNCfcA", # John Mayer - Heartbreak Warfare (Official Music Video)
        "https://www.youtube.com/watch?v=FgK7vTaJCEM", # All We Ever Do Is Say Goodbye
        "https://www.youtube.com/watch?v=zr6lp-45bOQ", # Half of My Heart
        "https://www.youtube.com/watch?v=KoLc_6BmyTc", # John Mayer - Perfectly Lonely (Official Audio)
        "https://www.youtube.com/watch?v=VDrZww-uHZU", # Assassin
        "https://www.youtube.com/watch?v=5zqRVADxYpM", # Crossroads
        "https://www.youtube.com/watch?v=E3ZAc6WlPYg", # War of My Life
        "https://www.youtube.com/watch?v=Nt-jb5JHWB8", # Edge of Desire
        "https://www.youtube.com/watch?v=cZVT8Zg0YwE", # Do You Know Me
        "https://www.youtube.com/watch?v=LaG0keIFX6o", # Friends, Lovers or Nothing
        # CONTINUUM
    ],
    "chris_stapleton":[
        # VOL 2
        "https://www.youtube.com/watch?v=sI0TeFf6uD8", # Chris Stapleton - Broken Halos (Official Audio)
        "https://www.youtube.com/watch?v=7IhQrVeXn2M", # Chris Stapleton - I Was Wrong (Official Audio)
        "https://www.youtube.com/watch?v=k4oGoiN4JtM", # Chris Stapleton - Without Your Love (Official Audio)
        "https://www.youtube.com/watch?v=m_TsUb0T95E", # Chris Stapleton - Death Row (Official Audio)
        # VOL 1
        "https://www.youtube.com/watch?v=MPoN-FNB2V8", # Chris Stapleton - Millionaire (Official Audio)
        # STARTING OVER
        "https://www.youtube.com/watch?v=wilhfxYfqfc", # You Should Probably Leave
        "https://www.youtube.com/watch?v=UIAo_Awfs-E", # Cold
        "https://www.youtube.com/watch?v=A3svABDnmio", # Chris Stapleton - Starting Over (Official Music Video)
        "https://www.youtube.com/watch?v=WbBt5qDoCAs", # Chris Stapleton - Devil Always Made Me Think Twice (Official Audio)
        "https://www.youtube.com/watch?v=jsE_zp_4vyo", # Chris Stapleton - Joy Of My Life (Official Audio)
        "https://www.youtube.com/watch?v=EzqskyzdWJw", # Chris Stapleton - Hillbilly Blood (Official Audio)
        # TRAVELER
        "https://www.youtube.com/watch?v=l6_w3887Rwo", # Tennessee Whiskey
    ],
    "tupac": [
        "https://www.youtube.com/watch?v=sf9MDMYca0w", # all eyes on me
        #"https://www.youtube.com/watch?v=41qC3w3UUkU", # hit em up
        #"https://www.youtube.com/watch?v=xg3J5slvB-k", # changes
        #"https://www.youtube.com/watch?v=Mb1ZvUDvLDY", # dear mama
        #"https://www.youtube.com/watch?v=Do5MMmEygsY", # ghetto gospel
        #"https://www.youtube.com/watch?v=mwgZalAFNhM", # california love remix
        "https://www.youtube.com/watch?v=Y2cWHiKaFjc", # do for love
        #"https://www.youtube.com/watch?v=77nB_9uIcN4", # ambitions as a ridah
        #"https://www.youtube.com/watch?v=rrLgvHG_GYc", # hail mary
        #"https://www.youtube.com/watch?v=9wVtWAwTMPU",
    ],
    "jay_z": [
        #"https://www.youtube.com/watch?v=vk6014HuxcE", # empire state of mind w/ alicia keys
        #"https://www.youtube.com/watch?v=dyUqaHAHH2c", # jigga what
        #"https://www.youtube.com/watch?v=Cgoqrgc_0cM", # big pimpin
        #"https://www.youtube.com/watch?v=Oz_-VaTHpc8", # dirt off your shoulder
        #"https://www.youtube.com/watch?v=MaQZF0msXxE", # encore
        #"https://www.youtube.com/watch?v=GRKmpn3SBdw", # izzo
        #"https://www.youtube.com/watch?v=Kzq15y2J4UM", # young forever
        #"https://www.youtube.com/watch?v=MzTLMp-vh9s", # 99 problems (clean)
        "https://www.youtube.com/watch?v=EeE7CfNs7Js", # run this town
        "https://www.youtube.com/watch?v=w5srnNrICJo", # song cry
        #"https://www.youtube.com/watch?v=wuhhSAa-yrs", # what more can i say
        #"https://www.youtube.com/watch?v=XzBB2VPQ5Os", # moment of clarity
        "https://www.youtube.com/watch?v=n2kigJH0uU0" # allure
    ],
    "adele": [
        #"https://www.youtube.com/watch?v=rYEDA3JcQqw", # rolling in the deep
        #"https://www.youtube.com/watch?v=uJdu4Lfy8aI", # set fire to the rain
        #"https://www.youtube.com/watch?v=hLQl3WQQoQ0", # someone like you
        #"https://www.youtube.com/watch?v=U3ASj1L6_sY", # easy on me
        #"https://www.youtube.com/watch?v=oytOOA9sOiE", # love in the dark
        #"https://www.youtube.com/watch?v=YQHsXMglC9A", # hello
        "https://www.youtube.com/watch?v=fk4BbF7B29w", # send my love
        "https://www.youtube.com/watch?v=jDvYDzFOK9A", # i drink wine
        #"https://www.youtube.com/watch?v=sonzlE32YVg", # all i ask
        #"https://www.youtube.com/watch?v=Xpc8mAJ_2nM", # when we were young
    ],
    "taylor_swift": [
        #"https://www.youtube.com/watch?v=e-ORhEE9VVg", # blank space
        #"https://www.youtube.com/watch?v=b1kbLwvqugk", # anti hero
        #"https://www.youtube.com/watch?v=nfWlot6h_JM", # shake it off
        #"https://www.youtube.com/watch?v=-CmadmM5cOk", # style
        #"https://www.youtube.com/watch?v=K-a8s8OLBSE", # cardigan
        #"https://www.youtube.com/watch?v=-BjZmE2gtdo", # lover
        #"https://www.youtube.com/watch?v=QcIy9NiNbmo", # bad blood

        # crowd sourced additions, maybe overlaps:
        "https://youtu.be/FNEoPctNIUE", # FNEoPctNIUE
        #"https://youtu.be/OWbDJFtHl3w", # OWbDJFtHl3w
        "https://youtu.be/kRJKB291Z1g", # kRJKB291Z1g
        #"https://youtu.be/XzKSPRqFg9E", # XzKSPRqFg9E
        #"https://youtu.be/KsZ6tROaVOQ", # KsZ6tROaVOQ
        "https://youtu.be/KaM1bCuG4xo", # KaM1bCuG4xo
        "https://youtu.be/GTEFSuFfgnU", # GTEFSuFfgnU
        #"https://youtu.be/u9raS7-NisU",
        "https://youtu.be/u1D1AgDfreg",
        #"https://youtu.be/9OQBDdNHmXo",

    ],
    #"phantogram": [
    #    "https://www.youtube.com/watch?v=a0ul-BghOAs", # black out days
    #    "https://www.youtube.com/watch?v=pmb1dDB2tak", # cruel world
    #    "https://www.youtube.com/watch?v=ZvSgLHWR16o", # mouth full of diamonds
    #    "https://www.youtube.com/watch?v=Ur17pfjIRVo", # don't move
    #],
    "ariana_grande": [
        #"https://www.youtube.com/watch?v=SXiSVQZLje8", # side to side
        #"https://www.youtube.com/watch?v=gl1aHhXnN1k", # thank u next
        #"https://www.youtube.com/watch?v=pE49WK-oNjU", # stuck with you
        #"https://www.youtube.com/watch?v=g5qU7p7yOY8", # love me harder
        #"https://www.youtube.com/watch?v=BPgEgaPk62M", # one last time
        #"https://www.youtube.com/watch?v=B6_iQvaIjXw", # 34+35
        #"https://www.youtube.com/watch?v=tcYodQoapMg", # positions
        #"https://www.youtube.com/watch?v=kHLHSlExFis", # god is a woman
        #"https://www.youtube.com/watch?v=uKqRAC-JNOM", # bloodline
        #"https://www.youtube.com/watch?v=m7XHduHsBvk", # bad idea
        #"https://www.youtube.com/watch?v=Z1pmpDRrQhU", # ghostin
        #"https://www.youtube.com/watch?v=LH4Y1ZUUx2g", # break up w your gf
    ],
    "miranda_lambert": [
        "https://www.youtube.com/watch?v=aWQdEDtveB0", # gunpowder and lead
        "https://www.youtube.com/watch?v=DQYNM6SjD_o", # house that built me
        "https://www.youtube.com/watch?v=nUB8ogvze_8", # bluebird
        "https://www.youtube.com/watch?v=EJEz_z7cE_0", # if I was a cowboy
        "https://www.youtube.com/watch?v=rB7ONnfIjaI", # kerosene
        "https://www.youtube.com/watch?v=62mEFlE4EPE", # tin man
        "https://www.youtube.com/watch?v=QoR2Oax82kY", # white liar
    ],
    "frank_sinatra": [
        "https://www.youtube.com/watch?v=qQzdAsjWGPg", # my way
        #"https://www.youtube.com/watch?v=rSrc7aulay8", # fly me to the moon
        "https://www.youtube.com/watch?v=XvfImv9NseY", # that's life
        #"https://www.youtube.com/watch?v=dthgRdTf0Ds", #
        #"https://www.youtube.com/watch?v=gFwuHsra6Oc", #
        #"https://www.youtube.com/watch?v=82_JCboW69U", #
        #"https://www.youtube.com/watch?v=LWXUdqvVO8Y", #
        #"https://www.youtube.com/watch?v=BTOeRwIUnG0", #
        #"https://www.youtube.com/watch?v=Qp6D71kQRhA", #
        "https://www.youtube.com/watch?v=TK0Vdb1RUCk", #
    ],
    "michael_buble": [
        "https://www.youtube.com/watch?v=Edwsf-8F3sI", #
        "https://www.youtube.com/watch?v=a90tZJHBklk", #
        "https://www.youtube.com/watch?v=lbSOLBMUvIE", #
        "https://www.youtube.com/watch?v=SPUJIbXN0WY", #
        "https://www.youtube.com/watch?v=1AJmKkU5POA", #
        "https://www.youtube.com/watch?v=xeMOO5EudYs", #
        "https://www.youtube.com/watch?v=5QYxuGQMCuU", #
        "https://www.youtube.com/watch?v=LAjfB0XfjkA", #
        "https://www.youtube.com/watch?v=hVu_hUTOvj0", #
        "https://www.youtube.com/watch?v=hGp5WE7IK-8", #
    ],
    "daft_punk": [
        "https://www.youtube.com/watch?v=5NV6Rdv1a3I", #
        "https://www.youtube.com/watch?v=a5uQMwRMHcs", #
        "https://www.youtube.com/watch?v=FGBhQbmPwH8", #
        "https://www.youtube.com/watch?v=K0HSD_i2DvA", #
        "https://www.youtube.com/watch?v=gAjR4_CbPpQ",
        "https://www.youtube.com/watch?v=NF-kLy44Hls",
        "https://www.youtube.com/watch?v=sOS9aOIXPEk",
    ],
    "andrea_bocelli": [
        "https://www.youtube.com/watch?v=m5UcZ9thgPI", #
        "https://www.youtube.com/watch?v=4L_yCwFD6Jo", #
        "https://www.youtube.com/watch?v=CNHL66K8S2I", #
        #"https://www.youtube.com/watch?v=ChcR2gKt5WM", #
        #"https://www.youtube.com/watch?v=xYz5CiEy5bY", #
        #"https://www.youtube.com/watch?v=nVUHHW1tJYA", #
        #"https://www.youtube.com/watch?v=NfU99xfo8MY", #
        #"https://www.youtube.com/watch?v=srti9S6wQpY", #
        #"https://www.youtube.com/watch?v=nexnnrYyTmc", #
        #"https://www.youtube.com/watch?v=4REbp0s_G9w", #
    ],
    "jason_aldean": [
        #"https://www.youtube.com/watch?v=7i1ImAbmcjM", #
        #"https://www.youtube.com/watch?v=jLCHpZ6B1gU", #
        #"https://www.youtube.com/watch?v=Zc3cxj5pDIs", #
        #"https://www.youtube.com/watch?v=Lb9q1ScC4cg", #
        "https://www.youtube.com/watch?v=xdImDqbgc2g", #
        #"https://www.youtube.com/watch?v=ZsvR6XAl1os", #
        #"https://www.youtube.com/watch?v=b3HW2BYxz5Q", #
        #"https://www.youtube.com/watch?v=zsM8GD2Q4nU", #
        #"https://www.youtube.com/watch?v=TAtWP5Mct5I", #
        "https://www.youtube.com/watch?v=OeFYetKv_XE", #
    ],
    "john_legend": [
        #"https://www.youtube.com/watch?v=450p7goxZqg", #
        "https://www.youtube.com/watch?v=jKIEUdAMtrQ", #
        #"https://www.youtube.com/watch?v=axySrE0Kg6k", #
        #"https://www.youtube.com/watch?v=iXvy8ZeCs5M", #
        #"https://www.youtube.com/watch?v=ZKr4ys2avI0", #
        "https://www.youtube.com/watch?v=qUD2GxTeVcI", #
        "https://www.youtube.com/watch?v=NmCFY1oYDeM", #
        #"https://www.youtube.com/watch?v=PIh07c_P4hc", #
        #"https://www.youtube.com/watch?v=SsjVHBvh1HQ", #
        #"https://www.youtube.com/watch?v=ZwbNesQeods", #
    ],
    "bts": [
        "https://www.youtube.com/watch?v=gdZLi9oWNZg", #
        "https://www.youtube.com/watch?v=IwzkfMmNMpM", #
        "https://www.youtube.com/watch?v=WMweEpGlu_U", #
        "https://www.youtube.com/watch?v=XsX3ATc3FbA", #
        "https://www.youtube.com/watch?v=a4YwJCZRh5M", #
        "https://www.youtube.com/watch?v=kTlv5_Bs8aw", #
        "https://www.youtube.com/watch?v=Z2z1TbTJpdQ", #
        "https://www.youtube.com/watch?v=CuklIb9d3fI", #
        "https://www.youtube.com/watch?v=7C2z4GqqS5E", #
        "https://www.youtube.com/watch?v=pBuZEGYXA6E",
    ],
    "alicia_keys": [
        #"https://www.youtube.com/watch?v=QtE3O3z1wcs", #
        #"https://www.youtube.com/watch?v=rywUS-ohqeE", #
        #"https://www.youtube.com/watch?v=J91ti_MpdHA", #
        #"https://www.youtube.com/watch?v=Ju8Hr50Ckwk", #
        #"https://www.youtube.com/watch?v=Urdlvw0SSEc", #
        #"https://www.youtube.com/watch?v=fPgf2meEX1w", #
        "https://www.youtube.com/watch?v=HhuGQUZJot8", #
        #"https://www.youtube.com/watch?v=_ST6ZRbhGiA", #
        #"https://www.youtube.com/watch?v=srMBZiqNMaM", #
        "https://www.youtube.com/watch?v=0yVdBlGSgRw", #
    ],
    "bon_iver": [
        "https://www.youtube.com/watch?v=MZSCXE4CpCA", #
        "https://www.youtube.com/watch?v=TWcyIpul8OE", #
        "https://www.youtube.com/watch?v=95FyXUHv8hk", #
        "https://www.youtube.com/watch?v=3w68krri0bw", #
        "https://www.youtube.com/watch?v=KMfL7rVAu0U", #
        "https://www.youtube.com/watch?v=HDAKS18Gv1U", #
        "https://www.youtube.com/watch?v=8NstorpFnjM", #
        "https://www.youtube.com/watch?v=ltIozO0pBms", #
        "https://www.youtube.com/watch?v=-gznDYiDC94", #
        "https://www.youtube.com/watch?v=4JjSyITsyIs", #
    ],
    "ed_sheeran": [
        "https://www.youtube.com/watch?v=JGwWNGJdvx8", #
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g", #
        "https://www.youtube.com/watch?v=nSDgHBxUbVQ", #
        "https://www.youtube.com/watch?v=lp-EO5I60KA", #
        "https://www.youtube.com/watch?v=Il0S8BoucSA", #
        "https://www.youtube.com/watch?v=u6wOyMUs74I", #
        "https://www.youtube.com/watch?v=orJSJGHjBLI", #
        "https://www.youtube.com/watch?v=mKEphyIbtXo", #
        "https://www.youtube.com/watch?v=pekzpzNCNDQ", #
        "https://www.youtube.com/watch?v=y83x7MgzWOA", #
    ],
    "kane_brown": [
        "https://www.youtube.com/watch?v=bLzUmfLckEw", #
        "https://www.youtube.com/watch?v=dRX0wDNK6S4", #
        "https://www.youtube.com/watch?v=29a6o5vRKVM", #
        "https://www.youtube.com/watch?v=fM8V1XOI-14", #
        "https://www.youtube.com/watch?v=GEAy7eXb2lo", #
        "https://www.youtube.com/watch?v=mS3TeZEp_PE", #
        "https://www.youtube.com/watch?v=5hqK-A0UxKw", #
        "https://www.youtube.com/watch?v=ELZNClmKX1E", #
        "https://www.youtube.com/watch?v=fPziOGGqEpw", #
        "https://www.youtube.com/watch?v=qpMOx2Ul9RA", #
    ],
    "britney_spears": [
        "https://www.youtube.com/watch?v=C-u5WLJ9Yk4", #
        "https://www.youtube.com/watch?v=LOZuxwVk7TU", #
        "https://www.youtube.com/watch?v=elueA2rofoo", #
        "https://www.youtube.com/watch?v=CduA0TULnow", #
        "https://www.youtube.com/watch?v=s6b33PTbGxk", #
        "https://www.youtube.com/watch?v=t0bPrt69rag", #
        "https://www.youtube.com/watch?v=rMqayQ-U74s", #
        "https://www.youtube.com/watch?v=qExVlz3zb0k", #
        "https://www.youtube.com/watch?v=lVhJ_A8XUgc", #
        "https://www.youtube.com/watch?v=Mzybwwf2HoQ", #
    ],
    "dave_matthews_band": [
        "https://www.youtube.com/watch?v=k7in-9E3ImQ", #
        "https://www.youtube.com/watch?v=Fi61TB6bsG4", #
        "https://www.youtube.com/watch?v=MNgJBIx-hK8", #
        "https://www.youtube.com/watch?v=elUwSHjfA94", #
        "https://www.youtube.com/watch?v=qjykrjAS5bQ", #
        "https://www.youtube.com/watch?v=GAamgBPebsk", #
        "https://www.youtube.com/watch?v=Isgqj4TK0QA", #
        "https://www.youtube.com/watch?v=FoezrZ-DCJw", #
        "https://www.youtube.com/watch?v=yiO13jTsBdQ", #
        "https://www.youtube.com/watch?v=SYCxdWaN6iU", #
    ],
    "bruce_springsteen": [
        #"https://www.youtube.com/watch?v=129kuDCQtHs", #
        #"https://www.youtube.com/watch?v=_91hNV6vuBY", #
        #"https://www.youtube.com/watch?v=EPhWR4d3FJQ", #
        #"https://www.youtube.com/watch?v=B9VTZ1gB2aA", #
        #"https://www.youtube.com/watch?v=lrpXArn3hII", #
        #"https://www.youtube.com/watch?v=tKdk97y2Wjg", #
        #"https://www.youtube.com/watch?v=9XQX-zRVK-w", #
        #"https://www.youtube.com/watch?v=6vQpW9XRiyM", #
        #"https://www.youtube.com/watch?v=GsTKEQzLkmw", #
        #"https://www.youtube.com/watch?v=WY1spB1J0vw", #
    ],
    "rihanna": [
        #"https://www.youtube.com/watch?v=lWA2pjMjpBs", #
        #"https://www.youtube.com/watch?v=CvBfHwUxHIk", #
        #"https://www.youtube.com/watch?v=QMP-o8WXSPM", #
        #"https://www.youtube.com/watch?v=Mx_OexsUI2M", #
        "https://www.youtube.com/watch?v=YbHe2gFnhq8", #
        #"https://www.youtube.com/watch?v=tg00YEETFzg", #
        "https://www.youtube.com/watch?v=JF8BRvqGCNs", #
        #"https://www.youtube.com/watch?v=HBxt_v0WF6Y", #
        #"https://www.youtube.com/watch?v=HL1UzIK-flA", #
        "https://www.youtube.com/watch?v=J3UjJ4wKLkg", #
    ],
    "coldplay": [
        #"https://www.youtube.com/watch?v=YykjpeuMNEk", #
        #"https://www.youtube.com/watch?v=yKNxeF4KMsY", #
        #"https://www.youtube.com/watch?v=dvgZkm1xWPE", #
        "https://www.youtube.com/watch?v=1G4isv_Fylg", #
        #"https://www.youtube.com/watch?v=VPRjCeoBqrI", #
        "https://www.youtube.com/watch?v=FM7MFYoylVs", #
        #"https://www.youtube.com/watch?v=RB-RcX5DS5A", #
        #"https://www.youtube.com/watch?v=QtXby3twMmI", #
        #"https://www.youtube.com/watch?v=d020hcWA_Wg", #
        #"https://www.youtube.com/watch?v=k4V3Mo61fJM", #
        "https://www.youtube.com/watch?v=Fpn1imb9qZg",
        #"https://www.youtube.com/watch?v=gnIZ7RMuLpU",
        #"https://www.youtube.com/watch?v=qhIVgSoJVRc",
        #"https://www.youtube.com/watch?v=HHsHw3UTlqE",
        "https://www.youtube.com/watch?v=yOW-X8kvpc8",
        "https://www.youtube.com/watch?v=Rr0RIWNG-PQ"
    ],
    "mtns": [
        "https://www.youtube.com/watch?v=84BJGgZR914", #
        "https://www.youtube.com/watch?v=DnvjuLaCxI0", #
        "https://www.youtube.com/watch?v=LCwL8yX86mg", #
        "https://www.youtube.com/watch?v=8WysnLe-6bs", #
        "https://www.youtube.com/watch?v=11fay5n-XuY", #
        "https://www.youtube.com/watch?v=TqXHm2BZA-Y", #
        "https://www.youtube.com/watch?v=jkdKvUVw_CA", #
        "https://www.youtube.com/watch?v=As69ZhiKjdk", #
        "https://www.youtube.com/watch?v=zM4EOTuFedE", #
        "https://www.youtube.com/watch?v=p1CfyV9YZ_U", #
    ],
    "beyonce": [
        "https://www.youtube.com/watch?v=v5SZrJQDoWo", #
        "https://www.youtube.com/watch?v=bnVUHWCynig", #
        "https://www.youtube.com/watch?v=ViwtNLUqkMY", #
        "https://www.youtube.com/watch?v=QrOe2h9RtWI", #
        "https://www.youtube.com/watch?v=STLaD0gu034", #
        "https://www.youtube.com/watch?v=2EwViQxSJJQ", #
        "https://www.youtube.com/watch?v=4m1EFMoRFvY", #
        "https://www.youtube.com/watch?v=AWpsOqh8q0M", #
        "https://www.youtube.com/watch?v=gU-ktsNlDIg", #
        "https://www.youtube.com/watch?v=p1JPKLa-Ofc", #
    ],
    "drake": [
        "https://www.youtube.com/watch?v=xpVfcZ0ZcFM", #
        "https://www.youtube.com/watch?v=ntp9_iznQ-0", #
        "https://www.youtube.com/watch?v=NveQffpaOlU", #
        "https://www.youtube.com/watch?v=uxpDa-c-4Mc", #
        "https://www.youtube.com/watch?v=I4DjHHVHWAE", #
        "https://www.youtube.com/watch?v=T8nbNQpRwNo", #
        "https://www.youtube.com/watch?v=cpsPTik5o-I", #
        "https://www.youtube.com/watch?v=V7UgPHjN9qE", #
        "https://www.youtube.com/watch?v=JFm7YDVlqnI", #
        "https://www.youtube.com/watch?v=3HFY0xuHybk", #
    ],
    "justin_bieber": [
        "https://www.youtube.com/watch?v=kTJczUoc26U", #
        "https://www.youtube.com/watch?v=kffacxfA7G4", #
        "https://www.youtube.com/watch?v=fRh_vgS2dFE", #
        "https://www.youtube.com/watch?v=Fp8msa5uYsc", #
        "https://www.youtube.com/watch?v=mAj1kgPdlg4", #
        "https://www.youtube.com/watch?v=oyEuk8j8imI", #
        "https://www.youtube.com/watch?v=tQ0yjYUFKAE", #
        "https://www.youtube.com/watch?v=3AyMjyHu1bA", #
        "https://www.youtube.com/watch?v=pE49WK-oNjU", #
        "https://www.youtube.com/watch?v=prmmCg5bKxA", #
    ],
    "led_zeppelin": [
        #"https://www.youtube.com/watch?v=QkF3oxziUI4", #
        #"https://www.youtube.com/watch?v=HQmmM_qwG4k", #
        "https://www.youtube.com/watch?v=P3Y8OWkiUts", #
        "https://www.youtube.com/watch?v=PD-MdiUm1_Y", #
        #"https://www.youtube.com/watch?v=ceZfF84V6UY", #
        #"https://www.youtube.com/watch?v=yYDh7lyqwms", #
        #"https://www.youtube.com/watch?v=XIiu0JI3I5g", #
        "https://www.youtube.com/watch?v=abw__u5w4A8", #
        #"https://www.youtube.com/watch?v=qyivczZI5pw", #
        #"https://www.youtube.com/watch?v=_h9MxNn8P7w", #
    ],
    "pink_floyd": [
        #"https://www.youtube.com/watch?v=KpfLHz_ufUQ", #
        "https://www.youtube.com/watch?v=HrxX9TBj2zY", #
        "https://www.youtube.com/watch?v=x-xTttimcNk", #
        #"https://www.youtube.com/watch?v=Qr0-7Ds79zo", #
        #"https://www.youtube.com/watch?v=mPGv8L3a_sY", #
        #"https://www.youtube.com/watch?v=jQcBwE6j09U", #
        #"https://www.youtube.com/watch?v=-0kcet4aPpQ", #
        "https://www.youtube.com/watch?v=7jMlFXouPk8", #
        #"https://www.youtube.com/watch?v=54W8kktFE_o", #
        #"https://www.youtube.com/watch?v=mrojrDCI02k", #
    ],
    "lauryn_hill": [
        "https://www.youtube.com/watch?v=cE-bnWqLqxE", #
        "https://www.youtube.com/watch?v=wVzvXW9bo5U", #
        "https://www.youtube.com/watch?v=zASJBw0R0gM", #
        "https://www.youtube.com/watch?v=b2IbsMCgz4A", #
        "https://www.youtube.com/watch?v=i3_dOWYHS7I", #
        "https://www.youtube.com/watch?v=fse2hyTvMy0", #
        "https://www.youtube.com/watch?v=SWz-RU3OtmA", #
        "https://www.youtube.com/watch?v=Yq_3A_8C7Ag", #
        "https://www.youtube.com/watch?v=doszNz67lmc", #
    ],
    "chelsea_cutler": [
        "https://www.youtube.com/watch?v=06k5XN78OP0", #
        "https://www.youtube.com/watch?v=6qkgVgjN188", #
        "https://www.youtube.com/watch?v=MFdzgnMOmlw", #
        "https://www.youtube.com/watch?v=qAJr0bzOe6A", #
        "https://www.youtube.com/watch?v=EYTUV32Gi0o", #
        "https://www.youtube.com/watch?v=oYjsEoTVXXM", #
        "https://www.youtube.com/watch?v=wWYr-35O0Ww", #
        "https://www.youtube.com/watch?v=WRARL8GUYG0", #
        "https://www.youtube.com/watch?v=ObRjPkZ0wwI", #
        "https://www.youtube.com/watch?v=bdtrsb3tPY8", #
    ],
    "louis_the_child": [
        "https://www.youtube.com/watch?v=u5kP_nfFVt4", #
        "https://www.youtube.com/watch?v=Pc-dxNilmBg", #
        "https://www.youtube.com/watch?v=rhrqbcufZXo", #
        "https://www.youtube.com/watch?v=vqOp3BkpYKk", #
        "https://www.youtube.com/watch?v=wQWVRfMAEEM", #
        "https://www.youtube.com/watch?v=v_55Vzq8cGY", #
        "https://www.youtube.com/watch?v=AIrlVwxziFE", #
        "https://www.youtube.com/watch?v=6t_y7inNGXU", #
        "https://www.youtube.com/watch?v=8xmZ7QcETBY", #
        "https://www.youtube.com/watch?v=3rxCL2JxOn4", #
    ],
    "dr_dre": [
        #"https://www.youtube.com/watch?v=_CL6n0FJZpk", #
        "https://www.youtube.com/watch?v=QZXc39hT8t4", #
        #"https://www.youtube.com/watch?v=8GliyDgAGQI", #
        #"https://www.youtube.com/watch?v=E5a93wABHNM", #
        #"https://www.youtube.com/watch?v=VQAtYyKK9fw", #
        #"https://www.youtube.com/watch?v=-Ubyt7iWJ8Q", #
        "https://www.youtube.com/watch?v=VA770wpLX-Q", #
        #"https://www.youtube.com/watch?v=WdlyIH2DX60", #
        #"https://www.youtube.com/watch?v=Voz6-bo44f4", #
        #"https://www.youtube.com/watch?v=erJQha5ur_U", #
    ],
    "eminem": [
        "https://www.youtube.com/watch?v=S9bCLPwzSC0", #
        "https://www.youtube.com/watch?v=YVkUvmDQ3HY", #
        "https://www.youtube.com/watch?v=8kYkciD9VjU", #
        "https://www.youtube.com/watch?v=eJO5HU_7_1w", #
        "https://www.youtube.com/watch?v=uelHwf8o7_U", #
        "https://www.youtube.com/watch?v=xFYQQPAOz7Y", #
        "https://www.youtube.com/watch?v=gOMhN-hfMtY", #
        "https://www.youtube.com/watch?v=r_0JjYUe5jo", #
        "https://www.youtube.com/watch?v=j5-yKhDd64s", #
        "https://www.youtube.com/watch?v=D4hAVemuQXY", #
    ],
    "eagles": [
        "https://www.youtube.com/watch?v=BciS5krYL80", #
        "https://www.youtube.com/watch?v=Odcn6qk94bs", #
        "https://www.youtube.com/watch?v=2dANDhfWU8g", #
        "https://www.youtube.com/watch?v=-Pa5nqYXEnY", #
        "https://www.youtube.com/watch?v=ESc2Tq2HzhQ", #
        "https://www.youtube.com/watch?v=AaBw37-nWaY", #
        "https://www.youtube.com/watch?v=aelpqWEBHR4", #
        "https://www.youtube.com/watch?v=po6QU0z1rSs", #
        "https://www.youtube.com/watch?v=6LqqRQqSeNw", #
        "https://www.youtube.com/watch?v=S-2BMyZXK5o", #
    ],
    "ac_dc": [
        #"https://www.youtube.com/watch?v=v2AC41dglnM", #
        #"https://www.youtube.com/watch?v=pAgnJDJN4VA", #
        "https://www.youtube.com/watch?v=l482T0yNkeo", #
        #"https://www.youtube.com/watch?v=Lo2qQmj0_h4", #
        "https://www.youtube.com/watch?v=gEPmA3USJdI", #
        "https://www.youtube.com/watch?v=xRQnJyP77tY", #
        "https://www.youtube.com/watch?v=etAIpkdhU9Q", #
        "https://www.youtube.com/watch?v=n_GFN3a0yj0", #
        #"https://www.youtube.com/watch?v=PiZHNw1MtzI", #
        "https://www.youtube.com/watch?v=NhsK5WExrnE", #
    ],
    "tim_mcgraw": [
        "https://www.youtube.com/watch?v=awzNHuGqoMc", #
        "https://www.youtube.com/watch?v=orFHkgg-6f0", #
        "https://www.youtube.com/watch?v=-vn6QdqxK3g", #
        "https://www.youtube.com/watch?v=2AJ4i4S_fP8", #
        "https://www.youtube.com/watch?v=_9TShlMkQnc", #
        "https://www.youtube.com/watch?v=hU0nP9dcI_w", #
        "https://www.youtube.com/watch?v=DKuE36e9ICo", #
        "https://www.youtube.com/watch?v=KmxaY_OVvWA", #
        "https://www.youtube.com/watch?v=kqlR4IEl_04", #
        "https://www.youtube.com/watch?v=HYRFgWbalBE", #
    ],
    "kenny_chesney": [
        "https://www.youtube.com/watch?v=WZihn6Q1fYE", #
        "https://www.youtube.com/watch?v=n56hFE9Aquc", #
        "https://www.youtube.com/watch?v=xP-Sxfntdb4", #
        "https://www.youtube.com/watch?v=de1aPKXBdAE", #
        "https://www.youtube.com/watch?v=4f0p5KqdU9U", #
        "https://www.youtube.com/watch?v=SLeTw46NNWg", #
        "https://www.youtube.com/watch?v=V6c8a90PWIM", #
        "https://www.youtube.com/watch?v=Q8XkLrErSHw", #
        "https://www.youtube.com/watch?v=-01jhW_Yzhs", #
        "https://www.youtube.com/watch?v=uWu4aynBK7E", #
    ],
    "morgan_wallen": [
        "https://www.youtube.com/watch?v=TyjgBxIVmEc", #
        "https://www.youtube.com/watch?v=Dw9VmOLwxoM", #
        "https://www.youtube.com/watch?v=5DCdL1zdpdM", #
        "https://www.youtube.com/watch?v=3CkLMG5NwUg", #
        "https://www.youtube.com/watch?v=kTbRnDwkR0Y", #
        "https://www.youtube.com/watch?v=FjBp30kjzTc", #
        "https://www.youtube.com/watch?v=UpYu9FgcxKo", #
        "https://www.youtube.com/watch?v=iBduQb1S-4s", #
        "https://www.youtube.com/watch?v=AHAE7Dw7yHM", #
        "https://www.youtube.com/watch?v=KEnFCa-5p9E", #
    ],
    "bach": [
        #"https://www.youtube.com/watch?v=VkjW2oNb5TI",
        #"https://www.youtube.com/watch?v=sZJjVpU3hL0",
        #"https://www.youtube.com/watch?v=-UhOPXd-LYY",
        #"https://www.youtube.com/watch?v=i2e_o4i5WbM",
        #"https://www.youtube.com/watch?v=-77aIj0SSoI",
        #"https://www.youtube.com/watch?v=Ax9Mri7VRes",
        #"https://www.youtube.com/watch?v=ELRAD5oqbuM",
        #"https://www.youtube.com/watch?v=rDVPiNe5cCU",
    ],
    "beethoven": [
        "https://www.youtube.com/watch?v=9_C6CTs0WhI",
        #"https://www.youtube.com/watch?v=_XG3h6LywNQ",
        "https://www.youtube.com/watch?v=KlrWjnzTnfw",
        #"https://www.youtube.com/watch?v=K_aXXMdzslU",
        #"https://www.youtube.com/watch?v=RbWP-jOwTFo",
        "https://www.youtube.com/watch?v=lC0ncp6VE5s",
        #"https://www.youtube.com/watch?v=KgzXryrMMbw",
        #"https://www.youtube.com/watch?v=MwszBQnvUqY",
        #"https://www.youtube.com/watch?v=uHXFb24FIZo",
        #"https://www.youtube.com/watch?v=GS0tQE6RLik",
    ],
    "john_coltrane": [
        #"https://www.youtube.com/watch?v=ej6gfL4yF4E", #
        #"https://www.youtube.com/watch?v=9Zyr0IDaRXQ", #
        "https://www.youtube.com/watch?v=K2kp2AiB3Ak", #
        #"https://www.youtube.com/watch?v=-81BzBWGXZM", #
        #"https://www.youtube.com/watch?v=KwIC6B_dvW4", #
        #"https://www.youtube.com/watch?v=fue4mYwJjeU", #
        #"https://www.youtube.com/watch?v=NLGlnSUkjVo", #
        "https://www.youtube.com/watch?v=3w-oeQFo6Hk", #
        #"https://www.youtube.com/watch?v=vMCHDC2Lurk", #
        "https://www.youtube.com/watch?v=rUpsutZTilo", #
    ],
    "miles_davis": [
        #"https://www.youtube.com/watch?v=ylXk1LBvIqU", #
        #"https://www.youtube.com/watch?v=TLDflhhdPCg", #
        "https://www.youtube.com/watch?v=ZZcuSBouhVA", #
        #"https://www.youtube.com/watch?v=CieM9gurwZ4", #
        #"https://www.youtube.com/watch?v=VLEj7E8ORU4", #
        #"https://www.youtube.com/watch?v=zqNTltOGh5c", #
        "https://www.youtube.com/watch?v=-488UORrfJ0", #
        #"https://www.youtube.com/watch?v=2CgEP7RciHo", #
        #"https://www.youtube.com/watch?v=p70s7LtbtMg", #
        #"https://www.youtube.com/watch?v=k94zDsJ-JMU", #
    ],
    "aretha_franklin": [
        "https://www.youtube.com/watch?v=2t5VNI0XlwY", #
        "https://www.youtube.com/watch?v=U0yIf9Tkgu4", #
        "https://www.youtube.com/watch?v=joyRFqTfNqI", #
        "https://www.youtube.com/watch?v=5C4FnlftQt4", #
        "https://www.youtube.com/watch?v=fDxzQJaA228", #
        "https://www.youtube.com/watch?v=tc36-Li5eww", #
        "https://www.youtube.com/watch?v=8jCFzreP1ng", #
        "https://www.youtube.com/watch?v=MB1FPOuSVeM", #
        "https://www.youtube.com/watch?v=Nbokg0KM-n8", #
        "https://www.youtube.com/watch?v=5-7ublizwZ0", #
    ],

    #"duke_ellington":[
    #]


    #"_____": [
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #],



    # crowd sourced via https://forms.gle/tNFhMZSqPsHGBXPL9

    "niki": [
        "https://www.youtube.com/watch?v=toHJ3yp4TY8",
        "https://www.youtube.com/watch?v=d4CF4km1rUQ",
        "https://www.youtube.com/watch?v=OXtZfPZIex4",
        "https://www.youtube.com/watch?v=ExLeQc-KvF0",
        "https://www.youtube.com/watch?v=Lqdx118ilhA",
        "https://www.youtube.com/watch?v=5YlJt5EYrlM",
        "https://www.youtube.com/watch?v=PqBEmfy3q0o",
    ],
    "mt_joy": [
        "https://www.youtube.com/watch?v=u2mGu-Sg20I"
        "https://www.youtube.com/watch?v=LV8eoai0HNk"
        "https://www.youtube.com/watch?v=fn0qTtLslhY"
        "https://www.youtube.com/watch?v=Xl1psdL6z0c"
        "https://www.youtube.com/watch?v=etrjS8dYeFc"
        "https://www.youtube.com/watch?v=KGL7JgxgTp8"
        "https://www.youtube.com/watch?v=KHZqi4sw224"
        "https://www.youtube.com/watch?v=ctfUOPgbJj0"
        "https://www.youtube.com/watch?v=CiiZHpgfdbc"
        "https://www.youtube.com/watch?v=w7o246-zEyM"
    ],
    "noah_kahan": [
        "https://www.youtube.com/watch?v=-fUfHerrgmQ",
        "https://www.youtube.com/watch?v=JKrDdsgXuso",
        "https://www.youtube.com/watch?v=dqbXCAt5VV4",
        "https://www.youtube.com/watch?v=Y76SBWfU2Bw",
        "https://www.youtube.com/watch?v=Jm76aFLbgRc",
        "https://www.youtube.com/watch?v=UncTpLrfr2I",
        "https://www.youtube.com/watch?v=uVQokyxiXzY",
        "https://www.youtube.com/watch?v=WtKTfzNcX9Y",
        "https://www.youtube.com/watch?v=WtKTfzNcX9Y",
        "https://www.youtube.com/watch?v=rcWodDfNklg",
    ],
    "harry_styles":[
        "https://youtu.be/o0LaNit1ts8",
        "https://youtu.be/xS1Gz7nMV0Q",
        "https://youtu.be/lVnzO7opqNs",
        "https://youtu.be/G2BYATpr4uY",
        "https://youtu.be/qN4ooNx77u0",
        "https://youtu.be/MdLx4iINoMM",
        "https://youtu.be/enuYFtMHgfU",
        "https://youtu.be/7o1EBarYGOs",
        "https://youtu.be/Pi2Gy7DG75g",
        "https://youtu.be/_ecXNJP-ERY",
    ]












    #"artist_name": [
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #],
    #"artist_name": [
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #    "_______", #
    #],

}



if __name__ == "__main__":

    print("DOWNLOADING AUDIO FROM YOUTUBE...")

    for artist_name, video_urls in VIDEO_URLS.items():
        print(artist_name.upper())
        if ARTIST_NAME and (ARTIST_NAME != artist_name):
            #print("... SKIPPING")
            pass
        else:
            #print("videos...")
            for video_url in video_urls:
                print(video_url)

                yt = YoutubeVideoService(video_url, artist_name=artist_name)
                video = yt.video
                if video:
                    print("... VIDEO:", video.video_id, video.author, video.title)
                    yt.download_metadata()
                    yt.download_audio()
                else:
                    print("... OOPS, SKIPPING...")

                #sleep(1)
