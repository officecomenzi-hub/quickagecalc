#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

OUT=Path("pinterest/2026-10")
OUT.mkdir(parents=True,exist_ok=True)
W,H=1000,1500
ITEMS=json.loads(r"""[{"f":"2026-10-01-01-cat-age-human-years.png","t":"Cat Age Calculator: How Old Is Your Cat in Human Years?","b":"Pet Age Calculators"},{"f":"2026-10-01-02-cat-years-not-seven.png","t":"Cat Years to Human Years: Why the 7-Year Rule Is Wrong","b":"Pet Age Calculators"},{"f":"2026-10-02-01-days-alive.png","t":"How Many Days Have You Been Alive? Exact Age in Days","b":"Age Calculators"},{"f":"2026-10-02-02-what-generation-am-i.png","t":"What Generation Am I? Gen X, Millennial, Gen Z or Gen Alpha","b":"Birth Year & Generations"},{"f":"2026-10-03-01-dog-age-size.png","t":"Dog Age Calculator: Human Years by Dog Size","b":"Pet Age Calculators"},{"f":"2026-10-03-02-birthday-countdown.png","t":"Birthday Countdown: How Many Days Until Your Next Birthday?","b":"Birthday Calculators"},{"f":"2026-10-04-01-cat-life-stages.png","t":"Cat Life Stages: Kitten, Young Adult, Mature or Senior?","b":"Pet Age Calculators"},{"f":"2026-10-04-02-age-in-weeks.png","t":"How Old Are You in Weeks? Find Your Exact Age in Weeks","b":"Age Calculators"},{"f":"2026-10-05-01-born-in-1990.png","t":"Born in 1990? Your Age in 2026 and Millennial Generation","b":"Birth Year & Generations"},{"f":"2026-10-05-02-age-gap.png","t":"Age Difference Calculator: Exact Gap in Years, Months and Days","b":"Date & Time Calculators"},{"f":"2026-10-06-01-pregnancy-due-date.png","t":"Pregnancy Due Date Calculator: Estimate Your Baby's Due Date","b":"Pregnancy & Baby Calculators"},{"f":"2026-10-06-02-age-in-months.png","t":"How Old Are You in Months? Exact Age in Months Calculator","b":"Age Calculators"},{"f":"2026-10-07-01-cat-age-chart.png","t":"Cat Age Chart: Cat Years to Human Years From Kitten to Senior","b":"Pet Age Calculators"},{"f":"2026-10-07-02-what-year-was-i-born.png","t":"What Year Was I Born? Calculate Birth Year From Your Age","b":"Birth Year & Generations"},{"f":"2026-10-08-01-age-in-hours.png","t":"How Old Are You in Hours? Exact Age in Hours Calculator","b":"Age Calculators"},{"f":"2026-10-08-02-millennial-or-gen-z.png","t":"Millennial or Gen Z? Check the Birth-Year Border","b":"Birth Year & Generations"},{"f":"2026-10-09-01-dog-seven-year-rule.png","t":"Dog Years: Why the 7-Year Rule Is Too Simple","b":"Pet Age Calculators"},{"f":"2026-10-09-02-date-difference.png","t":"Date Difference Calculator: Days, Weeks, Months and Years Between Dates","b":"Date & Time Calculators"},{"f":"2026-10-10-01-cat-two-years.png","t":"How Old Is a 2-Year-Old Cat in Human Years?","b":"Pet Age Calculators"},{"f":"2026-10-10-02-turn-40-50-65.png","t":"When Will I Turn 40, 50 or 65? Milestone Age Calculator","b":"Life Milestones"},{"f":"2026-10-11-01-ten-thousand-days.png","t":"When Is Your 10,000th Day Alive? Find the Date","b":"Age Calculators"},{"f":"2026-10-11-02-next-birthday.png","t":"Next Birthday Calculator: Your Exact Birthday Countdown","b":"Birthday Calculators"},{"f":"2026-10-12-01-age-in-2030.png","t":"How Old Will You Be in 2030? Age in Any Year Calculator","b":"Age Calculators"},{"f":"2026-10-12-02-senior-cat.png","t":"When Is a Cat Considered Senior? Cat Life Stage Guide","b":"Pet Age Calculators"},{"f":"2026-10-13-01-born-in-2000.png","t":"Born in 2000? Your Age in 2026 and Generation","b":"Birth Year & Generations"},{"f":"2026-10-13-02-age-in-minutes.png","t":"How Old Are You in Minutes? Turn Your Life Into One Big Number","b":"Age Calculators"},{"f":"2026-10-14-01-pregnancy-weeks.png","t":"Pregnancy Due Date and Current Week Calculator","b":"Pregnancy & Baby Calculators"},{"f":"2026-10-14-02-gen-z-or-alpha.png","t":"Gen Z or Gen Alpha? Check the Birth-Year Cutoff","b":"Birth Year & Generations"},{"f":"2026-10-15-01-cat-five-years.png","t":"How Old Is a 5-Year-Old Cat in Human Years?","b":"Pet Age Calculators"},{"f":"2026-10-15-02-who-is-older.png","t":"Who Is Older? Compare Two Birthdays Exactly","b":"Date & Time Calculators"},{"f":"2026-10-16-01-dog-age-calculator.png","t":"How Old Is Your Dog in Human Years? Free Dog Age Calculator","b":"Pet Age Calculators"},{"f":"2026-10-16-02-born-in-1985.png","t":"Born in 1985? Your Age in 2026 and Millennial Generation","b":"Birth Year & Generations"},{"f":"2026-10-17-01-october-birthday.png","t":"October Birthday? Calculate Your Exact Age Today","b":"Birthday Calculators"},{"f":"2026-10-17-02-cat-older-than-you-think.png","t":"Is Your Cat Older Than You Think? Convert Cat Years","b":"Pet Age Calculators"},{"f":"2026-10-18-01-birthday-to-days.png","t":"Turn Your Birthday Into Days Alive","b":"Age Calculators"},{"f":"2026-10-18-02-retirement-age.png","t":"Retirement Age Calculator: How Long Until Retirement?","b":"Life Milestones"},{"f":"2026-10-19-01-born-in-1965.png","t":"Born in 1965? Your Age in 2026 and Generation X","b":"Birth Year & Generations"},{"f":"2026-10-19-02-cat-age-save-chart.png","t":"Cat Age Conversion Chart: Save This for Later","b":"Pet Age Calculators"},{"f":"2026-10-20-01-age-in-2050.png","t":"How Old Will You Be in 2050? Future Age Calculator","b":"Age Calculators"},{"f":"2026-10-20-02-birthday-in-numbers.png","t":"Birthday in Numbers: Days, Minutes, Generation and More","b":"Birthday Calculators"},{"f":"2026-10-21-01-exact-age-weeks.png","t":"Exact Age in Weeks: How Many Weeks Have You Lived?","b":"Age Calculators"},{"f":"2026-10-21-02-cat-fifteen-years.png","t":"How Old Is a 15-Year-Old Cat in Human Years?","b":"Pet Age Calculators"},{"f":"2026-10-22-01-1996-1997-border.png","t":"Born in 1996 or 1997? Millennial vs Gen Z Border","b":"Birth Year & Generations"},{"f":"2026-10-22-02-days-between-dates.png","t":"How Many Days Between Two Dates? Exact Date Difference","b":"Date & Time Calculators"},{"f":"2026-10-23-01-cat-human-years-calculator.png","t":"Cat Human Years Calculator: Enter Your Cat's Age","b":"Pet Age Calculators"},{"f":"2026-10-23-02-born-in-2010.png","t":"Born in 2010? Your Age in 2026 and Generation","b":"Birth Year & Generations"},{"f":"2026-10-24-01-days-until-birthday.png","t":"How Many Days Until Your Birthday? Quick Countdown","b":"Birthday Calculators"},{"f":"2026-10-24-02-dog-age-myth.png","t":"Dog Age Myth: Stop Multiplying by 7","b":"Pet Age Calculators"},{"f":"2026-10-25-01-cat-five-human.png","t":"5-Year-Old Cat in Human Years: The Answer Is About 36","b":"Pet Age Calculators"},{"f":"2026-10-25-02-months-old.png","t":"How Many Months Old Are You? Exact Months-Old Calculator","b":"Age Calculators"},{"f":"2026-10-26-01-age-any-year.png","t":"Age in Any Year Calculator: Past or Future Age Instantly","b":"Age Calculators"},{"f":"2026-10-26-02-due-date-lmp.png","t":"Due Date From Last Period: Pregnancy Due Date Calculator","b":"Pregnancy & Baby Calculators"},{"f":"2026-10-27-01-cat-senior-over-ten.png","t":"Senior Cat Age: Cats Over 10 Years Enter the Senior Stage","b":"Pet Age Calculators"},{"f":"2026-10-27-02-born-in-1978.png","t":"Born in 1978? Your Age in 2026 and Generation X","b":"Birth Year & Generations"},{"f":"2026-10-28-01-seconds-alive.png","t":"How Many Seconds Have You Been Alive? Life in Numbers","b":"Age Calculators"},{"f":"2026-10-28-02-exact-age-gap.png","t":"Exact Age Gap: Years, Months and Days Between Two People","b":"Date & Time Calculators"},{"f":"2026-10-29-01-national-cat-day.png","t":"National Cat Day: Find Your Cat's Human Age","b":"Pet Age Calculators"},{"f":"2026-10-29-02-national-cat-day-chart.png","t":"National Cat Day Cat Age Chart: Save This Conversion","b":"Pet Age Calculators"},{"f":"2026-10-30-01-age-in-hours-viral.png","t":"Your Age in Hours Is Bigger Than You Think","b":"Age Calculators"},{"f":"2026-10-30-02-halloween-cat-age.png","t":"Halloween Cat Age: How Old Is Your Cat in Human Years?","b":"Pet Age Calculators"},{"f":"2026-10-31-01-born-on-halloween.png","t":"Born on Halloween? Calculate Your Exact Age Today","b":"Birthday Calculators"},{"f":"2026-10-31-02-halloween-generation.png","t":"Halloween Birthday: What Generation Are You?","b":"Birth Year & Generations"}]""")
PALETTES={
"Pet Age Calculators":((246,242,255),(124,58,237),(76,29,149),(237,233,254)),
"Age Calculators":((239,246,255),(37,99,235),(30,58,138),(219,234,254)),
"Birth Year & Generations":((240,253,250),(13,148,136),(19,78,74),(204,251,241)),
"Birthday Calculators":((253,242,248),(219,39,119),(131,24,67),(252,231,243)),
"Date & Time Calculators":((236,254,255),(8,145,178),(21,94,117),(207,250,254)),
"Pregnancy & Baby Calculators":((255,241,242),(225,29,72),(136,19,55),(255,228,230)),
"Life Milestones":((240,253,244),(22,163,74),(20,83,45),(220,252,231)),
}
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def ff(size,b=True): return ImageFont.truetype(BOLD if b else REG,size)
def wrap(draw,txt,font,maxw):
    lines=[]; cur=""
    for w in txt.split():
        c=(cur+" "+w).strip()
        if draw.textbbox((0,0),c,font=font)[2] <= maxw: cur=c
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def fit(draw,txt,maxw,maxlines=5):
    for s in range(76,43,-2):
        f=ff(s,True); lines=wrap(draw,txt,f,maxw)
        if len(lines)<=maxlines: return f,lines
    return ff(44,True),wrap(draw,txt,ff(44,True),maxw)[:maxlines]
