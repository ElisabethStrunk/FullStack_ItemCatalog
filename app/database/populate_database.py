#!/usr/bin/env python3
"""
Script to auto-populate the database for Elisabeth's Sports Item Catalog

Item names and descriptions from products in real web-shops. Sources:
    https://www.soccer.com/
    https://www.sport-bittl.com/
    https://www.forelle.com/
    https://www.hockeyoffice.com/
"""

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database_setup import Base, Categories, Items


__author__ = "Elisabeth M. Strunk"
__version__ = 1.1
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


def populate_database():
    engine = create_engine('sqlite:///item_catalog.db')
    Base.metadata.bind = engine
    db_session_maker = sessionmaker(bind=engine)
    session = db_session_maker()

    # create entries in categories table:
    session.add_all([Categories(name='Soccer'),
                     Categories(name='Basketball'),
                     Categories(name='Baseball'),
                     Categories(name='Snowboarding'),
                     Categories(name='Rock Climbing'),
                     Categories(name='Skating'),
                     Categories(name='Hockey')])
    # create entries in items table:
    session.add_all([Items(name="Diamond Soccer Ball",
                           description="Diamond Soccer Ball is a great "
                                       "club match and practice ball. Newly "
                                       "developed all-round ball with extra "
                                       "soft touch. Comes with a 2 "
                                       "year warranty.",
                           category="Soccer",
                           last_modified=datetime.datetime.now()),
                     Items(name="Nike Phantom Venom Academy FG Soccer Shoe "
                                "Men volt obsidian volt barely volt",
                           description="The Nike Phantom Venom Academy FG is "
                                       "engineered for powerful, precise "
                                       "strikes that win games. Ridges on the "
                                       "instep create spin to control the "
                                       "flight of the ball, while the "
                                       "firm-ground plate provides the "
                                       "traction needed to unleash at any "
                                       "moment.",
                           category="Soccer",
                           last_modified=datetime.datetime.now()),
                     Items(name="Nike Goalkeeper Match Soccer Gloves Unisex "
                                "blue hero white",
                           description="Padding plus grip. The Nike "
                                       "Goalkeeper Match Soccer Gloves "
                                       "have foam for cushioning and a "
                                       "smooth surface that gives you grip "
                                       "on the ball in wet or dry conditions.",
                           category="Soccer",
                           last_modified=datetime.datetime.now()),
                     Items(name="Nike Precision III Basketball Shoes Men grey "
                                "gold",
                           description="Make every move count in the Nike "
                                       "Precision III. This all-purpose "
                                       "mid-top delivers a comfortable "
                                       "combination of cushioning and "
                                       "containment. Its lightweight midsole "
                                       "and multi-directional traction team "
                                       "up for soft steps and quick cuts.",
                           category="Basketball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Spalding Street Game Ball BBL Platinum",
                           description="The successor of the legendary "
                                       "Streetball. Thanks to his resilience "
                                       "in street basketball, he has become "
                                       "an integral part of street basketball"
                                       ". Excellent grip and very good ball "
                                       "control.",
                           category="Basketball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Nike Backboard Dri-FIT Basketball T-Shirt "
                                "Kids game royal",
                           description="Sweat-wicking comfort. The Nike "
                                       "Dri-FIT T-Shirt has sweat-wicking "
                                       "fabric to help you stay dry and "
                                       "comfortable on the court.",
                           category="Basketball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Nike Dry Basketball Shorts Kids midnight "
                                "navy black",
                           description="Sweat-wicking comfort. The Nike "
                                       "Dri-FIT Shorts feature sweat-wicking "
                                       "technology and lightweight fabric "
                                       "to help keep you dry and comfortable "
                                       "while you play.",
                           category="Basketball",
                           last_modified=datetime.datetime.now()),
                     Items(name="New Era League Essential New York Yankees "
                                "Unisex blue",
                           description="You can wear the League Essential New "
                                       "York Yankees Cap everywhere . During "
                                       "sports, in the city or in the "
                                       "mountains - the cap protects the head "
                                       "and face from the sun. The simple "
                                       "design makes the blue cap a timeless "
                                       "classic. The big, stylish NY Yankee "
                                       "logo does not just make fan earts "
                                       "beat faster.",
                           category="Baseball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Rawlings Baseball / softball gloves",
                           description="New custom options now available! "
                                       "Ever wanted to design a glove like "
                                       "a pro player? Or are you looking "
                                       "for the perfect gift to a teammate? "
                                       "Forelle and Rawlings offer the "
                                       "Glove Builder exclusively in Europe. "
                                       "We invite you to play around s"
                                       "electing your favourite materials, "
                                       "colours, webs and patterns. Complete "
                                       "custom gloves with your own name, "
                                       "number and flag.",
                           category="Baseball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Worth FPS512 Sick 454 Baseball Bat",
                           description="Worth’s 454(TM) USA technology has "
                                       "a new two-phase resin system making "
                                       "the engineered carbon fiber composite "
                                       "hotter and stronger than ever. "
                                       "Balanced - Offers the most "
                                       "true-to-weight feel. Balanced bats "
                                       "are perfect for hitters seeking "
                                       "maximum bat control through the zone.",
                           category="Baseball",
                           last_modified=datetime.datetime.now()),
                     Items(name="Wilson WTA5500 Shock FX 2.0 Catcher's Helmet",
                           description="Floating Mas(TM) system with extended "
                                       "cage absorbs up to 50% more impact "
                                       "than regular masks. Strategic venting "
                                       "reduces weight and maximizes air flow."
                                       " Dri-Lex(R) moisture management liner."
                                       "Premium leather chin pad. Matte "
                                       "finish paint job.Number stickers "
                                       "and water resistant carry bag "
                                       "included. Meets NOCSAE Protection "
                                       "Standard",
                           category="Baseball",
                           last_modified=datetime.datetime.now()),
                     Items(name="All Star CP28Pro Body Protector",
                           description="Multi layered foam. Contoured neck "
                                       "colar. Fully adjustable 5 point "
                                       "harness. With shoulder cap",
                           category="Baseball",
                           last_modified=datetime.datetime.now()),
                     Items(name="O'Neill PM Contour Snowboard Jacket Women "
                                "grey",
                           description="Featuring 10K/10K waterproofing & "
                                       "breathability, O'Neill Hyperdry nano "
                                       "DWR, fully taped seams, side vents "
                                       "for those days when the heart rate "
                                       "is up and you need to lose some heat "
                                       "and O'Neill Firewall Magma lining "
                                       "so your insulation is where you need "
                                       "it most. Awesome style with the the "
                                       "super cool patterns and an "
                                       "asymmetrical zipper, you can trust "
                                       "this jacket to have your back from "
                                       "the most adventurous moments to "
                                       "chilling out at the outside après-ski "
                                       "bar afterwards.",
                           category="Snowboarding",
                           last_modified=datetime.datetime.now()),
                     Items(name="Scott Backcountry Guide AP 30l KIT "
                                "Avalanche Airbag black burnt orange",
                           description="There is no compromise on a safe "
                                       "day in the mountains. The SCOTT "
                                       "Backcountry Guide AP 30 is Scotts "
                                       "utilitarian sized ski pack, featuring "
                                       "specific features designed for "
                                       "backcountry adventurers and snow "
                                       "professionals a like. From one-lap "
                                       "dawn patrols to all-day tours and "
                                       "couloir missions, the AP 30 "
                                       "avalanche airbag has everything "
                                       "You need for a fun, safe day in "
                                       "the mountains.",
                           category="Snowboarding",
                           last_modified=datetime.datetime.now()),
                     Items(name="Climbing Technology Click Up Kit orange",
                           description="It can be used with 8.5-11 mm single "
                                       "ropes. It is compact and lightweight "
                                       "and allows for belaying a leader and "
                                       "belaying a top-roping climber with "
                                       "both hands handling the rope, or "
                                       "for lowering the climber. The "
                                       "V-Proof System (patent pending) "
                                       "reduces the chance of error due "
                                       "to an incorrect handling of the rope "
                                       "when braking. If the rope is "
                                       "incorrectly installed in the device "
                                       "(the rope sides are inverted), "
                                       "thanks to the specific tapered "
                                       "(V-shaped) friction notches, "
                                       "effective belaying is still ensured, "
                                       "with safe braking and easy lowering "
                                       "of the climber.",
                           category="Rock Climbing",
                           last_modified=datetime.datetime.now()),
                     Items(name="Red Chili Atomic 2 Climbing Shoe ocker "
                                "orange",
                           description="The new Climbing Shoe. The "
                                       "entry-area is completely redesigned "
                                       "and combines an even easier on/off "
                                       "convenience with a perfectly snug ﬁt."
                                       " The ATOMYC 2 is a precision down "
                                       "turn slipper designed to deliver "
                                       "the highest level of sensitivity on "
                                       "the most technical routes. An "
                                       "aggressive slingshot rand combines "
                                       "with a single velcro strap to press "
                                       "the foot forward into the down-turned "
                                       "toe box for maximum power.",
                           category="Rock Climbing",
                           last_modified=datetime.datetime.now()),
                     Items(name="SALEWA Agner DST Climbing Tights Women "
                                "dark purple",
                           description="Versatile, comfortable alpine "
                                       "climbing tights for women. The "
                                       "Agner Durastretch Women's Tights "
                                       "are designed for versatile comfort "
                                       "during summer alpine days and "
                                       "perform well on all manner of rock "
                                       "surfaces. The super-lightweight, "
                                       "breathable and durable Durastretch "
                                       "fabric offers next-to-skin comfort "
                                       "and a high level of stretch "
                                       "performance.",
                           category="Rock Climbing",
                           last_modified=datetime.datetime.now()),
                     Items(name="LACD Quickdraw Start Wire",
                           description="The Quickdraw Start Wire Express set "
                                       "by LACD is just as well suited for "
                                       "the first experience in rock climbing "
                                       "as for experienced rock climbers.",
                           category="Rock Climbing",
                           last_modified=datetime.datetime.now()),
                     Items(name="Powerslide Infinity Wheels 90mm / 85A "
                                "(pack of 4)",
                           description="High-quality speed wheels by "
                                       "Powerslide. These wheels have a race "
                                       "profile.",
                           category="Skating",
                           last_modified=datetime.datetime.now()),
                     Items(name="Powerslide Wristguards black",
                           description="The wrist protectors have an "
                                       "anatomical shape. Made of 600D "
                                       "nylon upper. With Triplestrap system "
                                       "for individual size adjustment. The "
                                       "air permeable mesh fabric offers high "
                                       "wearing comfort.",
                           category="Skating",
                           last_modified=datetime.datetime.now()),
                     Items(name="Balzer Star Lady New Eishockey Semi Softboot "
                                "white",
                           description="The Star Lady ice skate offers "
                                       "everything You need for a funny day "
                                       "on the ice.",
                           category="Hockey",
                           last_modified=datetime.datetime.now()),
                     Items(name="Bauer Rubena Puck black",
                           description="Let´s play. Bauer's Rubena Puck is "
                                       "an official match puck and is played "
                                       "in all leagues. The first choice of "
                                       "every hockey player.",
                           category="Hockey",
                           last_modified=datetime.datetime.now()),
                     Items(name="CCM Fitlite 40 Helmetcombo Junior with "
                                "FL40 facemask white",
                           description="CCM FitLite 40 helmet white combines "
                                       "white the advantage of a fully "
                                       "customizable lightweight fit with "
                                       "innovation in safety and protection.",
                           category="Hockey",
                           last_modified=datetime.datetime.now())
                     ])
    session.commit()
    session.close()
