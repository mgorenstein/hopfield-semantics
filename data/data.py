people = ['salesperson','cashier','clerk','chef','cook','nurse','waitress',
'janitor','secretary','accountant','teacher','driver','mechanic','auditor',
'guard','receptionist','landscaper','policeman','mailman','lawyer',
'electrician','technician','bartender','jailer','programmer','physician',
'doctor','firefighter','butcher','baker','architect','animator','biologist',
'decorator','economist','diplomat','editor','executive','fisherman',
'fishmonger','geologist','hairdresser','jeweler','journalist','judge',
'magician','musician','painter','photographer','pilot','plumber','sailor',
'scientist','soldier','surgeon']

machine = ['lathe','turbine','compressor','engine','refrigerator','clock',
'pump','conveyor','calculator','telephone','drill','sander','bandsaw','wheel']

lit = ['fiction','nonfiction','poetry','acrostic','essay','fable','tale',
'novella','novel','story','parable','drama','eclogue','ode',
'verse','limerick','quatrain']

music = ['symphony','concerto','cantata','fugue','sonata','lieder','nocturne',
'etude','oratorio','requiem','carol','motet','opera','minuet','concerto',
'quartet','quintet','rondo','rhapsody','scherzo','waltz','cabaret']

clothing = ['apron','bathrobe','bikini','blouse','cardigan','coat',
'cummerbund','dress','frock','glove','gown','jacket','jersey','kimono','kilt',
'leotard','mitten','overcoat','overall','pashmina','robe','sash','shawl',
'shirt','shoe','shorts','skirt','smock','sock','sweater','swimsuit',
'necktie','tunic']

fruit = ['apple','apricot','banana','blackberry','blueberry','cherry',
'coconut','date','cranberry','fig','grape','grapefruit','huckleberry','lemon',
'lime','kumquat','lychee','mango','cantaloupe','watermelon','mulberry',
'tangerine','papaya','pear','peach','persimmon','plum','pineapple',
'raspberry','strawberry']

vegetable = ['artichoke','asparagus','eggplant','bean','peas','broccoli',
'brussel sprouts','cauliflower','cabbage','celery','kale','spinach','basil',
'parsley','arugula','lettuce','onion','pepper','carrot','ginger',
'turnip','radish']

animal = ['aardvark','alligator','anaconda','antelope','baboon','bat','bear',
'buffalo','cat','cougar','crocodile','dog','dolphin','duck','eagle','falcon',
'flamingo','fox','frog','giraffe','goat','goose','hippopotamus','hedgehog',
'iguana','jaguar','kangaroo','koala','lion','lizard','lemur','marmoset',
'opossum','otter','owl','parrot','penguin','pig','puffin','rabbit','raccoon',
'rhinoceros','salamander','seal','shark','spider','swan','turtle','walrus',
'wolf','whale','zebra']

categories={'animal': {'examples': animal, 'high_freq': 'dog', 'low_freq': 'marmoset'},
'profession': {'examples': people, 'high_freq': 'doctor', 'low_freq': 'fishmonger'},
'machine': {'examples': machine, 'high_freq': 'engine', 'low_freq': 'lathe'},
'literature': {'examples': lit, 'high_freq': 'novel', 'low_freq': 'limerick'},
'music': {'examples': music, 'high_freq': 'symphony', 'low_freq': 'scherzo'},
'clothing': {'examples': clothing, 'high_freq': 'shirt', 'low_freq': 'kimono'},
'fruit': {'examples': fruit, 'high_freq': 'apple', 'low_freq': 'persimmon'},
'vegetable': {'examples': vegetable, 'high_freq': 'carrot', 'low_freq': 'cauliflower'}}