# David Lindsey - GISC 6389 - Master's Project
# Contact: dcl160230@utdallas.edu
# The following code represents the functionality for
# GUI_CountiesPerState.

# If a user selects a specific state, all counties associated with that state
# will need to populate within a drop-down list for the user to select from.
# All state and county names within this module were derived from the same U.S.
# Census Bureau Shapefile used for clipping hazard data, so no erroneous
# spelling discrepancies should presently exist.

# Empty dictionary for each state and its affiliated counties.
dict_state_counties = {}

# Alabama counties
counties_01_AL = "Autauga", "Baldwin", "Barbour", "Bibb", "Blount", "Bullock",\
                 "Butler", "Calhoun", "Chambers", "Cherokee", "Chilton",\
                 "Choctaw", "Clarke", "Clay", "Cleburne", "Coffee", "Colbert",\
                 "Conecuh", "Coosa", "Covington", "Crenshaw", "Cullman",\
                 "Dale", "Dallas", "DeKalb", "Elmore", "Escambia", "Etowah",\
                 "Fayette", "Franklin", "Geneva", "Greene", "Hale", "Henry",\
                 "Houston", "Jackson", "Jefferson", "Lamar", "Lauderdale",\
                 "Lawrence", "Lee", "Limestone", "Lowndes", "Macon", "Madison",\
                 "Marengo", "Marion", "Marshall", "Mobile", "Monroe",\
                 "Montgomery", "Morgan", "Perry", "Pickens", "Pike",\
                 "Randolph", "Russell", "Shelby", "St. Clair", "Sumter",\
                 "Talladega", "Tallapoosa", "Tuscaloosa", "Walker",\
                 "Washington", "Wilcox", "Winston"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["AL"] = counties_01_AL

# Alaska counties
counties_02_AK = "Aleutians East", "Aleutians West", "Anchorage", "Bethel",\
                 "Bristol Bay", "Denali", "Dillingham", "Fairbanks North Star",\
                 "Haines", "Hoonah-Angoon", "Juneau", "Kenai Peninsula",\
                 "Ketchikan Gateway", "Kodiak Island", "Kusilvak",\
                 "Lake and Peninsula", "Matanuska-Susitna", "Nome",\
                 "North Slope", "Northwest Arctic", "Petersburg",\
                 "Prince of Wales-Hyder", "Sitka", "Skagway",\
                 "Southeast Fairbanks", "Valdez-Cordova", "Wrangell",\
                 "Yakutat", "Yukon-Koyukuk"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["AK"] = counties_02_AK

# Arizona counties
counties_04_AZ = "Apache", "Cochise", "Coconino", "Gila", "Graham", "Greenlee",\
                 "La Paz", "Maricopa", "Mohave", "Navajo", "Pima", "Pinal",\
                 "Santa Cruz", "Yavapai", "Yuma"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["AZ"] = counties_04_AZ

# Arkansas counties
counties_05_AR = "Arkansas", "Ashley", "Baxter", "Benton", "Boone", "Bradley",\
                 "Calhoun", "Carroll", "Chicot", "Clark", "Clay", "Cleburne",\
                 "Cleveland", "Columbia", "Conway", "Craighead", "Crawford",\
                 "Crittenden", "Cross", "Dallas", "Desha", "Drew", "Faulkner",\
                 "Franklin", "Fulton", "Garland", "Grant", "Greene",\
                 "Hempstead", "Hot Spring", "Howard", "Independence", "Izard",\
                 "Jackson", "Jefferson", "Johnson", "Lafayette", "Lawrence",\
                 "Lee", "Lincoln", "Little River", "Logan", "Lonoke",\
                 "Madison", "Marion", "Miller", "Mississippi", "Monroe",\
                 "Montgomery", "Nevada", "Newton", "Ouachita", "Perry",\
                 "Phillips", "Pike", "Poinsett", "Polk", "Pope", "Prairie",\
                 "Pulaski", "Randolph", "Saline", "Scott", "Searcy",\
                 "Sebastian", "Sevier", "Sharp", "St. Francis", "Stone",\
                 "Union", "Van Buren", "Washington", "White", "Woodruff", "Yell"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["AR"] = counties_05_AR

# California counties
counties_06_CA = "Alameda", "Alpine", "Amador", "Butte", "Calaveras", "Colusa",\
                 "Contra Costa", "Del Norte", "El Dorado", "Fresno", "Glenn",\
                 "Humboldt", "Imperial", "Inyo", "Kern", "Kings", "Lake",\
                 "Lassen", "Los Angeles", "Madera", "Marin", "Mariposa",\
                 "Mendocino", "Merced", "Modoc", "Mono", "Monterey", "Napa",\
                 "Nevada", "Orange", "Placer", "Plumas", "Riverside",\
                 "Sacramento", "San Benito", "San Bernardino", "San Diego",\
                 "San Francisco", "San Joaquin", "San Luis Obispo",\
                 "San Mateo", "Santa Barbara", "Santa Clara", "Santa Cruz",\
                 "Shasta", "Sierra", "Siskiyou", "Solano", "Sonoma",\
                 "Stanislaus", "Sutter", "Tehama", "Trinity", "Tulare",\
                 "Tuolumne", "Ventura", "Yolo", "Yuba"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["CA"] = counties_06_CA

# Colorado counties
counties_08_CO = "Adams", "Alamosa", "Arapahoe", "Archuleta", "Baca", "Bent",\
                 "Boulder", "Broomfield", "Chaffee", "Cheyenne", "Clear Creek",\
                 "Conejos", "Costilla", "Crowley", "Custer", "Delta", "Denver",\
                 "Dolores", "Douglas", "Eagle", "El Paso", "Elbert", "Fremont",\
                 "Garfield", "Gilpin", "Grand", "Gunnison", "Hinsdale",\
                 "Huerfano", "Jackson", "Jefferson", "Kiowa", "Kit Carson",\
                 "La Plata", "Lake", "Larimer", "Las Animas", "Lincoln",\
                 "Logan", "Mesa", "Mineral", "Moffat", "Montezuma", "Montrose",\
                 "Morgan", "Otero", "Ouray", "Park", "Phillips", "Pitkin",\
                 "Prowers", "Pueblo", "Rio Blanco", "Rio Grande", "Routt",\
                 "Saguache", "San Juan", "San Miguel", "Sedgwick", "Summit",\
                 "Teller", "Washington", "Weld", "Yuma"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["CO"] = counties_08_CO

# Connecticut counties
counties_09_CT = "Fairfield", "Hartford", "Litchfield", "Middlesex",\
                 "New Haven", "New London", "Tolland", "Windham"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["CT"] = counties_09_CT

# Delaware counties
counties_10_DE = "Kent", "New Castle", "Sussex"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["DE"] = counties_10_DE

# District of Columbia
counties_11_DC = "District of Columbia",

# Add the district name value with the corresponding district name key
# to the dictionary.
dict_state_counties["DC"] = counties_11_DC

