"""
TrustScope AI — Demo Data Module
Provides realistic sample product data for hackathon demonstration.

Three demo products:
- DEMO001 (genuine): A product with mostly genuine reviews
- DEMO002 (suspicious): A product with many fake/duplicate reviews  
- DEMO003 (mixed): A product with mixed review patterns
"""

from typing import Dict, List
import random

# Seed for reproducibility
random.seed(42)

DEMO_PRODUCTS = {
    "genuine": {
        "product_info": {
            "product_name": "EcoBreeze Stainless Steel Water Bottle 1L — Insulated, BPA Free",
            "product_image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400",
            "average_rating": 4.3,
            "total_reviews_count": "1,284",
            "is_demo": True,
        },
        "reviews": [
            # Genuine reviews
            {"review_text": "I've been using this bottle for about 4 months now. It keeps drinks cold for well over 24 hours which impressed me. The lid mechanism is easy to use even with wet hands. My only complaint is that the straw is a bit tricky to clean thoroughly, but it comes with a cleaning brush which helps. Overall very satisfied.", "star_rating": 5, "reviewer_name": "Sarah M.", "review_date": "2024-10-15", "verified_purchase": True, "helpful_votes": 23, "review_title": "Great insulation, minor cleaning challenge"},
            {"review_text": "Bought this for my daily gym commute. Fits in my bag side pocket perfectly. The insulation works as advertised — my ice water was still cold after 3 hours in a hot car. The matte finish looks premium. Lost half a star because the logo started fading after 3 months.", "star_rating": 4, "reviewer_name": "James K.", "review_date": "2024-09-28", "verified_purchase": True, "helpful_votes": 18, "review_title": "Solid gym bottle, minor logo durability issue"},
            {"review_text": "Third stainless steel bottle I've owned and probably my favourite. The wide mouth makes it easy to add ice cubes. Doesn't sweat on the outside even with ice cold water inside. Lid doesn't leak when tilted. At this price point, excellent value.", "star_rating": 5, "reviewer_name": "Priya R.", "review_date": "2024-10-02", "verified_purchase": True, "helpful_votes": 31, "review_title": "Best bottle I've owned"},
            {"review_text": "Decent bottle. Does what it says. I've had it two weeks so can't comment on long-term durability. Temperature retention is good. The colour online looks slightly different in person — more muted. Not complaining, just noting for anyone who cares about exact shade.", "star_rating": 4, "reviewer_name": "Tom B.", "review_date": "2024-11-01", "verified_purchase": True, "helpful_votes": 7, "review_title": "Good so far, color slightly different"},
            {"review_text": "My previous water bottle cracked and I needed a quick replacement. This arrived next day. Quality feels solid, the double wall is noticeable in the weight but it's manageable. Used it for hiking over the weekend and worked perfectly. Kids also approved.", "star_rating": 5, "reviewer_name": "Fatima A.", "review_date": "2024-10-20", "verified_purchase": True, "helpful_votes": 14, "review_title": "Perfect replacement, quick delivery"},
            {"review_text": "Three stars because while the bottle itself is good quality, the lid developed a slight leak after 6 weeks. When I tilted it past 45 degrees some water seeped around the seal. Contacted seller and they're sending a replacement lid. Adjusting to 4 stars if the replacement fixes it.", "star_rating": 3, "reviewer_name": "David L.", "review_date": "2024-09-10", "verified_purchase": True, "helpful_votes": 42, "review_title": "Good bottle, lid developed leak"},
            {"review_text": "Great for office use. I fill it up once in the morning and it lasts all day. The 1L capacity is perfect. Fits in standard car cup holders which was important for me. No complaints after 2 months of daily use.", "star_rating": 5, "reviewer_name": "Meera S.", "review_date": "2024-10-30", "verified_purchase": True, "helpful_votes": 9, "review_title": "Perfect office companion"},
            {"review_text": "Good insulation but the bottle is heavier than expected when full. 1L of water plus the stainless steel weight makes it noticeably hefty. If you don't mind the weight, the performance is excellent. I've started using it only for shorter outings.", "star_rating": 4, "reviewer_name": "Chris P.", "review_date": "2024-11-05", "verified_purchase": True, "helpful_votes": 11, "review_title": "Great insulation but heavy"},
            {"review_text": "Gifted this to my husband for his cycling. He's very particular about his equipment and was skeptical at first. After 3 weeks he admitted it's genuinely good — stays cold through his entire 2 hour ride even in summer heat. Would buy again.", "star_rating": 5, "reviewer_name": "Rebecca T.", "review_date": "2024-10-11", "verified_purchase": True, "helpful_votes": 16, "review_title": "Cyclist approved"},
            {"review_text": "Fine bottle. I bought it because it's on sale. At the original price I'd hesitate. At the sale price it's good value. Keeps drinks cold for about 18 hours in my experience, not 24 as claimed, but that could be ambient temperature affecting it.", "star_rating": 3, "reviewer_name": "Alex W.", "review_date": "2024-09-25", "verified_purchase": True, "helpful_votes": 28, "review_title": "Good at sale price"},
            {"review_text": "Very happy with this purchase. The bottle arrived well packaged. No dents or scratches. The cap screws on tightly. I've dropped it twice from about a metre and it's fine. The cleaning brush included is a thoughtful addition. Recommend.", "star_rating": 5, "reviewer_name": "Nisha G.", "review_date": "2024-10-18", "verified_purchase": True, "helpful_votes": 21, "review_title": "Durable and thoughtfully packaged"},
            {"review_text": "I work in construction and needed something that could handle rough conditions. This has survived being dropped, thrown in the back of a truck, and used in 40 degree heat. The insulation still works. Exactly what I needed.", "star_rating": 5, "reviewer_name": "Raj M.", "review_date": "2024-09-15", "verified_purchase": True, "helpful_votes": 38, "review_title": "Survives construction site conditions"},
            {"review_text": "Decent product. The lid is my main concern — it rattles slightly when you shake the bottle. Not a big deal but a bit annoying. Everything else is as described. Temperature retention is excellent.", "star_rating": 4, "reviewer_name": "Lena K.", "review_date": "2024-11-08", "verified_purchase": True, "helpful_votes": 5, "review_title": "Good but lid rattles"},
            {"review_text": "Second purchase from this seller. First bottle served me for 2 years before the lid finally wore out. Came back for the updated model and it's even better. The mouthpiece redesign is an improvement. Highly recommended based on my experience.", "star_rating": 5, "reviewer_name": "Owen J.", "review_date": "2024-10-05", "verified_purchase": True, "helpful_votes": 44, "review_title": "Repeat customer — still excellent"},
            {"review_text": "My kids use these for school. Bought 3 for different family members. All three have worked without issues for 3 months. Kids like the colours. Easy to clean. No leaks. Good value for the quality.", "star_rating": 5, "reviewer_name": "Anna L.", "review_date": "2024-10-22", "verified_purchase": True, "helpful_votes": 19, "review_title": "Bought 3 for the family"},
            # A few lower quality but genuine reviews
            {"review_text": "It's okay.", "star_rating": 3, "reviewer_name": "User123", "review_date": "2024-10-01", "verified_purchase": False, "helpful_votes": 0, "review_title": "Okay"},
            {"review_text": "Works as described. Happy with it.", "star_rating": 4, "reviewer_name": "Mike H.", "review_date": "2024-09-20", "verified_purchase": True, "helpful_votes": 2, "review_title": "Works well"},
            {"review_text": "Good bottle, keeps drinks cold. The only thing is I wish it came in more colour options.", "star_rating": 4, "reviewer_name": "Pooja D.", "review_date": "2024-11-03", "verified_purchase": True, "helpful_votes": 3, "review_title": "Good but limited colours"},
            {"review_text": "Not happy with this purchase. The lid broke after 3 weeks. The bottle itself is fine but the lid is poorly made.", "star_rating": 2, "reviewer_name": "Greg F.", "review_date": "2024-10-12", "verified_purchase": True, "helpful_votes": 7, "review_title": "Lid broke quickly"},
            {"review_text": "Excellent water bottle. I've tried many over the years and this ranks among the top. The insulation is exceptional — keeps ice for over 30 hours in my testing. Build quality is premium. Worth every rupee.", "star_rating": 5, "reviewer_name": "Vinod K.", "review_date": "2024-10-28", "verified_purchase": True, "helpful_votes": 25, "review_title": "Top performer"},
        ]
    },
    
    "suspicious": {
        "product_info": {
            "product_name": "UltraSlim Pro X Weight Loss Supplement — 60 Capsules",
            "product_image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400",
            "average_rating": 4.8,
            "total_reviews_count": "3,891",
            "is_demo": True,
        },
        "reviews": [
            # Highly suspicious / fake reviews (duplicates, promotional)
            {"review_text": "Best product ever! Lost 10kg in 2 weeks! Amazing results! Must buy! Five stars!", "star_rating": 5, "reviewer_name": "User1001", "review_date": "2024-10-01", "verified_purchase": False, "helpful_votes": 0, "review_title": "Amazing!"},
            {"review_text": "Best product ever! Lost 10kg in 2 weeks! Amazing results! Must buy! Five stars!", "star_rating": 5, "reviewer_name": "User1002", "review_date": "2024-10-01", "verified_purchase": False, "helpful_votes": 0, "review_title": "Amazing!"},
            {"review_text": "Best product ever! Lost 10kg in 2 weeks! Amazing results! Must buy! Five stars!", "star_rating": 5, "reviewer_name": "User1003", "review_date": "2024-10-02", "verified_purchase": False, "helpful_votes": 0, "review_title": "Amazing Results!"},
            {"review_text": "Lost 10 kg in 2 weeks! Best product ever! Amazing! Must buy! Five stars!!!!", "star_rating": 5, "reviewer_name": "User1004", "review_date": "2024-10-02", "verified_purchase": False, "helpful_votes": 0, "review_title": "5 Stars!"},
            {"review_text": "Changed my life! Lost weight fast! Amazing product! Highly recommend! Buy now!", "star_rating": 5, "reviewer_name": "User1005", "review_date": "2024-10-03", "verified_purchase": False, "helpful_votes": 0, "review_title": "Life changing"},
            {"review_text": "Changed my life! Lost weight so fast! Amazing product! Highly recommend! Buy now!", "star_rating": 5, "reviewer_name": "User1006", "review_date": "2024-10-03", "verified_purchase": False, "helpful_votes": 0, "review_title": "Life Changing!!!"},
            {"review_text": "Changed my life! Amazing weight loss! Buy this product now! Highly recommend!", "star_rating": 5, "reviewer_name": "User1007", "review_date": "2024-10-03", "verified_purchase": False, "helpful_votes": 0, "review_title": "Changed My Life!"},
            {"review_text": "WOW! Lost 15kg in 1 month! This product is amazing! Everyone should buy this! FIVE STARS!!!", "star_rating": 5, "reviewer_name": "QuickReviewer", "review_date": "2024-10-04", "verified_purchase": False, "helpful_votes": 0, "review_title": "WOW Amazing"},
            {"review_text": "WOW! Lost 15 kg in one month!! This product is absolutely amazing!! EVERYONE should buy this!! FIVE STARS!", "star_rating": 5, "reviewer_name": "NewUser99", "review_date": "2024-10-04", "verified_purchase": False, "helpful_votes": 0, "review_title": "5 stars WOW"},
            {"review_text": "Great product! Excellent results! Must buy! Five stars! Amazing! Love it! Buy now!", "star_rating": 5, "reviewer_name": "Reviewer2001", "review_date": "2024-10-05", "verified_purchase": False, "helpful_votes": 0, "review_title": "Great"},
            {"review_text": "Great product excellent results must buy five stars amazing love it", "star_rating": 5, "reviewer_name": "Reviewer2002", "review_date": "2024-10-05", "verified_purchase": False, "helpful_votes": 0, "review_title": "Great product"},
            {"review_text": "Great product! Excellent! Five stars! Must buy! Amazing results! Love it!", "star_rating": 5, "reviewer_name": "Reviewer2003", "review_date": "2024-10-05", "verified_purchase": False, "helpful_votes": 0, "review_title": "5 Stars"},
            {"review_text": "Best supplement ever! Works miracles! Lost 20kg! Amazing! Must buy! HIGHLY RECOMMEND!", "star_rating": 5, "reviewer_name": "TopFan123", "review_date": "2024-10-06", "verified_purchase": False, "helpful_votes": 0, "review_title": "Miracle product"},
            {"review_text": "Best supplement! Works like a miracle! Lost 20 kg! Amazing! Must buy! HIGHLY RECOMMEND!!!", "star_rating": 5, "reviewer_name": "TopFan456", "review_date": "2024-10-06", "verified_purchase": False, "helpful_votes": 0, "review_title": "Miracle!"},
            {"review_text": "Excellent product!! Perfect!! Amazing!! LOVE IT!! Five stars!! Buy now!! Don't miss this!!", "star_rating": 5, "reviewer_name": "Excited_Buyer", "review_date": "2024-10-07", "verified_purchase": False, "helpful_votes": 0, "review_title": "EXCELLENT!!!"},
            # A few semi-suspicious
            {"review_text": "I lost some weight after using this for a month. I was also dieting and exercising so hard to know how much this helped.", "star_rating": 3, "reviewer_name": "HonestReviewer", "review_date": "2024-09-15", "verified_purchase": True, "helpful_votes": 45, "review_title": "Hard to tell if it works"},
            {"review_text": "I've been taking this for 3 weeks. Combined with a calorie deficit I've lost about 3kg. Would have lost weight without it too probably.", "star_rating": 3, "reviewer_name": "RealistReview", "review_date": "2024-09-20", "verified_purchase": True, "helpful_votes": 38, "review_title": "Can't tell if it's the supplement"},
            {"review_text": "Didn't work for me at all. Same diet and exercise routine. No difference. Very disappointed.", "star_rating": 1, "reviewer_name": "Disappointed", "review_date": "2024-09-25", "verified_purchase": True, "helpful_votes": 67, "review_title": "Didn't work"},
            {"review_text": "Gave me headaches for the first week. Stopped taking after 2 weeks. Not for me.", "star_rating": 1, "reviewer_name": "NegativeExperience", "review_date": "2024-10-10", "verified_purchase": True, "helpful_votes": 29, "review_title": "Side effects"},
            {"review_text": "Amazing! Perfect! Must have! Five stars! Buy immediately! You won't regret it! Life changing!", "star_rating": 5, "reviewer_name": "NewAccount2024", "review_date": "2024-10-15", "verified_purchase": False, "helpful_votes": 0, "review_title": "Amazing Must Buy"},
        ]
    },
    
    "mixed": {
        "product_info": {
            "product_name": "TechFlow Wireless Bluetooth Earbuds — Noise Cancelling, 30hr Battery",
            "product_image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400",
            "average_rating": 4.1,
            "total_reviews_count": "2,156",
            "is_demo": True,
        },
        "reviews": [
            # Genuine
            {"review_text": "Sound quality is surprisingly good for the price. Bass is punchy without being overwhelming. The noise cancellation works reasonably well in office environments but won't block out loud machinery. Battery lasts a solid 7 hours per charge on medium volume.", "star_rating": 4, "reviewer_name": "AudioEnthusiast", "review_date": "2024-10-05", "verified_purchase": True, "helpful_votes": 89, "review_title": "Good sound for the price"},
            {"review_text": "These are my second pair of budget earbuds and easily the better pair. The fit is comfortable and they don't fall out during light jogging. Mic quality on calls is acceptable — people can hear me clearly. The case charges the earbuds twice over.", "star_rating": 4, "reviewer_name": "RunningEnthusiast", "review_date": "2024-10-12", "verified_purchase": True, "helpful_votes": 56, "review_title": "Great fit for jogging"},
            {"review_text": "Had connectivity issues for the first few days — kept disconnecting from my phone. After updating the firmware through the app, the connection has been stable for 3 weeks. Sound quality is good. Customer support was helpful with the troubleshooting.", "star_rating": 4, "reviewer_name": "TechUser2024", "review_date": "2024-09-28", "verified_purchase": True, "helpful_votes": 73, "review_title": "Firmware update fixed connectivity"},
            {"review_text": "Not impressed. The noise cancellation is barely noticeable. The bass is muddy. For casual listening it's acceptable but don't buy these expecting premium audio experience. The price reflects what you get.", "star_rating": 2, "reviewer_name": "AudioCritic", "review_date": "2024-09-18", "verified_purchase": True, "helpful_votes": 112, "review_title": "Overhyped noise cancellation"},
            {"review_text": "Using these at work every day for 2 months. Comfortable for long sessions. Sound isolation helps me focus. The touch controls occasionally register accidental taps. Battery life is as advertised. Happy with the purchase.", "star_rating": 5, "reviewer_name": "WorkFromHome", "review_date": "2024-10-18", "verified_purchase": True, "helpful_votes": 44, "review_title": "Daily work companion"},
            # Suspicious/fake
            {"review_text": "Best earbuds ever! Amazing sound! Must buy! Five stars! Perfect! Amazing! Love them! Buy now!", "star_rating": 5, "reviewer_name": "NewUser001", "review_date": "2024-10-20", "verified_purchase": False, "helpful_votes": 0, "review_title": "Best ever!"},
            {"review_text": "Best earbuds ever!! Amazing sound quality!! Must buy now!! Five stars!! Perfect!! Amazing!! Love them!!", "star_rating": 5, "reviewer_name": "NewUser002", "review_date": "2024-10-20", "verified_purchase": False, "helpful_votes": 0, "review_title": "5 Stars"},
            {"review_text": "Excellent earbuds! Perfect sound! Highly recommend! Must buy! Life changing! Amazing! Five stars!", "star_rating": 5, "reviewer_name": "QuickRater01", "review_date": "2024-10-21", "verified_purchase": False, "helpful_votes": 0, "review_title": "Excellent"},
            # Genuine  
            {"review_text": "Value for money is good. I compared these to earbuds twice the price and while the premium ones are better, these punch above their weight class for budget earbuds. The case feels a bit plasticky but the earbuds themselves feel solid.", "star_rating": 4, "reviewer_name": "BudgetConsumer", "review_date": "2024-10-08", "verified_purchase": True, "helpful_votes": 61, "review_title": "Punches above budget class"},
            {"review_text": "One earbud stopped working after 6 weeks. The right one just went silent. Contacted seller and they sent a replacement pair within a week. Second pair has worked for 2 months without issues. Raising to 4 stars for the good customer service.", "star_rating": 4, "reviewer_name": "CustomerService", "review_date": "2024-09-30", "verified_purchase": True, "helpful_votes": 38, "review_title": "Had defect, great after-sales support"},
            # Suspicious
            {"review_text": "Amazing earbuds! Perfect! Five stars! Highly recommend! Buy immediately! Best purchase ever!", "star_rating": 5, "reviewer_name": "NewAccount2024a", "review_date": "2024-10-22", "verified_purchase": False, "helpful_votes": 0, "review_title": "Amazing"},
            # Genuine
            {"review_text": "These work well for my needs. I mainly use them for podcasts and YouTube while commuting. The noise cancellation is enough to drown out bus noise. I don't need audiophile quality. For this use case, they're perfect.", "star_rating": 5, "reviewer_name": "CommuterUser", "review_date": "2024-10-14", "verified_purchase": True, "helpful_votes": 29, "review_title": "Perfect for commuting"},
            {"review_text": "My third pair of wireless earbuds. These are the most comfortable and have the longest battery life of the three. Sound is good but not exceptional. Touch controls work reliably. The case magnet alignment could be better.", "star_rating": 4, "reviewer_name": "GadgetCollector", "review_date": "2024-10-02", "verified_purchase": True, "helpful_votes": 51, "review_title": "Best of three I've tried"},
            # Suspicious duplicate
            {"review_text": "Excellent earbuds! Perfect sound quality! Highly recommend to everyone! Must buy now! Life changing! Amazing quality! Five stars!", "star_rating": 5, "reviewer_name": "QuickRater02", "review_date": "2024-10-21", "verified_purchase": False, "helpful_votes": 0, "review_title": "Excellent Quality"},
            # Genuine  
            {"review_text": "Good earbuds but slightly uncomfortable after 2+ hours. The ear tips included fit most ears but I have smaller ears and the smallest option is still a bit large. The audio quality compensates for the minor discomfort.", "star_rating": 4, "reviewer_name": "SmallEarProblem", "review_date": "2024-11-01", "verified_purchase": True, "helpful_votes": 17, "review_title": "Comfort issue for small ears"},
            {"review_text": "Impressive for the price. I was expecting much worse based on past experience with budget earbuds. These genuinely surprised me. Sound stage is decent, the mids are clear, bass is controlled. NC works in moderately loud environments.", "star_rating": 5, "reviewer_name": "PleasantSurprise", "review_date": "2024-10-25", "verified_purchase": True, "helpful_votes": 82, "review_title": "Genuinely surprised"},
            {"review_text": "Returned them. The right earbud had channel imbalance — noticeably louder on the left. Couldn't get a replacement in time. The sound quality before the defect was actually quite good. Poor quality control.", "star_rating": 2, "reviewer_name": "ReturnedItem", "review_date": "2024-09-22", "verified_purchase": True, "helpful_votes": 48, "review_title": "Quality control issues"},
            {"review_text": "Using for gaming. Latency is acceptable for casual gaming. Not suitable for competitive gaming where audio timing matters. For single player games and media consumption they're excellent. Microphone quality in Discord calls is decent.", "star_rating": 4, "reviewer_name": "GamerReview", "review_date": "2024-10-29", "verified_purchase": True, "helpful_votes": 35, "review_title": "Good for casual gaming"},
            {"review_text": "My kids use these. They've dropped them multiple times on hard floors. Still working after 4 months. Kids say the sound is good for their music. Easy to pair. The app is straightforward. Good choice for a child's first wireless earbuds.", "star_rating": 5, "reviewer_name": "ParentReviewer", "review_date": "2024-10-07", "verified_purchase": True, "helpful_votes": 23, "review_title": "Durable for kids"},
            # Suspicious
            {"review_text": "Best earbuds EVER!!! Amazing!!! Perfect!!! Buy NOW!!! Five stars!!!!", "star_rating": 5, "reviewer_name": "NewUser999", "review_date": "2024-10-23", "verified_purchase": False, "helpful_votes": 0, "review_title": "BEST EVER!!!"},
        ]
    }
}

