from models import User, Post, Tag, PostTag, db, connect_db
from app import app

# Create all tables
# db.drop_all()
# db.create_all()
connect_db(app)
app.app_context().push()
db.drop_all()
db.create_all()

# sample data
henry = User(first_name='Henry', last_name='Rollins', image_url="https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1280x1280/products/46523/46391/ss2158728_-_photograph_of_henry_rollins_available_in_4_sizes_framed_or_unframed_buy_now_at_starstills__54545__29662.1394484410.jpg?c=2?imbypass=on")
chuck = User(first_name='Chuck', last_name='Dukowski', image_url="https://cdn.gemtracks.com/img/artist/848.jpg")
dez = User(first_name='Dez', last_name='Cadena', image_url="https://images.equipboard.com/uploads/source/image/109891/dez-cadena-was-the-third-vocalist-and-later-rhythm-guitarist-for-hardcore-punk-band-black-flag-from-1980-to-1983-and-played-guitar-with-the-misfits-from-2001-to-2015.jpg")
greg = User(first_name='Greg', last_name='Ginn', image_url="https://lastfm.freetls.fastly.net/i/u/ar0/19a4700b78e5436e82c3eeb4ca0827a9.jpg")
robo = User(first_name='Robo', last_name='ROBO', image_url="https://64.media.tumblr.com/58e9139333949cd4fe2cdb9ad510e8ea/tumblr_ml5cdz1baz1s474z1o1_500.jpg")

db.session.add(henry)
db.session.add(chuck)
db.session.add(dez)
db.session.add(greg)
db.session.add(robo)

modern_man = Post(title="Modern Man", content="He's too straight and you can't wait a modern...man", author_id=2)

sinking=Post(title="Sinking", content="""[Verse]
Sinking
Wanting
Thinking
Sinking all the while
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
When it's cold outside when it's cold inside
When it hurts to be alone and it hurts to be alone
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
When I'm feeling it when I'm down and out
When I'm feeling it when I'm down and out
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
All torn up, all torn down
I get messed up
And I'm thinking that I'm sinking when I'm sinking all the while
[Chorus]
It hurts to be alone
When it hurts to be alone
[Guitar solo]
[Verse]
Falling down, falling down
I stand up
I fall back down
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
Caving in
Caving in
I think my heart is caving in
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
Dead air
Dead phone
Dead quiet
Sinking all the while
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
Writhing my hands
Grinding my teeth
Staring at the floor
Sinking all the while
[Chorus]
It hurts to be alone
When it hurts to be alone
[Guitar solo 2]
[Verse]
Cutting my teeth on the blues
Soul sinking to the bottom of my shoes
Thinking my life's a waiting game
Staring at my grave and feeling the same
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
When all I want is all I want
When I want it, I want it!
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
When all I need is all I need
When I need it, I need it!
[Chorus]
It hurts to be alone
When it hurts to be alone
[Verse]
Sinking
Sinking
Sinking
Sinking all the way
[Chorus]
It hurts to be alone
When it hurts to be alone
""", author_id=1)

thirsty_and_miserable =Post(title="Thirsty and Miserable", content=""" [Verse 1]
Thirsty and miserable
You drop to the floor
You drink 'til you can't even see anymore
[Hook]
Thirsty and miserable, always wanting more
Thirsty and miserable, always wanting more
[Verse 2]
My brother wants a ride to the liquor store
You pity him for what he wants it for
[Hook]
Thirsty and miserable, always wanting more
Thirsty and miserable, always wanting more
[Verse 3]
It's 1:30 and we're all getting nervous
The store closes at two
There's not enough to last us (Oh Shit!)
[Hook]
Thirsty and miserable, always wanting more
Thirsty and miserable, always wanting more
[Outro]
See if you can find the key to your mother’s liquor cabinet  """, author_id=3)

rise_above = Post(title="Rise Above", content="""Jealous cowards try to control
Rise above! We're gonna rise above!
They distort what we say
Rise above! We're gonna rise above!
Try and stop what we do
Rise above! We're gonna rise above!
When they can't do it themselves
Rise above! We're gonna rise above!
[Chorus]
We are tired of your abuse
Try to stop us, it's no use
[Verse 2]
Society's arms of control
Rise above! We're gonna rise above!
Think they're smart, can't think for themselves
Rise above! We're gonna rise above!
Laugh at us behind our backs
Rise above! We're gonna rise above!
I find satisfaction in what they lack
Rise above! We're gonna rise above!
[Chorus]
We are tired of your abuse
Try to stop us, it's no use
[Chorus]
We are tired of your abuse
Try to stop us, it's no use
[Verse 3]
We're born with a chance
Rise above! We're gonna rise above!
I am gonna have my chance
Rise above! We're gonna rise above!
We're born with a chance
Rise above! We're gonna rise above!
And I am gonna have my chance
Rise above! We're gonna rise above!
[Chorus]
We are tired of your abuse
Try to stop us it's no use
[Outro]
Rise above! Rise above!
Rise above! We're gonna rise above!
We're gonna rise above! We're gonna rise above!""", author_id=4)

