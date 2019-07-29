
'''
Item names and descriptions from products in real web-shops. Sources:
    https://www.soccer.com/
    https://www.sport-bittl.com/
'''

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database_setup import Base, Categories, Items

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# create entries in categories table:
session.add_all([Categories(name='Soccer'),
                 Categories(name='Basketball'),
                 Categories(name='Baseball'),
                 Categories(name='Snowboarding'),
                 Categories(name='Rock Climbing'),
                 Categories(name='Skating'),
                 Categories(name='Hockey')])
# create entries in items table:
session.add_all([Items(name="Select Diamond Soccer Ball",
                       description="SELECT's Diamond Soccer Ball is a great "
                                   "club match and practice ball. Newly "
                                   "developed all-round ball with extra soft "
                                   "touch. Comes with SELECT's 2 year "
                                   "warranty.",
                       category="Soccer",
                       last_modified=datetime.datetime.now()),
                 Items(name="Nike Precision III Basketball Shoes Men grey "
                            "gold",
                       description="Make every move count in the Nike "
                                   "Precision III. This all-purpose mid-top "
                                   "delivers a comfortable combination of "
                                   "cushioning and containment. Its "
                                   "lightweight midsole and multi-directional "
                                   "traction team up for soft steps and quick "
                                   "cuts.",
                       category="Basketball",
                       last_modified=datetime.datetime.now()),
                 Items(name="New Era League Essential New York Yankees Unisex "
                            "blue",
                       description="You can wear the League Essential New "
                                   "York Yankees Cap everywhere . During "
                                   "sports, in the city or in the mountains - "
                                   "the cap protects the head and face from "
                                   "the sun. The simple design makes the blue "
                                   "cap a timeless classic. The big, stylish "
                                   "NY Yankee logo does not just make fan "
                                   "hearts beat faster.",
                       category="Baseball",
                       last_modified=datetime.datetime.now()),
                 Items(name="O'Neill PM Contour Snowboard Jacket Women grey",
                       description="Featuring 10K/10K waterproofing & "
                                   "breathability, O'Neill Hyperdry nano DWR, "
                                   "fully taped seams, side vents for those "
                                   "days when the heart rate is up and you "
                                   "need to lose some heat and O'Neill "
                                   "Firewall Magma lining so your insulation "
                                   "is where you need it most. Awesome style "
                                   "with the the super cool patterns and an "
                                   "asymmetrical zipper, you can trust this "
                                   "jacket to have your back from the most "
                                   "adventurous moments to chilling out at "
                                   "the outside après-ski bar afterwards.",
                       category="Snowboarding",
                       last_modified=datetime.datetime.now()),
                 Items(name="Climbing Technology Click Up Kit orange",
                       description="It can be used with 8.5-11 mm single "
                                   "ropes. It is compact and lightweight "
                                   "and allows for belaying a leader and "
                                   "belaying a top-roping climber with both "
                                   "hands handling the rope, or for lowering "
                                   "the climber. The V-Proof System (patent "
                                   "pending) reduces the chance of error due "
                                   "to an incorrect handling of the rope when "
                                   "braking. If the rope is incorrectly "
                                   "installed in the device (the rope sides "
                                   "are inverted), thanks to the specific "
                                   "tapered (V-shaped) friction notches, "
                                   "effective belaying is still ensured, with "
                                   "safe braking and easy lowering of the "
                                   "climber.",
                       category="Rock Climbing",
                       last_modified=datetime.datetime.now()),
                 Items(name="Powerslide Infinity Wheels 90mm / 85A (pack of "
                            "4)",
                       description="High-quality speed wheels by Powerslide. "
                                   "These wheels have a race profile.",
                       category="Skating",
                       last_modified=datetime.datetime.now()),
                 Items(name="Balzer Star Lady New Eishockey Semi Softboot "
                            "white",
                       description="The Star Lady ice skate offers everything "
                                   "You need for a funny day on the ice.",
                       category="Hockey",
                       last_modified=datetime.datetime.now()),
                 ])
session.commit()
session.close()
