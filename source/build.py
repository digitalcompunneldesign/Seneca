"""Build the Seneca master + child homepages from one shared template.
Add a child site = add one entry to PROPS (5 tokens, logo, photos, copy)."""
import base64, os, sys, copy
from jinja2 import Environment, FileSystemLoader, select_autoescape

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def U(pid, w=1800):
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&q=80"

def logo(name):
    with open(os.path.join(ASSETS, name + '.png'), 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

img = dict(
    falls=U('1489447068241-b3490214e879', 2200), falls_alt=U('1533094602577-198d3beab8ea', 2000),
    casino_floor=U('1596838132731-3301c3fd4317', 2200), slots=U('1518895312237-a9e23508077d', 1400),
    cards=U('1511193311914-0346f16efe90', 1400),
    room1=U('1611892440504-42a792e24d32', 1400), room2=U('1590490360182-c33d57733427', 1200), room3=U('1566665797739-1674de7a421a', 1200),
    dining1=U('1414235077428-338989a2e8c0', 1400), dining2=U('1517248135467-4c7edcad34c4', 1200),
    bar1=U('1514933651103-005eec06c04b', 1200), bar2=U('1572116469696-31de0f17cc34', 1200),
    concert_warm=U('1470229722913-7c0e2dbbafd3', 2000), concert_stage=U('1459749411175-04bf5292ceea', 2000), concert_color=U('1514525253161-7a46d19cd819', 1600),
    spa=U('1540555700478-4be289fbecef', 1200), pool=U('1576013551627-0cc20b96c2a7', 1200),
    golf_swing=U('1535131749006-b7f58c99034b', 2200), golf_ball=U('1587174486073-ae5e5cff23aa', 1400), golf_aerial=U('1500932334442-8761ee4810a7', 2000),
    hills=U('1470071459604-3b5ec3a7fe05', 2200), forest=U('1448375240586-882707db888b', 1600),
    city_night=U('1519501025264-65ba15a82390', 2000), ballroom=U('1519167758481-83f550bb49b3', 1600), conference=U('1511578314322-379afb476865', 1400),
)
logos = dict(master=logo('logo-master'), masterWhite=logo('logo-master-white'))

P = dict(  # icon paths for the quick-plan bar
    room='M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M3 14h18M3 18v2M21 18v2M7 10V7a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3',
    offer='M20 12v8H4v-8M2 7h20v5H2zM12 22V7M12 7c-2-4-6-4-6-1s4 1 6 1zM12 7c2-4 6-4 6-1s-4 1-6 1z',
    dine='M7 3v8a2 2 0 0 0 2 2v8M11 3v8M3 3v8a2 2 0 0 0 2 2M17 21V3c2 0 4 2 4 6s-2 5-4 5',
    ticket='M3 8a2 2 0 0 0 0 4v4h18v-4a2 2 0 0 1 0-4V4H3zM14 4v16',
    game='M4 4h16v16H4zM8.5 8.5h.01M15.5 15.5h.01M15.5 8.5h.01M8.5 15.5h.01M12 12h.01',
    pin='M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12zM12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z',
    flag='M5 21V4M5 4h11l-2 4 2 4H5')

casino_items = ['Slots', 'Table games', 'Poker & sportsbook (where offered)', 'Player services']
casino_note = 'Must be 21+. Play responsibly — 1-877-8-HOPENY.'

PROPS = [
  dict(key='niagara', file='seneca-niagara.html', name='Seneca Niagara Resort & Casino', short='Seneca Niagara', tiny='Niagara',
       city='Niagara Falls, NY', mapQuery='Seneca Niagara Resort & Casino, Niagara Falls, NY',
       accent='#659bd0', ink='#2f6ca8', onAccent='#0b1a2a', deep='#0b1a2a', tint='#eaf2fa',
       logo=logo('logo-niagara'), logoWhite=logo('logo-niagara-white'),
       hero=img['falls'], heroAlt='Horseshoe Falls at dusk, mist rising over the river',
       card=img['falls_alt'], cardAlt='Niagara Falls with mist rising',
       facts='Niagara Falls, NY · Hotel · Casino · Spa · Live entertainment',
       heroLine='Your Niagara getaway.', heroSub='Stay minutes from the Falls, then play, dine and catch a show without leaving the resort.',
       primary='Book a stay', primaryHref='#stay', secondary='Explore offers', secondaryHref='#offers', masterCta='Book a stay',
       hasHotel=True, hasCasino=True, offer1='[Room package title]', offer1Cat='Rooms & packages', offerImg=img['room1'],
       feature=img['casino_floor'], featureKicker='Gaming', featureTitle='Play the<br>Niagara floor.', featureItems=casino_items, featureNote=casino_note,
       diningTypes='Signature · Casual · Bars & lounges · Quick bites',
       amenities=[dict(n='Spa & salon', tag='On property'), dict(n='Pool & fitness', tag='On property'), dict(n='Shopping', tag='On property'),
                  dict(n='Niagara Falls State Park', tag='Nearby'), dict(n='Seneca Hickory Stick Golf', tag='Seneca property', href='seneca-hickory-stick.html')]),
  dict(key='allegany', file='seneca-allegany.html', name='Seneca Allegany Resort & Casino', short='Seneca Allegany', tiny='Allegany',
       city='Salamanca, NY', mapQuery='Seneca Allegany Resort & Casino, Salamanca, NY',
       accent='#b77e42', ink='#8a5a26', onAccent='#1f1408', deep='#2b1d12', tint='#f7efe4',
       logo=logo('logo-allegany'), logoWhite=logo('logo-allegany-white'),
       hero=img['hills'], heroAlt='Green hills and valley under drifting morning cloud',
       card=img['hills'], cardAlt='Allegany hills in morning mist',
       facts='Salamanca, NY · Hotel · Casino · Spa · Live entertainment',
       heroLine='Your Allegany escape.', heroSub='Mountain air by day, the casino floor and a show by night.',
       primary='Book a stay', primaryHref='#stay', secondary='Explore offers', secondaryHref='#offers', masterCta='Book a stay',
       hasHotel=True, hasCasino=True, offer1='[Room package title]', offer1Cat='Rooms & packages', offerImg=img['room2'],
       feature=img['slots'], featureKicker='Gaming', featureTitle='Play the<br>Allegany floor.', featureItems=casino_items, featureNote=casino_note,
       diningTypes='Signature · Casual · Bars & lounges · Quick bites',
       amenities=[dict(n='Spa & salon', tag='On property'), dict(n='Pool & fitness', tag='On property'), dict(n='Shopping', tag='On property'),
                  dict(n='Allegany State Park', tag='Nearby')]),
  dict(key='buffalo', file='seneca-buffalo-creek.html', name='Seneca Buffalo Creek Casino', short='Seneca Buffalo Creek', tiny='Buffalo Creek',
       city='Buffalo, NY', mapQuery='Seneca Buffalo Creek Casino, Buffalo, NY',
       accent='#bc4033', ink='#bc4033', onAccent='#ffffff', deep='#200807', tint='#fbeeec',
       logo=logo('logo-buffalo'), logoWhite=logo('logo-buffalo-white'),
       hero=img['city_night'], heroAlt='Downtown street glowing at night between tall buildings',
       card=img['city_night'], cardAlt='City lights at night',
       facts='Buffalo, NY · Casino · Dining · No hotel on site',
       heroLine='Downtown Buffalo’s night out.', heroSub='Gaming, dining and live music, a short walk from the waterfront and the arenas.',
       primary='View offers', primaryHref='#offers', secondary='What’s on', secondaryHref='#events', masterCta='View offers',
       hasHotel=False, hasCasino=True, offer1='[Casino offer title]', offer1Cat='Casino', offerImg=img['cards'],
       feature=img['casino_floor'], featureKicker='Gaming', featureTitle='Play<br>downtown.', featureItems=casino_items, featureNote=casino_note,
       diningTypes='Casual · Bars & lounges · Quick bites',
       amenities=[dict(n='Bars & live music', tag='On property'), dict(n='Canalside & waterfront', tag='Nearby'),
                  dict(n='Stay at Seneca Niagara', tag='Seneca property', href='seneca-niagara.html')]),
  dict(key='hickory', file='seneca-hickory-stick.html', name='Seneca Hickory Stick Golf', short='Hickory Stick Golf', tiny='the course',
       city='Lewiston, NY', mapQuery='Seneca Hickory Stick Golf, Lewiston, NY',
       accent='#89b24b', ink='#4e7426', onAccent='#14200b', deep='#1a2a10', tint='#eef4e4',
       logo=logo('logo-hickory'), logoWhite=logo('logo-hickory-white'),
       hero=img['golf_aerial'], heroAlt='Aerial view of fairways and sand bunkers',
       card=img['golf_swing'], cardAlt='Golfer driving from the tee on a green fairway',
       facts='Lewiston, NY · Championship golf · Not a casino',
       heroLine='Your round at Hickory Stick.', heroSub='Championship golf near Niagara Falls — book a tee time, then stay and play at Seneca Niagara.',
       primary='Book a tee time', primaryHref='#course', secondary='Golf packages', secondaryHref='#offers', masterCta='Book a tee time',
       hasHotel=False, hasCasino=False, offer1='[Stay & play package]', offer1Cat='Golf packages', offerImg=img['golf_ball'],
       feature=img['golf_swing'], featureKicker='The course', featureTitle='Plan<br>your round.',
       featureItems=['Tee times & rates', 'Lessons & clinics', 'Leagues & tournaments', 'Pro shop'], featureNote='Rates and availability vary by season — [season dates].',
       diningTypes='Clubhouse · Grill',
       amenities=[dict(n='Clubhouse & grill', tag='On property'), dict(n='Practice facility', tag='On property'),
                  dict(n='Stay at Seneca Niagara', tag='Seneca property', href='seneca-niagara.html')]),
]

# Display order everywhere (cards, nav, footers, siblings): palette order 1–4
ORDER = ['niagara', 'hickory', 'buffalo', 'allegany']
PROPS.sort(key=lambda p: ORDER.index(p['key']))

MASTER = dict(accent='#533095', ink='#533095', onAccent='#ffffff', deep='#120b1f', tint='#f6f4f9')

env = Environment(loader=FileSystemLoader(os.path.join(HERE, 'tpl')), autoescape=select_autoescape(['j2']))
byk = {p['key']: p for p in PROPS}

def where(*keys): return [byk[k] for k in ORDER if k in keys]
experiences = [
    dict(name='Rooms & stays', img=img['room1'], thumb=U('1611892440504-42a792e24d32', 200), alt='Warm, wood-panelled hotel room', where=where('niagara', 'allegany'), href='seneca-niagara.html#stay'),
    dict(name='Gaming', img=img['casino_floor'], thumb=U('1596838132731-3301c3fd4317', 200), alt='Casino floor with slot machines', where=where('niagara', 'allegany', 'buffalo'), href='seneca-niagara.html#gaming'),
    dict(name='Dining', img=img['dining1'], thumb=U('1414235077428-338989a2e8c0', 200), alt='Plated dinner and wine glasses', where=where('niagara', 'allegany', 'buffalo'), href='seneca-niagara.html#dining'),
    dict(name='Live entertainment', img=img['concert_stage'], thumb=U('1459749411175-04bf5292ceea', 200), alt='Crowd facing a lit stage', where=where('niagara', 'allegany'), href='#whatson'),
    dict(name='Spa & amenities', img=img['spa'], thumb=U('1540555700478-4be289fbecef', 200), alt='Spa towels and flowers', where=where('niagara', 'allegany'), href='seneca-niagara.html#amenities'),
    dict(name='Golf', img=img['golf_swing'], thumb=U('1535131749006-b7f58c99034b', 200), alt='Golfer on the tee', where=where('hickory'), href='seneca-hickory-stick.html'),
    dict(name='Meetings & events', img=img['ballroom'], thumb=U('1519167758481-83f550bb49b3', 200), alt='Ballroom set for a banquet', where=where('niagara', 'allegany'), href='#meetings'),
]

html = env.get_template('master.j2').render(
    title='Seneca Resorts & Casinos — Plan your visit', description='Choose a Seneca destination, find offers, see what’s on and book your stay.',
    t=MASTER, child=False, img=img, logos=logos, props=PROPS, by=byk, experiences=experiences)
open(os.path.join(OUT, 'index.html'), 'w').write(html)

for p in PROPS:
    t = copy.deepcopy(p)
    tasks = [
        dict(label='Book a room', icon=P['room'], href='#stay') if t['hasHotel'] else (None if t['hasCasino'] else dict(label='Book a tee time', icon=P['flag'], href='#course')),
        dict(label='View offers', icon=P['offer'], href='#offers'),
        dict(label='Dining', icon=P['dine'], href='#dining'),
        dict(label='Events & tickets', icon=P['ticket'], href='#events'),
        dict(label='Gaming', icon=P['game'], href='#gaming') if t['hasCasino'] else None,
        dict(label='Directions', icon=P['pin'], href='#visit'),
    ]
    nav = [dict(label='Stay', href='#stay') if t['hasHotel'] else None,
           dict(label='Offers', href='#offers'),
           dict(label='Gaming', href='#gaming') if t['hasCasino'] else dict(label='The course', href='#course'),
           dict(label='Dining', href='#dining'), dict(label='Entertainment', href='#events'),
           dict(label='Amenities', href='#amenities'), dict(label='Social Club', href='#club'), dict(label='Plan your visit', href='#visit')]
    rooms = [dict(name='[Room type 1]', meta='King or two queens · from [$rate]', img=img['room1'], alt='Hotel room with king bed'),
             dict(name='[Room type 2]', meta='View room · from [$rate]', img=img['room2'], alt='Room with sofa and queen bed'),
             dict(name='[Suite]', meta='Separate living area · from [$rate]', img=img['room3'], alt='Suite bedroom with soft lighting')]
    if t['hasCasino']:
        dining = [dict(name='[Signature restaurant]', meta='Signature · Reservations recommended', img=img['dining1'], alt='Plated fine-dining course'),
                  dict(name='[Casual restaurant]', meta='Casual · Walk-ins welcome', img=img['dining2'], alt='Casual dining room'),
                  dict(name='[Bar & lounge]', meta='Bars & lounges · Live music [days]', img=img['bar2'], alt='Backlit bar with pendant lights')]
        events = [dict(day='14', mon='NOV · SAT', title='[Headliner name]', sub='Concert · Doors [time] · 21+', venue='[Venue name]', tickets=True),
                  dict(day='28', mon='NOV · FRI', title='[Comedy headliner]', sub='Comedy · Show [time]', venue='[Venue name]', tickets=True),
                  dict(day='06', mon='DEC · SAT', title='[Live band]', sub='Live music · Free entry', venue='[Lounge name]', tickets=False)]
    else:
        dining = [dict(name='[Clubhouse grill]', meta='Clubhouse · Open in season', img=img['bar1'], alt='Warm clubhouse bar'),
                  dict(name='[Patio & halfway house]', meta='Quick bites on the course', img=img['dining2'], alt='Casual dining room'),
                  dict(name='Dine at Seneca Niagara', meta='Seneca property · Signature dining', img=img['dining1'], alt='Plated fine-dining course')]
        events = [dict(day='[DD]', mon='[MON]', title='[Member-guest tournament]', sub='Tournament · Registration open', venue='Hickory Stick', tickets=True),
                  dict(day='[DD]', mon='[MON]', title='[Junior clinic]', sub='Lessons · Ages [x–y]', venue='Practice facility', tickets=False)]
    siblings = [s for s in PROPS if s['key'] != t['key']]
    html = env.get_template('child.j2').render(
        title=f"{t['name']} — {t['heroLine']}", description=t['heroSub'], t=t, child=True, img=img, logos=logos,
        tasks=[k for k in tasks if k], nav=[n for n in nav if n], rooms=rooms, dining=dining, events=events, siblings=siblings)
    open(os.path.join(OUT, t['file']), 'w').write(html)
print('built', sorted(os.listdir(OUT)))