tv_party = Post(title="TV Party", content="""TV party tonight!
TV party tonight!
TV party tonight!
TV party tonight!
[Verse]
We're gonna have a TV party tonight (Alright!)
We're gonna have a TV party alright (Tonight!)
[Chorus]
We've got nothing better to do
Than watch TV and have a couple of brews
[Verse]
Everybody's gonna hang out here tonight (Alright!)
We'll pass out on the couch alright (Tonight!)
[Chorus]
We've got nothing better to do
Than watch TV and have a couple of brews
[Bridge]
Don't talk about anything else
We don't wanna know
We're dedicated
To our favorite shows
That's Incredible!
Hill Street Blues!
Dallas!
Fridays!
[Verse]
We sit glued to the TV set all night (And every night!)
Why go into the outside world at all? (It's such a fright!)
[Chorus]
We've got nothing better to do
Than watch TV and have a couple of brews
[Verse]
TV news shows what it's really like out there (It's a scare!)
You can go out if you want (We wouldn't dare!)
[Chorus]
We've got nothing better to do
Than watch TV and have a couple of brews
[Bridge]
Don't talk about anything else
We don't wanna know
We're dedicated
To our favorite shows
Saturday Night Live!
Monday Night Football!
Jeffersons!
Vega$!
[Verse]
I wouldn't be without my TV for a day (Or even a minute!)
I don't even bother to use my brain anymore (There's nothing left in it!)
[Chorus]
We've got nothing better to do
Than watch TV and have a couple of brews
[Verse]
Hey, wait a minute! My TV set doesn't work (It's broken!)
What are we gonna do tonight, this isn't fair! (We're hurtin'!)
[Chorus]
We've got nothing left to do
Left with no TV and just a couple of brews
[Bridge]
What are we gonna talk about?
I don't know!
We're gonna miss our favorite shows!
No That's Incredible!
No Monday Night Football!
No Jeffersons!
No Fridays!
No TV Party tonight""", author_id=4)

gimmie_gimmie_gimmie = Post(title="Gimmie Gimmie Gimmie", content="""Gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for
(One, two, three, four)
[Verse 1]
Sitting here like a loaded gun
Waiting to go off
I've got nothing to do
But shoot my mouth off
[Hook]
Gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for
[Verse 2]
I gotta go out
Get something for my head
If I keep on doing this
I'm gonna end up dead
[Hook]
Gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for
[Verse 3]
I know the world's got problems
I've got problems of my own
Not the kind that can't be solved
With an atom bomb
[Hook]
So gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for
[Hook]
Gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for
(One, two, three, four)
[Verse 1]
Sitting here like a loaded gun
Waiting to go off
I've got nothing to do
But shoot my mouth off
[Hook]
So gimme gimme gimme
I need some more
Gimme gimme gimme
Don't ask what for""", author_id=4)

padded_cell = Post(title="Padded Cell", content="""Earth's a padded cell
Defanged and declawed
I'm living in hell
It's a paradise fraud
Straight jacket minds
In line to be old
Telling me to let time slip through my teeth
Well I'm no fool
I'm going to town
Manic reactions are always a buzz
I'm suspect, the stranger in disguise
It's forced itself upon me
Something I can't hide
[Hook]
See it in... maniacs
Their eyes... maniacs maniacs maniacs
[Verse]
Looking at you, inside of you
Through your eyes, behind your mind
Looking at you, inside of you
I'm invisible, nowhere to hide
I'm obscene. the living dead
See the flys feed off your head
Looking at you, I'm inside of you
It's walden two, but the flower's dead
[Hook]
See it in... maniacs
Their eyes... maniacs maniacs maniacs
[Verse]
Earth's a padded cell
Defanged and declawed
I'm living in hell
It's a paradise fraud
Straight jacket minds
In line to be old
Telling me to want
Let time slip through my teeth
Well I'm not the fool
I'm going to town
Manic reactions are always a buzz
I'm suspect, the stranger in disguise
It's forced itself upon me
Something I can't hide
[Hook]
See it in... maniacs
Their eyes... maniacs maniacs maniacs""", author_id=2)

no_more = Post(title="No More", content="""No, I won't believe that this is all
I'm not happy, I'm not free
Pay check to pay check, living for what?
Every night I get drunk to get sunk
[Hook]
I need action
Won't take no more
No more, no more, no more
It won't work, won't work no more
[Verse]
I knew what I had when I grew up
I know that it really sucked
Now I'm a slave to the same lies
If I don't get out I'm gonna die
[Hook]
[Verse]
Control, control for who, for what?
I'm no robot
They can get fucked
Reaction's masochism this can't last
I need to live, I need it now
""", author_id=2)



for song in [modern_man, sinking, thirsty_and_miserable, rise_above, tv_party, gimmie_gimmie_gimmie, padded_cell, no_more]:
  db.session.add(song)



black_flag_tag = Tag(name="Black Flag")
loose_nut_tag = Tag(name="Loose Nut")
damaged_tag = Tag(name="Damaged")


for tag in [black_flag_tag, loose_nut_tag, damaged_tag]:
  db.session.add(tag)


modern_man.tags.append(black_flag_tag)
modern_man.tags.append(loose_nut_tag)

sinking.tags.append(black_flag_tag)
sinking.tags.append(loose_nut_tag)

thirsty_and_miserable.tags.append(black_flag_tag)
thirsty_and_miserable.tags.append(damaged_tag)

rise_above.tags.append(black_flag_tag)
rise_above.tags.append(damaged_tag)

tv_party.tags.append(black_flag_tag)
tv_party.tags.append(damaged_tag)

gimmie_gimmie_gimmie.tags.append(black_flag_tag)
gimmie_gimmie_gimmie.tags.append(damaged_tag)

padded_cell.tags.append(black_flag_tag) 
padded_cell.tags.append(damaged_tag)

no_more.tags.append(black_flag_tag)
no_more.tags.append(damaged_tag)


db.session.commit()