"""Midlife Reset 90-day guided journal interior. 6x9in, no bleed, 120 pages, B&W."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import *
from reportlab.pdfgen import canvas

W, H = 6*IN, 9*IN
INSIDE, OUTSIDE, TOP, BOT = 0.625*IN, 0.5*IN, 0.55*IN, 0.55*IN   # KDP min gutter 0.375 (24-150pp), outside 0.25 no bleed
GREY = 0.35

WEEKS = [
 ("Baseline", ["Describe how your body feels today in five words, then write why you picked each one.",
  "What are the three things that bother you most right now? Be specific and honest.",
  "Think of a day last year that felt good. What was different about it?",
  "Which part of your daily routine gives you energy, and which part drains it?",
  "Write a letter of kindness to yourself as if you were a close friend.",
  "What would 'feeling like myself again' look like in your ordinary week?",
  "List what you have noticed about your patterns this week. No judgment, just notes."]),
 ("Sleep", ["Describe your ideal evening, from dinner to lights out.",
  "What thoughts show up when you wake in the night? Write them down and let them go.",
  "Which habits near bedtime help you sleep, and which get in the way?",
  "How does your bedroom feel? Name one small change you could make this week.",
  "What do you do when you cannot sleep? What would you like to try instead?",
  "Write about the last time you woke up truly rested.",
  "What would you tell a friend who sleeps as badly as you do?"]),
 ("Energy", ["At what time of day is your energy highest? How could you protect that hour?",
  "What are you saying yes to out of habit that you would rather say no to?",
  "List five small things that recharge you in under ten minutes.",
  "When did you last feel properly rested during the day? What made it possible?",
  "What tasks could you drop, share, or do more simply?",
  "Describe a pace of life that would feel sustainable.",
  "What does your body ask for when it is tired? Did you listen today?"]),
 ("Mood", ["Name the feeling you have carried most today. Where do you notice it in your body?",
  "What triggers a short fuse for you lately? What helps you pause?",
  "Write about a moment this week when you felt calm.",
  "What do you need to hear today? Write it out in your own voice.",
  "Which feelings do you tend to hide? What would it be like to let one be seen?",
  "List three things that made you laugh, smile, or relax recently.",
  "If your mood had a weather forecast this week, what would it be and what would you wear?"]),
 ("Body", ["Write about how your body has changed in the last few years, with curiosity rather than criticism.",
  "What does your body do for you every day that you rarely thank it for?",
  "Which symptoms come and go, and have you noticed anything that seems to come before them?",
  "How do you want to feel in your clothes? What would help that?",
  "What does comfort mean for your body right now?",
  "Describe a form of touch, warmth, or rest that you enjoy.",
  "What questions about your body would you like to ask a professional?"]),
 ("Food and water", ["What did you eat today that made you feel good afterwards?",
  "How much water did you drink, and what makes drinking enough easier for you?",
  "Which meals feel rushed? How could one of them be calmer?",
  "Write down what you would cook if you had no rules and plenty of time.",
  "Notice caffeine, alcohol, and sugar today. How do you feel a few hours later?",
  "What foods connect you with people you love?",
  "Plan three simple, nourishing meals for the coming days."]),
 ("Movement", ["What kind of movement did you enjoy as a child? Could any of it return?",
  "Describe a ten-minute walk you could take today. Where would it go?",
  "How does your body feel after moving versus after sitting all day?",
  "Which kind of exercise feels kind to you right now? Which feels like punishment?",
  "Who could move with you? Write down a name and an invitation.",
  "Write about a time your body felt strong.",
  "Set one gentle movement goal for next week."]),
 ("Stress", ["List everything on your mind right now, then circle the three that truly need you.",
  "Where do you feel stress in your body, and what eases it a little?",
  "What is one expectation you place on yourself that you could soften?",
  "Describe a place where you feel safe and unhurried.",
  "What boundaries would give you more room to breathe?",
  "Write down a worry, then write what you would say to a friend with the same worry.",
  "What helps you switch off at the end of the day?"]),
 ("Relationships", ["Who makes you feel understood? How could you spend more time with them?",
  "What would you like the people close to you to know about this season of your life?",
  "Write about a conversation you have been putting off.",
  "Who in your life asks too much of you? What would a fair arrangement look like?",
  "Describe a friendship you would like to nurture.",
  "What does support look like to you? How do you ask for it?",
  "Write a thank-you note you may or may not send."]),
 ("Work and purpose", ["What part of your work are you proud of at the moment?",
  "If you could change one thing about your working week, what would it be?",
  "What did you want to be doing at this stage of life? What has changed?",
  "List skills you have gained over the years that you rarely give yourself credit for.",
  "What would you do with an extra free afternoon every week?",
  "Describe something new you would like to learn or try.",
  "What does 'enough' look like for you, at work and at home?"]),
 ("Self-image", ["Write ten things you like about who you are today, none of them about appearance.",
  "How do you speak to yourself when you look in the mirror? How could you speak differently?",
  "Which messages about getting older did you absorb growing up? Which do you reject?",
  "Describe a woman you admire who is older than you. What do you admire?",
  "What are you ready to let go of in this chapter?",
  "What do you want to carry forward with you?",
  "Write a short portrait of yourself ten years from now."]),
 ("Support and care", ["List the questions and notes you would like to bring to your next appointment.",
  "What information would help you feel more in control? Where could you look for reliable sources?",
  "Which people or professionals make you feel heard? What makes them different?",
  "Write about any worries you have about asking for help.",
  "What does your support circle look like? Is anyone missing?",
  "Note what has changed since week one: sleep, energy, mood, anything else.",
  "Describe one thing you could do for your own care this week."]),
 ("Looking ahead", ["Read back through your journal. What patterns do you notice?",
  "Which small habits made the biggest difference to you? Write them as a short list.",
  "What are you proud of from the last twelve weeks?",
  "What is still hard? What kind of help would make it easier?",
  "Write your own rules for a good week.",
  "Describe the woman you are becoming, in as much detail as you like.",
  "Write a promise to yourself for the next ninety days."]),
]
assert len(WEEKS)*7 == 91

def footer(c, pg):
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setFont("Sans", 8); c.setFillGray(0.5)
    c.drawCentredString(l + (W-l-r)/2, 0.3*IN, str(pg)); c.setFillGray(0)

def lines(c, pg, ytop, ybot, gap=0.31*IN):
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setStrokeGray(0.72); c.setLineWidth(0.5)
    y = ytop
    while y > ybot:
        c.line(l, y, W-r, y); y -= gap
    c.setStrokeGray(0)

def scale(c, x, y, label, n=5):
    c.setFont("Sans", 8); c.drawString(x, y, label)
    for i in range(n):
        c.setLineWidth(0.7); c.circle(x + 0.95*IN + i*0.27*IN, y+2.8, 0.085*IN)
        c.setFont("Sans", 6); c.drawCentredString(x + 0.95*IN + i*0.27*IN, y+0.9, str(i+1))

def daily(c, pg, day, week, theme, prompt):
    l, r = margins(pg, INSIDE, OUTSIDE); cw = W-l-r
    y = H-TOP
    c.setFont("Serif-B", 15); c.drawString(l, y-12, f"Day {day}")
    c.setFont("Sans", 8.5); c.setFillGray(GREY)
    c.drawRightString(W-r, y-10, f"Week {week}  |  {theme}"); c.setFillGray(0)
    c.setLineWidth(1); c.line(l, y-20, W-r, y-20)
    # date
    c.setFont("Sans", 8.5); c.drawString(l, y-36, "Date:"); c.setLineWidth(0.5); c.line(l+0.38*IN, y-37, l+1.9*IN, y-37)
    # tracker box
    top = y-50; hbox = 1.5*IN
    c.setLineWidth(0.7); c.roundRect(l, top-hbox, cw, hbox, 5)
    c.setFont("Sans-B", 8.5); c.drawString(l+8, top-14, "Today's check-in")
    scale(c, l+8, top-32, "Sleep quality"); scale(c, l+8, top-50, "Energy"); scale(c, l+8, top-68, "Mood")
    xr = l + 0.45*cw
    c.setFont("Sans", 8)
    c.drawString(xr+0.35*IN, top-32, "Hours slept:"); c.line(xr+1.0*IN, top-33, xr+1.6*IN, top-33)
    c.drawString(xr+0.35*IN, top-50, "Glasses of water:"); c.line(xr+1.3*IN, top-51, xr+1.6*IN, top-51)
    c.drawString(xr+0.35*IN, top-68, "Hot flushes:"); c.line(xr+1.0*IN, top-69, xr+1.6*IN, top-69)
    c.drawString(l+8, top-88, "Moved today:   [  ] walk   [  ] stretch   [  ] strength   [  ] other"); 
    c.drawString(l+8, top-104, "Other symptoms or notes:"); c.line(l+1.35*IN, top-105, W-r-8, top-105)
    # prompt
    py = top-hbox-0.28*IN
    c.setFont("Sans-B", 8.5); c.drawString(l, py, "TODAY'S PROMPT")
    from reportlab.lib.utils import simpleSplit
    c.setFont("Serif-I", 12)
    ty = py-17
    for ln in simpleSplit(prompt, "Serif-I", 12, cw):
        c.drawString(l, ty, ln); ty -= 15
    lines(c, pg, ty-8, BOT+0.95*IN)
    # gratitude
    gy = BOT+0.55*IN
    c.setFont("Sans-B", 8.5); c.drawString(l, gy+0.12*IN, "One good thing today:")
    c.setLineWidth(0.5); c.line(l+1.35*IN, gy+0.10*IN, W-r, gy+0.10*IN)
    c.line(l, gy-0.2*IN, W-r, gy-0.2*IN)
    footer(c, pg)

def weekly(c, pg, week, theme):
    l, r = margins(pg, INSIDE, OUTSIDE); cw = W-l-r
    y = H-TOP
    c.setFont("Serif-B", 16); c.drawString(l, y-12, f"Week {week} Review")
    c.setFont("Sans", 9); c.setFillGray(GREY); c.drawRightString(W-r, y-10, theme); c.setFillGray(0)
    c.setLineWidth(1); c.line(l, y-20, W-r, y-20)
    qs = ["What went well this week?", "What was hardest?", "What patterns did I notice (sleep, energy, mood, symptoms)?",
          "One small change I will try next week:", "Something I am proud of:"]
    yy = y-42
    for q in qs:
        c.setFont("Sans-B", 9.5); c.drawString(l, yy, q)
        lines(c, pg, yy-18, yy-18-2*0.31*IN+1, 0.31*IN) if False else None
        c.setStrokeGray(0.72); c.setLineWidth(0.5)
        for k in range(2): c.line(l, yy-20-k*0.3*IN, W-r, yy-20-k*0.3*IN)
        c.setStrokeGray(0); yy -= 1.15*IN
    c.setFont("Sans-B", 9.5); c.drawString(l, yy, "Week at a glance (circle 1 to 5):")
    yy -= 22
    for lab in ["Sleep", "Energy", "Mood", "Overall"]:
        scale(c, l, yy, lab); yy -= 18
    footer(c, pg)

def textpage(c, pg, title, body, sub=None):
    from reportlab.lib.utils import simpleSplit
    l, r = margins(pg, INSIDE, OUTSIDE); cw = W-l-r
    y = H-1.1*IN
    c.setFont("Serif-B", 20); c.drawString(l, y, title); y -= 14
    c.setLineWidth(1); c.line(l, y, W-r, y); y -= 26
    for para in body:
        font = "Serif"; size = 11.5
        if para.startswith("##"): font="Sans-B"; size=10.5; para=para[2:].strip(); y -= 6
        for ln in simpleSplit(para, font, size, cw):
            c.setFont(font, size); c.drawString(l, y, ln); y -= size*1.5
        y -= 6
    footer(c, pg)

def writepage(c, pg, title):
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setFont("Serif-B", 16); c.drawString(l, H-TOP-12, title)
    c.setLineWidth(1); c.line(l, H-TOP-20, W-r, H-TOP-20)
    lines(c, pg, H-TOP-48, BOT+0.2*IN); footer(c, pg)

def build(path):
    c = canvas.Canvas(path, pagesize=(W, H), initialFontName="Sans")
    c.setTitle("Midlife Reset: 90-Day Guided Journal"); c.setAuthor("Your Pen Name Here")
    pg = 1
    # 1 title
    c.setFont("Serif-B", 30); c.drawCentredString(W/2, H-2.6*IN, "Midlife Reset")
    c.setFont("Serif", 15); c.drawCentredString(W/2, H-3.1*IN, "A 90-Day Guided Journal")
    c.setFont("Serif-I", 12); c.drawCentredString(W/2, H-3.55*IN, "for sleep, energy, mood, and the changes of midlife")
    c.setLineWidth(1); c.line(W/2-0.8*IN, H-3.9*IN, W/2+0.8*IN, H-3.9*IN)
    c.setFont("Sans", 10); c.drawCentredString(W/2, 1.3*IN, "Your Pen Name Here")
    c.showPage(); pg += 1
    # 2 copyright
    c.setFont("Sans", 8.5)
    for i, t in enumerate(["Copyright (c) 2026 Your Pen Name Here. All rights reserved.",
        "No part of this book may be reproduced without written permission of the publisher,",
        "except for personal use of the pages by the owner of this copy.", "",
        "This journal is for personal reflection and self-tracking. It is not medical advice and does",
        "not diagnose, treat, or prevent any condition. Please talk with a qualified healthcare",
        "professional about symptoms, medication, or any health concern.", "",
        "First edition. Printed by Amazon KDP."]):
        c.drawString(margins(pg,INSIDE,OUTSIDE)[0], 3.0*IN - i*13, t)
    c.showPage(); pg += 1
    # 3 how to use
    textpage(c, pg, "How to Use This Journal", [
        "This journal gives you one page for each of 90 days. Each page has a quick check-in you can finish in a minute, a single prompt to write about, and a line to finish the day with something good.",
        "##The daily check-in",
        "Circle a number from 1 (low) to 5 (high) for sleep quality, energy, and mood. Add hours slept, glasses of water, and any hot flushes or other symptoms you notice. Tick any movement. There are no right answers. The aim is simply to see your own patterns.",
        "##The prompts",
        "The 90 days are divided into 13 weeks, each with a theme, from sleep and energy to relationships and purpose. Write as much or as little as you like. Skip a day if you need to and carry on the next. A gap is not a failure.",
        "##The weekly review",
        "At the end of each week, look back at your check-ins. What do you notice? Choose one small change to try next week.",
        "##Sharing with your care team",
        "Your check-ins can help you describe changes clearly at an appointment. Bring the journal, or the weekly review pages."]); c.showPage(); pg += 1
    # 4 baseline
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setFont("Serif-B", 20); c.drawString(l, H-1.1*IN, "My Starting Point"); c.setLineWidth(1); c.line(l, H-1.1*IN-14, W-r, H-1.1*IN-14)
    items = ["Today's date:", "What brought me to start this journal:", "What I most want to feel better about:", "My biggest worry right now:",
             "One thing I am hopeful about:", "Questions for my doctor or care team:"]
    yy = H-1.9*IN
    for it in items:
        c.setFont("Sans-B", 10); c.drawString(l, yy, it)
        c.setStrokeGray(0.72); c.setLineWidth(0.5)
        for k in range(2 if "date" not in it else 0): c.line(l, yy-22-k*0.3*IN, W-r, yy-22-k*0.3*IN)
        c.setStrokeGray(0); yy -= 1.05*IN if "date" not in it else 0.4*IN
    footer(c, pg); c.showPage(); pg += 1
    # 5 blank intentions page (so daily starts on recto page 7? keep simple)
    writepage(c, pg, "My Intentions for the Next 90 Days"); c.showPage(); pg += 1
    # daily + weekly
    day = 1
    for w, (theme, prompts) in enumerate(WEEKS, 1):
        for p in prompts:
            if day > 90: break
            daily(c, pg, day, w, theme, p); c.showPage(); pg += 1; day += 1
        if w <= 12 or True:
            if w < 13:
                weekly(c, pg, w, theme); c.showPage(); pg += 1
    # day 91 trimmed: we have 90 days only; final weekly review for week 13
    weekly(c, pg, 13, "Looking ahead"); c.showPage(); pg += 1
    textpage(c, pg, "My 90-Day Reflection", ["Look back across your pages. Write about what has changed, what has stayed the same, and what you will carry forward."]); 
    lines(c, pg, H-2.8*IN, BOT+0.2*IN); c.showPage(); pg += 1
    while pg < 120:
        writepage(c, pg, "Notes"); c.showPage(); pg += 1
    # page 120 closing
    c.setFont("Serif-I", 12); c.drawCentredString(W/2, H/2, "Thank you for taking time for yourself."); footer(c, pg)
    c.showPage(); c.save()
    return pg
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "midlife-reset-journal_interior_6x9_120pp.pdf")
    print("pages", build(out))