# Florida counties
counties_12_FL = "Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward",\
                 "Calhoun", "Charlotte", "Citrus", "Clay", "Collier",\
                 "Columbia", "DeSoto", "Dixie", "Duval", "Escambia", "Flagler",\
                 "Franklin", "Gadsden", "Gilchrist", "Glades", "Gulf",\
                 "Hamilton", "Hardee", "Hendry", "Hernando", "Highlands",\
                 "Hillsborough", "Holmes", "Indian River", "Jackson",\
                 "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy",\
                 "Liberty", "Madison", "Manatee", "Marion", "Martin",\
                 "Miami-Dade", "Monroe", "Nassau", "Okaloosa", "Okeechobee",\
                 "Orange", "Osceola", "Palm Beach", "Pasco", "Pinellas",\
                 "Polk", "Putnam", "Santa Rosa", "Sarasota", "Seminole",\
                 "St. Johns", "St. Lucie", "Sumter", "Suwannee", "Taylor",\
                 "Union", "Volusia", "Wakulla", "Walton", "Washington"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["FL"] = counties_12_FL

# Georgia counties
counties_13_GA = "Appling", "Atkinson", "Bacon", "Baker", "Baldwin", "Banks",\
                 "Barrow", "Bartow", "Ben Hill", "Berrien", "Bibb", "Bleckley",\
                 "Brantley", "Brooks", "Bryan", "Bulloch", "Burke", "Butts",\
                 "Calhoun", "Camden", "Candler", "Carroll", "Catoosa",\
                 "Charlton", "Chatham", "Chattahoochee", "Chattooga",\
                 "Cherokee", "Clarke", "Clay", "Clayton", "Clinch", "Cobb",\
                 "Coffee", "Colquitt", "Columbia", "Cook", "Coweta",\
                 "Crawford", "Crisp", "Dade", "Dawson", "DeKalb", "Decatur",\
                 "Dodge", "Dooly", "Dougherty", "Douglas", "Early", "Echols",\
                 "Effingham", "Elbert", "Emanuel", "Evans", "Fannin",\
                 "Fayette", "Floyd", "Forsyth", "Franklin", "Fulton", "Gilmer",\
                 "Glascock", "Glynn", "Gordon", "Grady", "Greene", "Gwinnett",\
                 "Habersham", "Hall", "Hancock", "Haralson", "Harris", "Hart",\
                 "Heard", "Henry", "Houston", "Irwin", "Jackson", "Jasper",\
                 "Jeff Davis", "Jefferson", "Jenkins", "Johnson", "Jones",\
                 "Lamar", "Lanier", "Laurens", "Lee", "Liberty", "Lincoln",\
                 "Long", "Lowndes", "Lumpkin", "Macon", "Madison", "Marion",\
                 "McDuffie", "McIntosh", "Meriwether", "Miller", "Mitchell",\
                 "Monroe", "Montgomery", "Morgan", "Murray", "Muscogee",\
                 "Newton", "Oconee", "Oglethorpe", "Paulding", "Peach",\
                 "Pickens", "Pierce", "Pike", "Polk", "Pulaski", "Putnam",\
                 "Quitman", "Rabun", "Randolph", "Richmond", "Rockdale",\
                 "Schley", "Screven", "Seminole", "Spalding", "Stephens",\
                 "Stewart", "Sumter", "Talbot", "Taliaferro", "Tattnall",\
                 "Taylor", "Telfair", "Terrell", "Thomas", "Tift", "Toombs",\
                 "Towns", "Treutlen", "Troup", "Turner", "Twiggs", "Union",\
                 "Upson", "Walker", "Walton", "Ware", "Warren", "Washington",\
                 "Wayne", "Webster", "Wheeler", "White", "Whitfield", "Wilcox",\
                 "Wilkes", "Wilkinson", "Worth"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["GA"] = counties_13_GA

# Hawaii counties
counties_15_HI = "Hawaii", "Honolulu", "Kalawao", "Kauai", "Maui"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["HI"] = counties_15_HI

# Idaho counties
counties_16_ID = "Ada", "Adams", "Bannock", "Bear Lake", "Benewah", "Bingham",\
                 "Blaine", "Boise", "Bonner", "Bonneville", "Boundary", \
                 "Butte", "Camas", "Canyon", "Caribou", "Cassia", "Clark", \
                 "Clearwater", "Custer", "Elmore", "Franklin", "Fremont", \
                 "Gem", "Gooding", "Idaho", "Jefferson", "Jerome", "Kootenai",\
                 "Latah", "Lemhi", "Lewis", "Lincoln", "Madison", "Minidoka",\
                 "Nez Perce", "Oneida", "Owyhee", "Payette", "Power",\
                 "Shoshone", "Teton", "Twin Falls", "Valley", "Washington"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["ID"] = counties_16_ID

# Illinois counties
counties_17_IL = "Adams", "Alexander", "Bond", "Boone", "Brown", "Bureau",\
                 "Calhoun", "Carroll", "Cass", "Champaign", "Christian",\
                 "Clark", "Clay", "Clinton", "Coles", "Cook", "Crawford",\
                 "Cumberland", "De Witt", "DeKalb", "Douglas", "DuPage",\
                 "Edgar", "Edwards", "Effingham", "Fayette", "Ford",\
                 "Franklin", "Fulton", "Gallatin", "Greene", "Grundy",\
                 "Hamilton", "Hancock", "Hardin", "Henderson", "Henry",\
                 "Iroquois", "Jackson", "Jasper", "Jefferson", "Jersey",\
                 "Jo Daviess", "Johnson", "Kane", "Kankakee", "Kendall",\
                 "Knox", "LaSalle", "Lake", "Lawrence", "Lee", "Livingston",\
                 "Logan", "Macon", "Macoupin", "Madison", "Marion", "Marshall",\
                 "Mason", "Massac", "McDonough", "McHenry", "McLean", "Menard",\
                 "Mercer", "Monroe", "Montgomery", "Morgan", "Moultrie",\
                 "Ogle", "Peoria", "Perry", "Piatt", "Pike", "Pope", "Pulaski",\
                 "Putnam", "Randolph", "Richland", "Rock Island", "Saline",\
                 "Sangamon", "Schuyler", "Scott", "Shelby", "St. Clair",\
                 "Stark", "Stephenson", "Tazewell", "Union", "Vermilion",\
                 "Wabash", "Warren", "Washington", "Wayne", "White",\
                 "Whiteside", "Will", "Williamson", "Winnebago", "Woodford"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["IL"] = counties_17_IL

# Indiana counties
counties_18_IN = "Adams", "Allen", "Bartholomew", "Benton", "Blackford",\
                 "Boone", "Brown", "Carroll", "Cass", "Clark", "Clay",\
                 "Clinton", "Crawford", "Daviess", "DeKalb", "Dearborn",\
                 "Decatur", "Delaware", "Dubois", "Elkhart", "Fayette",\
                 "Floyd", "Fountain", "Franklin", "Fulton", "Gibson", "Grant",\
                 "Greene", "Hamilton", "Hancock", "Harrison", "Hendricks",\
                 "Henry", "Howard", "Huntington", "Jackson", "Jasper", "Jay",\
                 "Jefferson", "Jennings", "Johnson", "Knox", "Kosciusko",\
                 "LaGrange", "LaPorte", "Lake", "Lawrence", "Madison",\
                 "Marion", "Marshall", "Martin", "Miami", "Monroe",\
                 "Montgomery", "Morgan", "Newton", "Noble", "Ohio", "Orange",\
                 "Owen", "Parke", "Perry", "Pike", "Porter", "Posey",\
                 "Pulaski", "Putnam", "Randolph", "Ripley", "Rush", "Scott",\
                 "Shelby", "Spencer", "St. Joseph", "Starke", "Steuben",\
                 "Sullivan", "Switzerland", "Tippecanoe", "Tipton", "Union",\
                 "Vanderburgh", "Vermillion", "Vigo", "Wabash", "Warren",\
                 "Warrick", "Washington", "Wayne", "Wells", "White", "Whitley"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["IN"] = counties_18_IN

