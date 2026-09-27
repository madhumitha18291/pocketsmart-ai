CATALOG = {

    "home": [

        {
            "name":
                "Minimal LED Ceiling Light",

            "price":
                1299,

            "platform":
                "Amazon",

            "url":
                "https://www.amazon.in/s?k=led+ceiling+light"
        },

        {
            "name":
                "LACK Wall Shelf",

            "price":
                1499,

            "platform":
                "IKEA",

            "url":
                "https://www.ikea.com/in/en/search/?q=wall%20shelf"
        },

        {
            "name":
                "Decorative Table Lamp",

            "price":
                899,

            "platform":
                "Flipkart",

            "url":
                "https://www.flipkart.com/search?q=table+lamp"
        },

        {
            "name":
                "Compact Study Table",

            "price":
                3499,

            "platform":
                "Amazon",

            "url":
                "https://www.amazon.in/s?k=compact+study+table"
        },

        {
            "name":
                "Cushion Cover Set",

            "price":
                699,

            "platform":
                "IKEA",

            "url":
                "https://www.ikea.com/in/en/search/?q=cushion%20cover"
        }
    ],


    "party": [

        {
            "name":
                "Vegetarian Party Catering Search",

            "price":
                350,

            "platform":
                "Swiggy",

            "url":
                "https://www.swiggy.com/search?query=party%20catering"
        },

        {
            "name":
                "Party Food & Catering Search",

            "price":
                400,

            "platform":
                "Zomato",

            "url":
                "https://www.zomato.com/search?q=party%20catering"
        },

        {
            "name":
                "Party Decoration Kit",

            "price":
                1299,

            "platform":
                "Amazon",

            "url":
                "https://www.amazon.in/s?k=party+decoration+kit"
        },

        {
            "name":
                "Budget Venue Search",

            "price":
                2500,

            "platform":
                "OYO",

            "url":
                "https://www.oyorooms.com/"
        },

        {
            "name":
                "Disposable Dinner Set",

            "price":
                799,

            "platform":
                "Flipkart",

            "url":
                "https://www.flipkart.com/search?q=party+dinner+set"
        }
    ],


    "jewelry": [

        {
            "name":
                "Gold-Tone Jhumka Earrings",

            "price":
                799,

            "platform":
                "Amazon",

            "url":
                "https://www.amazon.in/s?k=jhumka+earrings"
        },

        {
            "name":
                "Minimal Pendant Necklace",

            "price":
                999,

            "platform":
                "Flipkart",

            "url":
                "https://www.flipkart.com/search?q=pendant+necklace"
        },

        {
            "name":
                "Stone Stud Earrings",

            "price":
                599,

            "platform":
                "Amazon",

            "url":
                "https://www.amazon.in/s?k=stone+stud+earrings"
        },

        {
            "name":
                "Statement Necklace",

            "price":
                1499,

            "platform":
                "Flipkart",

            "url":
                "https://www.flipkart.com/search?q=statement+necklace"
        }
    ]
}


def catalog_for(
    category: str,
    budget: float
):

    items = CATALOG.get(
        category,
        []
    )

    matching_items = [
        item
        for item in items
        if item["price"] <= budget
    ]

    if matching_items:

        return matching_items

    return sorted(
        items,
        key=lambda item:
            item["price"]
    )[:3]