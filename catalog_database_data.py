from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalogitems.db')
DBsession = sessionmaker(bind=engine)
session = DBsession()

# Users
user1 = User(name="Phoenix Daphne", email="phoenix_daphne@gmail.com")
session.add(user1)
session.commit()

user2 = User(name="Sonny Tilander", email="sonny_tilander@gmail.com")
session.add(user1)
session.commit()

user3 = User(name="Hugh Altretch", email="hugh_altretch@gmail.com")
session.add(user1)
session.commit()

# Category 'Soccer'
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

item1 = Item(
    name="Pair of Shin Guards",
    description=("Description: Black pair of shin guards. "
                 "Made of foam rubber. Light and sturdy."),
    category=category1,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Soccer Jersey of Leeds",
    description=("Description: White jersey with blue logo on. "
                 "Made of cotton. Machine-fitted."),
    category=category1,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Soccer Shoes",
    description=("Description: Dark red pair of soccer cleats. "
                 "Made of quality leather. With conical metal cleats."),
    category=category1,
    user=user3)
session.add(item3)
session.commit()


# Category 'Basketball'
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

item1 = Item(
    name="Basketball Jersey of LA Lakers",
    description=("Description: Yellow jersey. Retro style. "
                 "Made of cotton. 500 threaded."),
    category=category2,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Basketball Jersey of Chicago Bulls",
    description=("Description: Black jersey with red logo on. "
                 "%100 polyester. From season 97-98"),
    category=category2,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Basketball Mouthguards",
    description=("Description: Light blue. "
                 "Triple layer design. Origin: USA"),
    category=category2,
    user=user3)
session.add(item3)
session.commit()


# Category 'Baseball'
category3 = Category(name="Baseball")
session.add(category3)
session.commit()

item1 = Item(
    name="Bat (Cat 7) ",
    description=("Description: Red bat. Three-pieced design. "
                 "31/32 inches."),
    category=category3,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Batting Gloves",
    description=("Description: White batting gloves. "
                 "Digital embossed synthetic overlays. Made of leather."),
    category=category3,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Baseball mouthguards",
    description=("Description: Gradient blue. "
                 "Made of silicon. Insta-Fit design"),
    category=category3,
    user=user3)
session.add(item3)
session.commit()


# Category 'Frisbee'
category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

item1 = Item(
    name="Frisbee (Orange)",
    description=("Description: Bright orange color. "
                 "175 grams. Premium plastic."),
    category=category4,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Frisbee (Red)",
    description=("Description: LED red color. "
                 "185 grams. Innovative design."),
    category=category4,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Frisbee (Brown)",
    description=("Description: Brown eagle color. 177 grams. "
                 "From championship series."),
    category=category4,
    user=user3)
session.add(item3)
session.commit()


# Category 'Snowboarding'
category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

item1 = Item(
    name="Goggles",
    description=("Description: Polyurethane frame with rigid face "
                 "foam feature. Lightweight. Height is 91 mm."),
    category=category5,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Snowboard",
    description=("Description: Freeride type. Base is extruded. "
                 "Length is 157W."),
    category=category5,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Snowboard Jacket",
    description=("Description: 5000mm waterproof. Mesh lining. "
                 "Removable hood."),
    category=category5,
    user=user3)
session.add(item3)
session.commit()


# Category 'Rock Climbing'
category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

item1 = Item(
    name="Climbing Shoes",
    description=("Description: Neutral type. Can be resoled. "
                 "Weight is 1 pound."),
    category=category6,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Climbing Cord",
    description=("Description: 6 mm. 32 ft. Strength is "
                 "7.4 kilonewtones."),
    category=category6,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Climbing Sling",
    description=("Description: Nylon webbing. 18mm wide. Strength is "
                 "22.5 kilonewtones."),
    category=category6,
    user=user3)
session.add(item3)
session.commit()


# Category 'Foosball'
category7 = Category(name="Foosball")
session.add(category6)
session.commit()

item1 = Item(
    name="Strongfeet Foosball Table",
    description=("Description: Full size table with dark brown maple cover. "
                 "3-man goalie setup. Adjustable leg levelers."),
    category=category7,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Green Mountain Foosball Table",
    description=("Description: Full size table with all black look. Playing "
                 "dimensions are 47\"L x 27\"W. With manual scoring units."),
    category=category7,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Foosball Balls",
    description=("Description: Traditional style. Black and white. "
                 "1.4 inches. Weight is 24 grams."),
    category=category7,
    user=user3)
session.add(item3)
session.commit()


# Category 'Skating'
category8 = Category(name="Skating")
session.add(category8)
session.commit()

item1 = Item(
    name="Skating Boots (Powell)",
    description=("Description: Brand is Powell. For men. Color is white "
                 "with small black side lines. US men shoe size is 1.5."),
    category=category8,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Skating Boots (Arch Sports)",
    description=("Description: Brand is Arch Sports. For women. Color is "
                 "white with gradient light green touch. One size fits all."),
    category=category8,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Skate Socks (FullSwing)",
    description=("Description: Brand is FullSwing. Used for ankle protection "
                 "in skating. Universal fit. Washable."),
    category=category8,
    user=user3)
session.add(item3)
session.commit()


# Category 'Hockey'
category9 = Category(name="Hockey")
session.add(category9)
session.commit()

item1 = Item(
    name="Hockey Pants (Giant Ice)",
    description=("Description: Brand is Giant Ice. With two-way belt closure "
                 "system. Size is Large. Waist is 34\" - 36\"."),
    category=category9,
    user=user1)
session.add(item1)
session.commit()

item2 = Item(
    name="Hockey Gloves",
    description=("Description: Black. 25 mm EPP foam. Made of nylon. "
                 "Ultra-light and breathable."),
    category=category9,
    user=user2)
session.add(item2)
session.commit()

item3 = Item(
    name="Hockey Stick (RPA)",
    description=("Description: Brand is RPA. Right hand. Flex is 51. "
                 "Length is 50. With shiny transparent finish."),
    category=category9,
    user=user3)
session.add(item3)
session.commit()

print "Sample categories, items and users are added!"