# Iowa counties
counties_19_IA = "Adair", "Adams", "Allamakee", "Appanoose", "Audubon",\
                 "Benton", "Black Hawk", "Boone", "Bremer", "Buchanan",\
                 "Buena Vista", "Butler", "Calhoun", "Carroll", "Cass",\
                 "Cedar", "Cerro Gordo", "Cherokee", "Chickasaw", "Clarke",\
                 "Clay", "Clayton", "Clinton", "Crawford", "Dallas", "Davis",\
                 "Decatur", "Delaware", "Des Moines", "Dickinson", "Dubuque",\
                 "Emmet", "Fayette", "Floyd", "Franklin", "Fremont", "Greene",\
                 "Grundy", "Guthrie", "Hamilton", "Hancock", "Hardin",\
                 "Harrison", "Henry", "Howard", "Humboldt", "Ida", "Iowa",\
                 "Jackson", "Jasper", "Jefferson", "Johnson", "Jones",\
                 "Keokuk", "Kossuth", "Lee", "Linn", "Louisa", "Lucas", "Lyon",\
                 "Madison", "Mahaska", "Marion", "Marshall", "Mills",\
                 "Mitchell", "Monona", "Monroe", "Montgomery", "Muscatine",\
                 "O'Brien", "Osceola", "Page", "Palo Alto", "Plymouth",\
                 "Pocahontas", "Polk", "Pottawattamie", "Poweshiek",\
                 "Ringgold", "Sac", "Scott", "Shelby", "Sioux", "Story",\
                 "Tama", "Taylor", "Union", "Van Buren", "Wapello", "Warren",\
                 "Washington", "Wayne", "Webster", "Winnebago", "Winneshiek",\
                 "Woodbury", "Worth", "Wright"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["IA"] = counties_19_IA

# Kansas counties
counties_20_KS = "Allen", "Anderson", "Atchison", "Barber", "Barton",\
                 "Bourbon", "Brown", "Butler", "Chase", "Chautauqua",\
                 "Cherokee", "Cheyenne", "Clark", "Clay", "Cloud", "Coffey",\
                 "Comanche", "Cowley", "Crawford", "Decatur", "Dickinson",\
                 "Doniphan", "Douglas", "Edwards", "Elk", "Ellis", "Ellsworth",\
                 "Finney", "Ford", "Franklin", "Geary", "Gove", "Graham",\
                 "Grant", "Gray", "Greeley", "Greenwood", "Hamilton", "Harper",\
                 "Harvey", "Haskell", "Hodgeman", "Jackson", "Jefferson",\
                 "Jewell", "Johnson", "Kearny", "Kingman", "Kiowa", "Labette",\
                 "Lane", "Leavenworth", "Lincoln", "Linn", "Logan", "Lyon",\
                 "Marion", "Marshall", "McPherson", "Meade", "Miami",\
                 "Mitchell", "Montgomery", "Morris", "Morton", "Nemaha",\
                 "Neosho", "Ness", "Norton", "Osage", "Osborne", "Ottawa",\
                 "Pawnee", "Phillips", "Pottawatomie", "Pratt", "Rawlins",\
                 "Reno", "Republic", "Rice", "Riley", "Rooks", "Rush",\
                 "Russell", "Saline", "Scott", "Sedgwick", "Seward", "Shawnee",\
                 "Sheridan", "Sherman", "Smith", "Stafford", "Stanton",\
                 "Stevens", "Sumner", "Thomas", "Trego", "Wabaunsee",\
                 "Wallace", "Washington", "Wichita", "Wilson", "Woodson",\
                 "Wyandotte"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["KS"] = counties_20_KS

# Kentucky counties
counties_21_KY = "Adair", "Allen", "Anderson", "Ballard", "Barren", "Bath",\
                 "Bell", "Boone", "Bourbon", "Boyd", "Boyle", "Bracken",\
                 "Breathitt", "Breckinridge", "Bullitt", "Butler", "Caldwell",\
                 "Calloway", "Campbell", "Carlisle", "Carroll", "Carter",\
                 "Casey", "Christian", "Clark", "Clay", "Clinton",\
                 "Crittenden", "Cumberland", "Daviess", "Edmonson", "Elliott",\
                 "Estill", "Fayette", "Fleming", "Floyd", "Franklin", "Fulton",\
                 "Gallatin", "Garrard", "Grant", "Graves", "Grayson", "Green",\
                 "Greenup", "Hancock", "Hardin", "Harlan", "Harrison", "Hart",\
                 "Henderson", "Henry", "Hickman", "Hopkins", "Jackson",\
                 "Jefferson", "Jessamine", "Johnson", "Kenton", "Knott",\
                 "Knox", "Larue", "Laurel", "Lawrence", "Lee", "Leslie",\
                 "Letcher", "Lewis", "Lincoln", "Livingston", "Logan", "Lyon",\
                 "Madison", "Magoffin", "Marion", "Marshall", "Martin",\
                 "Mason", "McCracken", "McCreary", "McLean", "Meade",\
                 "Menifee", "Mercer", "Metcalfe", "Monroe", "Montgomery",\
                 "Morgan", "Muhlenberg", "Nelson", "Nicholas", "Ohio",\
                 "Oldham", "Owen", "Owsley", "Pendleton", "Perry", "Pike",\
                 "Powell", "Pulaski", "Robertson", "Rockcastle", "Rowan",\
                 "Russell", "Scott", "Shelby", "Simpson", "Spencer", "Taylor",\
                 "Todd", "Trigg", "Trimble", "Union", "Warren", "Washington",\
                 "Wayne", "Webster", "Whitley", "Wolfe", "Woodford"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["KY"] = counties_21_KY

# Louisiana counties
counties_22_LA = "Acadia", "Allen", "Ascension", "Assumption", "Avoyelles",\
                 "Beauregard", "Bienville", "Bossier", "Caddo", "Calcasieu",\
                 "Caldwell", "Cameron", "Catahoula", "Claiborne", "Concordia",\
                 "De Soto", "East Baton Rouge", "East Carroll",\
                 "East Feliciana", "Evangeline", "Franklin", "Grant", "Iberia",\
                 "Iberville", "Jackson", "Jefferson", "Jefferson Davis",\
                 "LaSalle", "Lafayette", "Lafourche", "Lincoln", "Livingston",\
                 "Madison", "Morehouse", "Natchitoches", "Orleans", "Ouachita",\
                 "Plaquemines", "Pointe Coupee", "Rapides", "Red River",\
                 "Richland", "Sabine", "St. Bernard", "St. Charles",\
                 "St. Helena", "St. James", "St. John the Baptist",\
                 "St. Landry", "St. Martin", "St. Mary", "St. Tammany",\
                 "Tangipahoa", "Tensas", "Terrebonne", "Union", "Vermilion",\
                 "Vernon", "Washington", "Webster", "West Baton Rouge",\
                 "West Carroll", "West Feliciana", "Winn"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["LA"] = counties_22_LA