class DemoData:
    @staticmethod
    def get_product_data(demo_type: str) -> Dict:
        """Get demo product data by type: 'genuine', 'suspicious', or 'mixed'"""
        if demo_type not in DEMO_PRODUCTS:
            demo_type = "mixed"
        return DEMO_PRODUCTS[demo_type]
    
    @staticmethod
    def get_all_demo_products() -> List[Dict]:
        return [
            {
                "url": "https://www.amazon.com/dp/DEMO001",
                "name": DEMO_PRODUCTS["genuine"]["product_info"]["product_name"],
                "type": "Mostly Genuine Reviews",
                "description": "A product with authentic, detailed customer reviews",
                "platform": "Demo",
                "rating": DEMO_PRODUCTS["genuine"]["product_info"]["average_rating"],
            },
            {
                "url": "https://www.amazon.com/dp/DEMO002",
                "name": DEMO_PRODUCTS["suspicious"]["product_info"]["product_name"],
                "type": "High Suspicious Reviews",
                "description": "A product with many suspicious and duplicate reviews",
                "platform": "Demo",
                "rating": DEMO_PRODUCTS["suspicious"]["product_info"]["average_rating"],
            },
            {
                "url": "https://www.amazon.com/dp/DEMO003",
                "name": DEMO_PRODUCTS["mixed"]["product_info"]["product_name"],
                "type": "Mixed Review Patterns",
                "description": "A product with mixed genuine and suspicious reviews",
                "platform": "Demo",
                "rating": DEMO_PRODUCTS["mixed"]["product_info"]["average_rating"],
            },
        ]
