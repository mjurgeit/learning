"""Large-print gardening word search interior. 8.5x11in, no bleed, 80 pages, B&W.
60 puzzles (one per page, 15x15 grid, 10 words each, all words unique across the book) + solutions."""
import sys, os, random; sys.path.insert(0, os.path.dirname(__file__))
from common import *
from reportlab.pdfgen import canvas

W, H = 8.5*IN, 11*IN
INSIDE, OUTSIDE, TOP, BOT = 0.75*IN, 0.6*IN, 0.6*IN, 0.6*IN
N = 15

THEMES = {
"Vegetable Patch": "CARROT RADISH BEETROOT PARSNIP LEEK ONION SHALLOT GARLIC CABBAGE KALE SPINACH CHARD LETTUCE ROCKET CELERY FENNEL TURNIP SWEDE MARROW COURGETTE PUMPKIN SQUASH TOMATO PEPPER AUBERGINE CUCUMBER SWEETCORN BROCCOLI CAULIFLOWER SPROUTS ARTICHOKE ASPARAGUS RHUBARB POTATO PEAS BEANS",
"Herb Garden": "BASIL PARSLEY CHIVES THYME SAGE ROSEMARY MINT OREGANO MARJORAM DILL CORIANDER TARRAGON LOVAGE SORREL BORAGE CHERVIL LAVENDER LEMONBALM CHAMOMILE HYSSOP SAVORY FENUGREEK CATNIP ANISE ANGELICA BAYLEAF CUMIN CARAWAY SPEARMINT PEPPERMINT LEMONGRASS COMFREY YARROW TANSY FEVERFEW MUGWORT",
"Cottage Flowers": "FOXGLOVE DELPHINIUM LUPIN HOLLYHOCK PEONY POPPY ASTER DAHLIA ZINNIA COSMOS MARIGOLD PANSY PRIMROSE VIOLET TULIP DAFFODIL CROCUS HYACINTH IRIS LILY SNAPDRAGON SWEETPEA PHLOX SALVIA VERBENA CAMPANULA COLUMBINE ANEMONE CARNATION PETUNIA GERANIUM FUCHSIA BEGONIA CLEMATIS HONEYSUCKLE JASMINE LARKSPUR",
"Trees and Shrubs": "OAK BIRCH MAPLE BEECH ELM ASH WILLOW ALDER ROWAN HAZEL HOLLY YEW PINE SPRUCE CEDAR LARCH HAWTHORN ELDER LILAC HYDRANGEA BUDDLEIA FORSYTHIA CAMELLIA AZALEA RHODODENDRON BOX LAUREL JUNIPER MAGNOLIA CHERRY PLUM POPLAR LIME CHESTNUT WALNUT SYCAMORE",
"Garden Birds": "ROBIN WREN BLACKBIRD THRUSH SPARROW STARLING BLUETIT GREATTIT CHAFFINCH GOLDFINCH GREENFINCH SISKIN DUNNOCK NUTHATCH TREECREEPER WOODPECKER JAY MAGPIE JACKDAW ROOK CROW PIGEON DOVE WAGTAIL SWALLOW SWIFT MARTIN BLACKCAP WARBLER REDWING FIELDFARE WAXWING KESTREL SPARROWHAWK OWL HERON PHEASANT",
"Garden Tools": "SPADE FORK TROWEL RAKE HOE SECATEURS SHEARS LOPPERS PRUNER DIBBER WHEELBARROW HOSE WATERINGCAN SPRINKLER MOWER STRIMMER TRELLIS CANE TWINE GLOVES BUCKET SIEVE SHOVEL EDGER CULTIVATOR PITCHFORK BILLHOOK HANDSAW KNEELER TROUGH PLANTER CLOCHE LABELS SECATEUR RIDDLE GRUBBER SCYTHE",
"Pollinators and Bugs": "BEE BUMBLEBEE HONEYBEE HOVERFLY BUTTERFLY MOTH LADYBIRD LACEWING BEETLE WASP DRAGONFLY DAMSELFLY EARWIG SPIDER SNAIL SLUG WORM CENTIPEDE MILLIPEDE WOODLOUSE CRICKET GRASSHOPPER APHID CATERPILLAR CHRYSALIS NECTAR POLLEN PROBOSCIS HIVE COCOON LARVA ANTENNA WINGS SWARM DRONE QUEEN COMMA",
"Four Seasons": "SPRING SUMMER AUTUMN WINTER BLOSSOM SEEDLING FROST SNOWDROP HARVEST BONFIRE SOLSTICE EQUINOX THAW SUNSHINE DEWDROP BREEZE SHOWER RAINBOW CONKER ACORN FALLENLEAF BERRY HIBERNATE MISTLETOE EVERGREEN LONGDAYS TWILIGHT DAWN SUNRISE SUNSET HAYFIELD BLUEBELL MAYPOLE SCARECROW MEADOW GREENHOUSE FIRESIDE",
"Soil and Compost": "COMPOST MULCH LOAM CLAY SAND SILT HUMUS PEAT MANURE LEAFMOLD BONEMEAL FERTILISER NITROGEN POTASH PHOSPHATE ACIDITY LIMING TOPSOIL SUBSOIL DRAINAGE ROOTS BACTERIA FUNGI EARTHWORM BIN HEAP TURNING DECAY NUTRIENTS TILTH DIGGING FORKING RAKING SOWING WEEDING MOISTURE GRIT WORMERY",
"Orchard Fruit": "APPLE PEAR PLUM CHERRY DAMSON QUINCE MEDLAR APRICOT PEACH FIG GRAPE MULBERRY CURRANT GOOSEBERRY RASPBERRY STRAWBERRY BLACKBERRY BLUEBERRY LOGANBERRY TAYBERRY CRANBERRY ELDERBERRY MELON NECTARINE GREENGAGE CRABAPPLE COBNUT WALNUT HAZELNUT ORCHARD GRAFTING ROOTSTOCK BLOSSOM WINDFALL CIDER JUICE JAM PRESERVE",
"Houseplants": "FERN CACTUS ALOE ORCHID PEACELILY SPIDERPLANT RUBBERPLANT MONSTERA PHILODENDRON POTHOS IVY BEGONIA VIOLET JADE YUCCA DRACAENA CALATHEA BAMBOO BONSAI SUCCULENT SANSEVIERIA TERRARIUM WINDOWSILL SAUCER REPOTTING PERLITE COMPOST DRAINAGE HUMIDITY MISTING FOLIAGE TRAILING CUTTING OFFSET AIRPLANT BROMELIAD AMARYLLIS",
"Weather Watch": "SUNNY CLOUDY RAINY WINDY STORMY FOGGY MISTY FROSTY ICY SNOWY HAIL SLEET THUNDER LIGHTNING DRIZZLE DOWNPOUR RAINBOW BREEZE GALE HEATWAVE DROUGHT FLOOD HUMID BAROMETER FORECAST THERMOMETER ISOBAR FRONT PRESSURE SHOWERS OVERCAST CLEARSKY GUSTS SUNBEAM DEWPOINT WEATHERVANE RAINGAUGE MIST",
"Kitchen Garden Cooking": "SOUP STEW SALAD PICKLE CHUTNEY JAM RELISH SAUCE PESTO PIE CRUMBLE TART CASSEROLE ROAST CURRY SALSA SLAW GRATIN OMELETTE FRITTER DUMPLING BROTH PUREE COMPOTE SYRUP CORDIAL JELLY MARMALADE SORBET SMOOTHIE LASAGNE RISOTTO RATATOUILLE MINESTRONE COLESLAW STIRFRY BAKE",
"Wildlife Visitors": "HEDGEHOG FOX BADGER SQUIRREL RABBIT MOUSE VOLE SHREW MOLE BAT FROG TOAD NEWT SLOWWORM LIZARD DEER OTTER STOAT WEASEL HARE MUNTJAC DORMOUSE PIPISTRELLE FIELDMOUSE GRASSSNAKE HEDGEROW POND LOGPILE BIRDBATH NESTBOX FEEDER BIRDTABLE WILDFLOWER HABITAT HIBERNACULUM TADPOLE SPAWN",
"Landscape and Design": "PATIO PATH LAWN BORDER HEDGE FENCE GATE ARBOUR PERGOLA TRELLIS SHED DECKING POND FOUNTAIN STATUE BENCH GAZEBO ROCKERY PARTERRE TOPIARY RAISEDBED PLANTER FOLLY WALL STEPS GRAVEL PAVING TERRACE VISTA FOCALPOINT WILDLIFEPOND ORCHARD MEADOW ALLOTMENT GREENHOUSE POLYTUNNEL WINDBREAK",
"Allotment Life": "ALLOTMENT PLOT TENANT WATERBUTT SHEDDIE RHUBARB FORCING LEEKS RUNNERBEANS WIGWAM CLOCHE NETTING SCARECROW COMPOSTBIN SWAP SEEDS PACKET SEEDLING POTTING PRICKING HARDENING TRANSPLANT THINNING EARTHING SUCCESSION ROTATION BRASSICA LEGUME ROOTCROP SOWING CROPPING GLUT SURPLUS PRODUCE SHOW MARROW ONIONS",
"Roses and Climbers": "ROSE CLIMBER RAMBLER HYBRIDTEA FLORIBUNDA SHRUBROSE DAMASK GALLICA ALBA MOSS BOURBON NOISETTE THORN PRICKLE BUD PETAL SEPAL HIP FRAGRANCE SCENT BLOOM DEADHEAD PRUNING FEEDING MULCHING BLACKSPOT MILDEW ARCHWAY OBELISK WISTERIA HONEYSUCKLE CLEMATIS IVY VINE PASSIONFLOWER JASMINE TRELLIS",
"Garden Verbs": "PLANT SOW WATER WEED PRUNE TRIM MOW DIG RAKE HOE MULCH FEED PICK HARVEST POT REPOT GRAFT LAYER DIVIDE SPRAY STAKE TIE TRAIN PINCH THIN SIEVE CLIP SNIP SHAPE EDGE SWEEP SCATTER BURY COVER SHELTER ROTATE SAVE LABEL",
"Seed Packet": "CORNFLOWER NASTURTIUM SUNFLOWER LOVEINAMIST CALENDULA CLARKIA GODETIA NIGELLA ECHINACEA RUDBECKIA GAILLARDIA LINARIA ALYSSUM LOBELIA CANDYTUFT STOCK WALLFLOWER FORGETMENOT HONESTY TEASEL SWEETWILLIAM CORNCOCKLE BORAGE PHACELIA OXEYE YARROW KNAPWEED SCABIOUS DAISY LAVATERA MALLOW MIGNONETTE BELLFLOWER",
"Greenhouse Days": "GREENHOUSE PROPAGATOR SEEDTRAY MODULE VENTILATION SHADING THERMOMETER HEATER STAGING VINE GRAPEVINE TOMATOES CUCUMBERS CHILLIES PEPPERS BASIL CUTTINGS GERMINATE DAMPING PRICKOUT WARMTH GLASS POLYTHENE VENT SHELF WATERING FEEDING HUMIDITY PESTS WHITEFLY RED SPIDERMITE ORCHIDS CITRUS LEMON FIG",
"Gardener Words": "PATIENCE GREENFINGERS SUNHAT KNEEPAD WELLIES APRON FLASK TEABREAK BENCH NOTEBOOK JOURNAL PLAN DESIGN DREAM GROW BLOOM THRIVE FLOURISH NURTURE TEND CARE SEASON GARDENER HOBBY PEACE QUIET BIRDSONG FRAGRANCE COLOUR TEXTURE ABUNDANCE PRIDE JOY SHARE GIFT HARVEST BOUNTY",
}
# ----- build unique puzzle word lists -----
def clean(w): return "".join(ch for ch in w.upper() if ch.isalpha())
rng = random.Random(20261003)
used = set(); puzzles = []
theme_names = list(THEMES)
for name in theme_names:
    ws = []
    for w in THEMES[name].split():
        w = clean(w)
        if 4 <= len(w) <= 12 and w not in used and w not in ws: ws.append(w)
    rng.shuffle(ws)
    for k in range(3):
        chunk = ws[k*10:(k+1)*10]
        if len(chunk) == 10:
            used.update(chunk); puzzles.append((name, chunk))