# Maine counties
counties_23_ME = "Androscoggin", "Aroostook", "Cumberland", "Franklin",\
                 "Hancock", "Kennebec", "Knox", "Lincoln", "Oxford",\
                 "Penobscot", "Piscataquis", "Sagadahoc", "Somerset", "Waldo",\
                 "Washington", "York"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["ME"] = counties_23_ME

# Maryland counties
counties_24_MD = "Allegany", "Anne Arundel", "Baltimore", "Baltimore",\
                 "Calvert", "Caroline", "Carroll", "Cecil", "Charles",\
                 "Dorchester", "Frederick", "Garrett", "Harford", "Howard",\
                 "Kent", "Montgomery", "Prince George's", "Queen Anne's",\
                 "Somerset", "St. Mary's", "Talbot", "Washington", "Wicomico",\
                 "Worcester"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MD"] = counties_24_MD

# Massachusetts counties
counties_25_MA = "Barnstable", "Berkshire", "Bristol", "Dukes", "Essex",\
                 "Franklin", "Hampden", "Hampshire", "Middlesex", "Nantucket",\
                 "Norfolk", "Plymouth", "Suffolk", "Worcester"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MA"] = counties_25_MA

# Michigan counties
counties_26_MI = "Alcona", "Alger", "Allegan", "Alpena", "Antrim", "Arenac",\
                 "Baraga", "Barry", "Bay", "Benzie", "Berrien", "Branch",\
                 "Calhoun", "Cass", "Charlevoix", "Cheboygan", "Chippewa",\
                 "Clare", "Clinton", "Crawford", "Delta", "Dickinson", "Eaton",\
                 "Emmet", "Genesee", "Gladwin", "Gogebic", "Grand Traverse",\
                 "Gratiot", "Hillsdale", "Houghton", "Huron", "Ingham",\
                 "Ionia", "Iosco", "Iron", "Isabella", "Jackson", "Kalamazoo",\
                 "Kalkaska", "Kent", "Keweenaw", "Lake", "Lapeer", "Leelanau",\
                 "Lenawee", "Livingston", "Luce", "Mackinac", "Macomb",\
                 "Manistee", "Marquette", "Mason", "Mecosta", "Menominee",\
                 "Midland", "Missaukee", "Monroe", "Montcalm", "Montmorency",\
                 "Muskegon", "Newaygo", "Oakland", "Oceana", "Ogemaw",\
                 "Ontonagon", "Osceola", "Oscoda", "Otsego", "Ottawa",\
                 "Presque Isle", "Roscommon", "Saginaw", "Sanilac",\
                 "Schoolcraft", "Shiawassee", "St. Clair", "St. Joseph",\
                 "Tuscola", "Van Buren", "Washtenaw", "Wayne", "Wexford"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MI"] = counties_26_MI

# Minnesota counties
counties_27_MN = "Aitkin", "Anoka", "Becker", "Beltrami", "Benton",\
                 "Big Stone", "Blue Earth", "Brown", "Carlton", "Carver",\
                 "Cass", "Chippewa", "Chisago", "Clay", "Clearwater", "Cook",\
                 "Cottonwood", "Crow Wing", "Dakota", "Dodge", "Douglas",\
                 "Faribault", "Fillmore", "Freeborn", "Goodhue", "Grant",\
                 "Hennepin", "Houston", "Hubbard", "Isanti", "Itasca",\
                 "Jackson", "Kanabec", "Kandiyohi", "Kittson", "Koochiching",\
                 "Lac qui Parle", "Lake", "Lake of the Woods", "Le Sueur",\
                 "Lincoln", "Lyon", "Mahnomen", "Marshall", "Martin", "McLeod",\
                 "Meeker", "Mille Lacs", "Morrison", "Mower", "Murray",\
                 "Nicollet", "Nobles", "Norman", "Olmsted", "Otter Tail",\
                 "Pennington", "Pine", "Pipestone", "Polk", "Pope", "Ramsey",\
                 "Red Lake", "Redwood", "Renville", "Rice", "Rock", "Roseau",\
                 "Scott", "Sherburne", "Sibley", "St. Louis", "Stearns",\
                 "Steele", "Stevens", "Swift", "Todd", "Traverse", "Wabasha",\
                 "Wadena", "Waseca", "Washington", "Watonwan", "Wilkin",\
                 "Winona", "Wright", "Yellow Medicine"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MN"] = counties_27_MN

# Mississippi counties
counties_28_MS = "Adams", "Alcorn", "Amite", "Attala", "Benton", "Bolivar",\
                 "Calhoun", "Carroll", "Chickasaw", "Choctaw", "Claiborne",\
                 "Clarke", "Clay", "Coahoma", "Copiah", "Covington", "DeSoto",\
                 "Forrest", "Franklin", "George", "Greene", "Grenada",\
                 "Hancock", "Harrison", "Hinds", "Holmes", "Humphreys",\
                 "Issaquena", "Itawamba", "Jackson", "Jasper", "Jefferson",\
                 "Jefferson Davis", "Jones", "Kemper", "Lafayette", "Lamar",\
                 "Lauderdale", "Lawrence", "Leake", "Lee", "Leflore",\
                 "Lincoln", "Lowndes", "Madison", "Marion", "Marshall",\
                 "Monroe", "Montgomery", "Neshoba", "Newton", "Noxubee",\
                 "Oktibbeha", "Panola", "Pearl River", "Perry", "Pike",\
                 "Pontotoc", "Prentiss", "Quitman", "Rankin", "Scott",\
                 "Sharkey", "Simpson", "Smith", "Stone", "Sunflower",\
                 "Tallahatchie", "Tate", "Tippah", "Tishomingo", "Tunica",\
                 "Union", "Walthall", "Warren", "Washington", "Wayne",\
                 "Webster", "Wilkinson", "Winston", "Yalobusha", "Yazoo"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MS"] = counties_28_MS

# Missouri counties
counties_29_MO = "Adair", "Andrew", "Atchison", "Audrain", "Barry", "Barton",\
                 "Bates", "Benton", "Bollinger", "Boone", "Buchanan", "Butler",\
                 "Caldwell", "Callaway", "Camden", "Cape Girardeau", "Carroll",\
                 "Carter", "Cass", "Cedar", "Chariton", "Christian", "Clark",\
                 "Clay", "Clinton", "Cole", "Cooper", "Crawford", "Dade",\
                 "Dallas", "Daviess", "DeKalb", "Dent", "Douglas", "Dunklin",\
                 "Franklin", "Gasconade", "Gentry", "Greene", "Grundy",\
                 "Harrison", "Henry", "Hickory", "Holt", "Howard", "Howell",\
                 "Iron", "Jackson", "Jasper", "Jefferson", "Johnson", "Knox",\
                 "Laclede", "Lafayette", "Lawrence", "Lewis", "Lincoln",\
                 "Linn", "Livingston", "Macon", "Madison", "Maries", "Marion",\
                 "McDonald", "Mercer", "Miller", "Mississippi", "Moniteau",\
                 "Monroe", "Montgomery", "Morgan", "New Madrid", "Newton",\
                 "Nodaway", "Oregon", "Osage", "Ozark", "Pemiscot", "Perry",\
                 "Pettis", "Phelps", "Pike", "Platte", "Polk", "Pulaski",\
                 "Putnam", "Ralls", "Randolph", "Ray", "Reynolds", "Ripley",\
                 "Saline", "Schuyler", "Scotland", "Scott", "Shannon",\
                 "Shelby", "St. Charles", "St. Clair", "St. Francois",\
                 "St. Louis", "St. Louis", "Ste. Genevieve", "Stoddard",\
                 "Stone", "Sullivan", "Taney", "Texas", "Vernon", "Warren",\
                 "Washington", "Wayne", "Webster", "Worth", "Wright"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MO"] = counties_29_MO