def rr(draw,box,r,fill,outline=None,w=1): draw.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def icon(draw,cx,cy,board,accent,dark):
    if board=="Pet Age Calculators":
        draw.ellipse((cx-170,cy-160,cx+170,cy+170),fill=(255,255,255),outline=accent,width=10)
        draw.polygon([(cx-135,cy-95),(cx-85,cy-245),(cx-25,cy-120)],fill=(255,255,255),outline=accent)
        draw.polygon([(cx+135,cy-95),(cx+85,cy-245),(cx+25,cy-120)],fill=(255,255,255),outline=accent)
        draw.ellipse((cx-70,cy-35,cx-45,cy-10),fill=dark); draw.ellipse((cx+45,cy-35,cx+70,cy-10),fill=dark)
        draw.polygon([(cx,cy+18),(cx-22,cy+48),(cx+22,cy+48)],fill=accent)
    elif board=="Birth Year & Generations":
        labels=["X","Y","Z","α"]
        for i,l in enumerate(labels):
            y=cy-210+i*120
            rr(draw,(cx-230+i*18,y,cx+230+i*18,y+86),24,(255,255,255),accent,6)
            draw.text((cx-190+i*18,y+14),l,font=ff(44,True),fill=dark)
    elif board=="Pregnancy & Baby Calculators":
        r=105
        draw.ellipse((cx-r*1.35,cy-r,cx-r*.05,cy+r*.3),fill=accent)
        draw.ellipse((cx+r*.05,cy-r,cx+r*1.35,cy+r*.3),fill=accent)
        draw.polygon([(cx-r*1.15,cy),(cx+r*1.15,cy),(cx,cy+r*1.65)],fill=accent)
    elif board=="Date & Time Calculators":
        draw.ellipse((cx-170,cy-170,cx+170,cy+170),fill=(255,255,255),outline=accent,width=10)
        draw.line((cx,cy,cx,cy-95),fill=dark,width=12); draw.line((cx,cy,cx+105,cy+50),fill=accent,width=12)
    else:
        rr(draw,(cx-190,cy-150,cx+190,cy+165),36,(255,255,255),accent,8)
        draw.rectangle((cx-190,cy-150,cx+190,cy-65),fill=accent)
        for r in range(3):
            for c in range(4):
                x=cx-120+c*80; y=cy-10+r*70
                draw.ellipse((x-10,y-10,x+10,y+10),fill=dark if (r+c)%3 else accent)