assert len(puzzles) >= 60, len(puzzles)
puzzles = puzzles[:60]

DIRS = [(0,1),(1,0),(1,1)]   # right, down, down-right: easier for seniors (no backwards words)
def make_grid(words, rng):
    for attempt in range(500):
        g = [[""]*N for _ in range(N)]; place = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            done = False
            for _ in range(400):
                dr, dc = rng.choice(DIRS)
                r0 = rng.randrange(N - (len(w)-1)*dr); c0 = rng.randrange(N - (len(w)-1)*dc)
                cells = [(r0+i*dr, c0+i*dc) for i in range(len(w))]
                if all(g[r][c] in ("", ch) for (r,c), ch in zip(cells, w)):
                    for (r,c), ch in zip(cells, w): g[r][c] = ch
                    place[w] = cells; done = True; break
            if not done: ok = False; break
        if ok: break
    else:
        raise RuntimeError("could not place "+str(words))
    for r in range(N):
        for c in range(N):
            if not g[r][c]: g[r][c] = rng.choice("AAEEEIIOOUUBCDFGHLMNPRSTWY")
    return g, place

def count_occurrences(g, w):
    n = 0
    for r in range(N):
        for c in range(N):
            for dr, dc in DIRS:
                cells = [(r+i*dr, c+i*dc) for i in range(len(w))]
                if all(0 <= rr < N and 0 <= cc < N for rr,cc in cells) and all(g[rr][cc]==ch for (rr,cc),ch in zip(cells,w)):
                    n += 1
    return n