# Montana counties
counties_30_MT = "Beaverhead", "Big Horn", "Blaine", "Broadwater", "Carbon",\
                 "Carter", "Cascade", "Chouteau", "Custer", "Daniels",\
                 "Dawson", "Deer Lodge", "Fallon", "Fergus", "Flathead",\
                 "Gallatin", "Garfield", "Glacier", "Golden Valley", "Granite",\
                 "Hill", "Jefferson", "Judith Basin", "Lake",\
                 "Lewis and Clark", "Liberty", "Lincoln", "Madison", "McCone",\
                 "Meagher", "Mineral", "Missoula", "Musselshell", "Park",\
                 "Petroleum", "Phillips", "Pondera", "Powder River", "Powell",\
                 "Prairie", "Ravalli", "Richland", "Roosevelt", "Rosebud",\
                 "Sanders", "Sheridan", "Silver Bow", "Stillwater",\
                 "Sweet Grass", "Teton", "Toole", "Treasure", "Valley",\
                 "Wheatland", "Wibaux", "Yellowstone"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["MT"] = counties_30_MT

# Nebraska counties
counties_31_NE = "Adams", "Antelope", "Arthur", "Banner", "Blaine", "Boone",\
                 "Box Butte", "Boyd", "Brown", "Buffalo", "Burt", "Butler",\
                 "Cass", "Cedar", "Chase", "Cherry", "Cheyenne", "Clay",\
                 "Colfax", "Cuming", "Custer", "Dakota", "Dawes", "Dawson",\
                 "Deuel", "Dixon", "Dodge", "Douglas", "Dundy", "Fillmore",\
                 "Franklin", "Frontier", "Furnas", "Gage", "Garden",\
                 "Garfield", "Gosper", "Grant", "Greeley", "Hall", "Hamilton",\
                 "Harlan", "Hayes", "Hitchcock", "Holt", "Hooker", "Howard",\
                 "Jefferson", "Johnson", "Kearney", "Keith", "Keya Paha",\
                 "Kimball", "Knox", "Lancaster", "Lincoln", "Logan", "Loup",\
                 "Madison", "McPherson", "Merrick", "Morrill", "Nance",\
                 "Nemaha", "Nuckolls", "Otoe", "Pawnee", "Perkins", "Phelps",\
                 "Pierce", "Platte", "Polk", "Red Willow", "Richardson",\
                 "Rock", "Saline", "Sarpy", "Saunders", "Scotts Bluff",\
                 "Seward", "Sheridan", "Sherman", "Sioux", "Stanton", "Thayer",\
                 "Thomas", "Thurston", "Valley", "Washington", "Wayne",\
                 "Webster", "Wheeler", "York"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NE"] = counties_31_NE

# Nevada counties
counties_32_NV = "Carson City", "Churchill", "Clark", "Douglas", "Elko",\
                 "Esmeralda", "Eureka", "Humboldt", "Lander", "Lincoln",\
                 "Lyon", "Mineral", "Nye", "Pershing", "Storey", "Washoe",\
                 "White Pine"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NV"] = counties_32_NV

# New Hampshire counties
counties_33_NH = "Belknap", "Carroll", "Cheshire", "Coos", "Grafton",\
                 "Hillsborough", "Merrimack", "Rockingham", "Strafford",\
                 "Sullivan"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NH"] = counties_33_NH

# New Jersey counties
counties_34_NJ = "Atlantic", "Bergen", "Burlington", "Camden", "Cape May",\
                 "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon",\
                 "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean",\
                 "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NJ"] = counties_34_NJ

# New Mexico counties
counties_35_NM = "Bernalillo", "Catron", "Chaves", "Cibola", "Colfax", "Curry",\
                 "De Baca", "Doña Ana", "Eddy", "Grant", "Guadalupe",\
                 "Harding", "Hidalgo", "Lea", "Lincoln", "Los Alamos", "Luna",\
                 "McKinley", "Mora", "Otero", "Quay", "Rio Arriba",\
                 "Roosevelt", "San Juan", "San Miguel", "Sandoval", "Santa Fe",\
                 "Sierra", "Socorro", "Taos", "Torrance", "Union", "Valencia"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NM"] = counties_35_NM

# New York counties
counties_36_NY = "Albany", "Allegany", "Bronx", "Broome", "Cattaraugus",\
                 "Cayuga", "Chautauqua", "Chemung", "Chenango", "Clinton",\
                 "Columbia", "Cortland", "Delaware", "Dutchess", "Erie",\
                 "Essex", "Franklin", "Fulton", "Genesee", "Greene",\
                 "Hamilton", "Herkimer", "Jefferson", "Kings", "Lewis",\
                 "Livingston", "Madison", "Monroe", "Montgomery", "Nassau",\
                 "New York", "Niagara", "Oneida", "Onondaga", "Ontario",\
                 "Orange", "Orleans", "Oswego", "Otsego", "Putnam", "Queens",\
                 "Rensselaer", "Richmond", "Rockland", "Saratoga",\
                 "Schenectady", "Schoharie", "Schuyler", "Seneca",\
                 "St. Lawrence", "Steuben", "Suffolk", "Sullivan", "Tioga",\
                 "Tompkins", "Ulster", "Warren", "Washington", "Wayne",\
                 "Westchester", "Wyoming", "Yates"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NY"] = counties_36_NY

# North Carolina counties
counties_37_NC = "Alamance", "Alexander", "Alleghany", "Anson", "Ashe",\
                 "Avery", "Beaufort", "Bertie", "Bladen", "Brunswick",\
                 "Buncombe", "Burke", "Cabarrus", "Caldwell", "Camden",\
                 "Carteret", "Caswell", "Catawba", "Chatham", "Cherokee",\
                 "Chowan", "Clay", "Cleveland", "Columbus", "Craven",\
                 "Cumberland", "Currituck", "Dare", "Davidson", "Davie",\
                 "Duplin", "Durham", "Edgecombe", "Forsyth", "Franklin",\
                 "Gaston", "Gates", "Graham", "Granville", "Greene",\
                 "Guilford", "Halifax", "Harnett", "Haywood", "Henderson",\
                 "Hertford", "Hoke", "Hyde", "Iredell", "Jackson", "Johnston",\
                 "Jones", "Lee", "Lenoir", "Lincoln", "Macon", "Madison",\
                 "Martin", "McDowell", "Mecklenburg", "Mitchell", "Montgomery",\
                 "Moore", "Nash", "New Hanover", "Northampton", "Onslow",\
                 "Orange", "Pamlico", "Pasquotank", "Pender", "Perquimans",\
                 "Person", "Pitt", "Polk", "Randolph", "Richmond", "Robeson",\
                 "Rockingham", "Rowan", "Rutherford", "Sampson", "Scotland",\
                 "Stanly", "Stokes", "Surry", "Swain", "Transylvania",\
                 "Tyrrell", "Union", "Vance", "Wake", "Warren", "Washington",\
                 "Watauga", "Wayne", "Wilkes", "Wilson", "Yadkin", "Yancey"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["NC"] = counties_37_NC

