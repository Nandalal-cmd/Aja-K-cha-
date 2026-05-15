import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models import DailyChallenge


async def get_today_challenge(db: AsyncSession) -> DailyChallenge:
    today = datetime.date.today()
    result = await db.execute(
        select(DailyChallenge).where(DailyChallenge.date == today)
    )
    return result.scalar_one_or_none()


async def get_challenge_by_id(challenge_id: int, db: AsyncSession) -> DailyChallenge:
    result = await db.execute(
        select(DailyChallenge).where(DailyChallenge.id == challenge_id)
    )
    return result.scalar_one_or_none()


async def seed_challenges(db: AsyncSession):
    result = await db.execute(select(DailyChallenge).limit(1))
    if result.scalar_one_or_none():
        return

    challenges = [
        DailyChallenge(
            date=datetime.date.today(),
            title_np="आफ्नो सबैभन्दा राम्रो नृत्य देखाउनुहोस्",
            title_en="Show your best dance move",
            description_np="एक १५ सेकेन्डको भिडियो बनाउनुहोस् जहाँ तपाईं आफ्नो मनपर्ने नेपाली गीतमा नाच्दै हुनुहुन्छ। जति हास्यास्पद, त्यति राम्रो!",
            description_en="Create a 15-second video of yourself dancing to your favorite Nepali song. The funnier, the better!",
            challenge_type="funny",
            points=10,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=1),
            title_np="कसैको दिन बनाउनुहोस्",
            title_en="Make someone's day",
            description_np="आज कसैलाई अप्रत्याशित तारिफ गर्नुहोस्। मानिसलाई राम्रो महसुस गराउने केहि गर्नुहोस् र फोटो खिच्नुहोस्!",
            description_en="Give someone an unexpected compliment today. Do something that makes someone feel good and capture it!",
            challenge_type="wholesome",
            points=15,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=2),
            title_np="आफ्नो मनपर्ने खानाको फोटो",
            title_en="Photo of your favorite food",
            description_np="आज तपाईंले खाइरहेको सबैभन्दा मिठो चीजको फोटो पोस्ट गर्नुहोस्। होमियो खैर, म:म, अथवा कम्पनीको खाना? हामीलाई देखाउनुहोस्!",
            description_en="Post a photo of the yummiest thing you're eating today. Momo, chatpate, or daal bhat? Show us!",
            challenge_type="food",
            points=10,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=3),
            title_np="सेल्फी विद अ‍क्सफोर्ड कमा",
            title_en="Silly face selfie",
            description_np="आफ्नो सबैभन्दा हास्यास्पद अनुहार बनाएर सेल्फी लिनुहोस्। जति कुरूप, त्यति राम्रो!",
            description_en="Take a selfie with your silliest face. The uglier, the better!",
            challenge_type="funny",
            points=10,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=4),
            title_np="आफ्नो सीप देखाउनुहोस्",
            title_en="Show off a skill",
            description_np="तपाईंलाई के गर्न आउँछ? गितार बजाउने, चित्र कोर्ने, केहि पकाउने? आजको च्यालेन्ज: आफ्नो ट्यालेन्ट देखाउनुहोस्!",
            description_en="What can you do? Play guitar, draw, cook something? Today's challenge: show off your talent!",
            challenge_type="talent",
            points=15,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=5),
            title_np="साथीलाई ट्याग गर",
            title_en="Tag a friend",
            description_np="आफ्नो सबैभन्दा मिल्ने साथीलाई यो पोस्टमा ट्याग गर्नुहोस् र उसलाई भन्नुहोस् किन ऊ तपाईंको लागि विशेष छ।",
            description_en="Tag your best friend in this post and tell them why they're special to you.",
            challenge_type="wholesome",
            points=10,
        ),
        DailyChallenge(
            date=datetime.date.today() + datetime.timedelta(days=6),
            title_np="बाहिर निस्कनुहोस्",
            title_en="Step outside",
            description_np="प्रकृतिको फोटो खिच्नुहोस्। चाहे त्यो हिमाल होस्, बगैचा होस् वा आकाश। प्रकृतिसँग जोडिनुहोस्!",
            description_en="Take a photo of nature. Whether it's mountains, a garden, or the sky. Connect with nature!",
            challenge_type="wholesome",
            points=10,
        ),
    ]

    for c in challenges:
        db.add(c)
    await db.commit()