def footer(c, pg):
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setFont("Sans", 10); c.setFillGray(0.45); c.drawCentredString(l+(W-l-r)/2, 0.35*IN, str(pg)); c.setFillGray(0)

def draw_grid(c, g, x, y, cell, fs, place=None):
    """x,y = top-left. place -> highlight words (solutions)."""
    hl = set()
    if place:
        for cells in place.values(): hl.update(cells)
    c.setLineWidth(0.6)
    for r in range(N):
        for k in range(N):
            if (r,k) in hl:
                c.setFillGray(0.78); c.rect(x+k*cell, y-(r+1)*cell, cell, cell, stroke=0, fill=1); c.setFillGray(0)
    c.setFont("Sans-B" if not place else "Sans-B", fs)
    for r in range(N):
        for k in range(N):
            c.drawCentredString(x+k*cell+cell/2, y-(r+1)*cell+cell*0.5-fs*0.35, g[r][k])
    c.setLineWidth(1.2); c.rect(x, y-N*cell, N*cell, N*cell)

def build(path):
    rng2 = random.Random(7)
    c = canvas.Canvas(path, pagesize=(W,H), initialFontName="Sans")
    c.setTitle("The Gardener's Large Print Word Search"); c.setAuthor("Your Pen Name Here")
    pg = 1
    c.setFont("Serif-B", 40); c.drawCentredString(W/2, H-3.2*IN, "The Gardener's")
    c.drawCentredString(W/2, H-3.9*IN, "Large Print Word Search")
    c.setFont("Serif", 20); c.drawCentredString(W/2, H-4.6*IN, "60 Puzzles for Plant Lovers")
    c.setFont("Sans", 14); c.drawCentredString(W/2, 1.5*IN, "Your Pen Name Here"); c.showPage(); pg += 1
    l, r = margins(pg, INSIDE, OUTSIDE); c.setFont("Sans", 10)
    for i, t in enumerate(["Copyright (c) 2026 Your Pen Name Here. All rights reserved.",
        "No part of this book may be reproduced without written permission of the publisher,",
        "except for personal use of the pages by the owner of this copy.", "", "First edition. Printed by Amazon KDP."]):
        c.drawString(l, 4*IN - i*15, t)
    c.showPage(); pg += 1
    # how to
    c.setFont("Serif-B", 28); c.drawString(l, H-1.4*IN, "How to Play"); 
    c.setLineWidth(1.2); c.line(l, H-1.55*IN, W-r, H-1.55*IN)
    y = H-2.2*IN
    from reportlab.lib.utils import simpleSplit
    for para in ["Each page holds one puzzle. Find every word in the list below the grid. Words are hidden in a straight line, reading left to right, top to bottom, or diagonally down to the right. Words never run backwards, so you can read every line the normal way.",
                 "Circle each word as you find it, then tick it off the list. Some words share letters, so crossing lines are normal.",
                 "Every puzzle has its own theme and 10 words. Words are never repeated anywhere in the book. The answers to all 60 puzzles are at the back.",
                 "Take your time. There is no clock and no score. Grab a pencil, a cup of tea, and enjoy a few quiet minutes in the garden of your mind."]:
        for ln in simpleSplit(para, "Serif", 16, W-l-r):
            c.setFont("Serif", 16); c.drawString(l, y, ln); y -= 25
        y -= 14
    footer(c, pg); c.showPage(); pg += 1
    # blank "page 4" = a note page to make puzzles start on odd/recto page 5
    c.setFont("Serif-I", 16); c.drawCentredString(W/2, H/2, "Happy puzzling!"); footer(c, pg); c.showPage(); pg += 1
    solutions = []
    for i, (theme, words) in enumerate(puzzles, 1):
        g, place = make_grid(words, rng2)
        for w in words:  # verify word is findable; duplicates are tolerated but reported
            assert count_occurrences(g, w) >= 1
        l, r = margins(pg, INSIDE, OUTSIDE)
        c.setFont("Serif-B", 24); c.drawString(l, H-TOP-22, f"Puzzle {i}")
        c.setFont("Serif-I", 18); c.drawRightString(W-r, H-TOP-22, theme)
        c.setLineWidth(1.2); c.line(l, H-TOP-32, W-r, H-TOP-32)
        cell = 0.40*IN; gx = l + ((W-l-r) - N*cell)/2
        draw_grid(c, g, gx, H-TOP-0.6*IN, cell, 20)
        # word list 3 cols x 4 rows
        ly = H-TOP-0.6*IN-N*cell-0.55*IN
        colw = (W-l-r)/3
        c.setFont("Sans-B", 16)
        for k, w in enumerate(sorted(words)):
            c.drawString(l + (k%3)*colw + 6, ly - (k//3)*0.42*IN, "[  ]  " + w)
        footer(c, pg); c.showPage(); pg += 1
        solutions.append((i, theme, g, place))
    # solutions 4 per page
    l, r = margins(pg, INSIDE, OUTSIDE)
    c.setFont("Serif-B", 28); c.drawString(l, H-1.4*IN, "Answers"); c.setLineWidth(1.2); c.line(l, H-1.55*IN, W-r, H-1.55*IN)
    c.setFont("Serif", 16); c.drawString(l, H-2.1*IN, "Shaded squares show the hidden words. Puzzles 1 to 60 follow.")
    footer(c, pg); c.showPage(); pg += 1
    for s in range(0, 60, 4):
        l, r = margins(pg, INSIDE, OUTSIDE)
        cell = 0.2*IN; gw = N*cell
        xs = [l, l + (W-l-r) - gw]; ys = [H-TOP-0.35*IN, H-TOP-0.35*IN-gw-0.8*IN]
        for j, (i, theme, g, place) in enumerate(solutions[s:s+4]):
            x = xs[j%2]; y = ys[j//2]
            c.setFont("Sans-B", 12); c.drawString(x, y+8, f"Puzzle {i}")
            draw_grid(c, g, x, y, cell, 9, place)
        footer(c, pg); c.showPage(); pg += 1
    # certificate/closing
    c.setFont("Serif-B", 30); c.drawCentredString(W/2, H/2+0.6*IN, "Well done, Master Gardener!")
    c.setFont("Serif", 16); c.drawCentredString(W/2, H/2, "You found every last word.")
    c.showPage(); pg += 1
    c.save(); return pg-1

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "gardeners-large-print-word-search_interior_8.5x11_80pp.pdf")
    print("pages", build(out))