# North Dakota counties
counties_38_ND = "Adams", "Barnes", "Benson", "Billings", "Bottineau",\
                 "Bowman", "Burke", "Burleigh", "Cass", "Cavalier", "Dickey",\
                 "Divide", "Dunn", "Eddy", "Emmons", "Foster", "Golden Valley",\
                 "Grand Forks", "Grant", "Griggs", "Hettinger", "Kidder",\
                 "LaMoure", "Logan", "McHenry", "McIntosh", "McKenzie",\
                 "McLean", "Mercer", "Morton", "Mountrail", "Nelson", "Oliver",\
                 "Pembina", "Pierce", "Ramsey", "Ransom", "Renville",\
                 "Richland", "Rolette", "Sargent", "Sheridan", "Sioux",\
                 "Slope", "Stark", "Steele", "Stutsman", "Towner", "Traill",\
                 "Walsh", "Ward", "Wells", "Williams"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["ND"] = counties_38_ND

# Ohio counties
counties_39_OH = "Adams", "Allen", "Ashland", "Ashtabula", "Athens",\
                 "Auglaize", "Belmont", "Brown", "Butler", "Carroll",\
                 "Champaign", "Clark", "Clermont", "Clinton", "Columbiana",\
                 "Coshocton", "Crawford", "Cuyahoga", "Darke", "Defiance",\
                 "Delaware", "Erie", "Fairfield", "Fayette", "Franklin",\
                 "Fulton", "Gallia", "Geauga", "Greene", "Guernsey",\
                 "Hamilton", "Hancock", "Hardin", "Harrison", "Henry",\
                 "Highland", "Hocking", "Holmes", "Huron", "Jackson",\
                 "Jefferson", "Knox", "Lake", "Lawrence", "Licking", "Logan",\
                 "Lorain", "Lucas", "Madison", "Mahoning", "Marion", "Medina",\
                 "Meigs", "Mercer", "Miami", "Monroe", "Montgomery", "Morgan",\
                 "Morrow", "Muskingum", "Noble", "Ottawa", "Paulding", "Perry",\
                 "Pickaway", "Pike", "Portage", "Preble", "Putnam", "Richland",\
                 "Ross", "Sandusky", "Scioto", "Seneca", "Shelby", "Stark",\
                 "Summit", "Trumbull", "Tuscarawas", "Union", "Van Wert",\
                 "Vinton", "Warren", "Washington", "Wayne", "Williams", "Wood",\
                 "Wyandot"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["OH"] = counties_39_OH

# Oklahoma counties
counties_40_OK = "Adair", "Alfalfa", "Atoka", "Beaver", "Beckham", "Blaine",\
                 "Bryan", "Caddo", "Canadian", "Carter", "Cherokee", "Choctaw",\
                 "Cimarron", "Cleveland", "Coal", "Comanche", "Cotton",\
                 "Craig", "Creek", "Custer", "Delaware", "Dewey", "Ellis",\
                 "Garfield", "Garvin", "Grady", "Grant", "Greer", "Harmon",\
                 "Harper", "Haskell", "Hughes", "Jackson", "Jefferson",\
                 "Johnston", "Kay", "Kingfisher", "Kiowa", "Latimer",\
                 "Le Flore", "Lincoln", "Logan", "Love", "Major", "Marshall",\
                 "Mayes", "McClain", "McCurtain", "McIntosh", "Murray",\
                 "Muskogee", "Noble", "Nowata", "Okfuskee", "Oklahoma",\
                 "Okmulgee", "Osage", "Ottawa", "Pawnee", "Payne", "Pittsburg",\
                 "Pontotoc", "Pottawatomie", "Pushmataha", "Roger Mills",\
                 "Rogers", "Seminole", "Sequoyah", "Stephens", "Texas",\
                 "Tillman", "Tulsa", "Wagoner", "Washington", "Washita",\
                 "Woods", "Woodward"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["OK"] = counties_40_OK

# Oregon counties
counties_41_OR = "Baker", "Benton", "Clackamas", "Clatsop", "Columbia", "Coos",\
                 "Crook", "Curry", "Deschutes", "Douglas", "Gilliam", "Grant",\
                 "Harney", "Hood River", "Jackson", "Jefferson", "Josephine",\
                 "Klamath", "Lake", "Lane", "Lincoln", "Linn", "Malheur",\
                 "Marion", "Morrow", "Multnomah", "Polk", "Sherman",\
                 "Tillamook", "Umatilla", "Union", "Wallowa", "Wasco",\
                 "Washington", "Wheeler", "Yamhill"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["OR"] = counties_41_OR

# Pennsylvania counties
counties_42_PA = "Adams", "Allegheny", "Armstrong", "Beaver", "Bedford",\
                 "Berks", "Blair", "Bradford", "Bucks", "Butler", "Cambria",\
                 "Cameron", "Carbon", "Centre", "Chester", "Clarion",\
                 "Clearfield", "Clinton", "Columbia", "Crawford", "Cumberland",\
                 "Dauphin", "Delaware", "Elk", "Erie", "Fayette", "Forest",\
                 "Franklin", "Fulton", "Greene", "Huntingdon", "Indiana",\
                 "Jefferson", "Juniata", "Lackawanna", "Lancaster", "Lawrence",\
                 "Lebanon", "Lehigh", "Luzerne", "Lycoming", "McKean",\
                 "Mercer", "Mifflin", "Monroe", "Montgomery", "Montour",\
                 "Northampton", "Northumberland", "Perry", "Philadelphia",\
                 "Pike", "Potter", "Schuylkill", "Snyder", "Somerset",\
                 "Sullivan", "Susquehanna", "Tioga", "Union", "Venango",\
                 "Warren", "Washington", "Wayne", "Westmoreland", "Wyoming",\
                 "York"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["PA"] = counties_42_PA

# Rhode Island counties
counties_44_RI = "Bristol", "Kent", "Newport", "Providence", "Washington"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["RI"] = counties_44_RI

# South Carolina counties
counties_45_SC = "Abbeville", "Aiken", "Allendale", "Anderson", "Bamberg",\
                 "Barnwell", "Beaufort", "Berkeley", "Calhoun", "Charleston",\
                 "Cherokee", "Chester", "Chesterfield", "Clarendon",\
                 "Colleton", "Darlington", "Dillon", "Dorchester", "Edgefield",\
                 "Fairfield", "Florence", "Georgetown", "Greenville",\
                 "Greenwood", "Hampton", "Horry", "Jasper", "Kershaw",\
                 "Lancaster", "Laurens", "Lee", "Lexington", "Marion",\
                 "Marlboro", "McCormick", "Newberry", "Oconee", "Orangeburg",\
                 "Pickens", "Richland", "Saluda", "Spartanburg", "Sumter",\
                 "Union", "Williamsburg", "York"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["SC"] = counties_45_SC