def make(item):
    bg,accent,dark,pale=PALETTES.get(item["b"],PALETTES["Age Calculators"])
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    d.ellipse((720,-80,1120,320),fill=pale); d.ellipse((-130,1180,270,1580),fill=pale)
    rr(d,(55,55,945,1445),42,(255,255,255),(230,233,239),2)
    brand="QUICKAGECALC"; bf=ff(25,True); bw=d.textbbox((0,0),brand,font=bf)[2]
    rr(d,(95,95,95+bw+52,150),27,accent); d.text((121,109),brand,font=bf,fill="white")
    board=item["b"].replace(" Calculators","").upper()
    badge=ff(20,True); bw2=d.textbbox((0,0),board,font=badge)[2]
    rr(d,(890-bw2-30,98,910,148),24,pale); d.text((875-bw2,112),board,font=badge,fill=dark)
    tf,lines=fit(d,item["t"],780,5); y=220
    for line in lines:
        bb=d.textbbox((0,0),line,font=tf); d.text(((W-(bb[2]-bb[0]))/2,y),line,font=tf,fill=dark); y+=bb[3]-bb[1]+18
    y=max(y+35,515)
    rr(d,(135,y,865,1115),36,bg); icon(d,500,(y+1115)//2,item["b"],accent,dark)
    rr(d,(250,1265,750,1345),38,accent)
    cta="CALCULATE IT FREE  →"; cf=ff(29,True); cb=d.textbbox((0,0),cta,font=cf)
    d.text(((W-cb[2])/2,1288),cta,font=cf,fill="white")
    site="QuickAgeCalc.com"; sf=ff(25,True); sb=d.textbbox((0,0),site,font=sf)
    d.text(((W-sb[2])/2,1372),site,font=sf,fill=dark)
    im.save(OUT/item["f"],"PNG",optimize=True)
for it in ITEMS: make(it)
print(f"Generated {len(ITEMS)} Pinterest images in {OUT}")