# South Dakota counties
counties_46_SD = "Aurora", "Beadle", "Bennett", "Bon Homme", "Brookings",\
                 "Brown", "Brule", "Buffalo", "Butte", "Campbell",\
                 "Charles Mix", "Clark", "Clay", "Codington", "Corson",\
                 "Custer", "Davison", "Day", "Deuel", "Dewey", "Douglas",\
                 "Edmunds", "Fall River", "Faulk", "Grant", "Gregory",\
                 "Haakon", "Hamlin", "Hand", "Hanson", "Harding", "Hughes",\
                 "Hutchinson", "Hyde", "Jackson", "Jerauld", "Jones",\
                 "Kingsbury", "Lake", "Lawrence", "Lincoln", "Lyman",\
                 "Marshall", "McCook", "McPherson", "Meade", "Mellette",\
                 "Miner", "Minnehaha", "Moody", "Oglala Lakota", "Pennington",\
                 "Perkins", "Potter", "Roberts", "Sanborn", "Spink", "Stanley",\
                 "Sully", "Todd", "Tripp", "Turner", "Union", "Walworth",\
                 "Yankton", "Ziebach"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["SD"] = counties_46_SD

# Tennessee counties
counties_47_TN = "Anderson", "Bedford", "Benton", "Bledsoe", "Blount",\
                 "Bradley", "Campbell", "Cannon", "Carroll", "Carter",\
                 "Cheatham", "Chester", "Claiborne", "Clay", "Cocke", "Coffee",\
                 "Crockett", "Cumberland", "Davidson", "DeKalb", "Decatur",\
                 "Dickson", "Dyer", "Fayette", "Fentress", "Franklin",\
                 "Gibson", "Giles", "Grainger", "Greene", "Grundy", "Hamblen",\
                 "Hamilton", "Hancock", "Hardeman", "Hardin", "Hawkins",\
                 "Haywood", "Henderson", "Henry", "Hickman", "Houston",\
                 "Humphreys", "Jackson", "Jefferson", "Johnson", "Knox",\
                 "Lake", "Lauderdale", "Lawrence", "Lewis", "Lincoln",\
                 "Loudon", "Macon", "Madison", "Marion", "Marshall", "Maury",\
                 "McMinn", "McNairy", "Meigs", "Monroe", "Montgomery", "Moore",\
                 "Morgan", "Obion", "Overton", "Perry", "Pickett", "Polk",\
                 "Putnam", "Rhea", "Roane", "Robertson", "Rutherford", "Scott",\
                 "Sequatchie", "Sevier", "Shelby", "Smith", "Stewart",\
                 "Sullivan", "Sumner", "Tipton", "Trousdale", "Unicoi",\
                 "Union", "Van Buren", "Warren", "Washington", "Wayne",\
                 "Weakley", "White", "Williamson", "Wilson"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["TN"] = counties_47_TN

# Texas counties
counties_48_TX = "Anderson", "Andrews", "Angelina", "Aransas", "Archer",\
                 "Armstrong", "Atascosa", "Austin", "Bailey", "Bandera",\
                 "Bastrop", "Baylor", "Bee", "Bell", "Bexar", "Blanco",\
                 "Borden", "Bosque", "Bowie", "Brazoria", "Brazos", "Brewster",\
                 "Briscoe", "Brooks", "Brown", "Burleson", "Burnet",\
                 "Caldwell", "Calhoun", "Callahan", "Cameron", "Camp",\
                 "Carson", "Cass", "Castro", "Chambers", "Cherokee",\
                 "Childress", "Clay", "Cochran", "Coke", "Coleman", "Collin",\
                 "Collingsworth", "Colorado", "Comal", "Comanche", "Concho",\
                 "Cooke", "Coryell", "Cottle", "Crane", "Crockett", "Crosby",\
                 "Culberson", "Dallam", "Dallas", "Dawson", "DeWitt",\
                 "Deaf Smith", "Delta", "Denton", "Dickens", "Dimmit",\
                 "Donley", "Duval", "Eastland", "Ector", "Edwards", "El Paso",\
                 "Ellis", "Erath", "Falls", "Fannin", "Fayette", "Fisher",\
                 "Floyd", "Foard", "Fort Bend", "Franklin", "Freestone",\
                 "Frio", "Gaines", "Galveston", "Garza", "Gillespie",\
                 "Glasscock", "Goliad", "Gonzales", "Gray", "Grayson",\
                 "Gregg", "Grimes", "Guadalupe", "Hale", "Hall", "Hamilton",\
                 "Hansford", "Hardeman", "Hardin", "Harris", "Harrison",\
                 "Hartley", "Haskell", "Hays", "Hemphill", "Henderson",\
                 "Hidalgo", "Hill", "Hockley", "Hood", "Hopkins", "Houston",\
                 "Howard", "Hudspeth", "Hunt", "Hutchinson", "Irion", "Jack",\
                 "Jackson", "Jasper", "Jeff Davis", "Jefferson", "Jim Hogg",\
                 "Jim Wells", "Johnson", "Jones", "Karnes", "Kaufman",\
                 "Kendall", "Kenedy", "Kent", "Kerr", "Kimble", "King",\
                 "Kinney", "Kleberg", "Knox", "La Salle", "Lamar", "Lamb",\
                 "Lampasas", "Lavaca", "Lee", "Leon", "Liberty", "Limestone",\
                 "Lipscomb", "Live Oak", "Llano", "Loving", "Lubbock", "Lynn",\
                 "Madison", "Marion", "Martin", "Mason", "Matagorda",\
                 "Maverick", "McCulloch", "McLennan", "McMullen", "Medina",\
                 "Menard", "Midland", "Milam", "Mills", "Mitchell", "Montague",\
                 "Montgomery", "Moore", "Morris", "Motley", "Nacogdoches",\
                 "Navarro", "Newton", "Nolan", "Nueces", "Ochiltree", "Oldham",\
                 "Orange", "Palo Pinto", "Panola", "Parker", "Parmer", "Pecos",\
                 "Polk", "Potter", "Presidio", "Rains", "Randall", "Reagan",\
                 "Real", "Red River", "Reeves", "Refugio", "Roberts",\
                 "Robertson", "Rockwall", "Runnels", "Rusk", "Sabine",\
                 "San Augustine", "San Jacinto", "San Patricio", "San Saba",\
                 "Schleicher", "Scurry", "Shackelford", "Shelby", "Sherman",\
                 "Smith", "Somervell", "Starr", "Stephens", "Sterling",\
                 "Stonewall", "Sutton", "Swisher", "Tarrant", "Taylor",\
                 "Terrell", "Terry", "Throckmorton", "Titus", "Tom Green",\
                 "Travis", "Trinity", "Tyler", "Upshur", "Upton", "Uvalde",\
                 "Val Verde", "Van Zandt", "Victoria", "Walker", "Waller",\
                 "Ward", "Washington", "Webb", "Wharton", "Wheeler", "Wichita",\
                 "Wilbarger", "Willacy", "Williamson", "Wilson", "Winkler",\
                 "Wise", "Wood", "Yoakum", "Young", "Zapata", "Zavala"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["TX"] = counties_48_TX

# Utah counties
counties_49_UT = "Beaver", "Box Elder", "Cache", "Carbon", "Daggett", "Davis",\
                 "Duchesne", "Emery", "Garfield", "Grand", "Iron", "Juab",\
                 "Kane", "Millard", "Morgan", "Piute", "Rich", "Salt Lake",\
                 "San Juan", "Sanpete", "Sevier", "Summit", "Tooele", "Uintah",\
                 "Utah", "Wasatch", "Washington", "Wayne", "Weber"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["UT"] = counties_49_UT

# Vermont counties
counties_50_VT = "Addison", "Bennington", "Caledonia", "Chittenden", "Essex",\
                 "Franklin", "Grand Isle", "Lamoille", "Orange", "Orleans",\
                 "Rutland", "Washington", "Windham", "Windsor"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["VT"] = counties_50_VT

# Virginia counties
counties_51_VA = "Accomack", "Albemarle", "Alexandria", "Alleghany", "Amelia",\
                 "Amherst", "Appomattox", "Arlington", "Augusta", "Bath",\
                 "Bedford", "Bland", "Botetourt", "Bristol", "Brunswick",\
                 "Buchanan", "Buckingham", "Buena Vista", "Campbell",\
                 "Caroline", "Carroll", "Charles City", "Charlotte",\
                 "Charlottesville", "Chesapeake", "Chesterfield", "Clarke",\
                 "Colonial Heights", "Covington", "Craig", "Culpeper",\
                 "Cumberland", "Danville", "Dickenson", "Dinwiddie", "Emporia",\
                 "Essex", "Fairfax", "Fairfax", "Falls Church", "Fauquier",\
                 "Floyd", "Fluvanna", "Franklin", "Franklin", "Frederick",\
                 "Fredericksburg", "Galax", "Giles", "Gloucester", "Goochland",\
                 "Grayson", "Greene", "Greensville", "Halifax", "Hampton",\
                 "Hanover", "Harrisonburg", "Henrico", "Henry", "Highland",\
                 "Hopewell", "Isle of Wight", "James City", "King George",\
                 "King William", "King and Queen", "Lancaster", "Lee",\
                 "Lexington", "Loudoun", "Louisa", "Lunenburg", "Lynchburg",\
                 "Madison", "Manassas", "Manassas Park", "Martinsville",\
                 "Mathews", "Mecklenburg", "Middlesex", "Montgomery", "Nelson",\
                 "New Kent", "Newport News", "Norfolk", "Northampton",\
                 "Northumberland", "Norton", "Nottoway", "Orange", "Page",\
                 "Patrick", "Petersburg", "Pittsylvania", "Poquoson",\
                 "Portsmouth", "Powhatan", "Prince Edward", "Prince George",\
                 "Prince William", "Pulaski", "Radford", "Rappahannock",\
                 "Richmond", "Richmond", "Roanoke", "Roanoke", "Rockbridge",\
                 "Rockingham", "Russell", "Salem", "Scott", "Shenandoah",\
                 "Smyth", "Southampton", "Spotsylvania", "Stafford",\
                 "Staunton", "Suffolk", "Surry", "Sussex", "Tazewell",\
                 "Virginia Beach", "Warren", "Washington", "Waynesboro",\
                 "Westmoreland", "Williamsburg", "Winchester", "Wise", "Wythe",\
                 "York"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["VA"] = counties_51_VA

# Washington counties
counties_53_WA = "Adams", "Asotin", "Benton", "Chelan", "Clallam", "Clark",\
                 "Columbia", "Cowlitz", "Douglas", "Ferry", "Franklin",\
                 "Garfield", "Grant", "Grays Harbor", "Island", "Jefferson",\
                 "King", "Kitsap", "Kittitas", "Klickitat", "Lewis", "Lincoln",\
                 "Mason", "Okanogan", "Pacific", "Pend Oreille", "Pierce",\
                 "San Juan", "Skagit", "Skamania", "Snohomish", "Spokane",\
                 "Stevens", "Thurston", "Wahkiakum", "Walla Walla", "Whatcom",\
                 "Whitman", "Yakima"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["WA"] = counties_53_WA

# West Virginia counties
counties_54_WV = "Barbour", "Berkeley", "Boone", "Braxton", "Brooke", "Cabell",\
                 "Calhoun", "Clay", "Doddridge", "Fayette", "Gilmer", "Grant",\
                 "Greenbrier", "Hampshire", "Hancock", "Hardy", "Harrison",\
                 "Jackson", "Jefferson", "Kanawha", "Lewis", "Lincoln",\
                 "Logan", "Marion", "Marshall", "Mason", "McDowell", "Mercer",\
                 "Mineral", "Mingo", "Monongalia", "Monroe", "Morgan",\
                 "Nicholas", "Ohio", "Pendleton", "Pleasants", "Pocahontas",\
                 "Preston", "Putnam", "Raleigh", "Randolph", "Ritchie",\
                 "Roane", "Summers", "Taylor", "Tucker", "Tyler", "Upshur",\
                 "Wayne", "Webster", "Wetzel", "Wirt", "Wood", "Wyoming"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["WV"] = counties_54_WV

# Wisconsin counties
counties_55_WI = "Adams", "Ashland", "Barron", "Bayfield", "Brown", "Buffalo",\
                 "Burnett", "Calumet", "Chippewa", "Clark", "Columbia",\
                 "Crawford", "Dane", "Dodge", "Door", "Douglas", "Dunn",\
                 "Eau Claire", "Florence", "Fond du Lac", "Forest", "Grant",\
                 "Green", "Green Lake", "Iowa", "Iron", "Jackson", "Jefferson",\
                 "Juneau", "Kenosha", "Kewaunee", "La Crosse", "Lafayette",\
                 "Langlade", "Lincoln", "Manitowoc", "Marathon", "Marinette",\
                 "Marquette", "Menominee", "Milwaukee", "Monroe", "Oconto",\
                 "Oneida", "Outagamie", "Ozaukee", "Pepin", "Pierce", "Polk",\
                 "Portage", "Price", "Racine", "Richland", "Rock", "Rusk",\
                 "Sauk", "Sawyer", "Shawano", "Sheboygan", "St. Croix",\
                 "Taylor", "Trempealeau", "Vernon", "Vilas", "Walworth",\
                 "Washburn", "Washington", "Waukesha", "Waupaca", "Waushara",\
                 "Winnebago", "Wood"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["WI"] = counties_55_WI

# Wyoming counties
counties_56_WY = "Albany", "Big Horn", "Campbell", "Carbon", "Converse",\
                 "Crook", "Fremont", "Goshen", "Hot Springs", "Johnson",\
                 "Laramie", "Lincoln", "Natrona", "Niobrara", "Park", "Platte",\
                 "Sheridan", "Sublette", "Sweetwater", "Teton", "Uinta",\
                 "Washakie", "Weston"

# Add the county values with the corresponding state key to the dictionary.
dict_state_counties["WY"] = counties_56_WY